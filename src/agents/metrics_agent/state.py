
from langgraph.graph import MessagesState
from typing import Annotated, Union, Optional, Any

class metrics_state(MessagesState):

                    #### Main Workflow  (In this case, it is the input for the workflow)
    # Task type
    task_label: str 

    # Brand name
    brand_name: str 

    # Article/domain extracted text 
    scrapped_text: Optional[Union[dict[str,str],str]] 

                    
                    #### Subgraphs (Output of the subgraphs)
    # formatted response of the llm for all prompts
    prompts_with_citations: list[dict[str,str|list[dict[str,str]]]]


                    #### Article branch (Output of the article specialized nodes)
    # article related contextual prompts
    article_contextual_prompts: list[str]


                    #### Brand branch (Output of the brand specialized nodes)
    # brand related contextual prompts
    brand_contextual_prompts: list[str]

    # brand metrics 
    geo_brand_metrics: list[Any]

