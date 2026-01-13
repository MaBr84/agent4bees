
# 🐝 Hive SME: Intelligent Bee Health Monitor

A proof-of-concept AI agent built in 60 minutes. This project demonstrates how to use **LangGraph** and **GPT-4o-mini** to bridge the gap between real-time SQL sensor data and static biological manuals.

---

## 🚀 Quick Start (5-Minute Setup)

To fit a one-hour deadline, this project uses a `.env` file for secure API management.

### 1. Get your OpenAI API Key
* Go to the [OpenAI Dashboard](https://platform.openai.com/).
* Create a new secret key named **"Hive Demo"** and copy it.

### 2. Install Dependencies
Run the following command in your terminal:
```bash
pip install python-dotenv langchain-openai langgraph

```

### 3. Configure Environment Variables

Create a file named `.env` in the root directory and paste your key:

```plaintext
OPENAI_API_KEY=sk-your-actual-key-here

```

---

## 🧠 Project Architecture

The system is divided into three distinct phases:

### Phase 1: The Knowledge Base (`database.py`)

This file simulates our data sources:

* **SQL Database:** A mock SQLite DB containing sensor metadata (e.g., Sensor S1, MQTT upload frequencies).
* **The "Bee Manual":** A tool that provides biological thresholds (e.g., ideal hive temperature is 32-35°C).

### Phase 2: The Orchestrator (`main.py`)

The "brain" of the operation. It uses a **ReAct Agent** pattern to:

1. Analyze a user query.
2. Decide which tool to call (`get_hive_data` or `bee_manual`).
3. Synthesize a human-readable health report.

---

## 🛠️ How to Run the Demo

Execute the main script to see the agent in action:

```bash
python main.py

```

### Example Query

> *"What is the temperature right now, is it healthy, and how often is this data loaded?"*

**The AI's Logic Path:**

1. **Fetch SQL Data:** Retrieves current temp (34.5°C) and upload frequency (15 mins).
2. **Check Biology Manual:** Validates that 34.5°C falls within the healthy 32-35°C range.
3. **Synthesis:** Combines both technical and biological data into one response.

---

## 📈 Demo Highlights ("The Sizzle")

* **Security First:** Uses `.env` variables to prevent hardcoding sensitive keys.
* **Multi-Source Reasoning:** The agent successfully merges **live data** (SQL) with **expert knowledge** (Manual).
* **Autonomous Tool Use:** The model determines which functions to call without hardcoded "if/else" logic.

---

*Developed as a high-speed technical demonstration of LangGraph and LLM Orchestration.*

