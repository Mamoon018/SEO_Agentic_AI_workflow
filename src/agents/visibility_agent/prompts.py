"""
Here, we will define the prompts of the nodes.
"""

ENTITIES_EXTRACTOR_PROMPT= """

You are a Search Engine Optimization and Generative Engine Optimization expert. You will be provided with the text of the 
article and the title of the article. You need to indetify the most relevant and important entities based on the title and 
text of the article.
Here is the text of the article:
{text_of_article}
Here is the title of article
{title_of_article}

While extracting the entities, please consider the following points
1. Your extracted entities will be used as seed keywords to Google keyword planner to get relevant keywords to the given article. 
And those keywords will be used to find out the primary and secondary keywords for the article. Keep this in your mind.
2. Your extracted  keywords will be used to generate couple of contextual prompts that people are possibly using on AI platforms
to get relevant information about entities in context of concerning points discussed in article.
3. your entities can be a person, organization, event, location, or any other relevant entity discussed in the article. 
4. each entity should be a short phrase consisting of a couple words. Keep the purpose of the entities in mind to determine the best entities.

"""


PROMPT_GENERATOR_PROMPT = """
 It takes the shortlisted keywords based as an input - and generate 5-10 contextual prompts using those keywords. And also give the reason why each prompt you generated is addressing user intent and what makes the context relevant.
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
        (b) Identify the intent of the article - Is it Informational, Navigational, Transactional, Comparative? (How user would ideally want to search to get article's information?)
        (c) We have the entities of article - about which user intents to search. (What user can search (entities user possibly interested in) about the article?)
        (d) GKP-Keywords help us identifying the "intent of the users on web" & "entities they are interested in"
        (e) Now, we know user's interests & intent about topic on web - we know what interests & intent of user our article addresses.
        (f) Questions based on the intent & interests of the user about topic, under the context in which article is addressing that intent & interest - prompts will be based!
        (g) LLM needs to think about this whole scenario for broader context - we are only providing a direction.

        For example: 
        Topic: Study in Germany for Pakistani students?
        Entities in article: german universities, free education in germany, top german universities, pakistani students
        gkp-keywords: fee in germany, german universities, scholarhips in germany, jobs in germany

        Search Intent of users: fee in germany, scholarship in germany, jobs in germany (Informational) 
        Entities users interested in: fee, universities, scholarship, jobs
        inferring context from above two data-points: Interested in expense of students, subsidies for students, career oppotunities in germany

        Datadriven-Contextual-prompt-Method: Prompts based on user intent & interested entites & in the context article addresses those intents & interests.
        Suppose article has covered public-privdate universities fees comparison.
        
        Final output:
        Example of prompt:  What is the difference in the expense of students studying in private universities as compare to studying in public universities?
        Reason why this prompt aligns with web-based datapoint we have: XYZ
        [Prompt1, Reason_of_prompt1, etc]

Here is the entities of the article:
{entities}
Here is the text of the article:
{article_text}
Here is the list of gkp-keywords:
{shortlisted_keywords}
Here is the title of the article:
{article_title}
"""

PROMPT_SEARCHER_PROMPT = """
You are a Search Engine Optimization expert and Generative Engine Optimization expert. You will be provided with the contextual_prompt
that are basically considered as prompt which users are searching on LLMs. 
You need to answer that prompt so, that we can see if user searches prompt then what answers it will get. Also, you need to use
pre-built web search tool of perplexity that it uses to web search articles for using in generating its response and also
cite those articles which you have used. 

1) Store the output of the response in the following way
perplexity_response = list[dict] --> [contextual_prompts: what is XYZ?, llm_Response: It is XYZ]

2) you need to store the metadata of search results
perplexity_response_articles = =list[dict]

Here is the contextual_prompts:
{contextual_prompts}
"""

PROMPTS_CITATION_FORMATTER_PROMPT = """
You are a Search Engine Optimization expert and Generative Engine Optimization expert. You are provided with the
output of the perplexity. That output is not in the json format. It is not clean. 
It includes different types of information, the information that is relevant to us is the contextual prompt,
information of cited articles for that prompt, and perplexity response to the contextual prompt.
for each context prompt provide the cited articles and response for prompt in the output. 
Let's suppose we have the 15 prompts then we will have 15 objects that contains context prompts, cited articles, and response for prompt.


you will be provided with the output which includes different contextual prompts, perplexity response to the contextual prompt information about their respective cited articles.
Here is the perplexity output:
{perplexity_response}

"""

