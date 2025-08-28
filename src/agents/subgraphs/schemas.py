
from pydantic import BaseModel,Field
from typing import Optional, Union


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

