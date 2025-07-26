"""
Here we will define the schemas of the Nodes
"""

from pydantic import BaseModel, Field, AnyUrl
from typing import Optional, Union

class BaseStructuredModel(BaseModel):
    class Config:        
        
        extra = "forbid"


class EXTRACT_USER_ARTICLE_SCHEMA(BaseStructuredModel):
    """
    It represents output of the DIFFBOT tool scrapping 
    """

    scrapped_article: Optional[Union[dict[str,str],str]] = Field(
        ...,
        description= "It is output of the DIFFBOT tool that provides us scrapped information related to article.",
    )

class ENTITIES_EXTRACTOR_SCHEMA(BaseStructuredModel):
    """
    It represents the output of the entities extracted from the article
    """

    entities: list[str] = Field(
        ...,
        description= "These are the most important entities discussed in the article"
    )

