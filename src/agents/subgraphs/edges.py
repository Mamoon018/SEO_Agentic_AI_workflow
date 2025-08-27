
from src.agents.subgraphs.nodes import diffbot_text_extracter
from langgraph.graph import StateGraph, START, END
from src.agents.subgraphs.state import text_extracter_state
                            #### Text Extracter Subgraph Edges ####

text_extracter_builder = StateGraph(text_extracter_state)
text_extracter_builder.add_node(node="diffbot_text_extracter", action=diffbot_text_extracter)

text_extracter_builder.add_edge(START,"diffbot_text_extracter")
text_extracter_builder.add_edge("diffbot_text_extracter",END)

text_extracter_workflow = text_extracter_builder.compile()

