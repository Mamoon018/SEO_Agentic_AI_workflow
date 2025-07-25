
from src.tools.web_extractor_tool import DIFFBOT_TOOL
from src.utils.settings import settings, get_key


from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4.1-mini", api_key= get_key(settings.OPENAI_API_KEY) )
model_with_tools = model.bind_tools([DIFFBOT_TOOL()])


