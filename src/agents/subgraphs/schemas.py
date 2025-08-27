
from pydantic import BaseModel,Field
from typing import Optional, Union


class basestructuremodel(BaseModel):
    class config:

        extra = "forbid"


                                          ####  Text Extracter subgraph schema  ####

class text_extracter_schema(basestructuremodel):

    """
    It represents output of the DIFFBOT tool scrapping 
    """

    scrapped_article: Optional[Union[dict[str,str],str]] = Field(
        ...,
        description= "It is output of the DIFFBOT tool that provides us scrapped information related to article.",
    )

