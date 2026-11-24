#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd

# Loaded cleaned data
df = pd.read_csv("data/trends_clean.csv")


# 1. First five rows
print("First five rows:")
print(df.head(5))


# 2. DataFrame shape
print("\nDataFrame shape:", df.shape)


# 3. Average score
print("\nAverage score:",  df["score"].mean())


# 4. Average comments
print("Average comments:", df["num_comments"].mean())


# 5. NumPy analysis
scores = df["score"].to_numpy()

print("\nNumPy analysis:")
print("Mean:", np.mean(scores))
print("Median:", np.median(scores))
print("Standard deviation:", np.std(scores))
print("Maximum:", np.max(scores))
print("Minimum:", np.min(scores))

# 6. Category with the most stories
most_common_category = df["category"].value_counts().idxmax()

print("\nCategory with most stories:", most_common_category)


# 7. Story with the most comments
top_commented = df.loc[df["num_comments"].idxmax()]

print("\ntop commented story:")
print("Title:", top_commented["title"])
print("Comments:", top_commented["num_comments"])


# 8. Engagement
df["engagement"] = df["num_comments"] / (df["score"] + 1)


# 9. Is popular
df["is_popular"] = df["score"] > df["score"].mean()


# 10. Save analysed data
df.to_csv("data/trends_analysed.csv", index=False)

print("\nAnalysed data saved successfully.")

