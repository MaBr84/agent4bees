"""
agent.py

The main entry point for the "Hive SME" Agent.
Uses LangGraph to orchestrate reasoning and tool usage.
"""

import os
import sys
from typing import Annotated, Literal, Union

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages

# Import tools from our app package
from app.database import get_hive_data, search_bee_manual

# 1. Load Environment
load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY not found in .env")
    print("Please create .env file with your key.")
    sys.exit(1)

# 2. Define Tools
class HiveQuery(BaseModel):
    query: str = Field(description="The natural language query to search hive data.")

@tool(args_schema=HiveQuery)
def tool_get_hive_data(query: str) -> str:
    """
    Query the Hive SQL Database for sensor readings.
    Useful for questions like "What is the temperature?", "Show me humidity readings".
    """
    return get_hive_data(query)

class ManualQuery(BaseModel):
    query: str = Field(description="The natural language query to search the manual.")

@tool(args_schema=ManualQuery)
def tool_search_bee_manual(query: str) -> str:
    """
    Search the Bee Manual (PDF Knowledge Base) for biological facts.
    Useful for questions like "What is the ideal temperature?", "Is 35 degrees healthy?".
    """
    return search_bee_manual(query)

tools = [tool_get_hive_data, tool_search_bee_manual]

# 3. Define State
class AgentState(BaseModel):
    messages: Annotated[list[BaseMessage], add_messages]

# 4. Define Nodes
def agent_node(state: AgentState) -> dict[str, list[BaseMessage]]:
    """
    The main agent node. Decides what to do next.
    """
    messages = state.messages
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    model = model.bind_tools(tools)
    response = model.invoke(messages)
    return {"messages": [response]}

# 5. Build Graph
workflow = StateGraph(AgentState)

workflow.add_node("agent", agent_node)
workflow.add_node("tools", ToolNode(tools))

workflow.set_entry_point("agent")

# Conditional edge: If agent produced tool_calls, go to 'tools', else END
workflow.add_conditional_edges(
    "agent",
    tools_condition,
)

# Edge: After tools run, go back to agent to synthesize answer
workflow.add_edge("tools", "agent")

app = workflow.compile()

# 6. Interactive Loop
if __name__ == "__main__":
    print("🐝 Hive SME Agent Ready! (Type 'exit' to quit)")
    print("---------------------------------------------")
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit", "q"]:
                break
            
            # Run the graph
            inputs = {"messages": [("user", user_input)]}
            print("Agent: Thinking...")
            
            # Stream events or just get final state. For CLI, streaming is nicer but simple invoke works.
            for event in app.stream(inputs, stream_mode="values"):
                pass
                
            # extracting final response
            final_message = event["messages"][-1]
            print(f"Agent: {final_message.content}\n")
            
        except Exception as e:
            print(f"Error: {e}")
