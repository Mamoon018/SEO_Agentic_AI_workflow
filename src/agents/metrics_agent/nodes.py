
from src.agents.metrics_agent.state import metrics_state
from src.agents.metrics_agent.schemas import PROMPT_CITATION_FORMATTER_SCHEMA,BRAND_GEO_METRICS_SCHEMA
from src.agents.subgraphs.edges import prompt_caller_builder_workflow
from src.agents.metrics_agent.prompts import BRAND_GEO_METRICS_PROMPT
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from src.utils.models_initializer import initialize_model_with_fallbacks
from src.utils.models_initializer import get_openai_model,get_gemini_model
from typing import Any

# lets initialize model for the brand_geo_metrics_node
GEO_METRICS_MODEL_WITH_FALLBACK = initialize_model_with_fallbacks(
    primary_model_fn=get_openai_model,
    primary_model_kwargs={"model_num":2, "temperature":0.2},
    fallback_model_fns=[get_gemini_model],
    fallback_model_kwargs_list=[{"model_num":1,"temperature":0.2}],
    structured_output_schema=BRAND_GEO_METRICS_SCHEMA

)


# Article prompt caller subgraph invoker
async def article_prompt_caller_subgraph_invoker(state:metrics_state):

    """
    It takes the article related contextual prompts as an input and invoke the subgraph of prompts response caller
    that gives the formatted results of the llm response for each prompt. 

    **Args:**
    article_contextual_prompts (list[str]): It is the list of article related contextual prompts for which we will get responses.

    **Returns:**
    prompts_with_citations (list[dict[str,str|list[dict[str,str]]]]): It is the formatted results of the prompts, llm response for prompts, and their citations respectively.

    **Raises:**
    It raises the error if it is unable to invoke the subgraph.

    """

    # lets get the input variable
    article_contextual_prompts: list[str] = state["article_contextual_prompts"]

    # lets initialize the final output of the subgraph which is prompts and their citations in required format
    prompts_with_citations: list[dict[str,str|list[dict[str,str]]]] = []

    try:
        # lets invoke the prompts caller subgraph
        formatted_citations: PROMPT_CITATION_FORMATTER_SCHEMA = await prompt_caller_builder_workflow.ainvoke(input={"contextual_prompts":article_contextual_prompts})

        # lets get the output of the subgraph
        prompts_with_citations = formatted_citations["prompts_with_citations"]


        return {
            "prompts_with_citations": prompts_with_citations
        }

    except Exception as e:
        raise RuntimeError(f"Error occurred in the article prompt caller subgraph invoker due to {e}") from e



# Brand prompt caller subgraph
async def brand_prompt_caller_subgraph_invokder(state:metrics_state):
    """
    It takes the brand related contextual prompts as an input and invokes the subgraph that contains node related 
    to getting llm response for each prompt, and also format the llm response into required format. 

    **Args:** 
    brand_contextual_prompts (list[str]): It is the list of the brand related contextual prompts for which we need to get llm response

    **Returns:**
    prompts_with_citations: list[dict[str,str|list[dict[str,str]]]] 
    
    **Raises:**
    It raises the error when it is unable to invoke the subgraph
    """

    # lets get the input variables 
    brand_contextual_prompts: list[str] = state["brand_contextual_prompts"]

    # lets initialize the prompts_with_citations
    prompts_with_citations: list[dict[str,str|list[dict[str,str]]]] = []

    try:

        # lets invoke the subgraph 
        formatted_citations: PROMPT_CITATION_FORMATTER_SCHEMA = await prompt_caller_builder_workflow.ainvoke(input={"contextual_prompts":brand_contextual_prompts})

        # lets fetch the results from subgraph 
        prompts_with_citations = formatted_citations["prompts_with_citations"]

        return {
            "prompts_with_citations": prompts_with_citations
        }

    except Exception as e:
        raise RuntimeError(f"Error raised in brand prompt caller subgraph invoker due to {e}") from e 


async def brand_geo_metrics(state:metrics_state):

    """
    It takes the llm response, citations that appear in the response and their details to calculate the 
    metrics according to the given criteria. 

    **Args:**
    prompts_with_citations (list[dict[str,str|list[dict[str,str]]]]): It is the formatted response of the llm for the contextual
    prompts which will be used to calculate metrics.

    **Returns:**
    brand_geo_metrics (list): It returns the list of different geo metrics for the brand visibility
    
    """

    # lets get the input variables from the state
    prompts_with_citations: list[dict[str,str|list[dict[str,str]]]] = state["prompts_with_citations"]

    brand_name: str = state["brand_name"]

    # lets get the prompt 
    prompt = PromptTemplate(input_variables=["prompts_with_citations","brand_name"], template= BRAND_GEO_METRICS_PROMPT )
    brand_geo_metrics_prompt = prompt.format(prompts_with_citations=prompts_with_citations, brand_name= brand_name)

    # lets initialize the object to store output
    brand_metrics: list[Any]

    try:
        # lets invoke the llm 
        brand_geo_metrics_response: BRAND_GEO_METRICS_SCHEMA = await GEO_METRICS_MODEL_WITH_FALLBACK.ainvoke(
            [HumanMessage(content=brand_geo_metrics_prompt)]
        )

        brand_metrics = brand_geo_metrics_response.brand_metrics

        return {
            "brand_metrics": brand_metrics
        }

    except Exception as e:
        raise RuntimeError(f"Error occurred in brand geo metrics due to {e}") from e 