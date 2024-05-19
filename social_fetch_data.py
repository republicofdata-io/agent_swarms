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
    "limit": 50,
    "dimensions": [
        "media_conversations.article_url",
        "media_conversations.post_natural_key",
        "media_conversations.social_network_profile_username",
        "media_conversations.social_network_profile_location_admin1_name",
        "media_conversations.post_text",
        "media_conversations.conversation_natural_key",
        "media_conversations.post_creation_ts",
        "media_conversations.post_impression_count",
        "media_conversations.post_reply_count",
        "media_conversations.post_quote_count",
        "media_conversations.post_like_count",
        "media_conversations.post_retweet_count",
        "media_conversations.post_bookmark_count"
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

    # Iterate through the retrieved data and group tweets by conversation_natural_key
    for item in data:
        conversation_key = item.get("media_conversations.conversation_natural_key")
        post_key = item.get("media_conversations.post_natural_key")
        post_data = {
            "post_id": item.get("media_conversations.post_natural_key"),
            "article_url": item.get("media_conversations.article_url"),
            "post_author": item.get("media_conversations.social_network_profile_username"),
            "post_author_admin1_name": item.get("media_conversations.social_network_profile_location_admin1_name"),
            "post_text": item.get("media_conversations.post_text"),
            "post_creation_ts": item.get("media_conversations.post_creation_ts"),
            "post_impression_count": item.get("media_conversations.post_impression_count"),
            "post_reply_count": item.get("media_conversations.post_reply_count"),
            "post_quote_count": item.get("media_conversations.post_quote_count"),
            "post_like_count": item.get("media_conversations.post_like_count"),
            "post_retweet_count": item.get("media_conversations.post_retweet_count"),
            "post_bookmark_count": item.get("media_conversations.post_bookmark_count")
        }

        if conversation_key not in transformed_data:
            transformed_data[conversation_key] = {
                "parent": None,
                "replies": []
            }

        if conversation_key == post_key:
            transformed_data[conversation_key]["parent"] = post_data
        else:
            transformed_data[conversation_key]["replies"].append({
                "post_text": item.get("media_conversations.post_text"),
                "post_author": item.get("media_conversations.social_network_profile_username"),
                "post_author_admin1_name": item.get("media_conversations.social_network_profile_location_admin1_name")
            })

    # Remove conversations that do not have a parent tweet
    transformed_data = {key: value for key, value in transformed_data.items() if value["parent"] is not None}

    # Generate a unique filename using the current date and time
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'social_data_{timestamp}.json'

    # Save the transformed data to a JSON file
    with open(filename, 'w') as f:
        json.dump(transformed_data, f, indent=4, sort_keys=True)

    print("Social data saved to JSON file.")
else:
    print("Failed to retrieve data:", response.status_code, response.text)
