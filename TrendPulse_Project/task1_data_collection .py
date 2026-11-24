#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import json
import os
from datetime import datetime, timezone

TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
STORY_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

MAX_STORIES_TO_CHECK = 500
MAX_STORIES_PER_CATEGORY = 25

# 1. Fetching top story IDs

try:
    response = requests.get(
        TOP_STORIES_URL,
        timeout=10
    )

    response.raise_for_status()

    top_story_ids = response.json()

except requests.RequestException as error:
    print("Failed to fetch story IDs:", error)
    top_story_ids = []


print("Total IDs:", len(top_story_ids))
print("Considering first", MAX_STORIES_TO_CHECK, "IDs")


# 2. Creating categories

categories = {
    "technology": [],
    "worldnews": [],
    "sports": [],
    "science": [],
    "entertainment": []
}

# 3. KeyWords that decide the category of a story title
keywords = {
    "technology": ["ai", "software", "computer", "programming", "code", "chip",
                   "cloud", "linux", "python", "rust", "app", "data", "google",
                   "apple", "microsoft", "openai", "security", "web", "tech"],
    "worldnews": ["election", "government", "war", "president", "policy", "law",
                  "china", "russia", "ukraine", "india", "europe", "court",
                  "tax", "ban", "police", "economy", "military"],
    "sports": ["football", "cricket", "tennis", "basketball", "baseball", "nfl",
               "nba", "olympics", "soccer", "golf", "race", "athlete", "sport"],
    "science": ["research", "nasa", "space", "physics", "biology", "climate",
                "study", "scientist", "planet", "mars", "quantum", "dna",
                "brain", "energy", "math", "medicine"],
    "entertainment": ["movie", "music", "actor", "film", "tv", "game", "netflix",
                      "song", "album", "show", "anime", "book", "podcast",
                      "youtube", "streaming"],
}

# 4. Defining a Function to classify  story titles


def find_category(title):
    title = title.lower()
    for category, words in keywords.items():
        for word in words:
            if word in title:
                return category
    return None



# 5. Collection timestamp

collection_timestamp = datetime.now(
    timezone.utc
).isoformat()


# 6. Fetching and classifying stories

for story_id in top_story_ids[:MAX_STORIES_TO_CHECK]:

    # Stops when all categories have 25 stories
    if all(len(categories[category]) >= MAX_STORIES_PER_CATEGORY
        for category in categories):
        break

    try:

        story_response = requests.get(
            STORY_URL.format(story_id),
            timeout=10
        )

        story_response.raise_for_status()

        story = story_response.json()

    except requests.RequestException as error:
        print(f"Failed to fetch story {story_id}: {error}")
        continue


    # Making sure the item is a story

    if story.get("type") != "story":
        continue
    title = story.get("title", "")
    if not title:
        continue


    # Classify the title

    category = find_category(title)
    if category is None:
        continue


    # Don't collect more than 25 per category
    if len(categories[category]) >= MAX_STORIES_PER_CATEGORY:
        continue


    # Creating the required story record
    story_data = {
        "post_id": story.get("id"),
        "title": title,
        "category": category,
        "score": story.get("score", 0),
        "num_comments": story.get("descendants", 0),
        "author": story.get("by", ""),
        "collected_at": collection_timestamp
    }


    categories[category].append(story_data)

# 7. Combining all categories

all_stories = []

for category in categories:

    all_stories.extend(categories[category])

# 8. Creating a data folder

os.makedirs("data", exist_ok=True)



# 9. Creating  dated filename

today = datetime.now().strftime("%Y%m%d")

filename = f"data/trends_{today}.json"


# --------------------------------------------------
# 10. Save JSON file
# --------------------------------------------------

with open(filename,"w",encoding="utf-8") as file:
    json.dump(all_stories,file,indent=2,ensure_ascii=False)

print("\nCollection completed!")
print("Total stories collected:", len(all_stories))

for category in categories:
    print( f"{category}: {len(categories[category])}")
print(f"\nSaved to: {filename}")


# 12. Checking minimum requirement

if len(all_stories) >= 100:
    print("SUCCESS: At least 100 stories collected.")
else:
    print("WARNING: Less than 100 stories collected.")




# In[ ]:




