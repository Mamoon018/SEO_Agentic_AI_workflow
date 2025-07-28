
from src.tools.web_extractor_tool import DIFFBOT_TOOL
from src.utils.settings import settings, get_key
from src.agents.visibility_agent.temp_data import planner_list2
from collections import defaultdict
from itertools import accumulate
import numpy as np

from langchain_openai import ChatOpenAI

# Tools_testing

# model = ChatOpenAI(model="gpt-4.1-mini", api_key= get_key(settings.OPENAI_API_KEY) )
# model_with_tools = model.bind_tools([DIFFBOT_TOOL()])


### Keyword Processor Function ###

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




    




if __name__ == "__main__":

    results =  keyword_processor(mainkeyword_list=planner_list2)

    print(results)
