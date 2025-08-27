from langgraph.graph import MessagesState
from typing import Optional, Union
from pydantic import AnyUrl


                                    ####  Text extracter subgraph state  ####

class text_extracter_state(MessagesState):

    # temporarily added user url variable to test the subgraph ---> NEED TO REMOVBE FOR FINAL TEST
    user_url: AnyUrl


    # scrapped article text
    scrapped_article: Optional[Union[dict[str,str],str]] 

    # bool for tool execution confirmation
    output_confirmation : bool
