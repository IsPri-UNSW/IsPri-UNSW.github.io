#!/usr/bin/env python3
"""
Script to add new news articles to the website

:param --title: The title of the article (optional, triggers automation mode)
:param --date: The date of the article in YYYY-MM-DD format (optional)
:param --content: The content of the article (optional)
:returns: None
"""

import sys
import argparse
from datetime import datetime
from pathlib import Path
import urllib.request
import urllib.error

from paths import NEWS_DIR as DEFAULT_NEWS_DIR


def slugify(text):
    """
    Converts text to a URL-friendly slug

    :param text: The input string to convert
    :returns: A URL-safe slug string
    """
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
    """
    Gets date from user interactively, defaulting to today

    :returns: A datetime object
    """
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
    """
    Gets multiline input from user

    :param prompt: The prompt to display to the user
    :returns: A single string containing the joined lines
    """
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


def create_news_article(title, date, content, base_path=None, image_url=None):
    """
    Creates a new news article file structure

    :param title: The title of the article
    :param date: The date object for the article
    :param content: The body content of the article
    :param base_path: The root directory for news
    :param image_url: Optional URL to download featured image from
    :returns: Boolean indicating success or failure
    """
    if base_path is None:
        base_path = DEFAULT_NEWS_DIR
    else:
        base_path = Path(base_path)
    
    if not base_path.exists():
        # Auto-create for CI environments if it does not exist
        try:
            base_path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"Error: Could not create news directory at {base_path}. {e}")
            return False
    
    # Create folder name: YY-MM-DD-slug
    date_prefix = date.strftime('%y-%m-%d')
    title_slug = slugify(title)
    folder_name = f"{date_prefix}-{title_slug}"
    
    article_dir = base_path / folder_name
    
    # Check if folder already exists
    if article_dir.exists():
        print(f"Error: Folder '{folder_name}' already exists.")
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
    
    # Download featured image if URL provided
    if image_url and image_url.strip():
        featured_image = article_dir / 'featured.jpg'
        try:
            print(f"\nDownloading featured image from: {image_url}")
            urllib.request.urlretrieve(image_url.strip(), featured_image)
            print(f"✓ Featured image saved: {featured_image}")
        except urllib.error.URLError as e:
            print(f"Warning: Could not download image from {image_url}: {e}")
        except Exception as e:
            print(f"Warning: Error saving image: {e}")
    
    print(f"\n✓ News article created successfully!")
    print(f"  Location: {article_dir}")
    print(f"  File: {index_file}")
    
    return True


def main():
    """
    Main function handling both CLI args and interactive input
    
    :returns: None
    """
    parser = argparse.ArgumentParser(description="Add news article")
    parser.add_argument('--title', help="Article title")
    parser.add_argument('--date', help="Article date (YYYY-MM-DD)")
    parser.add_argument('--content', help="Article content")
    parser.add_argument('--image-url', help="URL to featured image (will be saved as featured.jpg)")
    args = parser.parse_args()

    # Automation Mode (CI/CD)
    if args.title and args.content:
        # Default to today if date is missing or empty string
        article_date = datetime.now()
        
        if args.date and args.date.strip():
            try:
                article_date = datetime.strptime(args.date.strip(), '%Y-%m-%d')
            except ValueError:
                print(f"Warning: Invalid date format '{args.date}'. Using today.")
                # Fallback to today is already set above

        success = create_news_article(args.title, article_date, args.content, image_url=args.image_url)
        sys.exit(0 if success else 1)

    # Interactive Mode
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
