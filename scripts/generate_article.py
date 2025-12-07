#!/usr/bin/env python3
"""
Daily article generator for The Daily Signal.
Uses Google Gemini API to generate AI/Quantum/Tech news articles.
"""

import os
import re
from datetime import datetime
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

def get_today_date():
    """Get formatted date string."""
    return datetime.now().strftime('%B %-d, %Y')

def generate_article():
    """Generate a news article using Gemini."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    today = get_today_date()
    
    prompt = f"""You are a journalist for "The Daily Signal", a news site covering AI, Quantum Computing, and Technology Policy.

Today is {today}. Search your knowledge for the most significant, globally-relevant news story in AI, Quantum Computing, or Tech Policy from the past 24-48 hours.

Requirements:
- Choose a story with GLOBAL significance (affects multiple countries/regions)
- Write in the style of investigative journalism (like Seymour Hersh)
- Be factual and cite real institutions, researchers, or officials
- Article should be 800-1200 words
- Include a compelling headline and subheadline
- Include 3-4 section headers (h2)
- Include one relevant quote (can be paraphrased from real sources)

Return the article in this exact JSON format:
{{
  "kicker": "CATEGORY · SUBCATEGORY",
  "headline": "Main headline here",
  "subhead": "Compelling subheadline that expands on the story",
  "lede_first_letter": "T",
  "lede_rest": "he rest of the opening paragraph...",
  "body_html": "<p>Rest of article with <h2>Section Headers</h2> and <blockquote class=\\"article-quote\\">quotes<cite>— Source</cite></blockquote></p>",
  "source_url": "https://...",
  "source_name": "Source Name",
  "source_description": "Brief description of the source"
}}

IMPORTANT: Return ONLY valid JSON, no markdown code blocks."""

    response = model.generate_content(prompt)
    return response.text

def update_index_html(article_json):
    """Update index.html with new article content."""
    import json
    
    # Parse the JSON response
    # Handle potential markdown code blocks
    text = article_json.strip()
    if text.startswith('```'):
        text = re.sub(r'^```json?\n?', '', text)
        text = re.sub(r'\n?```$', '', text)
    
    article = json.loads(text)
    
    # Read current index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    today = get_today_date()
    
    # Update kicker
    html = re.sub(
        r'<span class="article-kicker">.*?</span>',
        f'<span class="article-kicker">{article["kicker"]}</span>',
        html, flags=re.DOTALL
    )
    
    # Update headline
    html = re.sub(
        r'<h1 class="article-headline">.*?</h1>',
        f'<h1 class="article-headline">{article["headline"]}</h1>',
        html, flags=re.DOTALL
    )
    
    # Update subhead
    html = re.sub(
        r'<p class="article-subhead">.*?</p>',
        f'<p class="article-subhead">{article["subhead"]}</p>',
        html, flags=re.DOTALL
    )
    
    # Update timestamp
    html = re.sub(
        r'<span class="article-timestamp">.*?</span>',
        f'<span class="article-timestamp">{today} · 8 min read</span>',
        html, flags=re.DOTALL
    )
    
    # Update article body
    lede = f'<span class="drop-cap">{article["lede_first_letter"]}</span>{article["lede_rest"]}'
    new_body = f'''<div class="article-body">
                <p class="article-lede">{lede}</p>

                {article["body_html"]}

                <p class="article-end-mark">◆</p>
            </div>'''
    
    html = re.sub(
        r'<div class="article-body">.*?<p class="article-end-mark">◆</p>\s*</div>',
        new_body,
        html, flags=re.DOTALL
    )
    
    # Update source
    html = re.sub(
        r'<ul class="sources-list">.*?</ul>',
        f'''<ul class="sources-list">
                    <li><a href="{article["source_url"]}" target="_blank" rel="noopener">{article["source_name"]}</a> — {article["source_description"]}</li>
                </ul>''',
        html, flags=re.DOTALL
    )
    
    # Write updated HTML
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Article updated: {article['headline']}")

def main():
    print("Generating new article...")
    article_json = generate_article()
    print("Updating index.html...")
    update_index_html(article_json)
    print("Done!")

if __name__ == '__main__':
    main()
