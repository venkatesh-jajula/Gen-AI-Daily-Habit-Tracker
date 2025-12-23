from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
# predefined LangGraph node : Register tools, LLm picks tool, ToolNode executes the function, result is returned back into the graph.
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

from app.agent.state import AgentState
from app.agent.prompts import SYSTEM_PROMPT
from app.tools.habit_tools import add_habit,tick_habit,get_weekly_summary,list_habits,daily_status

# Registering a list of tools (Python functions)
TOOLS=[add_habit,tick_habit,get_weekly_summary,list_habits,daily_status]

def build_graph(model_name):
    # Constructs the agent
    llm = ChatOpenAI(model=model_name, temperature=0).bind_tools(TOOLS)

    tool_node = ToolNode(TOOLS)

    def llm_node(state: AgentState):
        messages = state["messages"]
        resp = llm.invoke([SystemMessage(content=SYSTEM_PROMPT), *state["messages"]])
        return {"messages":messages + [resp], "tool_outputs": state.get("tool_outputs", [])}
    
    def route(state: AgentState):
        """This is a router function that decides whether the graph should run the Tools node or stop execution."""
        last = state["messages"][-1]
        return "tools" if getattr(last, "tool_calls", None) else "end" # If the LLM wants to use a tool → tool_calls exists If not → tool_calls does not exist
    
    graph = StateGraph(AgentState)
    graph.add_node("llm",llm_node)
    graph.add_node("tools",tool_node)

    graph.add_edge(START,"llm")
    graph.add_conditional_edges(
        "llm",
        route,
        {
            "tools": "tools",
            "end": END
            }
    )
    graph.add_edge("tools","llm")

    app_graph = graph.compile()
    # Export workflow diagram as PNG 
    app_graph.get_graph().draw_mermaid_png(output_file_path="workflow.png")

    return app_graph


def run_agent(app_graph, user_text: str) -> str:
    # runs the agent once - Execution
    init: AgentState = {"messages": [HumanMessage(content=user_text)]}
    out = app_graph.invoke(init)
    return out["messages"][-1].content


"""Bind Tools: These tools exist. You are allowed to use them whenever they are relevant

LLM NODE - sends the current conversation state to the LLM and adds the LLMs response back into the state.
Example:
State Before: [HumanMessage("add habit gym")]
LLM node output: AIMessage(
  tool_calls=[{"name": "add_habit", "arguments": {"name": "gym"}}]
)
state After:  [
  HumanMessage("add habit gym"),
  AIMessage(tool_calls=[...])
]

TOOLS NODE - executes the tool that the LLM asked for and adds the tools result back into the state.
Example:
[
  HumanMessage("add habit gym"),
  AIMessage(tool_calls=[...]),
  ToolMessage("Added Habit: gym")
]


"""