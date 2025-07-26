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
to get relevant information of entities in context of concerning points discussed in article.
3. your entities can be a person, organization, event, location, or any other relevant entity discussed in the article. 
4. each entity should be a short phrase consisting of a couple words. Keep the purpose of the entities in mind to determine the best entities.

"""