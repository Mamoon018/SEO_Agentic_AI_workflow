

from src.agents.visibility_agent.state import visibility_state
from src.agents.visibility_agent.schemas import EXTRACT_USER_ARTICLE_SCHEMA, ENTITIES_EXTRACTOR_SCHEMA
from src.agents.visibility_agent.prompts import ENTITIES_EXTRACTOR_PROMPT
from src.tools.web_extractor_tool import DIFFBOT_TOOL
from src.utils.settings import get_key, settings
from pydantic import AnyUrl
from typing import Union, Optional
from langgraph.graph import StateGraph
from langgraph.graph import END, START
from langgraph.prebuilt import ToolNode, tools_condition
import asyncio


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

builder.add_edge(START, "extract_user_article")
builder.add_conditional_edges(
    source= "extract_user_article",
    path= extract_user_article_router,
    path_map= {
        "text_extracted":"entities_extractor",
        "text_not_extracted":END
    }
)
builder.add_edge("entities_extractor",END)

workflow = builder.compile()


# Lets call the graph with Opik 
opik_project_name = get_key(settings.OPIK_PROJECT_NAME)
#opik_key = get_key(settings.OPIK_API_KEY)
#opik_workspace = get_key(settings.OPIK_WORKSPACE)
os.getenv("OPIK_API_KEY")


tracer = OpikTracer(graph=workflow.get_graph(xray=True),project_name= opik_project_name)
inputs = {"user_url": "https://medium.com/@vivekvjnk/introduction-to-tool-use-with-langgraphs-toolnode-0121f3c8c323"}
result = asyncio.run(workflow.ainvoke(inputs,config={"callbacks": [tracer]}))



"""


async def remaining_workflow_nodes(state:visibility_state):
    
    It is just for the testing purpose that if we get the article content scrapped then we will proceed with next node
    after executing node with tool.
    
    print("All is good")


async def router_scraping_comfirmation(state:visibility_state):
    
    It checks the value of the article_scrapped and decides if workflow should continue or not. In case link is not accessible,
    then value of 'article_scrapped' will be 'None' so, then workflow should not continue.
    
    

    if state["article_scrapped"] != None:
        return "remaining_workflow"
    if state["article_scrapped"] == None:
        return "end"













# lets define the builder 
builder = StateGraph(state_schema=visibility_state)

tools_list = [DIFFBOT_TOOL()]
# lets add the nodes
builder.add_node(node="extract_user_article", action= extract_user_article)
builder.add_node(node="Web_scraping_tool", action= ToolNode(tools = tools_list))
builder.add_node(node="remaining_workflow", action= remaining_workflow_nodes)

# lets add edges
builder.add_edge(START,extract_user_article)
builder.add_conditional_edges(source=extract_user_article,
                              path=tools_condition,
                              path_map={
                                  'tools': 'Web_scraping_tool',
                                  '__end__': 'router_scraping_comfirmation'
                              })
builder.add_conditional_edges(
    source=extract_user_article,
    path= router_scraping_comfirmation,
    path_map={
        "remaining_workflow": "remaining_workflow_nodes",
        "end": END
    }
)
builder.add_edge(remaining_workflow_nodes,END)


# lets compile the workflow 
workflow = builder.compile()

# Lets call the graph with Opik 
opik_project_name = get_key(settings.OPIK_PROJECT_NAME)
#opik_key = get_key(settings.OPIK_API_KEY)
#opik_workspace = get_key(settings.OPIK_WORKSPACE)
os.getenv("OPIK_API_KEY")


tracer = OpikTracer(graph=workflow.get_graph(xray=True),project_name= opik_project_name)
inputs = {"user_url": "https://medium.com/@vivekvjnk/introduction-to-tool-use-with-langgraphs-toolnode-0121f3c8c323"}
result = asyncio.run(workflow.ainvoke(inputs,config={"callbacks": [tracer]}))
#print(result["article_scrapped"])



"""