#!/usr/bin/env python3
"""
AI Newspaper MVP
Fetches AI news + papers, summarizes with GPT, outputs Markdown.
"""

import os
import feedparser
from datetime import date
from openai import OpenAI

# ---------- Config ----------
RSS_FEEDS = [
    "http://export.arxiv.org/rss/cs.AI",               # arXiv AI
    "https://hnrss.org/newest?q=AI"                    # Hacker News AI
]

OUTPUT_DIR = "output"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("Set OPENAI_API_KEY as environment variable.")

client = OpenAI(api_key=OPENAI_API_KEY)

# ---------- Fetch articles ----------
articles = []
for feed_url in RSS_FEEDS:
    feed = feedparser.parse(feed_url)
    for entry in feed.entries[:3]:  # top 3 articles per feed
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "summary": entry.get("summary", "")
        })

# ---------- Summarize with GPT ----------
prompt = f"""
Summarize the following articles into a mini AI Newspaper:
1. 3 Headlines
2. 2 Research Highlights
3. 1 Cool Tool or Project
Keep it short and clear.

Articles:
{articles}
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.2,
    max_tokens=600
)

summary = response.choices[0].message.content

# ---------- Save Markdown ----------
os.makedirs(OUTPUT_DIR, exist_ok=True)
out_file = os.path.join(OUTPUT_DIR, f"AI_Times_{date.today()}.md")
with open(out_file, "w", encoding="utf-8") as f:
    f.write(f"# 📰 AI Times — {date.today()}\n\n")
    f.write(summary)

print(f"✅ AI Newspaper saved to {out_file}")
