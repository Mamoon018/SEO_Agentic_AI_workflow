

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
      "text": "LangGraph flexibility to create agentic workflow",
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
      "text": "AI models in agents with autonomous decision making",
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
      "text": "ToolNode often crashes",
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
      "text": "AI applications changing course of SaaS",
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
      "text": "Agentic AI offering wide range of architects",
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
      "text": "tools integration",
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