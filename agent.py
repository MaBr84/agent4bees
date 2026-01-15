"""
agent.py

SPECIFICATIONS:
---------------------------------------------------------
1. Agent Type:
   - Architecture: ReAct (Reasoning + Acting) Agent.
   - Framework: LangGraph (StateGraph).
   - Model: GPT-4o-mini (via OpenAI API).

2. Tool Integration (MCP Clients):
   - The agent does NOT define the logic for data access.
   - It consumes tools provided/defined in `database.py` (via MCP pattern).
   - Tools:
     - `get_hive_data`: To check current sensor readings.
     - `search_bee_manual`: To check biological constraints/info.

3. Workflow:
   - Input: User natural language query.
   - Node 1 (Agent): Decides to call a tool or answer.
   - Node 2 (Tools): Executes the selected tool (SQL or Vector search).
   - Loop: Returns to Agent with tool output.
   - End: Generates final synthesized response.

4. Execution:
   - Validates `.env` API keys.
   - Compiles the graph.
   - Runs the graph with the user input.
"""
