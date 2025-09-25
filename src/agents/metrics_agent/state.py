
from langgraph.graph import MessagesState
from typing import Union, Optional, Any
from pydantic import AnyUrl

class metrics_state(MessagesState):

                    #### Main Workflow  (In this case, it is the input for the workflow)
    # Task type
    task_label: str 

    # Brand name
    brand_name: str 

    # Article/domain extracted text 
    scrapped_text: Optional[Union[dict[str,str],str]]

    # Article domain 
    article_domain: AnyUrl

                    
                    #### Subgraphs (Output of the subgraphs)
    # formatted response of the llm for all prompts
    prompts_with_citations: list[dict[str,str|list[dict[str,str]]]]


                    #### Article branch (Output of the article specialized nodes)
    # article related contextual prompts
    article_contextual_prompts: list[str]

    # article metrics
    article_geo_metrics: list[Any]


                    #### Brand branch (Output of the brand specialized nodes)
    # brand related contextual prompts
    brand_contextual_prompts: list[str]

    # brand metrics 
    brand_geo_metrics: list[Any]

