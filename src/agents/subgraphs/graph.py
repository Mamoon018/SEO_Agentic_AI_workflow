

from src.agents.subgraphs.edges import text_extracter_workflow, prompt_generator_builder_workflow
from src.utils.settings import get_key, settings
from opik.integrations.langchain import OpikTracer
import asyncio
import os
import opik
opik.configure(api_key=get_key(settings.OPIK_API_KEY),use_local=False)
import dotenv
dotenv.load_dotenv()
                                ####  Text Extracter Workflow Subgraph Graph  ####

opik_project_name = get_key(settings.OPIK_PROJECT_NAME)
os.getenv("OPIK_API_KEY")
opik_api_key = get_key(settings.OPIK_API_KEY)

tracer = OpikTracer(graph=text_extracter_workflow.get_graph(xray=True),project_name= opik_project_name)
inputs = {"user_url": "https://langchain-ai.github.io/langgraph/how-tos/tool-calling/"}
result = asyncio.run(text_extracter_workflow.ainvoke(inputs,config={"callbacks": [tracer]}))


                                ####  Prompt Generator Workflow Subgraph Graph  ####

tracer = OpikTracer(graph=prompt_generator_builder_workflow.get_graph(xray=True),project_name= opik_project_name)
inputs = {"article_text": "Hello how are you, this is ai agent calling you", "article_title":"This is langgraph tool", "entities": {"AI Agents","Langgraph tool calling", "Tool Node"}}
result = asyncio.run(prompt_generator_builder_workflow.ainvoke(inputs,config={"callbacks": [tracer]}))
# Cannot test here because some of the input variables required to run these nodes coming from the Main state so, 
#it has to be invoked with those input variables

