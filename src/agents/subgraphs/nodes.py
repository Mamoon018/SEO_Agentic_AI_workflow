
from src.agents.subgraphs.state import text_extracter_state
from src.agents.subgraphs.schemas import text_extracter_schema
from src.tools.web_extractor_tool import DIFFBOT_TOOL
from pydantic import AnyUrl
from typing import Optional, Union



                    ####  Text Extracter Subgraph Nodes  ####

async def diffbot_text_extracter(state:text_extracter_state):
    """
    It takes the url of the article/site as an input and executes the diffbot tool to extract the content on the site.
    
    **Args:**
    user_url (Anyurl): It is the url of the article/site from which diffbot needs to extract the content.

    **Returns:**
    scraping_output: It is the output of the DIFFBOT tool. If article is accessible then we will get scrapped information
    stored in dictionary as an output. If article is inaccessible then we will get either of two error message specified 
    in the DIFFBOT tool.

    **Raises:**
    It raises the error if tool is unable to get initialized or API fails.

    """

    # let's get the input variable from the state
    user_url: AnyUrl = state["user_url"]

    # Let's initialize the scrapped_article object 
    scrapped_article: Optional[Union[dict[str,str],str]] = {}

    # lets initialize the boolean variable to confirm if output is returned so, that we can proceed with workflow
    output_confirmation: bool = True 

    # lets get the DIFFBOT tool and generate the output of the node
    try:

        # lets get the instance of the diffbot tool class to access its method 
        scrapping_tool = DIFFBOT_TOOL()
        
        # lets execute the diffbot tool
        scrapping_output: text_extracter_schema = await scrapping_tool._arun(user_url=user_url)

        # lets define value of output_confirmation based on the output of the tool
        if scrapping_output in ("Client/Server side error", "Invalid URL"):
            output_confirmation = False 

        # lets store the output of the tool in the initialized variable
        scrapped_article: dict[str,str] = scrapping_output

        return {"scrapped_article": scrapped_article,
                "output_confirmation": output_confirmation}

    except Exception as e:
        raise RuntimeError(f"error raised due to {e}")

