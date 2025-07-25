

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
          "primary": true,
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

