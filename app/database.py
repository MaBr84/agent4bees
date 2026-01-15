"""
database.py

This module acts as the "Server" side of our data architecture.
It exposes functions that serve as tools for the Agent.
"""

import os
import sqlite3
import glob
from typing import List, Tuple, Any
from dotenv import load_dotenv

# Load env vars immediately for standalone usage
load_dotenv()

# Pydantic Imports
from .models import SensorReading
from .seed_data import SEED_DATA

# Third-party imports for Vector DB

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

# Constants
DB_PATH: str = "hive_data.db"
VECTOR_DB_PATH: str = "./vector_store"
DOC_FOLDER: str = "doc"

# --- 1. SQL Database Component (SQLite) ---

def init_sql_db() -> None:
    """Initializes the SQLite database with a 'sensors' table and seed data."""
    conn: sqlite3.Connection = sqlite3.connect(DB_PATH)
    cursor: sqlite3.Cursor = conn.cursor()
    
    # Create Table
    # PK is now (sensor_id, insert_timestamp)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensors (
            sensor_id TEXT,
            insert_timestamp TIMESTAMP,
            type TEXT,
            value REAL,
            unit TEXT,
            upload_freq TEXT,
            PRIMARY KEY (sensor_id, insert_timestamp)
        )
    ''')
    
    # Check if data exists
    cursor.execute("SELECT count(*) FROM sensors")
    count_result: Tuple[int] = cursor.fetchone()
    
    if count_result[0] == 0:
        print(f"[SQL] Seeding database with {len(SEED_DATA)} entries...")
        
        # Prepare data for insertion using Pydantic models
        insert_data: List[Tuple[Any, ...]] = [
            (
                reading.sensor_id, 
                reading.insert_timestamp, 
                reading.type, 
                reading.value, 
                reading.unit, 
                reading.upload_freq
            )
            for reading in SEED_DATA
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO sensors (sensor_id, insert_timestamp, type, value, unit, upload_freq)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', insert_data)
        
        conn.commit()
        print(f"[SQL] Seed complete.")
    else:
        print("[SQL] Database already contains data. Skipping seed.")
    
    conn.close()

def get_hive_data(query_string: str) -> str:
    """
    Simulates an MCP Tool to query the SQL database.
    Retains 'str' -> 'str' signature for Tool compatibility, 
    but uses Pydantic internally for row validation.
    """
    conn: sqlite3.Connection = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor: sqlite3.Cursor = conn.cursor()
    
    # We want the LATEST reading for each sensor usually
    sql: str = """
        SELECT * FROM sensors s1
        WHERE insert_timestamp = (
            SELECT MAX(insert_timestamp) 
            FROM sensors s2 
            WHERE s2.sensor_id = s1.sensor_id
        )
    """
    params: List[Any] = []
    
    # Basic keyword search mock
    query_lower: str = query_string.lower()
    if "temp" in query_lower:
        sql += " AND type = 'temperature'"
    elif "humid" in query_lower:
        sql += " AND type = 'humidity'"
    elif "weight" in query_lower:
        sql += " AND type = 'weight'"
        
    cursor.execute(sql, params)
    rows: List[sqlite3.Row] = cursor.fetchall()
    conn.close()
    
    if not rows:
        return "No sensor data found."
    
    # Parse rows into Pydantic models and then format
    results: List[str] = []
    for row in rows:
        # Validate data integrity via Pydantic
        # Note: SQLite stores timestamps as strings often, Pydantic parses them back to datetime
        reading: SensorReading = SensorReading(
            sensor_id=row['sensor_id'],
            insert_timestamp=row['insert_timestamp'],
            type=row['type'],
            value=row['value'],
            unit=row['unit'],
            upload_freq=row['upload_freq']
        )
        
        results.append(f"Sensor {reading.sensor_id} ({reading.type}): {reading.value}{reading.unit} (Timestamp: {reading.insert_timestamp})")
    
    return "\n".join(results)

# --- 2. Vector Database Component (The "Bee Manual") ---

def init_vector_db() -> None:
    """Reads PDFs from DOC_FOLDER and rebuilds the Vector DB."""

    if not os.path.exists(DOC_FOLDER):
        os.makedirs(DOC_FOLDER)
        print(f"[Vector] Created '{DOC_FOLDER}' directory. Please add PDFs.")
        return

    pdf_files: List[str] = glob.glob(os.path.join(DOC_FOLDER, "*.pdf"))
    if not pdf_files:
        print(f"[Vector] No PDFs found in '{DOC_FOLDER}'. Vector DB will be empty.")
        return

    print(f"[Vector] Found {len(pdf_files)} PDF(s). Processing...")
    
    documents: List[Document] = []
    for pdf_path in pdf_files:
        # 1. Loader: Reads raw text from PDF files
        loader = PyPDFLoader(pdf_path)
        # 2. Splitter: Breaks large documents into smaller chunks (pages) for LLM context
        docs: List[Document] = loader.load_and_split()
        documents.extend(docs)
        
    if documents:
        # 3. Embedder: Converts text chunks into numerical vectors (semantic meaning)
        embeddings = OpenAIEmbeddings()
        # 4. Vector Store: Saves vectors locally for similarity search
        Chroma.from_documents(
            documents=documents, 
            embedding=embeddings, 
            persist_directory=VECTOR_DB_PATH
        )
        print(f"[Vector] Database built with {len(documents)} chunks.")
    else:
        print("[Vector] No content extracted from PDFs.")

def search_bee_manual(query_string: str) -> str:
    """
    Simulates an MCP Tool to search the Vector Database.
    
    This function implements the 'Retrieval' phase of RAG:
    1. Query Embedding: Converts the user's question (e.g., "ideal temperature") into a vector using the same OpenAI model.
    2. Similarity Search: Queries ChromaDB to find the top k (3) document chunks whose vectors are mathematically closest 
       (cosine similarity) to the query vector. This finds the most semantically relevant text.
    3. Context Loading: Retrieves the actual text content of those top chunks.
    4. Return: Returns the text to the Agent, which uses it as 'Context' to answer the user's question.
    """

    if not os.path.exists(VECTOR_DB_PATH):
        return "Error: Vector database not initialized. (Run main.py first)"
        
    try:
        # 1. Query Embedding: Converts user question into a vector
        embeddings = OpenAIEmbeddings()
        vector_db = Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=embeddings)
        
        # 2. Similarity Search: Finds top k chunks semantically closest to the query
        results: List[Document] = vector_db.similarity_search(query_string, k=3)
        
        # 3. Context Loading: Retrieves text content from top chunks
        if not results:
            return "No relevant info found in the Bee Manual."
            
        context: str = "\n---\n".join([doc.page_content for doc in results])
        return f"From Bee Manual:\n{context}"
        
    except Exception as e:
        return f"Error querying Vector DB: {str(e)}"

# --- Self-Run for Testing ---
if __name__ == "__main__":
    # Test initialization directly if run as script
    init_sql_db()
    init_vector_db()
    print("Test Query (SQL):", get_hive_data("temperature"))
    print("Test Query (Vector):", search_bee_manual("ideal temperature"))
