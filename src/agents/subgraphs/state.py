from langgraph.graph import MessagesState
from typing import Optional, Union
from pydantic import AnyUrl


                                    ####  Text extracter subgraph state  ####

class text_extracter_state(MessagesState):

    # temporarily added user url variable to test the subgraph as it will be provided by the  ---> NEED TO REMOVBE FOR FINAL TEST as we are passing this as user input.
    user_url: AnyUrl


    # scrapped article text
    scrapped_article: Optional[Union[dict[str,str],str]] 

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


