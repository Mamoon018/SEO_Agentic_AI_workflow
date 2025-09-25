
from langgraph.graph import StateGraph, START, END
from src.agents.metrics_agent.nodes import article_prompt_caller_subgraph_invoker, brand_prompt_caller_subgraph_invokder,brand_geo_metrics_calculator, article_geo_metrics_calculator
from src.agents.metrics_agent.state import metrics_state


# Task label router
def task_label_router(state:metrics_state):
    """
    It is the router that checks the type of the task it recieved from the previous workflow, and accordingly
    signals current workflow to either execute Article branch or Brand branch 
    """

    task_label = state["task_label"]
    
    if task_label == "Article task":
        return "Article task"
    if task_label == "Brand task":
        return "Brand task"

                                        ####   Compiling Graph for the Workflow   ####

builder = StateGraph(metrics_state)

builder.add_node(node="article_prompt_caller_subgraph_invoker", action=article_prompt_caller_subgraph_invoker)
builder.add_node(node="brand_prompt_caller_subgraph_invokder", action=brand_prompt_caller_subgraph_invokder)
builder.add_node(node="brand_geo_metrics_calculator",action=brand_geo_metrics_calculator)
builder.add_node(node="article_geo_metrics_calculator",action=article_geo_metrics_calculator)

builder.add_conditional_edges(
    source= START,
    path= task_label_router,
    path_map= {"Article task": "article_prompt_caller_subgraph_invoker",
        "Brand task": "brand_prompt_caller_subgraph_invokder"
    }
    )

builder.add_edge("brand_prompt_caller_subgraph_invokder","brand_geo_metrics_calculator")
builder.add_edge("brand_geo_metrics_calculator",END)
builder.add_edge("article_prompt_caller_subgraph_invoker","article_geo_metrics_calculator")
builder.add_edge("article_geo_metrics_calculator",END)
geo_metrics_workflow = builder.compile()

