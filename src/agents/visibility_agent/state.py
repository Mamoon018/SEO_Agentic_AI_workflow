"""
Lets build the state for the visibility agent 
"""
# Let's get the imports
from typing import Literal, Any, Optional
from pydantic import AnyUrl
from langgraph.graph import MessagesState


class visibility_state(MessagesState):

    # Input url of the user
    user_url: AnyUrl
    
    # Output of the extract_user_article node. It contains the information about the user article 
    scrapped_article: dict[str,str]



