# IsPri UNSW Website

[![Deploy Hugo site to Pages](https://github.com/IsPri-UNSW/new_page/actions/workflows/hugo.yml/badge.svg)](https://github.com/IsPri-UNSW/new_page/actions/workflows/hugo.yml)
[![Update ORCID Data](https://github.com/IsPri-UNSW/new_page/actions/workflows/update_orcid.yml/badge.svg)](https://github.com/IsPri-UNSW/new_page/actions/workflows/update_orcid.yml)
[![Protect Theme Directory](https://github.com/IsPri-UNSW/new_page/actions/workflows/check-theme-protection.yml/badge.svg)](https://github.com/IsPri-UNSW/new_page/actions/workflows/check-theme-protection.yml)

A Hugo site for The Information Security and Privacy Research Group at UNSW.

## Table of Contents 📑

- [Table of Contents 📑](#table-of-contents-)
- [Adding News 📰](#adding-news-)
- [Adding Team Members 👥](#adding-team-members-)
- [Administrator \& Developer Information 🛠️](#administrator--developer-information-️)


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

## Adding Team Members 👥

To add a new team member to the website, follow these steps:

1. **Copy the template directory:**
   ```bash
   cp -r templates/authors/sample content/authors/f-lastname
   ```
   Replace `f-lastname` with the first letter of the first name and the full last name (e.g., `j-doe` for John Doe).
   
   Note, that due to limitations of the theme, we do not support more than one last name. Please use the last name shown in publications as your last name and everything else as first name(s).
   For example, if your name is "Anna Smith Johnson" (and you publish under this name), with your last name being "Smith Johnson", please use "a-johnson" as the directory name and "Anna Smith" as the first name in the `_index.md` file, i.e., use your first lastname as your middle name. 
   Currently, this is the only way to ensure that publications are correctly linked to the author profile.

2. **Edit the `_index.md` file** in your new directory (`content/authors/f-lastname/_index.md`):
   - Update all personal information (name, title, role, interests, education, etc.)
   - Set the `slug` field to match the directory name (e.g., `j-doe`)
   - Choose the appropriate `user_groups`:
     - `Academics` (faculty members)
     - `Postdoctoral Researchers`
     - `Graduate Students` (PhD and MPhil students)
     - `Administration`
     - `Visitors`
     - `Alumni` (former members)
   - Add social media links and ORCID if available

3. **Add a profile photo:**
   - Name the file `avatar.jpg`
   - Use a **1:1 aspect ratio** (square format)
   - Place it in the same directory as `_index.md`

4. **Commit and push your changes:**
   ```bash
   git add content/authors/f-lastname/
   git commit -m "Add team member: [Full Name]"
   git push
   ```

**Important naming convention:**
- Directory name format: `firstletter-lastname` (e.g., `j-doe`, `e-buchholz`)
- The `slug` field in `_index.md` must match the directory name
- Profile photo must be named `avatar.jpg` with 1:1 aspect ratio

## Administrator & Developer Information 🛠️

Built on the [Hugo Research Group Template](https://github.com/HugoBlox/theme-research-group)

Theme location: `themes/blox-bootstrap/` (local copy)

Original remote theme location: `~/Library/Caches/hugo_cache/modules/filecache/modules/pkg/mod/github.com/!hugo!blox/hugo-blox-builder/modules/blox-bootstrap/v5@v5.9.8-0.20241012174104-661cadc17327/`

**Never make any changes to the files in the `themes/blox-bootstrap/` folder directly!**
We should probably go back to using the remote module at some point.
However, for now, it is easier to have the local copy as a point of reference for customisation.