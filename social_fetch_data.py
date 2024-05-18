import requests
import json

# URL from your curl request
url = "https://neighbouring-rhinoceros.gcp-us-central1.cubecloudapp.dev/cubejs-api/v1/load"

# Headers including the authorization token
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiY2FpdGxpbkByZXB1YmxpY29mZGF0YS5pbyJ9.1qTH-R-zKevtKNC13XXQxCrIn4pDOWKt8JFFe1FHRCk"
}

# Query data
query = {
    "limit": 100,
    "dimensions": [
        "media_conversations.article_url",
        "media_conversations.article_title",
        "media_conversations.article_tags",
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

    # Iterate through the retrieved data and transform it
    for item in data:
        conversation_key = item.get("media_conversations.conversation_natural_key")
        post_data = {
            "post_id": item.get("media_conversations.post_natural_key"),
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
        if conversation_key in transformed_data:
            transformed_data[conversation_key].append(post_data)
        else:
            transformed_data[conversation_key] = [post_data]

    # Save the transformed data to a JSON file
    with open('transformed_data.json', 'w') as f:
        json.dump(transformed_data, f, indent=4, sort_keys=True)

    print("Data saved to JSON file.")
else:
    print("Failed to retrieve data:", response.status_code, response.text)
