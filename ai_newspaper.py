#!/usr/bin/env python3
"""
AI Newspaper MVP
Fetches AI news, summarizes with GPT, outputs Markdown, organizes by month.
"""

import os
import glob
from datetime import date
from openai import OpenAI

# ---------- OpenAI Setup ----------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("Set OPENAI_API_KEY as environment variable.")

def get_ai_summary():
    """Call GPT to generate AI news summary"""
    prompt = """
Summarize the top 3 AI news updates for today in markdown format.
Include:
- 3 Headlines
- 2 Research Highlights
- 1 Cool Tool or Project
Keep it concise and clear.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=600
    )
    return response.choices[0].message.content

# ---------- Generate today's edition ----------
today = date.today()
month_folder = today.strftime("%Y-%m")
output_dir = os.path.join("output", month_folder)
os.makedirs(output_dir, exist_ok=True)

today_str = today.strftime("%Y-%m-%d")
output_file = os.path.join(output_dir, f"ai_news_{today_str}.md")

# Generate AI summary
summary = get_ai_summary()

# Save today's edition
with open(output_file, "w", encoding="utf-8") as f:
    f.write(f"# 📰 AI Newspaper – {today_str}\n\n")
    f.write("### Powered by AI, bringing you the latest in tech & trends\n\n")
    f.write(summary)

# ---------- Build homepage (index.md) ----------
index_file = os.path.join("output", "index.md")

# Find all editions grouped by month
months = sorted(glob.glob("output/[0-9][0-9][0-9][0-9]-[0-9][0-9]"), reverse=True)

with open(index_file, "w", encoding="utf-8") as f:
    # Title banner
    f.write("# 📰 AI Newspaper\n\n")
    f.write("> *Your daily AI-powered digest of tech, innovation & trends.*\n\n")
    f.write("---\n\n")

    # Show today's edition
    with open(output_file, "r", encoding="utf-8") as latest:
        f.write("## 🗞️ Today’s Edition\n\n")
        f.write(latest.read())
        f.write("\n\n---\n\n")

    # Archive grouped by month
    f.write("## 📚 Past Editions\n\n")
    for month in months:
        month_name = os.path.basename(month)
        f.write(f"### {month_name}\n")
        editions = sorted(glob.glob(os.path.join(month, "ai_news_*.md")), reverse=True)
        for edition in editions:
            filename = os.path.basename(edition)
            date_str = filename.replace("ai_news_", "").replace(".md", "")
            f.write(f"- [{date_str}]({month_name}/{filename.replace('.md','.html')})\n")
        f.write("\n")

    # Footer
    f.write("\n---\n")
    f.write("© Powered by AI | Updated daily at 6 AM UTC\n")

print(f"✅ AI Newspaper saved to {output_file}")
