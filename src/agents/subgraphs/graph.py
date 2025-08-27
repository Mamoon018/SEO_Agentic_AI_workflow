

from src.agents.subgraphs.edges import text_extracter_workflow 
from src.utils.settings import get_key, settings
from opik.integrations.langchain import OpikTracer
import asyncio
import os

                                    ####  Text Extracter Workflow Subgraph Graph  ####

opik_project_name = get_key(settings.OPIK_PROJECT_NAME)
os.getenv("OPIK_API_KEY")
opik_api_key = get_key(settings.OPIK_API_KEY)



tracer = OpikTracer(graph=text_extracter_workflow.get_graph(xray=True),project_name= opik_project_name)
inputs = {"user_url": "https://langchain-ai.github.io/langgraph/how-tos/tool-calling/"}
result = asyncio.run(text_extracter_workflow.ainvoke(inputs,config={"callbacks": [tracer]}))

