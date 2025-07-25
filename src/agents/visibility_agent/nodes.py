

from src.agents.visibility_agent.state import visibility_state
from src.agents.visibility_agent.schemas import EXTRACT_USER_ARTICLE_SCHEMA
from src.agents.visibility_agent.prompts import EXTRACT_USER_ARTICLE_PROMPT
from src.tools.web_extractor_tool import DIFFBOT_TOOL
from src.utils.settings import get_key, settings
from pydantic import AnyUrl
from typing import Union
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
MODEL_WITH_FALLBACK_EXTRACT_USER_ARTICLE= initialize_model_with_fallbacks(
    primary_model_fn=get_mistral_model,
    primary_model_kwargs={"model_num": 2, "temperature": 0.5},
    fallback_model_fns=[get_mistral_model],
    fallback_model_kwargs_list=[{"model_num": 1, "temperature": 0.5}],
    structured_output_schema=EXTRACT_USER_ARTICLE_SCHEMA,
    #bind_tools=True, 
    #tools=[DIFFBOT_TOOL()],
    #tool_choice= "Web_scraping_tool"
)


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
    It raises the error if tool 
    
    
    """















   ######      Let's Build the Graph      ######


builder = StateGraph(state_schema=visibility_state)


builder.add_node(node="extract_user_article",action=extract_user_article)

builder.add_edge(START,"extract_user_article")
builder.add_edge("extract_user_article",END)


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