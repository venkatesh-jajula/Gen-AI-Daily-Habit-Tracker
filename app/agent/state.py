from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

"""
TypedDict:shape of a dictionary.
messages stores the conversation history:
                        HumanMessage : What user said
                        AIMessage : what LLLM replied
                        ToolMessage : what a tool returned
                        SystemMessage : Rules for LLM

Why state? Each step must see what happened before, So we need one shared memory object which is "state".    
add_messages : appends the new messsages instead of replacing.
Annotated : wrapper that combines both
Example:
state = {
    "messages": [
        HumanMessage("add habit gym"),
        AIMessage("Calling add_habit tool"),
        ToolMessage("Habit gym added"),
        AIMessage("Gym habit successfully added.")
    ]
}
"""