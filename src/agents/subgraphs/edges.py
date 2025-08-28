
from src.agents.subgraphs.nodes import diffbot_text_extracter, gkp_caller, keyword_shortlister
from langgraph.graph import StateGraph, START, END
from src.agents.subgraphs.state import text_extracter_state, prompt_generator_subgraph_state
                            #### Text Extracter Subgraph Edges ####

text_extracter_builder = StateGraph(text_extracter_state)
text_extracter_builder.add_node(node="diffbot_text_extracter", action=diffbot_text_extracter)

text_extracter_builder.add_edge(START,"diffbot_text_extracter")
text_extracter_builder.add_edge("diffbot_text_extracter",END)

text_extracter_workflow = text_extracter_builder.compile()

                            #### Prompt Generator Subgraph Graph ####

prompt_generator_builder = StateGraph(prompt_generator_subgraph_state)
prompt_generator_builder.add_node(node="gkp_caller",action=gkp_caller)
prompt_generator_builder.add_node(node="keyword_shortlister", action=keyword_shortlister)


prompt_generator_builder.add_edge(START,"gkp_caller")
prompt_generator_builder.add_edge("gkp_caller","keyword_shortlister")
prompt_generator_builder.add_edge("keyword_shortlister", END)

prompt_generator_builder_workflow = prompt_generator_builder.compile()
