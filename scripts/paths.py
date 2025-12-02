"""
Centralized path definitions for the IsPri-UNSW website scripts.
"""
import os
from pathlib import Path

# Determine root path of the repository - this scripts module is in scripts/
ROOT_PATH = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Content directories
CONTENT_DIR = ROOT_PATH / 'content'
AUTHORS_DIR = CONTENT_DIR / 'authors'
PUBLICATIONS_DIR = CONTENT_DIR / 'publication'
FILTERED_PUBLICATIONS_DIR = CONTENT_DIR / 'filtered_publication'
NEWS_DIR = CONTENT_DIR / 'news'

# BibTeX directory
BIBTEX_DIR = CONTENT_DIR / 'bibtex'

# Output files
FILTERED_PUBLICATIONS_YAML = PUBLICATIONS_DIR / 'filtered_publications.yaml'
