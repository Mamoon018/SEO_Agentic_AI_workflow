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

        Return no more than 2 prompts in total.

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
Information about the cited articles include title of artciles, url of articles, date of article, last date article updated.

In case, you do not find information for any required field, or you find that in the perplexity output field is assigned NULL then just put NULL in the value of the particle field in your structured output.

you will be provided with the output which includes different contextual prompts, perplexity response to the contextual prompt and information about their respective cited articles.
Here is the perplexity output:
{perplexity_response}

"""

GEO_METRICS_PROMPT = """
You are a Search Engine Optimization expert and Generative Engine Optimization expert. You will be provided with 
the structured output of the perplexity response that contains information about the contextual prompts, details of
the cited articles for those prompts, and perplexity response for prompts.

Now, using this output we are supposed to calculate different metrics to measure the performance of user article (user_url) in terms of 
its visibility in AI output (Here Perplexity structured output) that you will be provided.

Below are the given metrics and the way you need to calculate them:
Metric-1: Prompt_cited_score
Definition: No of context prompts that has cited the user domain or URL in their response
Instructions for calculation of Prompt_cited_score: You should look for exact same url or domain from the user url
to check if article was cited or not. Give the count of the prompts and list of prompts that include user article in their response. 
To compile this metric you need to look into context prompt & response for prompt.

Metric-2: Prompts_categories
Definition: Types of context prompts that have cited the user article. 
There are different categories of the Prompts as given below
1) "how-to-guides prompts": User queries like Best practices, Walkthoughs, Troubleshooting etc.
2) "Solution centric prompts": User queries about casual questions, comparisons, explanations, definitions etc. 
3) "Opinion seeking prompts": User queries about opinion of AI on different things, brainstoriming, roleplay 
4) "Evaluation prompts": User queries about reviews info, pros & cons, recommendations, service/product evaluations
Instructions for calculation of Prompts_categories: Pick those prompts that have cited the user article and analyze them to decide their categories based on provided definitions

Metric-3: citation_rank
Definition: It is the rank at which user article is placed in the citations
Instructions for calculation of citation_rank: Pick those prompts that have cited the user article and go through its objects that contains details of the cited articles,
and in the provided order of the cited articles check rank of the object that contains the user article details. If first object contains that it means rank for that prompt is 1. In this way
you will check the rank of user article for contextual prompts that have cited it, and then determine what is the highest rank and lowest rank with their respective contextual prompts out of all the contextual prompt that have cited it
1 is the highest rank.

Metric-4: missed_content_details
Definition: It refers to the core topics, ideas, key concepts, or area of focus addressing a particular aspect that is core of llm response for a 
given prompt but are absent in the scrapped article of user. It is the core idea for llm response that scrapped article did not include in its 
content. so, it is missed content. You should give missed content only for those prompts that have not cited user domain or URL.
Instruction for calculation of missed_content_details:
1) Review the LLM response for the given prompt and extract its main relevant core topics, ideas, key concepts, or area of focus.
2) Compare these against the user article.
3) Identify which core topics, ideas, key concepts, or area of focus are missing in the scrapped article.
4) Return missed content as keywords only (0 to 3 items,). If nothing is missing, return 0.

Make sure you provide content missed details for each prompt that have cited article separately. Make sure you give clean output and plain text for all fields and no json lines should be included in output.


Here is the perplexity structured output
{prompts_with_citations}
Here is the user article
{user_url}
Here is the scrapped_article of user
{scrapped_article}

"""