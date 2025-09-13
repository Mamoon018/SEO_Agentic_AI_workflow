from langgraph.graph import MessagesState
from typing import Optional, Union, Annotated
import operator
from pydantic import AnyUrl


                                    ####  Text extracter subgraph state  ####

class text_extracter_state(MessagesState):

    # temporarily added user url variable to test the subgraph as it will be provided by the  ---> NEED TO REMOVBE FOR FINAL TEST as we are passing this as user input.
    user_url: AnyUrl


    # scrapped article text
    scrapped_text: Optional[Union[dict[str,str],str]] 

    # bool for tool execution confirmation
    output_confirmation : bool


                                    ####  Prompt generator subgraph state  ####

class prompt_generator_subgraph_state(MessagesState):

    user_url: AnyUrl
    
    entities: list[str]
    
    # GKP caller node output: list of keywords and their metrics
    gkp_planner_list: list[dict[str, str | int | dict[str,int]]]

    # Keyword shortlister node output: list of keywords shortlisted based on their metrics
    shortlisted_keywords: list[str]


                                    ####  Prompts call send api subgraph state  ####

class prompts_caller_subgraph_state(MessagesState):

    # contextual prompts received by the subgraph from the main graph
    contextual_prompts: list[str]

    # llm name to be used will be received as an input variable for the node
    llm_name: str

    # citation for prompts node will return the llm_response for all contextual prompts as an output
    llm_response: Annotated[list[str], operator.add]

    # prompt response reducer will convert the raw output of the llm into strctured output
    # structured output of llm response
    prompts_with_citations: list[dict[str,str|list[dict[str,str]]]]

