
from src.agents.subgraphs.state import text_extracter_state, prompt_generator_subgraph_state
from src.agents.subgraphs.schemas import text_extracter_schema, keyword_shortlister_schema
from src.agents.subgraphs.prompts import prompt_generator_prompt
from src.tools.web_extractor_tool import DIFFBOT_TOOL
from src.utils.keyword_preprocessor import keyword_processor
from src.utils.models_initializer import initialize_model_with_fallbacks, get_openai_model
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from pydantic import AnyUrl
from typing import Optional, Union
from src.agents.visibility_agent.temp_data import planner_list1



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




                                ####  Prompts generator subgraph nodes  ####

# gkp Caller Node
async def gkp_caller(state:prompt_generator_subgraph_state):
    """
    It feeds all extracted entities to google keyword planner as seed keywords and in return google keyword planner
    provides us relevant primary and secondary keywords along with their metrics and it also uses user_url as input along
    with extracted entities.

    **Args:**
    entities (list): It is the list of extracted entities from the article. It will be used as seed keywords in Google Keyword Planner.
    user_url (Anyurl): It is the url of an article provided by user.

    **Returns:**
    gkp_planner_list: It is the list of the keywords of google planner
    
    """

    try:

        user_url: AnyUrl = state["user_url"]
        entities: list[str] = state["entities"]

        # lets initialize the object that will store the gkp_planner_list
        #gkp_planner_list: GKP_CALLER = await gkp.generate_keywords(keywords=entities,url=user_url)

        # For now, we will use dummy results of the gkp.generate_keywords
        gkp_planner_list: list[dict[str, str | int | dict[str,int]]] = planner_list1


        return {
            "gkp_planner_list": gkp_planner_list
        }

    except Exception as e:
        raise RuntimeError(f"error occured in gkp_caller due to {e}") from e



# Keyword Processor Node
async def keyword_shortlister(state:prompt_generator_subgraph_state):
    """
    It takes the keywords from the gkp_planner_list and based on the criteria to shortlist the top keywords only, it
    generates the list in the output that contains only keywords with higher proportion of share in the total combined
    search volume of all keywords.
    
    """

    # lets get the input variable
    gkp_planner_list: list[dict[str, str | int | dict[str,int]]] = state["gkp_planner_list"]

    # lets initialize the shortlisted keywords
    shortlisted_keywords: list[str] = []

    try:
        # lets get the keywords 
        shortlisted_keywords_response: keyword_shortlister_schema = keyword_processor(gkp_planner_list)

        # lets store the output of the node in the initialized variable

        shortlisted_keywords = shortlisted_keywords_response

        return {
            "shortlisted_keywords": shortlisted_keywords
        }

    except Exception as e:
        raise RuntimeError(f"Error occurred keyword shortlister node in {e}") from e 



