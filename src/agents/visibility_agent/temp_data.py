

## DIFFBOT API Sample Output data ##

{
  "request": {
    "pageUrl": "https://example.com",
    "api": "article",
    "version": 3
  },
  "objects": [
    {
      "date": "Thu, 22 Feb 2024 07:41:24 GMT",
      "sentiment": 0.78,
      "images": [
        {
          "naturalHeight": 84,
          "width": 300,
          "url": "https://example.com/image.jpg",
          "naturalWidth": 150,
          "primary": True,
          "height": 168
        }
      ],
      "author": "John Doe",
      "estimatedDate": "Thu, 22 Feb 2024 07:41:24 GMT",
      "icon": "https://example.com/icon.jpg",
      "diffbotUri": "article|3|-1403181592",
      "siteName": "Medium",
      "type": "article",
      "title": "Sample Article Title",
      "tags": [
        {
          "score": 0.92,
          "sentiment": 0.78,
          "count": 4,
          "label": "Python",
          "uri": "https://diffbot.com/entity/example",
          "rdfTypes": ["http://dbpedia.org/ontology/Skill"]
        }
      ],
      "humanLanguage": "en",
      "pageUrl": "https://example.com",
      "html": "<p>Sample HTML content</p>",
      "categories": [
        {
          "score": 0.70,
          "name": "Technology",
          "id": "iabv2-596"
        }
      ],
      "text": "Sample plain text content of the article..."
    }
  ]
}



# GKP API results

planner_list1 = [
    {
      "text": "Agentic AI",
      "competition": "LOW",
      "average_monthly_searches": 390,
      "competition_index": 11,
      "monthly_search_volumes": {
        "May 2024": 480,
        "June 2024": 880,
        "July 2024": 260,
        "August 2024": 390,
        "September 2024": 480,
        "October 2024": 390,
        "November 2024": 260,
        "December 2024": 260,
        "January 2025": 390,
        "February 2025": 390,
        "March 2025": 390,
        "April 2025": 390
      }
    },
    {
      "text": "LangGraph usability in Agentic AI",
      "competition": "LOW",
      "average_monthly_searches": 260,
      "competition_index": 24,
      "monthly_search_volumes": {
        "May 2024": 320,
        "June 2024": 480,
        "July 2024": 260,
        "August 2024": 260,
        "September 2024": 480,
        "October 2024": 260,
        "November 2024": 140,
        "December 2024": 210,
        "January 2025": 210,
        "February 2025": 170,
        "March 2025": 210,
        "April 2025": 210
      }
    },
    {
      "text": "ToolNode handles the tool results for LLM",
      "competition": "LOW",
      "average_monthly_searches": 260,
      "competition_index": 24,
      "monthly_search_volumes": {
        "May 2024": 320,
        "June 2024": 480,
        "July 2024": 260,
        "August 2024": 260,
        "September 2024": 480,
        "October 2024": 260,
        "November 2024": 140,
        "December 2024": 210,
        "January 2025": 210,
        "February 2025": 170,
        "March 2025": 210,
        "April 2025": 210
      }
    },
    {
      "text": "AI applications automating tasks",
      "competition": "LOW",
      "average_monthly_searches": 40,
      "competition_index": 19,
      "monthly_search_volumes": {
        "May 2024": 110,
        "June 2024": 50,
        "July 2024": 10,
        "August 2024": 10,
        "September 2024": 10,
        "October 2024": 10,
        "November 2024": 20,
        "December 2024": 30,
        "January 2025": 40,
        "February 2025": 30,
        "March 2025": 90,
        "April 2025": 110
      }
    },
    {
      "text": "AI models fine tuning for better results",
      "competition": "LOW",
      "average_monthly_searches": 30,
      "competition_index": 18,
      "monthly_search_volumes": {
        "May 2024": 50,
        "June 2024": 40,
        "July 2024": 10,
        "August 2024": 10,
        "September 2024": 10,
        "October 2024": 10,
        "November 2024": 10,
        "December 2024": 10,
        "January 2025": 20,
        "February 2025": 40,
        "March 2025": 50,
        "April 2025": 50
      }
    },
    {
      "text": "tool use capabilities giving extra powers to AI applications",
      "competition": "LOW",
      "average_monthly_searches": 10,
      "competition_index": 7,
      "monthly_search_volumes": {
        "May 2024": 10,
        "June 2024": 0,
        "July 2024": 0,
        "August 2024": 0,
        "September 2024": 0,
        "October 2024": 0,
        "November 2024": 0,
        "December 2024": 0,
        "January 2025": 10,
        "February 2025": 0,
        "March 2025": 0,
        "April 2025": 10
      }
    }
]



# GKP API results

planner_list2 = [
    {
      "text": "Tesla Model 3 price 2025",
      "competition": "LOW",
      "average_monthly_searches": 390,
      "competition_index": 11,
      "monthly_search_volumes": {
        "May 2024": 480,
        "June 2024": 880,
        "July 2024": 260,
        "August 2024": 390,
        "September 2024": 480,
        "October 2024": 390,
        "November 2024": 260,
        "December 2024": 260,
        "January 2025": 390,
        "February 2025": 390,
        "March 2025": 390,
        "April 2025": 390
      }
    },
    {
      "text": "Tesla Model Y cost comparison",
      "competition": "LOW",
      "average_monthly_searches": 260,
      "competition_index": 24,
      "monthly_search_volumes": {
        "May 2024": 320,
        "June 2024": 480,
        "July 2024": 260,
        "August 2024": 260,
        "September 2024": 480,
        "October 2024": 260,
        "November 2024": 140,
        "December 2024": 210,
        "January 2025": 210,
        "February 2025": 170,
        "March 2025": 210,
        "April 2025": 210
      }
    },
    {
      "text": "Tesla vs BYD EV prices",
      "competition": "LOW",
      "average_monthly_searches": 260,
      "competition_index": 24,
      "monthly_search_volumes": {
        "May 2024": 320,
        "June 2024": 480,
        "July 2024": 260,
        "August 2024": 260,
        "September 2024": 480,
        "October 2024": 260,
        "November 2024": 140,
        "December 2024": 210,
        "January 2025": 210,
        "February 2025": 170,
        "March 2025": 210,
        "April 2025": 210
      }
    },
    {
      "text": "Cheapest Tesla car in Europe",
      "competition": "LOW",
      "average_monthly_searches": 40,
      "competition_index": 19,
      "monthly_search_volumes": {
        "May 2024": 110,
        "June 2024": 50,
        "July 2024": 10,
        "August 2024": 10,
        "September 2024": 10,
        "October 2024": 10,
        "November 2024": 20,
        "December 2024": 30,
        "January 2025": 40,
        "February 2025": 30,
        "March 2025": 90,
        "April 2025": 110
      }
    },
    {
      "text": "Tesla Model S price Germany",
      "competition": "LOW",
      "average_monthly_searches": 30,
      "competition_index": 18,
      "monthly_search_volumes": {
        "May 2024": 50,
        "June 2024": 40,
        "July 2024": 10,
        "August 2024": 10,
        "September 2024": 10,
        "October 2024": 10,
        "November 2024": 10,
        "December 2024": 10,
        "January 2025": 20,
        "February 2025": 40,
        "March 2025": 50,
        "April 2025": 50
      }
    },
    {
      "text": "Tesla vs Hyundai Ioniq 5 price",
      "competition": "LOW",
      "average_monthly_searches": 10,
      "competition_index": 7,
      "monthly_search_volumes": {
        "May 2024": 10,
        "June 2024": 0,
        "July 2024": 0,
        "August 2024": 0,
        "September 2024": 0,
        "October 2024": 0,
        "November 2024": 0,
        "December 2024": 0,
        "January 2025": 10,
        "February 2025": 0,
        "March 2025": 0,
        "April 2025": 10
      }
    }
]


# Perplexity output 
"""
{"id": "16cb0bb2-c4c4-44e0-9573-3c2e0992207d", "model": "sonar", "created": 1755302482, "usage": {"prompt_tokens": 13, "completion_tokens": 222, "total_tokens": 235, "search_context_size": "low", "cost": {"input_tokens_cost": 0.0, "output_tokens_cost": 0.0, "request_cost": 0.005, "total_cost": 0.005}}, "citations": ["https://www.espn.com/tennis/rankings", "https://en.wikipedia.org/wiki/List_of_ATP_number_1_ranked_singles_tennis_players", "https://www.tntsports.co.uk/tennis/atp/standings.shtml", "https://www.tennistv.com/players", "https://www.atptour.com/en/rankings/singles"], "search_results": [{"title": "Men's Tennis ATP Rankings 2025", "url": "https://www.espn.com/tennis/rankings", "date": "2025-08-11", "last_updated": "2025-08-11"}, {"title": "List of ATP number 1 ranked singles tennis players - Wikipedia", "url": "https://en.wikipedia.org/wiki/List_of_ATP_number_1_ranked_singles_tennis_players", "date": "2005-08-30", "last_updated": "2025-08-14"}, {"title": "ATP 2025 World Ranking - Tennis", "url": "https://www.tntsports.co.uk/tennis/atp/standings.shtml", "date": null, "last_updated": null}, {"title": "Tennis Players Rankings & Videos | ATP Player Profiles", "url": "https://www.tennistv.com/players", "date": "2021-10-20", "last_updated": "2025-08-13"}, {"title": "PIF ATP Rankings (Singles) | ATP Tour | Tennis", "url": "https://www.atptour.com/en/rankings/singles", "date": "2024-12-01", "last_updated": "2025-08-08"}], "object": "chat.completion", "choices": [{"index": 0, "finish_reason": "stop", "message": {"role": "assistant", "content": "The current top 10 men's tennis players in the world according to the ATP rankings as of early August 2025 are:\n\n1. Jannik Sinner  \n2. Carlos Alcaraz  \n3. Alexander Zverev  \n4. Taylor Fritz  \n\nThe available search results list only the top 4 players explicitly from the ATP rankings as of August 2025[1][3]. Other positions in the top 10 were not detailed in the search results.\n\nAdditional context: Jannik Sinner is the current world No. 1 according to ATP rankings and has recently ascended to the top spot, ahead of Carlos Alcaraz and Alexander Zverev[1][2][3]. These rankings reflect the latest data from the ATP Tour, updated in late July and early August 2025[1][3].\n\nNo complete top 10 list was found in the search results, but the top 4 is confirmed from multiple sources. For the full top 10, consulting the official ATP Tour website ranked page would provide the most precise and current listing beyond the top 4."}, "delta": {"role": "assistant", "content": ""}}]}



"""


import httpx
from src.utils.settings import settings, get_key
from pydantic import SecretStr
import asyncio


# lets get the response of the perplexity api using http post request
prompt = "get the names of the top 10 tennis players in the world"

# Perplexity Model
async def get_perplexity_llm(model_num: int = 1, prompt:str = None):
        """
        It returns the url, headers, payload variables which will be used in initializing the httpx request.
        """

        # lets get api of perplexity
        get_perplexity_api: SecretStr | None = get_key(api_key=settings.PERPLEXITY_API_KEY)
        if get_perplexity_api is None:
            raise ValueError("Perplexity api is not set, please check .env")
        
        # lets get base url of perplexity
        get_perplexity_base_url: SecretStr | None = get_key(api_key= settings.PERPLEXITY_BASE_URL)
        if get_perplexity_base_url is None:
            raise ValueError("Perplexity base url is not set, please check .env")

        # lets get the available perplexity models
        models = {1: "sonar", 2: "sonar-pro"}

        url = get_perplexity_base_url
        headers = {"Authorization": f"Bearer {get_perplexity_api}"}
        payload = {
            "model": models.get(model_num,"sonar-pro"),
            "messages": [
                {
                    "role": "user",
                    "content": f"{prompt}"
                }
            ]
        }

        # lets get the asyncClient for api call using httpx
        async with httpx.AsyncClient(timeout=45) as asyncclient:
            try:
                response = await asyncclient.post(url=url, headers=headers, json= payload)

                response.status_code

                return response.text
            except ConnectionError as e:
                raise ConnectionError("Perplexity api is not reachable")

if __name__ == "__main__":
    
    output = asyncio.run(get_perplexity_llm(1, prompt=prompt))

    print(type(output))


  