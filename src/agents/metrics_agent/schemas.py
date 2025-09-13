
from pydantic import BaseModel, Field

class BaseStructuredModel(BaseModel):

    class config:

        extra = "forbid"


class CITED_ARTICLES_INFO(BaseStructuredModel):
    """
    It contains the field that includes the information about the cited articles, like 
    title of the articles, date, last date updated, & urls.
    """
    article_title: str = Field(
        ..., description= "It is the list of the titles of the cited articles"
    )
    article_date: str = Field(
        ..., description= "It contains the list of date of the cited article"
    )
    article_last_update: str = Field(
        ..., description= "It is the list of the date on which article was updated last time"
    )
    article_urls: str = Field(
        ..., description= "It is the list of the urls of cited articles"
    )


class CITATION_FORMAT_SCHEMA(BaseStructuredModel):
    """
    It contains the fields which are going to be the part of the information that llm will be generating in the 
    structured output
    """
    context_prompt: str = Field(
        ..., description= "It is the contextual prompt that is the part of the perplexity output"
    )
    cited_articles: list[CITED_ARTICLES_INFO] = Field(
        ..., 
        description= "It contains the list of datapoints related to the cited articles"
    )
    response_for_prompt: str = Field(
        ...,
        description= "It is the answer of perplexity for the contexual prompt - it does not include articles"
    )

class PROMPT_CITATION_FORMATTER_SCHEMA(BaseStructuredModel):
    """
    It represents the output that contains the information about contextual prompt, cited articles, and peprlexity answer
    in a cleaner format
    """
    prompts_with_citations: list[CITATION_FORMAT_SCHEMA] = Field(
        ...,
        description= "It contains the list of data points for multiple contextual prompts according to the defined format of PROMPT_CITATION_FORMAT_SCHEMA "
    )

