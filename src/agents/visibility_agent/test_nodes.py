

from src.agents.visibility_agent.state import visibility_state
from src.agents.visibility_agent.schemas import EXTRACT_USER_ARTICLE_SCHEMA, ENTITIES_EXTRACTOR_SCHEMA, KEYWORD_SHORTLISTER_SCHEMA, ARTICLE_PROMPT_GENERATOR_SCHEMA, BRAND_PROMPT_GENERATOR_SCHEMA, PROMPT_CITATION_FORMATTER_SCHEMA, GEO_METRICS_SCHEMA
from src.agents.visibility_agent.prompts import ENTITIES_EXTRACTOR_PROMPT, PROMPT_GENERATOR_PROMPT, PROMPT_SEARCHER_PROMPT, PROMPTS_CITATION_FORMATTER_PROMPT, GEO_METRICS_PROMPT, BRAND_PROMPTS_GENERATOR_PROMPT
from src.tools.web_extractor_tool import DIFFBOT_TOOL
from src.agents.subgraphs.edges import text_extracter_workflow, prompt_generator_builder_workflow, prompt_caller_builder_workflow
from src.utils.settings import get_key, settings
from pydantic import AnyUrl
from typing import Union, Optional, Annotated
import operator
from langgraph.graph import StateGraph
from langgraph.types import Send
from langgraph.graph import END, START
import asyncio
from src.agents.keywords_agent.nodes import GoogleKeywordsAPI
from src.agents.visibility_agent.temp_data import planner_list1

import json 
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

from src.utils.models_initializer import initialize_model_with_fallbacks , get_openai_model, get_perplexity_llm

# extract_user_article model
ENTITIES_EXTRACTOR_MODEL_WITH_FALLBACKS= initialize_model_with_fallbacks(
    primary_model_fn=get_openai_model,
    primary_model_kwargs={"model_num": 2, "temperature": 0.5},
    fallback_model_fns=[get_openai_model],
    fallback_model_kwargs_list=[{"model_num": 1, "temperature": 0.5}],
    structured_output_schema=ENTITIES_EXTRACTOR_SCHEMA,
    #bind_tools=True, 
    #tools=[DIFFBOT_TOOL()],
    #tool_choice= "Web_scraping_tool"
)

# Prompt generator model
ARTICLE_PROMPT_GENERATOR_MODEL_WITH_FALLBACKS= initialize_model_with_fallbacks(
    primary_model_fn=get_openai_model,
    primary_model_kwargs={"model_num": 2, "temperature": 0.5},
    fallback_model_fns=[get_openai_model],
    fallback_model_kwargs_list=[{"model_num": 1, "temperature": 0.5}],
    structured_output_schema=ARTICLE_PROMPT_GENERATOR_SCHEMA,
)

# Prompt generator model
BRAND_PROMPT_GENERATOR_MODEL_WITH_FALLBACKS= initialize_model_with_fallbacks(
    primary_model_fn=get_openai_model,
    primary_model_kwargs={"model_num": 2, "temperature": 0.5},
    fallback_model_fns=[get_openai_model],
    fallback_model_kwargs_list=[{"model_num": 1, "temperature": 0.5}],
    structured_output_schema=BRAND_PROMPT_GENERATOR_SCHEMA,
)

# prompts citations formatter model
PROMPTS_CITATION_FORMATTER_MODEL_WITH_FALLBACKS= initialize_model_with_fallbacks(
    primary_model_fn=get_openai_model,
    primary_model_kwargs={"model_num": 2, "temperature": 0.0},
    fallback_model_fns=[get_openai_model],
    fallback_model_kwargs_list=[{"model_num": 2, "temperature": 0.0}],
    structured_output_schema=PROMPT_CITATION_FORMATTER_SCHEMA,
)


# Metrics compilation model
GEO_METRICS_MODEL_WITH_FALLBACKS= initialize_model_with_fallbacks(
    primary_model_fn=get_openai_model,
    primary_model_kwargs={"model_num": 2, "temperature":0.5},
    fallback_model_fns=[get_openai_model],
    fallback_model_kwargs_list=[{"model_num":1, "temperature":0.5}],
    structured_output_schema= GEO_METRICS_SCHEMA
)



# lets initialize the class of the google planner so, that we can use its method 
gkp = GoogleKeywordsAPI()



                                ####   Nodes of Graph   ####


### Label the task Node ###
async def label_the_task(state:visibility_state):
    
    """
    It reviews the input of the user and assign the "Task label" a value as either "Article task"
    or "Brand task" so, that we can run the common nodes between Article task & Brand task with input,prompts
    and output to be stored as per the task type.
    """

    task_label: str = None



    if state["brand_domain"] is not None:
        task_label = "Brand task"
    else: 
        task_label = "Article task"

    return {"task_label": task_label}


### Article extracter subgraph invoker ###
async def article_extracter_subgraph_invoker(state:visibility_state):
    """
    It is the generic subgraph (independent of the task for the larger task for which it is assisting), that will 
    be invoked in either case be the router passes query with label of Article task or Brand task. It will be 
    the part of the both branches. 

    In case where router has labelled the task as "Article task", it takes the user_url as an input and extract the
    content of the user article.

    **Args:**
    user_url (str): It is the url of the user article 
    
    **Returns:**
    scrapped_text (Optional[Union[dict[str,str],str]]): It is the text extracted from the article 

    It is the output of the DIFFBOT tool. If article is accessible then we will get scrapped information
    stored in dictionary as an output. If article is inaccessible then we will get either of two error message specified 
    in the DIFFBOT tool.

    output_confirmation (bool): It is the confirmation if the text was successfully extracted or not.

    """
    try:
        # lets get the input variable 
        user_url: AnyUrl = state["user_url"]

        # lets initialize the scrapped article 
        # Let's initialize the scrapped_text object 
        scrapped_text: Optional[Union[dict[str,str],str]] = {}

        # lets initialize the boolean variable to confirm if output is returned so, that we can proceed with workflow
        output_confirmation: bool = True 

        article_extracter_results = await text_extracter_workflow.ainvoke(input={"user_url": user_url})
        scrapped_text = article_extracter_results["scrapped_text"]
        output_confirmation = article_extracter_results["output_confirmation"]
        

        return {
            "scrapped_text": scrapped_text,
            "output_confirmation": output_confirmation
        }
    except Exception as e:
        raise KeyError(f"Error occurred in article_extracter_subgraph_invokder due to error {e}") from e 




### EXTRACT USER ARTICLE NODE ###
#async def extract_user_article(state:visibility_state):

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

"""

### LLM ENTITIES EXTRACTOR ###

async def entities_extractor(state:visibility_state):
    """
    It extracts 1-3 most relevant entities from the text of the scrapped article.

    It will use the 'state["scrapped_text"]' to identify and extract most relevant entities discussed
    in the article in the context of the entire article. 
    Those entities will serve as a foundation for generating seed keywords in google keyword planner (GKP).

    **Args:**
    scrapped_text (dict): It will be used to access title of the article and text of the article.

    **Returns:**
    Entities (list): It is the list of the relevant entities.

    """

    # lets get the required input variables
    text_of_article: str = state["scrapped_text"].get("article_text","N/A")
    title_of_article: str = state["scrapped_text"].get("title","N/A")

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


### Keyword shortlister subgraph invoker 
async def article_keyword_shortlister_subgraph_invoker(state:visibility_state):
    """
    It takes the entities extracted as an input and invokes the subgraph which contains three nodes 
    gkp caller, keyword shortlister. 

    It is the generic subgraph that we are going to invoke for the article.

    **Args:**
    entities (list[str]): It is the list of the entities that are extracted by the entities extracter from the 
    user article.
    user_url (AnyUrl): It is the url of the article which needs to be fed to GKP 

    **Returns:**
    shortlisted_keywords (list[str]): It returns the list of the shortlisted keywords
    
    """
    try:
        # lets initialize the input variable
        user_url: AnyUrl = state["user_url"]
        entities: list[str] = state["entities"]

        # lets initialize the keywords shortlisted list
        shortlisted_keywords: list[str] = []

        # lets invoke the article prompt generator subgraph
        keywords_shortlisted: KEYWORD_SHORTLISTER_SCHEMA = await prompt_generator_builder_workflow.ainvoke(input={"user_url":user_url,"entities":entities})

        shortlisted_keywords = keywords_shortlisted["shortlisted_keywords"]

        return {
            "shortlisted_keywords": shortlisted_keywords
        }
    
    except Exception as e:
        raise RuntimeError(f"Error occurred in article keyword shortlister subgraph invoker due to {e}") from e










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

    """

### Keyword Processor Node ###

async def keyword_shortlister(state:visibility_state):
    """
    It takes the keywords from the gkp_planner_list1 and based on the criteria to shortlist the top keywords only, it
    generates the list in the output that contains only keywords with higher proportion of share in the total combined
    search volume of all keywords.
    

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

    """

### Prompts Generator Node ###
async def article_prompt_generator(state:visibility_state):
    """
    It takes the shortlisted keywords based as an input - and generate 5-10 contextual prompts using those keywords.
    These contextual prompts are based on the user-intent that we catch from the keyword searches on web. 

    1) What is contextual prompt? It is the prompt about the article topic with context which user would searching on LLMs.
    We kept it contextual because users like to provide some context in their prompts in order to be more specific & precise while asking their queries to LLMs.
    2) How are we generating contextual prompt? 
        (a) What are possible contexts under which users are searching prompts?
        That depends on the intent of user search. If users are looking for information about EV - then prompts will be information extraction based.
        Different intent buckets to cover possible user contexts about any topic:
        1) Informational: Benefits of EV?, Consequences of EV?, new updates in EV?, upcoming possibilities in EV?   
        2) Navigational: How to guide charge EV?
        3) Transactional: Buyers look for EV? highest sales of EV ?
        4) Comparative: reviews, top, best, EV vs non-EV which got more speed?
        These are the possible intent that can drive the different contexts in the user prompts. 
            
            -- We have one topic of article underconsideration --
        (b) Identify the intent of the article - Is it Informational, Navigational, Transactional, Comparative? (How user would ideally want
        to search to get article's information?)
        (c) We have the entities of article - about which user intents to search. (What user can search (entities user possibly interested in) 
        about the article?)
        (d) GKP-Keywords help us identifying the "intent of the users on web" & "entities they are interested in"
        (e) Now, we know user's interests & intent about topic on web - we know what interests & intent of user our article addresses.
        (f) Questions based on the intent & interests of the user about topic, under the context in which article is addressing that intent & 
        interest - prompts will be based!
        (g) LLM needs to think about this whole scenario for broader context - we are only providing a direction.

        For Example: 
        Topic: Study in Germany for Pakistani students?
        Entities in article: german universities, free education in germany, top german universities, pakistani students
        gkp-keywords: fee in germany, german universities, scholarhips in germany, jobs in germany

        Search Intent of users: fee in germany, scholarship in germany, jobs in germany (Informational) 
        Entities users interested in: fee, universities, scholarship, jobs
        inferring context from above two data-points: Interested in expense of students, subsidies for students, career oppotunities in germany

        prompts: 
        Option-1: Prompts totally based on user intent & interested entities (Are german universities free?)
        Option-2: Prompts based on user intent & interested entites & in the context article addresses those intents & interests.
        suppose article has covered public-privdate universities fees comparison.
        (What is the difference in the expense of students studying in private universities as compare to studying in public universities?)
    
        Return no more than 2 prompts in total.
    """

    # lets get the input variables from state
    article_text: str = state["scrapped_text"].get("article_text","N/A")
    article_title: str = state["scrapped_text"].get("title","N/A")
    entities: list[str] = state["entities"]
    shortlisted_keywords: list[str] = state["shortlisted_keywords"]

    # lets get the prompt of the node
    prompt = PromptTemplate(input_variables= ["article_text", "article_title", "entities", "shortlisted_keywords"],
                            template=PROMPT_GENERATOR_PROMPT)
    
    keyword_generator_prompt = prompt.format(article_text=article_text,article_title=article_title,
                                            entities=entities, shortlisted_keywords=shortlisted_keywords)
    
    # lets initialize the list to store prompts
    article_contextual_prompts: list[str] = []

    try:

        prompt_generator_response: ARTICLE_PROMPT_GENERATOR_SCHEMA = await ARTICLE_PROMPT_GENERATOR_MODEL_WITH_FALLBACKS.ainvoke(
            input= [HumanMessage(content=keyword_generator_prompt)]
        )

        article_contextual_prompts = prompt_generator_response.article_contextual_prompts

        return {
            "article_contextual_prompts": article_contextual_prompts
        }

    except Exception as e:
        raise RuntimeError(f"error raised in prompt_generator node due to {e}") from e



### lets call the text extracter subgraph for brand domain extraction
async def brand_text_extracter_subgraph_invoker(state:visibility_state):
    """
    It takes the user url of brand domain as an input and invokes the text extracter subgraph to extract the
    content on the domain.
    
    **Args:**
    brand_domain (AnyUrl): It is the domain of the brand website that we will extract using text extracter

    """
    try:
        # lets get the input variable 
        user_url: AnyUrl = state["brand_domain"]

        # Let's initialize the scrapped_text object 
        scrapped_text: Optional[Union[dict[str,str],str]] = {}

        # lets initialize the boolean variable to confirm if output is returned so, that we can proceed with workflow
        output_confirmation: bool = True 

        brand_extracter_results = await text_extracter_workflow.ainvoke(input={"user_url": user_url})
        scrapped_text = brand_extracter_results["scrapped_text"]
        output_confirmation = brand_extracter_results["output_confirmation"]
        

        return {
            "scrapped_text": scrapped_text,
            "output_confirmation": output_confirmation}
    
    except Exception as e:
        raise RuntimeError(f"Error occurred in brand_extracter_subgraph_invokder due to error {e}") from e 



### Keyword shortlister subgraph invoker 
async def brand_keyword_shortlister_subgraph_invoker(state:visibility_state):
    """
    It takes the brand related keywords provided by the user - these keywords will be provided by the user
    as an input, and we consider these keywords related to the problem/Query regarding which user
    is interested to generate prompts. 

    It is the generic subgraph that we are going to invoke for the brand.

    **Args:**
    user_url (AnyUrl): It is the url of the article which needs to be fed to GKP 
    brand_related_keywords (list[str] | None): It is the list of keywords provided by the user 

    **Returns:**
    shortlisted_keywords (list[str]): It returns the list of the shortlisted keywords
    
    """
    try:
        # lets initialize the input variable
        user_url: AnyUrl = state["brand_domain"]
        entities: list[str] = state["brand_related_keywords"]

        # lets initialize the keywords shortlisted list
        shortlisted_keywords: list[str] = []

        # lets invoke the keyword shortlister subgraph
        keywords_shortlisted: KEYWORD_SHORTLISTER_SCHEMA = await prompt_generator_builder_workflow.ainvoke(input={"user_url":user_url,"entities":entities})

        shortlisted_keywords = keywords_shortlisted["shortlisted_keywords"]

        return {
            "shortlisted_keywords": shortlisted_keywords
        }
    except Exception as e:
        raise RuntimeError(f"Error occurred in article keyword shortlister subgraph invoker due to {e}") from e

### lets get the brand prompt generator 
async def brand_prompt_generator(state:visibility_state):

    """
    It takes the related keywords, domain text, shortlisted keywords from gkp as an input and also the 
    aspect of the brand for which user want to track the brand. 

    **Args:**
    shortlisted_keywords (list[str]): It is the list of the shortlisted keywords from the list of gkp
    scrapped_text (Optional[Union[dict[str,str],str]]): It is the text that is extracted from the domain of the brand
    brand_user_intent (str): It shows what is the aspect about brand for which user want to check visibility

    **Returns:**
    contextual_prompts (list[str]): It is the list of the contextual prompts for which user brand will be tracked

    """

    shortlisted_keywords: list[str] = state["shortlisted_keywords"]
    brandsite_text: str = state["scrapped_text"].get("article_text","N/A")
    brand_user_intent: str = state["brand_user_intent"]
    brand_related_keywords: list[str] = state["brand_related_keywords"]

    # lets get the prompt of the node
    prompt = PromptTemplate(input_variables= ["brandsite_text", "brand_related_keywords" , "brand_user_intent", "shortlisted_keywords"],
                            template=BRAND_PROMPTS_GENERATOR_PROMPT)
    
    keyword_generator_prompt = prompt.format(brandsite_text=brandsite_text,
                                            brand_user_intent=brand_user_intent, brand_related_keywords = brand_related_keywords , shortlisted_keywords=shortlisted_keywords)
    
    # lets initialize the list to store prompts
    brand_contextual_prompts: list[str] = []

    try:

        prompt_generator_response: BRAND_PROMPT_GENERATOR_SCHEMA = await BRAND_PROMPT_GENERATOR_MODEL_WITH_FALLBACKS.ainvoke(
            input= [HumanMessage(content=keyword_generator_prompt)]
        )

        brand_contextual_prompts = prompt_generator_response.brand_contextual_prompts

        return {
            "brand_contextual_prompts": brand_contextual_prompts
        }

    except Exception as e:
        raise RuntimeError(f"error raised in prompt_generator node due to {e}") from e




# Article prompt caller subgraph invoker
async def article_prompt_caller_subgraph_invoker(state:visibility_state):

    """
    It takes the article related contextual prompts as an input and invoke the subgraph of prompts response caller
    that gives the formatted results of the llm response for each prompt. 

    **Args:**
    article_contextual_prompts (list[str]): It is the list of article related contextual prompts for which we will get responses.

    **Returns:**
    prompts_with_citations (list[dict[str,str|list[dict[str,str]]]]): It is the formatted results of the prompts, llm response for prompts, and their citations respectively.

    **Raises:**
    It raises the error if it is unable to invoke the subgraph.

    """

    # lets get the input variable
    article_contextual_prompts: list[str] = state["article_contextual_prompts"]

    # lets initialize the final output of the subgraph which is prompts and their citations in required format
    prompts_with_citations: list[dict[str,str|list[dict[str,str]]]] = []

    try:
        # lets invoke the prompts caller subgraph
        formatted_citations: PROMPT_CITATION_FORMATTER_SCHEMA = await prompt_caller_builder_workflow.ainvoke(input={"contextual_prompts":article_contextual_prompts})

        # lets get the output of the subgraph
        prompts_with_citations = formatted_citations["prompts_with_citations"]

        return {
            "prompts_with_citations": prompts_with_citations
        }

    except Exception as e:
        raise RuntimeError(f"Error occurred in the article prompt caller subgraph invoker due to {e}") from e



# Brand prompt caller subgraph
async def brand_prompt_caller_subgraph_invokder(state:visibility_state):
    """
    It takes the brand related contextual prompts as an input and invokes the subgraph that contains node related 
    to getting llm response for each prompt, and also format the llm response into required format. 

    **Args:** 
    brand_contextual_prompts (list[str]): It is the list of the brand related contextual prompts for which we need to get llm response

    **Returns:**
    prompts_with_citations: list[dict[str,str|list[dict[str,str]]]] 
    
    **Raises:**
    It raises the error when it is unable to invoke the subgraph
    """

    # lets get the input variables 
    brand_contextual_prompts: list[str] = state["brand_contextual_prompts"]

    # lets initialize the prompts_with_citations
    prompts_with_citations: list[dict[str,str|list[dict[str,str]]]] = []

    try:

        # lets invoke the subgraph 
        formatted_citations: PROMPT_CITATION_FORMATTER_SCHEMA = await prompt_caller_builder_workflow.ainvoke(input={"contextual_prompts":brand_contextual_prompts})

        # lets fetch the results from subgraph 
        prompts_with_citations = formatted_citations["prompts_with_citations"]

        return {
            "prompts_with_citations": prompts_with_citations
        }

    except Exception as e:
        raise RuntimeError(f"Error raised in brand prompt caller subgraph invoker due to {e}") from e 



# GEO Metrics for Brand 
async def brand_geo_metrics(state:visibility_state):
    """
    It takes the formatted response of the llm for all the contextual prompts, and compile the metrics using that
    data. Metrics are related to brand visibility, brand sentiment, factors driving those sentiments, 
    
    """






                        ##### TILL HERE WE HAVE NEW AGENTIC WORKFLOW #####




"""
# lets use the perplexity model to get the search results
async def perplexity_citations_for_prompts(state:visibility_state):
    
"""
    #It takes the generated contextual prompts as an input and generate the responses for it to simulate the user
    #searches and then check which articles are appearing in the response. 
    
"""

    # lets get the input variables
    contextual_prompts: str = state["contextual_prompts"]

    # lets get the prompt of the node
    prompt = PromptTemplate(input_variables= "contextual_prompts", template=PROMPT_SEARCHER_PROMPT)
    perplexity_citations_for_prompts_prompt = prompt.format(contextual_prompts=contextual_prompts)

    # lets initialize the object to store the output of the node
    perplexity_response: list[str] = []
    
    # lets get the llm
    #citation_results = await get_perplexity_llm(1,prompt=perplexity_citations_for_prompts_prompt)

    
    # lets get the result and store it
    #perplexity_response = [citation_results]
    

    return {
        "perplexity_response": perplexity_response
    }

    # Lets use the LangGraph SEND API that will use defined llm node for running all the prompts in parallelization
async def continue_perplexity_citations_for_prompts(state:visibility_state):
    return  [Send("perplexity_citations_for_prompts",{"contextual_prompts": cp}) for cp in state["contextual_prompts"]]
    # Here send will take each contextual prompt and pass it to the target node specified as param. It will pass 
    # all prompts parallely. 


# lets get the reducer node ---> We  need to parse the results of the "perplexity_response" here.
async def prompts_citation_reducer(state:visibility_state):
    
"""
    #This node takes the perplexity output as an input and extracts the information about cited articles, 
    #perplexity answer for contextual prompt, and contextual prompt itself.

    #**Args:**
    #perplexity_response (str): It is the raw output of the perplexity for all contextual prompts

    #**Returns:**
    #prompts_with_citations (dict[dict]): It returns the clean information of the required fields in json format 
    
"""

    # lets get the required input variable 
    perplexity_response: str = state["perplexity_response"]

    # lets get the prompt 
    prompt = PromptTemplate(input_variables="perplexity_response", template= PROMPTS_CITATION_FORMATTER_PROMPT)
    prompts_citation_formatter_prompt = prompt.format(perplexity_response=perplexity_response)

    # lets initialize the object to store the output of llm
    prompts_with_citations  = []

    # lets invoke the llm 
    #formatter_response: PROMPT_CITATION_FORMATTER_SCHEMA = await PROMPTS_CITATION_FORMATTER_MODEL_WITH_FALLBACKS.ainvoke(
    #    [HumanMessage(content=prompts_citation_formatter_prompt)]
    #)

    #prompts_with_citations = formatter_response.prompts_with_citations

    return {
            "prompts_with_citations": prompts_with_citations
            }



## Node for Metrics ##

async def geo_article_metrics(state:visibility_state):
"""
    #This node takes the structured output of perplexity response for each prompt as an input, and uses it 
    #to calculate the different metrics and then give structured output for those metrics.

    #**Args:**
    #prompts_with_citations (list): It is the list of the datapoints that contains information about the perplexity output in structured way

    #**Returns:**
    #It return output containing list of different metrics
    
    
"""

    # lets get the input variable from state
    prompts_with_citations = state["prompts_with_citations"]
    user_url = state["user_url"]
    scrapped_article = state["scrapped_article"].get("article_text",[])

    # lets get the prompt 
    prompt = PromptTemplate(input_variables= ["prompts_with_citations", "user_url", "scrapped_article"], template= GEO_METRICS_PROMPT)
    geo_metrics_prompt = prompt.format(prompts_with_citations= prompts_with_citations, user_url = user_url, scrapped_article = scrapped_article)

    # lets initialize the input variable to store the metrics
    geo_metrics_cal = {}

    # lets invoke the LLM to get the metrics
    #geo_metrics_response: GEO_METRICS_SCHEMA = await GEO_METRICS_MODEL_WITH_FALLBACKS.ainvoke(
    #    [HumanMessage(content=geo_metrics_prompt)]
    #)

    #geo_metrics_cal = geo_metrics_response

    return geo_metrics_cal


"""


                ####  BRAND METRICS  ####










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


### ROUTER TO CHECK IF THE WORKFLOW IS GOING TO PERFORM ARTICLE TASK OR BRAND TASK

def check_the_task(state:visibility_state):
    if state["task_label"] == "Article task":
        return "Article task"
    if state["task_label"] == "Brand task":
        return "Brand task"

   ######      Let's Build the Graph      ######


builder = StateGraph(state_schema=visibility_state)

builder.add_node(node="label_the_task", action=label_the_task)
#builder.add_node(node="extract_user_article",action=extract_user_article)
builder.add_node(node="article_extracter_subgraph_invoker", action=article_extracter_subgraph_invoker)
builder.add_node(node="entities_extractor", action= entities_extractor)
#builder.add_node(node="gkp_caller1", action=gkp_caller1)
#builder.add_node(node="keyword_shortlister", action=keyword_shortlister)
builder.add_node(node="article_keyword_shortlister_subgraph_invoker", action=article_keyword_shortlister_subgraph_invoker)
builder.add_node(node="article_prompt_generator", action=article_prompt_generator)
#builder.add_node(node="perplexity_citations_for_prompts", action=perplexity_citations_for_prompts)
#builder.add_node(node="prompts_citation_reducer", action=prompts_citation_reducer)
#builder.add_node(node="geo_article_metrics", action=geo_article_metrics)
builder.add_node(node="brand_text_extracter_subgraph_invoker",action= brand_text_extracter_subgraph_invoker)
builder.add_node(node="brand_keyword_shortlister_subgraph_invoker",action=brand_keyword_shortlister_subgraph_invoker)
builder.add_node(node="brand_prompt_generator", action=brand_prompt_generator)
builder.add_node(node="article_prompt_caller_subgraph_invoker", action=article_prompt_caller_subgraph_invoker)
builder.add_node(node="brand_prompt_caller_subgraph_invokder", action=brand_prompt_caller_subgraph_invokder)

builder.add_edge(START,"label_the_task")
builder.add_conditional_edges(source="label_the_task",
                              path=check_the_task,
                              path_map= {"Article task": "article_extracter_subgraph_invoker",
                              "Brand task": "brand_text_extracter_subgraph_invoker"}
                              )

builder.add_conditional_edges(
    source= "article_extracter_subgraph_invoker",
    path= extract_user_article_router,
    path_map= {
        "text_extracted":"entities_extractor",
        "text_not_extracted":END
    }
)
builder.add_conditional_edges(
    source= "brand_text_extracter_subgraph_invoker",
    path= extract_user_article_router,
    path_map= {
        "text_extracted":"brand_keyword_shortlister_subgraph_invoker",
        "text_not_extracted":END
    }
)
builder.add_edge("brand_keyword_shortlister_subgraph_invoker","brand_prompt_generator")
builder.add_edge("brand_prompt_generator", "brand_prompt_caller_subgraph_invokder")
builder.add_edge("brand_prompt_caller_subgraph_invokder", END)
"""
builder.add_edge("entities_extractor","gkp_caller1")
builder.add_edge("gkp_caller1", "keyword_shortlister")
builder.add_edge("keyword_shortlister","prompt_generator")
"""


builder.add_edge("entities_extractor","article_keyword_shortlister_subgraph_invoker")
#builder.add_conditional_edges(    "article_prompts_generator_subgraph_invoker",continue_perplexity_citations_for_prompts,["perplexity_citations_for_prompts"])

builder.add_edge("article_keyword_shortlister_subgraph_invoker","article_prompt_generator")
builder.add_edge("article_prompt_generator","article_prompt_caller_subgraph_invoker")
builder.add_edge("article_prompt_caller_subgraph_invoker", END)

#builder.add_edge("perplexity_citations_for_prompts","prompts_citation_reducer")
#builder.add_edge("prompts_citation_reducer", "geo_article_metrics")
#builder.add_edge("geo_article_metrics", END)


workflow = builder.compile()


# Lets call the graph with Opik 
opik_project_name = get_key(settings.OPIK_PROJECT_NAME)
#opik_key = get_key(settings.OPIK_API_KEY)
#opik_workspace = get_key(settings.OPIK_WORKSPACE)
os.getenv("OPIK_API_KEY")


tracer = OpikTracer(graph=workflow.get_graph(xray=True),project_name= opik_project_name)
inputs = {"brand_domain": "https://www.drivingelectric.com/best-cars/584/best-electric-cars", "brand_related_keywords": ["Tesla prices", "EV cars", "affordable electric vehicles"], 
          "brand_user_intent": "I want to check how LLMs are comparing the prices of Tesla with other EV cars." }
result = asyncio.run(workflow.ainvoke(inputs,config={"callbacks": [tracer]}))



