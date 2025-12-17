# imports
import os
import re
import yaml
import shutil
import argparse
from paths import AUTHORS_DIR, FILTERED_PUBLICATIONS_DIR, PUBLICATIONS_DIR, FILTERED_PUBLICATIONS_YAML

# Roles to recognise (case-insensitive match)
student_roles = ['phd candidate', 'student', 'alumni', 'alumnus', 'alumna', 'mphil', 'master', 'research associate']
student_groups = ['Graduate Students', 'Visitors', 'Postdoctoral Researchers', 'Students']
supervisor_roles = ['professor', 'associate professor', 'assistant professor', 'senior lecturer', 'lecturer', 'supervisor']
supervisor_groups = ['Academics']


def load_yaml_front_matter(path):
    """Return parsed YAML front matter from a file, or None if not found/parsable."""
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Detect YAML front matter delimited by '---'
    if text.lstrip().startswith('---'):
        parts = text.split('---')
        if len(parts) >= 3:
            fm = parts[1]
            try:
                return yaml.safe_load(fm) or {}
            except yaml.YAMLError:
                return None

    # Fallback: attempt to parse whole file as YAML (for .yaml files)
    try:
        return yaml.safe_load(text) or {}
    except yaml.YAMLError:
        return None


def normalize_name(name):
    if not name:
        return ''
    # normalize spacing and lowercase for robust matching
    return re.sub(r"\s+"," ", name.strip()).lower()


def name_to_slug(name):
    """Convert a full name to a slug (first-initial + last-name).
    Example: 'Salil S. Kanhere' -> 's-kanhere'
    Example: "Nicholas D'Silva" -> 'n-dsilva'
    """
    if not name:
        return ''
    name = name.strip()
    parts = name.split()
    if len(parts) < 1:
        return ''
    
    # Get first initial
    first_initial = parts[0][0].lower() if parts[0] else ''
    
    # Get last name and clean it
    last_name = parts[-1].lower()
    # Remove apostrophes and special characters
    last_name = last_name.replace("'", "").replace("'", "").replace("`", "")
    
    if first_initial and last_name:
        return f"{first_initial}-{last_name}"
    return ''


def parse_authors_field(value):
    """Return a list of author slugs from common field types.
    Converts full names like 'Erik Buchholz' to slugs like 'e-buchholz'.
    """
    if not value:
        return []
    if isinstance(value, list):
        return [name_to_slug(v) for v in value if v and name_to_slug(v)]
    if isinstance(value, str):
        # common separators: ' and ', ',', ';'
        if ' and ' in value:
            parts = [p.strip() for p in value.split(' and ') if p.strip()]
        elif ',' in value:
            parts = [p.strip() for p in value.split(',') if p.strip()]
        else:
            parts = [value.strip()]
        return [name_to_slug(p) for p in parts if name_to_slug(p)]
    return []


def is_student(role, user_groups):
    # Check role
    if role:
        r = str(role).lower()
        if any(s in r for s in student_roles):
            return True
    
    # Check user_groups
    if user_groups:
        if isinstance(user_groups, str):
            user_groups = [user_groups]
        if isinstance(user_groups, list):
            for group in user_groups:
                if group and any(sg.lower() in str(group).lower() for sg in student_groups):
                    return True
    
    return False


def is_supervisor(role, user_groups):
    # Check role
    if role:
        r = str(role).lower()
        if any(s in r for s in supervisor_roles):
            return True
    
    # Check user_groups
    if user_groups:
        if isinstance(user_groups, str):
            user_groups = [user_groups]
        if isinstance(user_groups, list):
            for group in user_groups:
                if group and any(sg.lower() in str(group).lower() for sg in supervisor_groups):
                    return True
    
    return False


def collect_author_sets():
    """Scan `content/authors/` and return two sets: supervisors, students_alumni (normalized names)."""
    supervisors = set()
    students_alumni = set()

    # Walk authors directory recursively to support per-author folders
    for root, dirs, files in os.walk(AUTHORS_DIR):
        for fname in files:
            if not (fname.endswith('.yaml') or fname.endswith('.yml') or fname.endswith('.md')):
                continue
            path = os.path.join(root, fname)
            data = load_yaml_front_matter(path)
            if not data:
                continue
            # YAML front matter sometimes parses to a list; pick the first mapping if so
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        data = item
                        break
                else:
                    continue

            # Prefer explicit first_name + last_name if present
            first = data.get('first_name') or data.get('given_name')
            last = data.get('last_name') or data.get('family_name')
            if first and last:
                display_name = f"{first} {last}"
            else:
                # fallback to title, name, or the folder name
                display_name = data.get('title') or data.get('name') or os.path.basename(root)

            # Generate slug from full name and also use folder slug as fallback
            slug_from_name = name_to_slug(display_name)
            folder_slug = normalize_name(os.path.basename(root))

            role = data.get('role') or data.get('position') or ''
            user_groups = data.get('user_groups') or data.get('groups') or []
            if is_supervisor(role, user_groups):
                if slug_from_name:
                    supervisors.add(slug_from_name)
                if folder_slug:
                    supervisors.add(folder_slug)
            else:
                # Default to student
                if slug_from_name:
                    students_alumni.add(slug_from_name)
                if folder_slug:
                    students_alumni.add(folder_slug)

    return supervisors, students_alumni


def filter_publications(supervisors, students_alumni, mode='loose'):
    """Return list of publication metadata dicts filtered by `mode`.

    Modes:
      - 'strict': keep publications that have at least one supervisor AND at least one student/alumni
      - 'loose' : keep publications that have at least one supervisor (regardless of other coauthors)
    """
    results = []
    # Walk the publications directory recursively to find files inside unique subfolders
    for root, dirs, files in os.walk(PUBLICATIONS_DIR):
        for fname in files:
            if not (fname.endswith('.yaml') or fname.endswith('.yml') or fname.endswith('.md')):
                continue
            path = os.path.join(root, fname)
            data = load_yaml_front_matter(path)
            if not data:
                continue
            # YAML front matter sometimes parses to a list; pick the first mapping if so
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        data = item
                        break
                else:
                    continue

            authors_field = data.get('authors') or data.get('author') or data.get('creator')
            author_slugs = set(parse_authors_field(authors_field))

            # match by slug membership
            has_supervisor = bool(author_slugs & supervisors)
            has_student = bool(author_slugs & students_alumni)

            # Include publication based on selected mode.
            if mode == 'strict':
                # require both supervisor and student/alumni
                keep = has_supervisor and has_student
            elif mode == 'loose':
                # any publication with at least one supervisor
                keep = has_supervisor
            else:
                # unknown mode: default to strict
                keep = has_supervisor and has_student

            if keep:
                relpath = os.path.relpath(path, PUBLICATIONS_DIR)
                results.append({
                    'file': relpath,
                    'title': data.get('title'),
                    'authors': list(author_slugs),
                    'date': data.get('date')
                })

    return results


def main():
    supervisors, students_alumni = collect_author_sets()
    print(f"Found supervisors: {supervisors}")
    print(f"Found students/alumni: {students_alumni}")

    # parse CLI args
    parser = argparse.ArgumentParser(description='Filter publications by supervisor/student roles')
    parser.add_argument('--mode', choices=['strict', 'loose'], default='loose',
                        help='Filtering mode: strict or loose (default)')
    parser.add_argument('--dest', default=str(FILTERED_PUBLICATIONS_DIR), help='Destination folder for copied publication md files')
    args, extra = parser.parse_known_args()

    mode = args.mode
    dest_root = args.dest

    filtered = filter_publications(supervisors, students_alumni, mode=mode)
    print(f"Mode={mode}. Filtered {len(filtered)} publications (matching condition).")

    # Save metadata YAML – obsoleted in favor of directories
    # os.makedirs(os.path.dirname(FILTERED_PUBLICATIONS_YAML), exist_ok=True)
    # with open(FILTERED_PUBLICATIONS_YAML, 'w', encoding='utf-8') as out:
    #     yaml.safe_dump(filtered, out, sort_keys=False, allow_unicode=True)

    # Also copy matched publication markdown files into the destination root
    filtered_pub_root = dest_root
    for entry in filtered:
        rel = entry.get('file')
        if not rel:
            continue
        src = os.path.join(PUBLICATIONS_DIR, rel)
        # Determine publication folder name (use first path component)
        parts = rel.split(os.sep)
        pub_folder = parts[0] if parts else os.path.splitext(os.path.basename(rel))[0]
        dest_dir = os.path.join(filtered_pub_root, pub_folder)
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, os.path.basename(rel))
        try:
            shutil.copyfile(src, dest_path)
            print(f"Copied {src} -> {dest_path}")
        except Exception as e:
            print(f"Failed to copy {src} -> {dest_path}: {e}")

    # print(f"Saved filtered publications to {FILTERED_PUBLICATIONS_YAML} and copied markdown files to {filtered_pub_root}")
    print(f"Saved filtered publications by copying markdown files to {filtered_pub_root}")


if __name__ == '__main__':
    main()