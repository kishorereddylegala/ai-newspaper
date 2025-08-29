# AI Newspaper MVP

This project fetches AI news and papers, summarizes them using OpenAI GPT, and outputs a daily/weekly AI Newspaper.

## Setup

1. Create virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set your OpenAI API key:
   ```
   export OPENAI_API_KEY="your_key_here"    # Linux/Mac
   set OPENAI_API_KEY="your_key_here"       # Windows
   ```

4. Run script:
   ```
   python ai_newspaper.py
   ```

5. Output will be saved in `output/` folder.
