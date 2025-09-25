
from pydantic import BaseModel, Field
from typing import Annotated
import operator

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



class brand_prompts_cited_score_Schema(BaseStructuredModel):
    """
    It represents the fields like No. of contextual prompts for which llm response's referred to brand in some way, and includes list of those contextual prompts
    """
    num_visible_prompts: int = Field(
        ..., 
        description= "It is the exact number that shows how many contextual prompts are there that have referred to the brand using brand name i.e 1,2,0 etc."
    )
    visible_prompts: list[str] = Field(
        ..., 
        description= "It is the list of the contextual prompts for which llm response have reffered to the brand name in some way i.e ['prompt1','prompt2']"
    )

class brand_cited_prompts_categories_schema(BaseStructuredModel):
    """
    It represents the field that assigns the category to the each prompt according to the response of llm for it.
    """
    cited_categories: list[str] = Field(
        ...,
        description= "It is the list of the contextual prompts and respective categories assigned to the contextual prompts which have referred to the brand, according to the type of response generated for each contextual prompt i.e ['Category-1', 'Category-2']"
    )

class brand_citation_rank_schema(BaseStructuredModel):
    """
    It represent the fields that gives an idea about the brand ranking in the llm response, relative to its competitors. It gives
    highest rank in the llm respons because it is possible brand name is mentioned multiple times and respective prompt.
    """
    highest_rank: int = Field(
        ...,
        description="It is the highest rank of the brand relative to its competitors in the llm response i.e 2"
    )
    given_prompt: str = Field(
        ...,
        description= "It is prompt for which rank is calculated"
    )

class brand_sentiment_analysis_schema(BaseStructuredModel):
    """
    It represent the field that gives the sentiment with which brand was referred to in the llm response. 
    """
    sentiment: str = Field(
        ..., 
        description= "It refers to the sentiment that was associated with the brand"
    )

class brand_sentiment_phrases_Schema(BaseStructuredModel):
    """
    It represent the fields that gives an idea about the factors and phrases which are driving the sentiment of the brand!
    """
    sentiment_phrase: str = Field(
        ...,
        description= "It refers to the EXACT PHRASE that refers to brand with some sentiment and based on which you decided sentiment of the brand"
    )
    prompts_of_sentiment: str = Field(
        ...,
        description= "It is the prompt of which llm response was used to get the sentiment phrase"
    )

class brand_competitor_phrases_schema(BaseStructuredModel):
    """
    It represent the fields that gives an idea about the competitors that were mentioned when brand name was not referred in any of the contextual prompt, 
    sentiment asosciated with that competitor, and EXACT phrase which is driving the sentiment regarding the competitor. 
    """
    competitor_name: str = Field(
        ..., 
        description= "It is the competitor name that was mentioned in the llm response"
    )
    comeptitor_sentiment: str = Field(
        ...,
        description= "It is the sentiment associated with the competitor in the llm response"
    )
    phrase_of_competitor_sentiment: str = Field(
        ..., 
        description= "It is the EXACT phrase that driving the sentiment of the competitor"
    )





class Brand_geo_metrics_compilation(BaseStructuredModel):
    """
    It represent the brand geo visibility metrics which gives the insights about the visibility of the brand name in the llm response. 
    """
    prompts_cited_score: list[brand_prompts_cited_score_Schema] = Field(
        ...,
        description= "It contains datapoints related to the metric prompts_cited_score"
    )
    cited_prompts_categories: list[brand_cited_prompts_categories_schema] = Field(
        ...,
        description= "It contains the datapoints related to the metric cited prompts categories"
    )
    citation_rank: Annotated[list[brand_citation_rank_schema],operator.add] = Field(
        ...,
        description= "It contains the datapoints related to the ranking of the brand in the llm response"
    )
    brand_sentiment: Annotated[list[brand_sentiment_analysis_schema],operator.add] = Field(
        ...,
        description= "It includes datapoint related to the sentiment of the brand"
    )
    brand_sentiment_phrases: Annotated[list[brand_sentiment_phrases_Schema],operator.add] = Field(
        ...,
        description= " It includes the datapoints related to the brand sentiment phrases"
    )
    brand_competitor_phrases: Annotated[list[brand_competitor_phrases_schema],operator.add] = Field(
        ...,
        description= "It includes the datapoints related to the brand competitors"
    )


class BRAND_GEO_METRICS_SCHEMA(BaseStructuredModel):
    """
    It represent the brand geo visibility metrics which gives the insights about the visibility of the brand in llm responses.
    """
    brand_metrics: list[Brand_geo_metrics_compilation] = Field(
        ...,
        description= "It includes the metrics related to the brand visibility in llm responses"
    )



            ## ARTICLES GEO METRICS CALCULATION ##

class articles_prompts_cited_score_Schema(BaseStructuredModel):
    """
    It represents the datapoints related to the visibility of the article in the contextual prompts responses
    """
    num_visible_prompts: int = Field(
        ..., 
        description= "It is the number of prompts that for which llm responses cited the article domain"
    )
    visible_prompts: list[str] = Field(
        ..., 
        description= "It is the list of the contextual prompts for which llm response have cited the article domain in some way i.e ['prompt1','prompt2']"
    )

class articles_cited_prompts_categories_Schema(BaseStructuredModel):
    """
    It represent the type of the contextual prompts that have cited the article domain. It gives an idea that for what
    sort of prompts llm is pulling the content from the article domain.
    """
    cited_categories: list[str] = Field(
        ...,
        description= "It is the list of the 'type' of prompts that have cited the article domain"
    )

class articles_citation_rank_Schema(BaseStructuredModel):
    """
    It contains the details about the ranking of the article domain citation relative to its competitors
    """
    highest_rank: str = Field(
        ...,
        description= "It contains the ranking of the article domain for the given prompt"
    )
    given_prompt: str = Field(
        ...,
        description= "It contains the prompt for given ranking of the article domain was calculated"
    )

class articles_missed_content_details_Schema(BaseStructuredModel):
    """
    Represents details associated with each missed content item.
    """
    content: list[str] = Field(
        ...,
        description="topics, phrases, lines, key terms that exist in LLM answers but not in user articles. Focus on primary stuff in LLM answer not some generic stuff, important terms that help help answer prompt for that LLM answer"
    )
    evidence: list[str] = Field(
        ...,
        description="Exact sentence or long phrase from LLM answer that you used to construct the missed content suggestions"
    )
    missed_content_prompt: str = Field(
        ...,
        description="Prompt that the LLM answer belonged to"
    )
    missed_content_suggestions: list[str] = Field(
        ...,
        description="2 sentences, very specific suggestion for users to integrate the missed content into their article. Make sure the suggestion is very relevant with example to the user's existing article content, tone and context"
    )


class ARTICLES_GEO_METRICS_COMPILATION(BaseStructuredModel):
    """
    It represent the datapoints related to the article visibility on the llm responses. 
    """
    articles_prompts_cited_score: list[articles_prompts_cited_score_Schema] = Field(
        ...,
        description= "It contains the datapoints related score of citation"
    )

    articles_cited_prompts_categories: list[articles_cited_prompts_categories_Schema] = Field(
        ...,
        description= "It contains the datapoints related to the type of contextual prompts"
    )
    
    articles_citation_ranking: Annotated[list[articles_citation_rank_Schema],operator.add] = Field(
        ...,
        description= "It contains the list of the prompts in which article domain was cited and ranking of the article domain for the given prompt"
    )

    articles_missed_content: Annotated[list[articles_missed_content_details_Schema], operator.add] = Field(
        ...,
        description= "It contains the details related to the gaps in the article content in context of the llm answers for each prompt"
    )

    
class ARTICLE_GEO_METRICS_SCHEMA(BaseStructuredModel):
    """
    It represent the datapoints related to the visibility of the article in AI responses generated by the LLMs. 
    """
    article_metrics: list[ARTICLES_GEO_METRICS_COMPILATION] = Field(
        ...,
        description= "It represent the metrics of article visibility on AI platforms"
    )