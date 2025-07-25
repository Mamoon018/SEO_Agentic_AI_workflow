"""
Here we will define the web scraper tool.
"""

import urllib.parse
import requests

from typing import Optional
from langchain_core.tools import BaseTool
from langchain_core.tools.base import ArgsSchema
from pydantic import BaseModel, Field, AnyUrl
import asyncio
import httpx
from httpx import AsyncClient

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun
)
from src.utils.settings import get_key, settings
import validators




class DIFFBOT_INPUT(BaseModel):
    """
    Here we will define the schema of the tool.
    """

    user_url: AnyUrl = Field(description= "It is the url of the published article of user that needs to be scrapped")



class DIFFBOT_TOOL(BaseTool):
        
    """
    Tool:  Website content extractor

    **Args:**
    It takes the the URL as input, and scrap the content that is on the given URL.

    **Input:**
    URL (str): It is the input URL of the website that we want to scrap.

    **Raisies:**
    It raises error when tool is either not able to access the website or URL is not correct.


    STEPS:
    1) Generate API URL using the api key and user URL
    2) Using the API URL to scrap the data in JSON format

    """

    name: str = "Web_scraping_tool"
    description: str = ("It conducts the web scrapping task using the diffbot url api. It returns the data in the json format"
    "It takes the URL as an input, which is the link of the website that we want to scrap. It scraps its content."
    "Tool results contain objects array that contains metadata and content of the website")
    args_schema: Optional[ArgsSchema] = DIFFBOT_INPUT


    # lets get the the response of the api in the json format
    def _run(self, user_url: AnyUrl):


        # If URL is not provided then do not execute the tool
        if not validators.url(user_url):
            return "Invalid URL"

        # lets get the api url using diffbot url generator
        api_url = self.diffbot_url_generator(user_url)

        # lets initiate the response request using api url for the given url
        api_response = requests.get(api_url)

        # lets parse the json format data
        data_scrapped = api_response.json()

        # If URL is not accessible then data_scrapped should contain "errorCode" in dictionary
        if "errorCode" in data_scrapped:
            return "Client/Server side error"

        # lets get the output parsed
        parsed_result = self.parse_diffbot_output(data_scrapped)

        return parsed_result


    async def _arun(self, user_url: AnyUrl):

        # If URL is not provided then do not execute the tool
        if not validators.url(user_url):
            return "Invalid URL"

        # lets get the api url using diffbot url generator
        api_url = self.diffbot_url_generator(user_url)

        # lets use httpx to make GET request as it supports async I/O
        timeout = httpx.Timeout(timeout=10, connect=7, read=5)
        async with httpx.AsyncClient() as client:
            api_response = await client.get(api_url, timeout= timeout)

        # lets parse the json format data
        data_scrapped = api_response.json()

        # If URL is not accessible then data_scrapped should contain "errorCode" in dictionary
        if "errorCode" in data_scrapped:
            return "Client/Server side error"

        # lets get the output parsed
        parsed_result = self.parse_diffbot_output(data_scrapped)

        return parsed_result


    # lets generate the DIFFBOT API URL that will be used to request the data
    def diffbot_url_generator(self,url: AnyUrl):

        # Encode the URL to pass as query parameter in another url (will replace special characters with '%')
        encoded_url = urllib.parse.quote_plus(url)

        # lets get the DIFFBOT API key
        diffbot_api_key: str | None = get_key(api_key= settings.DIFFBOT_API_KEY)
        

        # lets get the diffbot url using url and diffbot api key
        diffbot_api_url = f'https://api.diffbot.com/v3/article?url={encoded_url}&token={diffbot_api_key}'


        return diffbot_api_url
    

    # lets parse the scrapped data and get the relevant objects from it 

    def parse_diffbot_output(self,scrapped_data_object:dict):


        scrapped_objects = scrapped_data_object["objects"][0]
        title = scrapped_objects.get("title","N/A")
        contentlanguage = scrapped_objects.get("humanLanguage","N/A")
        article_text = scrapped_objects.get("text","N/A")
        content_type = scrapped_objects.get("type","N/A")
        website = scrapped_objects.get("siteName","N/A")
        published_date = scrapped_objects.get("estimatedDate","N/A")
        author_name = scrapped_objects.get("author","N/A")

        scrapping_result = {
            "title": title,
            "contentlanguage": contentlanguage,
            "article_text": article_text[1: 500],
            "content_type": content_type,
            "website": website,
            "published_date": published_date,
           "author_name": author_name

        }

        return scrapping_result
    


def main():
    diff_tool = DIFFBOT_TOOL()

    # lets get the link to be scrapped
    url = "https://medium.com/@vinnethvicky/in-the-realm-of-web-scraping-efficiency-and-simplicity-are-paramount-c3ff0497f255"
    
    # TEST with invalid URL
    #url = "http://www.isnal.com/" 
    
    result =  asyncio.run(diff_tool._arun(user_url=url))

    print(result)

if __name__ == "__main__":
    main()



# Final Output
{'title': 'Python Web Scraper: Harvesting Data Made Easy with Diffbot and Selenium', 'contentlanguage': 'en', 
 'article_text': 'ython Web Scraper: Harvesting Data Made Easy with Diffbot and Selenium\nIn the realm of web scraping, efficiency and simplicity are paramount. Developers are constantly seeking tools and methods to st', 
 'content_type': 'article', 'website': 'Medium', 'published_date': 'Thu, 22 Feb 2024 07:41:24 GMT', 'author_name': 'Gazzela vivakar'}

