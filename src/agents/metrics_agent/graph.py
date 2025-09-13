from src.agents.metrics_agent.test_data import scrapped_text
from src.agents.metrics_agent.edges import geo_metrics_workflow
from src.utils.settings import get_key, settings
from opik.integrations.langchain import OpikTracer
import asyncio
import os
import opik
opik.configure(api_key=get_key(settings.OPIK_API_KEY),use_local=False)
import dotenv
dotenv.load_dotenv()

opik_project_name = get_key(settings.OPIK_PROJECT_NAME)
os.getenv("OPIK_API_KEY")
opik_api_key = get_key(settings.OPIK_API_KEY)

                                    ####  Metrics workflow  ####

tracer = OpikTracer(graph=geo_metrics_workflow.get_graph(xray=True),project_name= opik_project_name)
inputs = {"task_label":"Brand task", "brand_contextual_prompts": [
    "what are the best models in EV cars?",
    "what are the best tesla models?"
  ],
  "scrapped_text": scrapped_text, "brand_name": "Tesla" }
result = asyncio.run(geo_metrics_workflow.ainvoke(inputs,config={"callbacks": [tracer]}))
