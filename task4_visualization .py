#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/trends_analysed.csv")
# Chart 1 — Top stories by score

top10 = df.nlargest(10, "score").sort_values("score")

    # shortening long titles to fit in

short_titles = [t[:40] for t in top10["title"]] 

plt.figure(figsize=(10, 6))
plt.barh(short_titles, top10["score"])
plt.xlabel("Score")
plt.title("Top 10 Stories by Score")
plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png")
plt.show()
plt.close()

# Chart 2 — Stories by category

counts = df["category"].value_counts()
plt.figure(figsize=(8, 5))
plt.bar(counts.index, counts.values)
plt.xlabel("Category")
plt.ylabel("Number of stories")
plt.title("Stories by Category")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/chart2_categories.png")
plt.show()
plt.close()

# Chart 3: score vs comments
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]
plt.figure(figsize=(8, 6))
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not popular")
plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.xlabel("Score")
plt.ylabel("Number of comments")
plt.title("Score vs Comments")
plt.legend()
plt.savefig("outputs/chart3_scatter.png")
plt.show()
plt.close()

print("Saved 3 charts in the outputs folder")

# Dashboard creation
fig, axes = plt.subplots(2, 2, figsize=(16, 10))


# 1. Top 10 stories
axes[0, 0].barh(
    top10["title"],
    top10["score"]
)

axes[0, 0].set_title("Top 10 Stories by Score")
axes[0, 0].set_xlabel("Score")
axes[0, 0].set_ylabel("Story")

axes[0, 0].invert_yaxis()


# 2. Stories by category
axes[0, 1].bar(
    category_counts.index,
    category_counts.values
)

axes[0, 1].set_title("Stories by Category")
axes[0, 1].set_xlabel("Category")
axes[0, 1].set_ylabel("Number of Stories")

axes[0, 1].tick_params(axis="x", rotation=45)


# 3. Score vs comments
axes[1, 0].scatter(
    not_popular["score"],
    not_popular["num_comments"],
    label="Not Popular"
)

axes[1, 0].scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular"
)

axes[1, 0].set_title("Score vs Comments")
axes[1, 0].set_xlabel("Score")
axes[1, 0].set_ylabel("Number of Comments")

axes[1, 0].legend()


# 4. Extra chart — Score distribution
axes[1, 1].hist(
    df["score"],
    bins=20
)

axes[1, 1].set_title("Score Distribution")
axes[1, 1].set_xlabel("Score")
axes[1, 1].set_ylabel("Number of Stories")


# Overall dashboard title
fig.suptitle(
    "TrendPulse — Hacker News Analysis Dashboard",
    fontsize=18
)

plt.tight_layout()
plt.savefig("outputs/Dashboard.png")
plt.show()

