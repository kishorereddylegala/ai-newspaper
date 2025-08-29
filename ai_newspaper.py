from datetime import date
import os
import glob

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

today = date.today().strftime("%Y-%m-%d")
output_file = os.path.join(output_dir, f"ai_news_{today}.md")

# Save today's edition
with open(output_file, "w", encoding="utf-8") as f:
    f.write("# 📰 AI Newspaper\n\n")
    f.write(f"## Edition: {today}\n\n")
    f.write(summary)  # <-- replace with your summary variable

# --- Build homepage ---
index_file = os.path.join(output_dir, "index.md")

# Find all editions
editions = sorted(glob.glob(os.path.join(output_dir, "ai_news_*.md")), reverse=True)

with open(index_file, "w", encoding="utf-8") as f:
    f.write("# 📰 AI Newspaper\n\n")
    f.write("Welcome to your AI-powered daily newspaper! 📡\n\n")

    # Show today's news directly
    latest_file = editions[0]
    with open(latest_file, "r", encoding="utf-8") as latest:
        f.write("## 🗞️ Today's Edition\n\n")
        f.write(latest.read())
        f.write("\n\n---\n\n")

    # List archive links
    f.write("## 📚 Archive\n\n")
    for edition in editions:
        filename = os.path.basename(edition)
        date_str = filename.replace("ai_news_", "").replace(".md", "")
        f.write(f"- [{date_str}]({filename.replace('.md','.html')})\n")
