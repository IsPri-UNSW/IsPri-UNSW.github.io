#!/usr/bin/env python3
"""
Script to add a new team member to the website.

Prompts for the user's name, computes the correct slug,
creates the author directory, and generates a template _index.md file.

Usage:
    python scripts/add_user.py
"""

import sys
import shutil

from paths import AUTHORS_DIR, ROOT_PATH

TEMPLATE_DIR = ROOT_PATH / "templates" / "authors" / "sample"


def compute_slug(first_name: str, last_name: str) -> str:
    """
    Compute the author slug from first and last name.

    Convention: first letter of first name + '-' + full last name, all lowercase.
    Spaces and special characters are stripped from the last name.

    :param first_name: The author's first name(s)
    :param last_name: The author's last name (single word)
    :returns: The slug string, e.g. 'j-doe'
    """
    first_initial = first_name.strip()[0].lower()
    cleaned_last = last_name.strip().lower().replace(" ", "")
    return f"{first_initial}-{cleaned_last}"


def choose_user_group() -> str:
    """
    Let the user pick a user group interactively.

    :returns: The selected user group string
    """
    groups = [
        "Academics",
        "Postdoctoral Researchers",
        "Graduate Students",
        "Students",
        "Administration",
        "Visitors",
        "Alumni",
    ]
    print("\nAvailable user groups:")
    for i, group in enumerate(groups, 1):
        print(f"  {i}. {group}")
    while True:
        choice = input("\nSelect a user group [1-7]: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(groups):
            return groups[int(choice) - 1]
        print("Invalid selection. Please enter a number between 1 and 7.")


def generate_index_md(
    first_name: str,
    last_name: str,
    slug: str,
    user_group: str,
) -> str:
    """
    Generate the content of the _index.md file for a new author.

    :param first_name: The author's first name(s)
    :param last_name: The author's last name
    :param slug: The computed slug
    :param user_group: The organisational group
    :returns: The _index.md content as a string
    """
    title = f"{first_name} {last_name}"
    return f"""---
# Display name (This should be your full name)
title: {title}

# Slug: Use the first letter of your firstname - lastname
slug: {slug}

# Full Name (for SEO)
# If your lastname consists of multiple parts, please only use the last part as your lastname, even if that's not correct.
# This is a limitation of the template.
# For example, if your firstname is "John" and your last name "Wang Doe", please use "John Wang" as firstname and "Doe" as lastname.
first_name: {first_name}
last_name: {last_name}

# Don't touch this unless you know what you're doing
superuser: false

# Role/position
role: ""

# Organizations/Affiliations
organizations:
  - name: University of New South Wales
    url: ''

# Short bio (displayed in user profile at end of posts)
# bio: A brief bio about your research interests and background
# This is optional – comment if not used.

interests:
  - Interest 1
  - Interest 2

education:
  courses:
    - course: Degree in Subject
      institution: University Name, Country
      year: 2024

# ORCID ID for automated publication fetching (REQUIRED! Create one if you don't have one!)
orcid: 0000-0000-0000-0000

# Social/Academic Networking
# Please comment out any links you do not wish to display.
social:
  # - icon: home
  #   icon_pack: fa
  #   link: https://example.com/
  - icon: envelope
    icon_pack: fas
    link: 'mailto:{slug.replace("-", ".")}@unsw.edu.au'
  # - icon: google-scholar
  #   icon_pack: fab
  #   link: https://scholar.google.com/
  # - icon: orcid
  #   icon_pack: fab
  #   link: https://orcid.org/0000-0000-0000-0000
  # - icon: github
  #   icon_pack: fab
  #   link: https://github.com/
  # - icon: linkedin
  #   icon_pack: fab
  #   link: https://www.linkedin.com/in/
  # - icon: researchgate
  #   icon_pack: fab
  #   link: https://www.researchgate.net/profile/

# Ignore this!
email: ''

# Highlight the author in author lists? (true/false)
highlight_name: true

# Organizational groups that you belong to (for People widget)
#   Set this to `[]` or comment out if you are not using People widget.
# Available user_groups:
#   - Academics (faculty members)
#   - Postdoctoral Researchers
#   - Graduate Students (PhD and MPhil students)
#   - Students (coursework students)
#   - Administration
#   - Visitors
#   - Alumni (former members)
user_groups:
  - {user_group}
---
"""


def main():
    print("=" * 50)
    print("  Add New Team Member")
    print("=" * 50)

    # --- Collect input ---
    first_name = input("\nFirst name(s) (e.g. 'John' or 'Anna Marie'): ").strip()
    if not first_name:
        print("Error: First name cannot be empty.")
        sys.exit(1)

    last_name = input("Last name (single word, e.g. 'Doe'): ").strip()
    if not last_name:
        print("Error: Last name cannot be empty.")
        sys.exit(1)

    slug = compute_slug(first_name, last_name)
    user_group = choose_user_group()

    # --- Preview ---
    author_dir = AUTHORS_DIR / slug

    print("\n" + "-" * 50)
    print(f"  Name:       {first_name} {last_name}")
    print(f"  Slug:       {slug}")
    print(f"  Group:      {user_group}")
    print(f"  Directory:  {author_dir.relative_to(ROOT_PATH)}")
    print("-" * 50)

    confirm = input("\nCreate this author profile? [Y/n]: ").strip().lower()
    if confirm not in ("", "y", "yes"):
        print("Aborted.")
        sys.exit(0)

    # --- Create directory and file ---
    if author_dir.exists():
        print(f"Error: Directory '{author_dir.relative_to(ROOT_PATH)}' already exists.")
        sys.exit(1)

    author_dir.mkdir(parents=True)

    index_md = author_dir / "_index.md"
    index_md.write_text(generate_index_md(first_name, last_name, slug, user_group))

    # Copy template avatar if available
    template_avatar = TEMPLATE_DIR / "avatar.jpg"
    if template_avatar.exists():
        shutil.copy2(template_avatar, author_dir / "avatar.jpg")
        print(f"  Copied template avatar.jpg (replace with actual photo)")

    print(f"\nCreated author profile at: {author_dir.relative_to(ROOT_PATH)}/")
    print(f"  - _index.md")
    print(f"\nNext steps:")
    print(f"  1. Edit {author_dir.relative_to(ROOT_PATH)}/_index.md to fill in details")
    print(f"  2. Replace avatar.jpg with a real photo (1:1 aspect ratio)")
    print(f"  3. Commit and push:")
    print(f"       git add {author_dir.relative_to(ROOT_PATH)}/")
    print(f'       git commit -m "Add team member: {first_name} {last_name}"')
    print(f"       git push")


if __name__ == "__main__":
    main()
