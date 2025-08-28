



prompt_generator_prompt = """
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