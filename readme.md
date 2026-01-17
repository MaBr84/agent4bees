
# 🐝 Hive SME: Intelligent Bee Health Monitor

A proof-of-concept AI agent built in 60 minutes. This project demonstrates how to use **LangGraph** and **GPT-4o-mini** to bridge the gap between real-time SQL sensor data and static biological manuals.

---

## 🚀 Quick Start (5-Minute Setup)

To fit a one-hour deadline, this project uses a `.env` file for secure API management.

### 0. Install Python (Windows)

If you have not installed Python yet:
1. Open the Microsoft Store.
2. Search for **Python 3.12** (or latest).
3. Click **Get** or **Install**.
4. Verify by opening a terminal (PowerShell) and typing `python --version`.

### 1. Get your OpenAI API Key
* Go to the [OpenAI Dashboard](https://platform.openai.com/).
* Create a new secret key named **"Hive Demo"** and copy it.

### 2. Install Dependencies
Run the following command in your terminal:
```bash
pip install python-dotenv langchain-openai langgraph
pip install langchain-openai langchain-chroma pypdf
pip install langchain_community
pip install --upgrade langchain-core langchain-openai langchain-chroma langchain-community pydantic
```

### 3. Configure Environment Variables

Create a file named `.env` in this folder (same location as `readme.md`) and paste your key:

```plaintext
OPENAI_API_KEY=sk-your-actual-key-here
```

---

## 🧠 Project Architecture

The system follows a modular architecture, separating data logic, agent orchestration, and initialization:

### 1. The Application Layer (`app/`)
The core logic resides in the `app/` package:
*   **`database.py`**: The "Connector" layer. It handles:
    *   **SQL Operations**: Interacting with the mock SQLite database for sensor data.
    *   **Vector Operations**: Interacting with the Chroma vector store for semantic search in the PDF manual.
*   **`models.py`**:  Defines the data structures (Pydantic models) used throughout the application to ensure data consistency.
*   **`seed_data.py`**:  Contains the logic and sample data used to populate the mock database during initialization.

### 2. The Agent Logic (`agent.py`)
The intelligent core of the system. It uses **LangGraph** to:
1.  **Reason**: Analyze user queries to understand intent.
2.  **Act**:  Decide whether to query the SQL database (for sensor stats) or the Vector store (for biological facts).
3.  **Synthesize**:  Combine retrieved information into a coherent, expert-level response.

### 3. The Initialization (`main.py`)
The system bootstrapper. It performs the necessary checks and setup steps:
*   Validates environment variables (API keys).
*   Initializes and seeds the SQL database.
*   Sets up the Vector store and ingests the PDF documents.

---

## 🛠️ How to Run the Demo

### Step 1: Initialize the System
Run the setup script to prepare the database and environment:
```bash
python main.py
```

### Step 2: Launch the Agent
Start the interactive agent loop:
```bash
python agent.py
```

### Example Query
> *"What is the temperature right now, is it healthy, and how often is this data loaded?"*

**The AI's Logic Path:**
1.  **Fetch SQL Data (`get_hive_data`)**: Retrieves current temp (e.g., 34.5°C) and generic metadata.
2.  **Check Biology Manual (`search_bee_manual`)**: Validates that 34.5°C falls within the healthy 32-35°C range.
3.  **Synthesis**:  Combines live data + expert knowledge + chat history into one helpful answer.

---

## 📈 Demo Highlights

*   **Secure Configuration**: Uses `.env` for API key management.
*   **Hybrid Intelligence**: Seamlessly merges validatable SQL data with unstructured knowledge bases.
*   **Agentic Workflow**: Uses LangGraph state machines instead of brittle if/else chains.
