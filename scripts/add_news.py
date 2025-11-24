#!/usr/bin/env python3
"""
Script to add new news articles to the website.
Usage: python add_news.py
"""

import os
import sys
from datetime import datetime
from pathlib import Path


def slugify(text):
    """Convert text to a URL-friendly slug."""
    text = text.lower()
    text = text.replace(' ', '-')
    # Remove special characters
    allowed = set('abcdefghijklmnopqrstuvwxyz0123456789-')
    text = ''.join(c for c in text if c in allowed)
    # Remove multiple consecutive dashes
    while '--' in text:
        text = text.replace('--', '-')
    return text.strip('-')


def get_date_input():
    """Get date from user, defaulting to today."""
    today = datetime.now()
    default_date = today.strftime('%Y-%m-%d')
    
    print(f"\nEnter date (YYYY-MM-DD) or press Enter for today [{default_date}]: ", end='')
    date_str = input().strip()
    
    if not date_str:
        return today
    
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        print("Invalid date format. Using today's date.")
        return today


def get_multiline_input(prompt):
    """Get multiline input from user."""
    print(f"\n{prompt}")
    print("(Enter your text. Press Ctrl+D (Mac/Linux) or Ctrl+Z (Windows) when done)")
    print("-" * 60)
    
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    
    return '\n'.join(lines).strip()


def create_news_article(title, date, content, base_path=None):
    """Create a new news article."""
    if base_path is None:
        # Get the script's directory and go up to find content/news
        script_dir = Path(__file__).parent
        base_path = script_dir.parent / 'content' / 'news'
    else:
        base_path = Path(base_path)
    
    if not base_path.exists():
        print(f"Error: News directory not found at {base_path}")
        return False
    
    # Create folder name: YY-MM-DD-slug
    date_prefix = date.strftime('%y-%m-%d')
    title_slug = slugify(title)
    folder_name = f"{date_prefix}-{title_slug}"
    
    article_dir = base_path / folder_name
    
    # Check if folder already exists
    if article_dir.exists():
        print(f"\nWarning: Folder '{folder_name}' already exists.")
        print("Do you want to overwrite it? (yes/no): ", end='')
        response = input().strip().lower()
        if response not in ['yes', 'y']:
            print("Cancelled.")
            return False
    
    # Create directory
    article_dir.mkdir(parents=True, exist_ok=True)
    
    # Create index.md
    index_file = article_dir / 'index.md'
    
    # Format date for front matter
    date_str = date.strftime('%Y-%m-%d')
    
    # Create content
    front_matter = f"""---
title: {title}
date: {date_str}
---

{content}
"""
    
    # Write file
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(front_matter)
    
    print(f"\n✓ News article created successfully!")
    print(f"  Location: {article_dir}")
    print(f"  File: {index_file}")
    
    return True


def main():
    """Main function."""
    print("=" * 60)
    print("Add New News Article")
    print("=" * 60)
    
    # Get title
    print("\nEnter article title: ", end='')
    title = input().strip()
    
    if not title:
        print("Error: Title cannot be empty.")
        sys.exit(1)
    
    # Get date
    date = get_date_input()
    
    # Get content
    content = get_multiline_input("Enter article content:")
    
    if not content:
        print("Error: Content cannot be empty.")
        sys.exit(1)
    
    # Confirm
    print("\n" + "=" * 60)
    print("Preview:")
    print("=" * 60)
    print(f"Title: {title}")
    print(f"Date: {date.strftime('%Y-%m-%d')}")
    print(f"Content:\n{content}")
    print("=" * 60)
    
    print("\nCreate this article? (yes/no): ", end='')
    response = input().strip().lower()
    
    if response not in ['yes', 'y']:
        print("Cancelled.")
        sys.exit(0)
    
    # Create article
    if create_news_article(title, date, content):
        print("\n✓ Done! You can now commit and push the changes.")
    else:
        print("\n✗ Failed to create article.")
        sys.exit(1)


if __name__ == '__main__':
    main()
