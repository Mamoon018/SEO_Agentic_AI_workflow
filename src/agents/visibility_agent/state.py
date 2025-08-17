"""
Lets build the state for the visibility agent 
"""
# Let's get the imports
from typing import Optional, Union, Annotated
from pydantic import AnyUrl
from langgraph.graph import MessagesState
import operator

class visibility_state(MessagesState):

    # Input url of the user
    user_url: AnyUrl
    
    # Output of the extract_user_article node. It contains the information about the user article (either scrapped data or error message)
    scrapped_article: Optional[Union[dict[str,str],str]]

    # bool for tool execution confirmation
    output_confirmation : bool

    # list of entities extracted from the article
    entities: list[str]

    # list of gkp planner keywords
    gkp_planner_list1: list[dict[str, str | int | dict[str,int]]]

    # list of the shortlisted keywords
    shortlisted_keywords: list[str]

    # list of contextual-prompts
    contextual_prompts: list[str]

    # list of the articles cited by LLM
    perplexity_response: Annotated[list[str], operator.add]


