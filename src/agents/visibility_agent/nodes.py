

from src.agents.visibility_agent.state import visibility_state
from src.agents.visibility_agent.schemas import EXTRACT_USER_ARTICLE_SCHEMA, ENTITIES_EXTRACTOR_SCHEMA, KEYWORD_SHORTLISTER_SCHEMA
from src.agents.visibility_agent.prompts import ENTITIES_EXTRACTOR_PROMPT
from src.tools.web_extractor_tool import DIFFBOT_TOOL
from src.utils.settings import get_key, settings
from pydantic import AnyUrl
from typing import Union, Optional
from langgraph.graph import StateGraph
from langgraph.graph import END, START
from langgraph.prebuilt import ToolNode, tools_condition
import asyncio
from src.agents.keywords_agent.nodes import GoogleKeywordsAPI
from src.agents.visibility_agent.temp_data import planner_list1


import numpy as np
from itertools import accumulate
import dotenv
import os 
dotenv.load_dotenv()
import opik
opik.configure(use_local=False)
from opik.integrations.langchain import OpikTracer
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage

from src.utils.models_initializer import initialize_model_with_fallbacks, get_mistral_model , get_openai_model

# extract_user_article model
ENTITIES_EXTRACTOR_MODEL_WITH_FALLBACKS= initialize_model_with_fallbacks(
    primary_model_fn=get_mistral_model,
    primary_model_kwargs={"model_num": 2, "temperature": 0.5},
    fallback_model_fns=[get_mistral_model],
    fallback_model_kwargs_list=[{"model_num": 1, "temperature": 0.5}],
    structured_output_schema=ENTITIES_EXTRACTOR_SCHEMA,
    #bind_tools=True, 
    #tools=[DIFFBOT_TOOL()],
    #tool_choice= "Web_scraping_tool"
)

# lets initialize the class of the google planner so, that we can use its method 
gkp = GoogleKeywordsAPI()



                                ####   Nodes of Graph   ####


### EXTRACT USER ARTICLE NODE ###
async def extract_user_article(state:visibility_state):

    """
    It takes the user_url as an input variable that will be provided by user to initiate the workflow. This node 
    simply calls the DIFFBOT Tool to scrap the content from that url. We will get the parsed output of the tool.
    It will be the dictionary containing fields and values storing article information.

    **Args:**
    user_url (Anyurl): It is the url of the article which needs to be scrapped. It is provided by the user as input.

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
        scrapping_output: EXTRACT_USER_ARTICLE_SCHEMA = await scrapping_tool._arun(user_url=user_url)

        # lets define value of output_confirmation based on the output of the tool
        if scrapping_output in ("Client/Server side error", "Invalid URL"):
            output_confirmation = False 

        # lets store the output of the tool in the initialized variable
        scrapped_article: dict[str,str] = scrapping_output

        return {"scrapped_article": scrapped_article,
                "output_confirmation": output_confirmation}

    except Exception as e:
        raise RuntimeError(f"error raised due to {e}")



### LLM ENTITIES EXTRACTOR ###

async def entities_extractor(state:visibility_state):
    """
    It extracts 1-3 most relevant entities from the text of the scrapped article.

    It will use the 'state["scrapped_article"]' to identify and extract most relevant entities discussed
    in the article in the context of the entire article. 
    Those entities will serve as a foundation for generating seed keywords in google keyword planner (GKP).

    **Args:**
    scrapped_article (dict): It will be used to access title of the article and text of the article.

    **Returns:**
    Entities (list): It is the list of the relevant entities.

    """

    # lets get the required input variables
    text_of_article: str = state["scrapped_article"].get("article_text","N/A")
    title_of_article: str = state["scrapped_article"].get("title","N/A")

    # lets get the prompt of the entities_extractor
    prompt = PromptTemplate(
        input_variables= ["text_of_article","title_of_article"],
        template= ENTITIES_EXTRACTOR_PROMPT
    )

    entities_prompt = prompt.format(text_of_article= text_of_article, title_of_article=title_of_article)

    # lets initialize the object to store the entities as a result of the node
    entities: list[str] = []

    # lets get the result of the LLM 
    entities_extractor_response: ENTITIES_EXTRACTOR_SCHEMA = await ENTITIES_EXTRACTOR_MODEL_WITH_FALLBACKS.ainvoke(
        input= [HumanMessage(content=entities_prompt)]
    )

    # lets store the output of the LLM in the entities object
    entities: list[str] = entities_extractor_response.entities

    # lets update the state with addition of entities in it
    return {
        "entities": entities
    }


### GKP CALLER - 1 NODE ###

async def gkp_caller1(state:visibility_state):
    """
    It feeds all extracted entities to google keyword planner as seed keywords and in return google keyword planner
    provides us relevant primary and secondary keywords along with their metrics and it also uses user_url as input along
    with extracted entities.

    **Args:**
    entities (list): It is the list of extracted entities from the article. It will be used as seed keywords in Google Keyword Planner.
    user_url (Anyurl): It is the url of an article provided by user.

    **Returns:**
    gkp_planner_list1: It is the list of the keywords of google planner
    
    """

    # let's get the input variables
    user_url: AnyUrl = state["user_url"]
    entities: list[str] = state["entities"]


    try:
        # lets initialize the object that will store the gkp_planner_list1
        #gkp_planner_list1: GKP_CALLER1 = await gkp.generate_keywords(keywords=entities,url=user_url)

        # For now, we will use dummy results of the gkp.generate_keywords
        gkp_planner_list1: list[dict[str, str | int | dict[str,int]]] = planner_list1


        return {
            "gkp_planner_list1": gkp_planner_list1
        }

    except Exception as e:
        raise RuntimeError(f"error occured in gkp_caller due to {e}") from e



### Keyword Processor Node

async def keyword_shortlister(state:visibility_state):
    """
    It takes the keywords from the gkp_planner_list1 and based on the criteria to shortlist the top keywords only, it
    generates the list in the output that contains only keywords with higher proportion of share in the total combined
    search volume of all keywords.
    
    """

    # lets get the input variable
    gkp_planner_list1: list[dict[str, str | int | dict[str,int]]] = state["gkp_planner_list1"]

    # lets initialize the shortlisted keywords
    shortlisted_keywords: list[str] = []

    try:
        # lets get the keywords 
        shortlisted_keywords_response: KEYWORD_SHORTLISTER_SCHEMA = keyword_processor(gkp_planner_list1)

        # lets store the output of the node in the initialized variable

        shortlisted_keywords = shortlisted_keywords_response

        return {
            "shortlisted_keywords": shortlisted_keywords
        }

    except Exception as e:
        raise RuntimeError(f"Error occurred keyword shortlister node in {e}") from e 











### GET THE TOP KEYWORDS FROM THE ### 

def keyword_processor(mainkeyword_list):

    # lets get the keyword planner list
    raw_keyword_list = mainkeyword_list
    # lets initialize the dictionary that will contain keywords and search volumes as values
    keywords_metrics = {}
    # list of the keywords
    keywords = []
    # list of the values
    metrics = []

    # lets fetch the keywords and their search volumes and put them all in a dict as keys & values
    for nested_dict in raw_keyword_list:

        keyword = nested_dict["text"]
        metric = nested_dict["average_monthly_searches"]

    # list of keywords and list of metrics
        keywords.append(keyword)
        metrics.append(metric)        

    # lets get the dictionary of the keywords & search volumes
    for x,y in zip(keywords,metrics):

        keywords_metrics[x] = y

    # lets sort the dictionary based on the search volumes in descending order
    keywords_metrics = dict(sorted(keywords_metrics.items(), key= lambda x:x[1] , reverse=True))

    # lets get the list of the values and list of the keys from the sorted dict
    sorted_values = list(keywords_metrics.values())
    sorted_keys = list(keywords_metrics.keys())
    
    # total search volume for all keywords
    total_search_volume = 0
    for volume_value in sorted_values:
        total_search_volume += volume_value

    # share of keyword value in total search volume
    share_of_values = []
    for metric_value in sorted_values:
        prop_of_value = metric_value/total_search_volume
        share_of_values.append(prop_of_value)
    
    # lets get the cumulative sum of all values
    cumulative_share_of_values = list(accumulate(share_of_values))

    # lets get the elbow-index for the 

    """
    1) Calculate the % by which each keyword contributes in the total search volume
    2) Calculate the marginal change in the contribution of the each keyword in the total search volume
    3) Keyword after which marginal contribution is least, that's the cutt-off point for us.
    """

    first_derivative = np.gradient(cumulative_share_of_values)
    second_derivative = np.gradient(first_derivative)
    elbow_index = int(np.argmin(second_derivative))

    # final shortlisted keywords
    shortlisted_keywords = sorted_keys[:elbow_index + 1]

    return shortlisted_keywords


### ROUTER TO CHECK IF WORKFLOW GOT TEXT TO PROCEED OR NOT ###

def extract_user_article_router(state: visibility_state):
    if state["output_confirmation"]:
        return "text_extracted"
    else:
        return "text_not_extracted"


   ######      Let's Build the Graph      ######


builder = StateGraph(state_schema=visibility_state)

builder.add_node(node="extract_user_article",action=extract_user_article)
builder.add_node(node="entities_extractor", action= entities_extractor)
builder.add_node(node="gkp_caller1", action=gkp_caller1)
builder.add_node(node="keyword_shortlister", action=keyword_shortlister)

builder.add_edge(START, "extract_user_article")
builder.add_conditional_edges(
    source= "extract_user_article",
    path= extract_user_article_router,
    path_map= {
        "text_extracted":"entities_extractor",
        "text_not_extracted":END
    }
)
builder.add_edge("entities_extractor","gkp_caller1")
builder.add_edge("gkp_caller1", "keyword_shortlister")
builder.add_edge("keyword_shortlister",END)

workflow = builder.compile()


# Lets call the graph with Opik 
opik_project_name = get_key(settings.OPIK_PROJECT_NAME)
#opik_key = get_key(settings.OPIK_API_KEY)
#opik_workspace = get_key(settings.OPIK_WORKSPACE)
os.getenv("OPIK_API_KEY")


tracer = OpikTracer(graph=workflow.get_graph(xray=True),project_name= opik_project_name)
inputs = {"user_url": "https://medium.com/@vivekvjnk/introduction-to-tool-use-with-langgraphs-toolnode-0121f3c8c323"}
result = asyncio.run(workflow.ainvoke(inputs,config={"callbacks": [tracer]}))



