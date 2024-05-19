import os
import requests
import json
from datetime import datetime

# Load the environment variable
auth_key = os.getenv('ROD_AUTH_KEY')

# URL from your curl request
url = "https://neighbouring-rhinoceros.gcp-us-central1.cubecloudapp.dev/cubejs-api/v1/load"

# Headers including the authorization token
headers = {
    "Authorization": f"Bearer {auth_key}"
}

# Query data
query = {
    "limit": 100,
    "dimensions": [
        "media_conversations.article_url",
        "media_conversations.article_title",
        "media_conversations.article_tags",
        "media_conversations.article_summary",
        "media_conversations.article_description",
        "media_conversations.article_content",
        "media_conversations.article_author"

    ],
    "timeDimensions": [
        {
            "dimension": "media_conversations.article_publication_ts",
            "granularity": "day",
            "dateRange": "This week"
        }
    ],
    "order": {
        "media_conversations.article_url": "asc"
    }
}

# Make the GET request
response = requests.get(url, headers=headers, params={'query': json.dumps(query)})

# Check the response
if response.status_code == 200:
    response_data = response.json()
    data = response_data.get("data", [])
    transformed_data = {}

    # Iterate through the retrieved data and transform it
    for item in data:
        conversation_key = item.get("media_conversations.article_url")
        article_data = {
            "article_url": item.get("media_conversations.article_url"),
            "article_title": item.get("media_conversations.article_title"),
            "article_tags": item.get("media_conversations.article_tags"),
            "article_summary": item.get("media_conversations.article_summary"),
            "article_description": item.get("media_conversations.article_description"),
            "article_content": item.get("media_conversations.article_content"),
            "article_author": item.get("media_conversations.article_author") 
        }
        if conversation_key in transformed_data:
            transformed_data[conversation_key].append(article_data)
        else:
            transformed_data[conversation_key] = [article_data]
    
    # Generate a unique filename using the current date and time
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'article_data_{timestamp}.json'

    # Save the transformed data to a JSON file
    with open(filename, 'w') as f:
        json.dump(transformed_data, f, indent=4, sort_keys=True)

    print("Article data saved to JSON file.")
else:
    print("Failed to retrieve data:", response.status_code, response.text)