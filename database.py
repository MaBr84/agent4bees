"""
database.py

SPECIFICATIONS:
---------------------------------------------------------
1. SQL Database Component:
   - Technology: SQLite (mock data).
   - Data Model:
     - Table: `sensors`
     - Columns: `sensor_id` (PK), `type` (e.g., 'temperature'), `value` (float), `upload_freq` (string).
   - MCP Integration:
     - Expose a resource or tool via Model Context Protocol (MCP) to query this data.
     - Function: `get_hive_data(query_string)` -> returns variable structured data.

2. Vector Database Component (The "Bee Manual"):
   - Source: PDF documents located in `doc/` folder.
   - Technology: Local Vector Store (e.g., ChromaDB, FAISS, or simple in-memory numpy mock for PoC).
   - Pipeline:
     - Load PDF.
     - Chunk text.
     - Embed using a lightweight embedding model (e.g., all-MiniLM-L6-v2).
     - Store in Vector DB.
   - MCP Integration:
     - Expose a tool via MCP: `search_bee_manual(query_string)`.
     - Returns: Relevant context/chunks from the manual.

3. Responsibility:
   - This module handles all "Knowledge Base" interactions.
   - It acts as the server-side logic for the data tools.
"""
