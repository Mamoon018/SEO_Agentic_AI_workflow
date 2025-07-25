"""
Here we will define the schemas of the Nodes
"""

from pydantic import BaseModel, Field
from typing import Literal, Any

class BaseStructuredModel(BaseModel):
    class Config:
        
        
        extra = "forbid"


class EXTRACT_USER_ARTICLE_SCHEMA(BaseStructuredModel):
    """
    Represents the extracted information from the user article.
    """

    scrapped_data: str = Field(
        ...,
        description="Contains the parsed content from the provided URL as strings."
    )


