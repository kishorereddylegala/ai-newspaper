#!/usr/bin/env python3
"""
AI Newspaper (Multi-page Edition)
Generates a 16-page AI Newspaper with different sections, outputs in Markdown.
"""

import os
from datetime import date
from openai import OpenAI

# ---------- OpenAI Setup ----------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("Set OPENAI_API_KEY as environment variable.")

# ---------- Prompts for each section ----------
SECTIONS = [
    ("Page 1", "Main Headlines: Summarize 3 biggest AI news stories."),
    ("Page 2", "Research Highlights: Summarize 2 new AI research papers."),
    ("Page 3", "Cool Tools: Introduce 2-3 new AI tools, startups or repos."),
    ("Page 4", "Entrepreneur Insights: How AI is impacting business."),
    ("Page 5", "For Kids: Fun facts or beginner-level AI explanations."),
    ("Page 6", "AI in Healthcare: Latest medical AI applications."),
    ("Page 7", "AI in Education: Tools & research for learning."),
    ("Page 8", "AI & Society: Ethics, regulations, policy."),
    ("Page 9", "AI in Art & Creativity: Generative AI, music, design."),
    ("Page 10", "AI in Gaming: Latest use of AI in gaming."),
    ("Page 11", "Productivity & Work: AI in offices, workflow."),
    ("Page 12", "Coding Corner: AI tools for developers."),
    ("Page 13", "Future Trends: What’s next in AI."),
    ("Page 14", "Interview / Quote of the Day."),
    ("Page 15", "Startups & Funding News."),
    ("Page 16", "Summary & Closing Notes."),
]

def generate_page(content_prompt):
    """Ask GPT to generate one section of the newspaper"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": content_prompt}],
        temperature=0.4,
        max_tokens=700
    )
    return response.choices[0].message.content

# ---------- Generate today's edition ----------
today = date.today()
month_folder = today.strftime("%Y-%m")
output_dir = os.path.join("output", month_folder, today.strftime("%Y-%m-%d"))
os.makedirs(output_dir, exist_ok=True)

index_content = [f"# 📰 AI Newspaper – {today}\n\n",
                 "### Powered by AI, 16-page daily digest\n\n",
                 "---\n\n",
                 "## 📑 Pages\n\n"]

# Generate all 16 pages
for i, (title, prompt) in enumerate(SECTIONS, start=1):
    print(f"Generating {title}...")
    content = generate_page(prompt)
    filename = f"page_{i:02d}.md"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(content)
    index_content.append(f"- [{title}]({today.strftime('%Y-%m-%d')}/{filename})\n")

# Save index.md (homepage for today)
index_file = os.path.join("output", "index.md")
with open(index_file, "w", encoding="utf-8") as f:
    f.writelines(index_content)
    f.write("\n---\n")
    f.write("© Powered by AI | Updated daily at 6 AM UTC\n")

print(f"✅ 16-page AI Newspaper generated in {output_dir}")
