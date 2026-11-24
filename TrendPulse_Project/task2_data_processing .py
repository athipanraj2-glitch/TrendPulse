#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd

df = pd.read_json("data/trends_20260929.json")

print("Loaded", len(df), "stories")

# 1. Removing duplicate post IDs

df = df.drop_duplicates(subset="post_id")
print("After Dropping duplicates:", len(df))

# 2. Dropping rows missing required fields

df = df.dropna(subset=["post_id", "title", "score"])
print("After Dropping nulls:", len(df))

# 3. Converting score and num_comments into integers.

df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce")

# 4. Remove stories with score below 5
df = df[df["score"] >= 5]
print("After removing low scores:", len(df))

# 5. Removing extra spaces from titles
df["title"] = df["title"].str.strip()

df.to_csv("data/trends_clean.csv", index=False)
print("Rows after cleaning:", len(df))
print("\nStories per category:")
print(df["category"].value_counts())

