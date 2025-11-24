# IsPri UNSW Website

[![Deploy Hugo site to Pages](https://github.com/IsPri-UNSW/new_page/actions/workflows/hugo.yml/badge.svg)](https://github.com/IsPri-UNSW/new_page/actions/workflows/hugo.yml)
[![Update ORCID Data](https://github.com/IsPri-UNSW/new_page/actions/workflows/update_orcid.yml/badge.svg)](https://github.com/IsPri-UNSW/new_page/actions/workflows/update_orcid.yml)
[![Protect Theme Directory](https://github.com/IsPri-UNSW/new_page/actions/workflows/check-theme-protection.yml/badge.svg)](https://github.com/IsPri-UNSW/new_page/actions/workflows/check-theme-protection.yml)

A Hugo site for The Information Security and Privacy Research Group at UNSW.

Built on the [Hugo Research Group Template](https://github.com/HugoBlox/theme-research-group)

Theme location: `themes/blox-bootstrap/` (local copy)

Original remote theme location: `~/Library/Caches/hugo_cache/modules/filecache/modules/pkg/mod/github.com/!hugo!blox/hugo-blox-builder/modules/blox-bootstrap/v5@v5.9.8-0.20241012174104-661cadc17327/`

**Never make any changes to the files in the `themes/blox-bootstrap/` folder directly!**
We should probably go back to using the remote module at some point.
However, for now, it is easier to have the local copy as a point of reference for customisation.

## Adding News 📰

To add a new news article to the website, follow these steps:

1. **Run the news script:**
   ```bash
   python scripts/add_news.py
   ```

2. **Enter the article information when prompted:**
   - **Title:** Enter the news title (e.g., "Paper accepted at ICSE 2025")
   - **Date:** Enter the date in YYYY-MM-DD format, or press Enter to use today's date
   - **Content:** Type or paste the article content. Press `Ctrl+D` (Mac/Linux) or `Ctrl+Z` (Windows) when finished

3. **Review the preview** and confirm by typing `yes`

4. **Check the created file** in `content/news/YY-MM-DD-slug/index.md` to ensure everything looks correct

5. **(Optional) Add a featured image:**
   - Add an image file named `featured.jpg` to the same directory
   - This image will be displayed as a thumbnail with the news article

6. **Commit and push your changes:**
   ```bash
   git add content/news/
   git commit -m "Add news: [your title]"
   git push
   ```

The website will automatically rebuild and deploy via GitHub Actions.