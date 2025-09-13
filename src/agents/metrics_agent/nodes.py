
from src.agents.metrics_agent.state import metrics_state
from src.agents.metrics_agent.schemas import PROMPT_CITATION_FORMATTER_SCHEMA
from src.agents.subgraphs.edges import prompt_caller_builder_workflow
from src.agents.metrics_agent.test_data import prompts_with_citations



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
