"""
Commit Message Generator — Creates natural-looking commit messages
based on which files were changed, added, or deleted.
"""

import os
import random
import subprocess


# Action verbs that sound natural
VERBS_MODIFY = ["Update", "Improve", "Refactor", "Enhance", "Optimize", "Polish", "Fix"]
VERBS_ADD = ["Add", "Implement", "Create", "Introduce", "Build"]
VERBS_DELETE = ["Remove", "Clean up", "Delete unused"]

# Module name to friendly description mappings
MODULE_DESCRIPTIONS = {
    "auth": "authentication module",
    "login": "login system",
    "ui_candidate": "candidate dashboard UI",
    "ui_employer": "employer portal UI",
    "ui_admin": "admin panel UI",
    "ai_matcher": "AI matching algorithm",
    "category_detector": "category detection system",
    "market_predictor": "market prediction engine",
    "interview_prep": "interview preparation module",
    "employer_analytics": "employer analytics dashboard",
    "config": "configuration settings",
    "app": "main application",
    "models": "data models",
    "utils": "utility functions",
    "database": "database layer",
    "api": "API endpoints",
    "tests": "test suite",
    "requirements": "project dependencies",
    "readme": "documentation",
    "setup": "project setup",
}

# File extension to category mappings
EXTENSION_CATEGORIES = {
    ".py": "Python",
    ".js": "JavaScript",
    ".html": "HTML",
    ".css": "CSS",
    ".json": "configuration",
    ".yml": "configuration",
    ".yaml": "configuration",
    ".md": "documentation",
    ".txt": "documentation",
    ".csv": "data",
    ".sql": "database",
    ".sh": "scripts",
    ".bat": "scripts",
    ".ps1": "scripts",
}


def get_changed_files(repo_path):
    """Get lists of modified, added, and deleted files."""
    modified, added, deleted = [], [], []

    try:
        # Get status of staged files
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-status"],
            cwd=repo_path,
            capture_output=True, text=True, timeout=30
        )

        for line in result.stdout.strip().split("\n"):
            if not line.strip():
                continue
            parts = line.strip().split("\t")
            if len(parts) >= 2:
                status, filepath = parts[0], parts[-1]
                if status.startswith("M"):
                    modified.append(filepath)
                elif status.startswith("A"):
                    added.append(filepath)
                elif status.startswith("D"):
                    deleted.append(filepath)

        # If no staged changes, check unstaged
        if not modified and not added and not deleted:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=repo_path,
                capture_output=True, text=True, timeout=30
            )
            for line in result.stdout.strip().split("\n"):
                if not line.strip():
                    continue
                status = line[:2].strip()
                filepath = line[3:].strip()
                if status in ("M", "MM"):
                    modified.append(filepath)
                elif status in ("A", "??"):
                    added.append(filepath)
                elif status == "D":
                    deleted.append(filepath)

    except Exception:
        pass

    return modified, added, deleted


def _get_module_name(filepath):
    """Extract a friendly module name from a filepath."""
    basename = os.path.splitext(os.path.basename(filepath))[0].lower()

    # Check direct matches
    if basename in MODULE_DESCRIPTIONS:
        return MODULE_DESCRIPTIONS[basename]

    # Check partial matches
    for key, desc in MODULE_DESCRIPTIONS.items():
        if key in basename:
            return desc

    # Fall back to cleaned-up filename
    name = basename.replace("_", " ").replace("-", " ")
    return name


def _get_file_category(filepath):
    """Get the category based on file extension."""
    _, ext = os.path.splitext(filepath)
    return EXTENSION_CATEGORIES.get(ext.lower(), "files")


def generate_message(repo_path):
    """
    Generate a natural commit message based on the changed files.
    Returns a string commit message.
    """
    modified, added, deleted = get_changed_files(repo_path)

    if not modified and not added and not deleted:
        return "Update project files"

    parts = []

    # Handle added files
    if added:
        if len(added) <= 3:
            modules = list(set([_get_module_name(f) for f in added]))
            verb = random.choice(VERBS_ADD)
            if len(modules) == 1:
                parts.append(f"{verb} {modules[0]}")
            elif len(modules) == 2:
                parts.append(f"{verb} {modules[0]} and {modules[1]}")
            else:
                parts.append(f"{verb} {modules[0]} and {len(modules)-1} more modules")
        else:
            parts.append(f"Add {len(added)} new files")

    # Handle modified files
    if modified:
        if len(modified) <= 3:
            modules = list(set([_get_module_name(f) for f in modified]))
            verb = random.choice(VERBS_MODIFY)
            if len(modules) == 1:
                parts.append(f"{verb} {modules[0]}")
            elif len(modules) == 2:
                parts.append(f"{verb} {modules[0]} and {modules[1]}")
            else:
                parts.append(f"{verb} {modules[0]} and {len(modules)-1} more modules")
        else:
            verb = random.choice(VERBS_MODIFY)
            category = _get_file_category(modified[0])
            parts.append(f"{verb} {len(modified)} {category} files")

    # Handle deleted files
    if deleted:
        verb = random.choice(VERBS_DELETE)
        if len(deleted) <= 2:
            modules = [_get_module_name(f) for f in deleted]
            parts.append(f"{verb} {', '.join(modules)}")
        else:
            parts.append(f"{verb} {len(deleted)} files")

    # Combine parts
    if len(parts) == 1:
        message = parts[0]
    elif len(parts) == 2:
        message = f"{parts[0]} and {parts[1].lower()}"
    else:
        message = ", ".join(parts[:-1]) + f", and {parts[-1].lower()}"

    # Ensure first letter is capitalized and length is reasonable
    message = message[0].upper() + message[1:]
    if len(message) > 72:
        message = message[:69] + "..."

    return message


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    msg = generate_message(target)
    print(f"📝 Generated commit message: \"{msg}\"")
