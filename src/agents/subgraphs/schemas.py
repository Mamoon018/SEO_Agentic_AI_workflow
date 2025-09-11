
from pydantic import BaseModel,Field
from typing import Optional, Union, Annotated
import operator


class basestructuremodel(BaseModel):
    class config:

        extra = "forbid"


                                    ####  Text Extracter subgraph nodes schemas  ####

class text_extracter_schema(basestructuremodel):

    """
    It represents output of the DIFFBOT tool scrapping 
    """

    scrapped_text: Optional[Union[dict[str,str],str]] = Field(
        ...,
        description= "It is output of the DIFFBOT tool that provides us scrapped information related to article.",
    )

                                    ####  Prompts generator subgraph nodes schemas  ####

# Node: Schema for keyword shortlister in subgraph
class keyword_shortlister_schema(basestructuremodel):
    """
    It represent the schema for the node that outputs list of the keywords
    """
    shortlisted_keywords: list[str] = Field(
        ...,
        description= "It is the list of the keywords with highest contribution to total search volume of all keywords"
    )

                                    ####  Prompts caller send api subgraph schemas  ####

# Node: citations_for_prompts in subgraph
class prompts_caller_schema(basestructuremodel):
    """
    It represent the schema of the node that output llm response 
    """
    llm_response: Annotated[list[str], operator.add] = Field(
        ...,
        description= "It is the raw output of the llm for each contextual prompt"
    )

# Node: llm_output_reducer in subgraph 
class cited_article_info(basestructuremodel):
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



class citation_format_schema(basestructuremodel):
    """
    It contains the fields which are going to be the part of the information that llm will be generating in the 
    structured output
    """
    context_prompt: str = Field(
        ..., description= "It is the contextual prompt that is the part of the perplexity output"
    )
    cited_articles: list[cited_article_info] = Field(
        ..., 
        description= "It contains the list of datapoints related to the cited articles"
    )
    response_for_prompt: str = Field(
        ...,
        description= "It is the answer of perplexity for the contexual prompt - it does not include articles"
    )

class prompt_citation_formatter_schema(basestructuremodel):
    """
    It represents the output that contains the information about contextual prompt, cited articles, and peprlexity answer
    in a cleaner format
    """
    prompts_with_citations: list[citation_format_schema] = Field(
        ...,
        description= "It contains the list of data points for multiple contextual prompts according to the defined format of PROMPT_CITATION_FORMAT_SCHEMA "
    )
