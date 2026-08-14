"""
Auto GitHub Committer — Main Script
Automatically commits and pushes code changes to GitHub.
Supports drip-feed mode for gradually pushing existing projects.

Usage:
    python auto_commit.py              # Normal auto-commit
    python auto_commit.py --dry-run    # Simulate without pushing
    python auto_commit.py --drip       # Run drip-feed for configured projects
    python auto_commit.py --setup      # First-time setup (create repos, init git)
    python auto_commit.py --status     # Show status of all projects
"""

import json
import os
import sys
import subprocess
import random
import time
import math
import shutil
from datetime import datetime, timedelta
from pathlib import Path

# Import local modules
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from secret_scanner import scan_directory, print_findings
from commit_messages import generate_message

# ============================================
# CONFIGURATION
# ============================================

CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")
DRIP_STATE_PATH = os.path.join(SCRIPT_DIR, "drip_state.json")
LOG_DIR = os.path.join(SCRIPT_DIR, "logs")


def load_config():
    """Load configuration from config.json."""
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def get_github_token():
    """Get GitHub PAT from environment variable."""
    config = load_config()
    env_var = config.get("github_token_env_var", "GITHUB_PAT")
    token = os.environ.get(env_var)
    if not token:
        print(f"❌ GitHub token not found in environment variable '{env_var}'")
        print(f"   Run: setx {env_var} \"your_token_here\"")
        print(f"   Then restart your terminal.")
        return None
    return token


def log_message(message, project_name="general"):
    """Log a message to the daily log file."""
    os.makedirs(LOG_DIR, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(LOG_DIR, f"{today}.log")

    timestamp = datetime.now().strftime("%H:%M:%S")
    log_line = f"[{timestamp}] [{project_name}] {message}\n"

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_line)

    print(f"  {message}")


# ============================================
# GIT OPERATIONS
# ============================================

def run_git(args, cwd, token=None):
    """Run a git command and return (success, output)."""
    env = os.environ.copy()
    if token:
        env["GIT_ASKPASS"] = "echo"
        env["GIT_TERMINAL_PROMPT"] = "0"

    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            capture_output=True, text=True,
            timeout=120,
            env=env
        )
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)


def is_git_repo(path):
    """Check if a directory is a git repository."""
    return os.path.exists(os.path.join(path, ".git"))


def init_git_repo(path, branch="main"):
    """Initialize a new git repository."""
    success, out, err = run_git(["init", "-b", branch], cwd=path)
    return success


def has_remote(path):
    """Check if the git repo has a remote 'origin'."""
    success, out, err = run_git(["remote", "get-url", "origin"], cwd=path)
    return success


def set_remote(path, repo_url):
    """Set the remote origin URL."""
    if has_remote(path):
        run_git(["remote", "set-url", "origin", repo_url], cwd=path)
    else:
        run_git(["remote", "add", "origin", repo_url], cwd=path)


def has_changes(path):
    """Check if there are uncommitted changes."""
    success, out, err = run_git(["status", "--porcelain"], cwd=path)
    return bool(out.strip())


def get_untracked_and_modified(path):
    """Get list of all changed/untracked files."""
    success, out, err = run_git(["status", "--porcelain"], cwd=path)
    files = []
    if success and out:
        for line in out.strip().split("\n"):
            if line.strip():
                # Status is first 2 chars, filename starts at position 3
                filepath = line[3:].strip().strip('"')
                files.append(filepath)
    return files


def create_github_repo(repo_name, description="", private=False, token=None):
    """Create a new GitHub repository using the REST API."""
    import urllib.request
    import urllib.error

    url = "https://api.github.com/user/repos"
    data = json.dumps({
        "name": repo_name,
        "description": description,
        "private": private,
        "auto_init": False
    }).encode("utf-8")

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }

    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        return True, result.get("html_url", "")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        if "already exists" in error_body.lower():
            return True, f"https://github.com/{load_config()['github_username']}/{repo_name}"
        return False, f"HTTP {e.code}: {error_body}"
    except Exception as e:
        return False, str(e)


# ============================================
# DRIP FEED SYSTEM
# ============================================

def load_drip_state():
    """Load drip-feed state (which files have been committed for each project)."""
    if os.path.exists(DRIP_STATE_PATH):
        with open(DRIP_STATE_PATH, "r") as f:
            return json.load(f)
    return {}


def save_drip_state(state):
    """Save drip-feed state."""
    with open(DRIP_STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


def get_project_files(project_path):
    """
    Get all untracked and modified files, respecting .gitignore,
    organized into logical groups for drip-feeding.
    """
    all_files = set()
    
    # Get untracked files (respecting .gitignore)
    success1, out1, _ = run_git(["ls-files", "--others", "--exclude-standard"], cwd=project_path)
    if success1 and out1:
        for line in out1.strip().split('\n'):
            if line.strip(): all_files.add(line.strip().strip('"'))
            
    # Get modified tracked files
    success2, out2, _ = run_git(["ls-files", "-m"], cwd=project_path)
    if success2 and out2:
        for line in out2.strip().split('\n'):
            if line.strip(): all_files.add(line.strip().strip('"'))

    return list(all_files)


def create_drip_groups(project_path, project_config):
    """
    Organize project files into logical groups for drip-feeding.
    Each group represents one day's commit.
    """
    all_files = get_project_files(project_path)
    drip_days = project_config.get("drip_days", 10)

    if not all_files:
        return []

    # Categorize files
    categories = {}
    for filepath in all_files:
        parts = filepath.replace("\\", "/").split("/")
        if len(parts) > 1:
            category = parts[0]  # Top-level directory
        else:
            # Root-level files — group by type
            basename = os.path.splitext(parts[0])[0].lower()
            if basename in ('app', 'main', 'index', '__init__'):
                category = "_main_app"
            elif basename in ('readme', 'license', 'requirements', 'setup', 'manifest'):
                category = "_docs_and_setup"
            elif basename in ('config', 'settings', '.gitignore'):
                category = "_config"
            else:
                category = "_other_root"
        categories.setdefault(category, []).append(filepath)

    # Create ordered groups
    groups = []

    # Day 1: Always start with project structure + main app file
    day1 = []
    for cat in ["_config", "_main_app"]:
        if cat in categories:
            day1.extend(categories.pop(cat))
    # Add .gitignore if it exists
    for f in all_files:
        if f.lower() == '.gitignore' and f not in day1:
            day1.append(f)
    if day1:
        groups.append(day1)

    # Last day: Documentation and setup files
    last_day = []
    for cat in ["_docs_and_setup"]:
        if cat in categories:
            last_day.extend(categories.pop(cat))

    # Middle days: Distribute remaining categories
    remaining_categories = list(categories.items())
    # Sort by size for even distribution
    remaining_categories.sort(key=lambda x: len(x[1]), reverse=True)

    if remaining_categories:
        # Calculate how many days we have for the middle
        middle_days = max(1, drip_days - len(groups) - (1 if last_day else 0))

        if len(remaining_categories) <= middle_days:
            # Each category gets its own day
            for cat_name, cat_files in remaining_categories:
                groups.append(cat_files)
        else:
            # Distribute categories across available days
            per_day = math.ceil(len(remaining_categories) / middle_days)
            for i in range(0, len(remaining_categories), per_day):
                batch = remaining_categories[i:i + per_day]
                day_files = []
                for _, files in batch:
                    day_files.extend(files)
                groups.append(day_files)

    # Add root files
    if "_other_root" in categories or any(f for f in all_files if "/" not in f and "\\" not in f):
        root_files = categories.get("_other_root", [])
        if root_files and groups:
            groups[0].extend(root_files)  # Add to first day
        elif root_files:
            groups.append(root_files)

    # Add docs/setup as last day
    if last_day:
        groups.append(last_day)

    return groups


def run_drip_feed(project_config, dry_run=False):
    """Execute one day's drip-feed commit for a project."""
    project_path = project_config["local_path"]
    repo_name = project_config["repo_name"]
    project_name = repo_name

    log_message(f"Starting drip-feed for '{project_name}'", project_name)

    # Load state
    state = load_drip_state()
    project_state = state.get(project_name, {
        "current_day": 0,
        "total_days": 0,
        "completed": False,
        "committed_files": []
    })

    if project_state.get("completed"):
        log_message(f"Drip-feed already completed for '{project_name}'", project_name)
        return True

    
    if project_name == "15-Days-of-Advanced-Deep-Learning":
        from datetime import datetime
        if datetime.now().day == 9:
            log_message("Skipping Day 1 until tomorrow as requested.", project_name)
            return True
            
    # Load the custom drip plan

    try:
        from drip_plan import get_plan
        plan = get_plan(project_name)
    except ImportError:
        # Fallback to auto-generated groups
        plan = None

    if plan:
        total_days = len(plan)
        current_day = project_state["current_day"]

        if current_day == 0:
            project_state["total_days"] = total_days
            total_files = sum(len(files) for _, files in plan)
            log_message(f"Using custom 12-day drip plan ({total_files} total files)", project_name)

        if current_day >= total_days:
            project_state["completed"] = True
            state[project_name] = project_state
            save_drip_state(state)
            log_message(f"Drip-feed complete! All files committed over {total_days} days.", project_name)
            return True

        # Get today's commit message and files
        message, today_files = plan[current_day]
        log_message(f"Day {current_day + 1}/{total_days}: Committing {len(today_files)} files", project_name)
        log_message(f"Message: \"{message}\"", project_name)

    else:
        # Fallback: auto-generated groups
        groups = create_drip_groups(project_path, project_config)
        total_days = len(groups)
        current_day = project_state["current_day"]

        if current_day >= total_days:
            project_state["completed"] = True
            state[project_name] = project_state
            save_drip_state(state)
            log_message(f"Drip-feed complete!", project_name)
            return True

        today_files = groups[current_day]
        message = generate_message(project_path)
        log_message(f"Day {current_day + 1}/{total_days}: Committing {len(today_files)} files", project_name)

    if dry_run:
        for f in today_files:
            log_message(f"  [DRY-RUN] Would add: {f}", project_name)
        log_message(f"  [DRY-RUN] Commit message: \"{message}\"", project_name)
        return True

    # Ensure git repo exists
    if not is_git_repo(project_path):
        init_git_repo(project_path, project_config.get("branch", "main"))
        log_message("Initialized new git repository", project_name)

    # Ensure .gitignore exists in the project
    project_gitignore = os.path.join(project_path, ".gitignore")
    if not os.path.exists(project_gitignore):
        with open(project_gitignore, "w") as f:
            f.write("# Auto-generated .gitignore\n")
            f.write(".env\n.env.*\n*.pem\n*.key\ncredentials.json\nsecrets.json\n")
            f.write("__pycache__/\n*.pyc\n.venv/\nvenv/\n")
            f.write(".idea/\n.vscode/\n")
            f.write("*.zip\n*.exe\n*.db\n*.sqlite\n*.sqlite3\n")
            f.write("Thumbs.db\n.DS_Store\n")
        log_message("Created .gitignore for project", project_name)

    # Add .gitignore first if it's day 1
    if current_day == 0:
        run_git(["add", ".gitignore"], cwd=project_path)

    # Add only today's files
    for filepath in today_files:
        full_path = os.path.join(project_path, filepath)
        if os.path.exists(full_path):
            run_git(["add", filepath], cwd=project_path)
        else:
            log_message(f"  Warning: File not found: {filepath}", project_name)

    # Scan for secrets before committing
    relevant_findings = {}
    for filepath in today_files:
        full_path = os.path.join(project_path, filepath)
        if os.path.exists(full_path):
            from secret_scanner import scan_file
            file_findings = scan_file(full_path)
            if file_findings:
                relevant_findings[full_path] = file_findings

    if relevant_findings:
        log_message("SECRETS DETECTED - Skipping this batch!", project_name)
        print_findings(relevant_findings)
        run_git(["reset", "HEAD"], cwd=project_path)
        return False

    # Commit
    success, out, err = run_git(["commit", "-m", message], cwd=project_path)
    if success:
        log_message(f"Committed: \"{message}\"", project_name)
        project_state["current_day"] = current_day + 1
        project_state["committed_files"].extend(today_files)
    else:
        if "nothing to commit" in (err + out).lower():
            log_message("No changes to commit (files may be gitignored)", project_name)
            project_state["current_day"] = current_day + 1
        else:
            log_message(f"Commit failed: {err}", project_name)
            return False

    # Save state
    state[project_name] = project_state
    save_drip_state(state)

    return True


# ============================================
# NORMAL AUTO-COMMIT
# ============================================

def auto_commit_project(project_config, dry_run=False):
    """Auto-commit changes for a single project."""
    project_path = project_config["local_path"]
    repo_name = project_config["repo_name"]
    branch = project_config.get("branch", "main")
    project_name = repo_name

    log_message(f"Checking '{project_name}' at {project_path}", project_name)

    # Verify path exists
    if not os.path.exists(project_path):
        log_message(f"Path does not exist: {project_path}", project_name)
        return False

    # Check if git repo, init if not
    if not is_git_repo(project_path):
        if dry_run:
            log_message("[DRY-RUN] Would initialize git repo", project_name)
        else:
            init_git_repo(project_path, branch)
            log_message("Initialized git repository", project_name)

    # Check for changes
    if not has_changes(project_path):
        log_message("No changes detected — skipping", project_name)
        return True

    if dry_run:
        files = get_untracked_and_modified(project_path)
        log_message(f"[DRY-RUN] {len(files)} files changed:", project_name)
        for f in files[:10]:
            log_message(f"  [DRY-RUN]   {f}", project_name)
        if len(files) > 10:
            log_message(f"  [DRY-RUN]   ... and {len(files)-10} more", project_name)
        return True

    # Stage all changes
    run_git(["add", "-A"], cwd=project_path)

    # Scan for secrets
    findings, is_safe = {}, True
    try:
        from secret_scanner import scan_staged_files
        findings, is_safe = scan_staged_files(project_path)
    except Exception:
        findings = scan_directory(project_path)
        is_safe = len(findings) == 0

    if not is_safe:
        log_message("SECRETS DETECTED — COMMIT BLOCKED!", project_name)
        print_findings(findings)
        run_git(["reset", "HEAD"], cwd=project_path)
        return False

    # Generate commit message
    message = generate_message(project_path)

    # Commit
    success, out, err = run_git(["commit", "-m", message], cwd=project_path)
    if success:
        log_message(f"Committed: \"{message}\"", project_name)
    else:
        if "nothing to commit" in (out + err).lower():
            log_message("No changes to commit", project_name)
            return True
        log_message(f"Commit failed: {err}", project_name)
        return False

    return True


def push_project(project_config, dry_run=False):
    """Push committed changes to GitHub."""
    config = load_config()
    token = get_github_token()
    if not token and not dry_run:
        return False

    project_path = project_config["local_path"]
    repo_name = project_config["repo_name"]
    branch = project_config.get("branch", "main")
    username = config["github_username"]
    project_name = repo_name

    if dry_run:
        log_message(f"[DRY-RUN] Would push to github.com/{username}/{repo_name}", project_name)
        return True

    # Set remote URL with token
    remote_url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"
    set_remote(project_path, remote_url)

    # Configure git user to ensure contributions count
    run_git(["config", "user.email", "gantishivakeerth@gmail.com"], cwd=project_path)
    run_git(["config", "user.name", "Ganti Shiva Keerth"], cwd=project_path)

    # Push
    success, out, err = run_git(["push", "-u", "origin", branch], cwd=project_path)
    if success:
        # Remove token from remote URL for security
        safe_url = f"https://github.com/{username}/{repo_name}.git"
        set_remote(project_path, safe_url)
        log_message(f"Pushed to github.com/{username}/{repo_name}", project_name)
        return True
    else:
        # Remove token from remote URL even on failure
        safe_url = f"https://github.com/{username}/{repo_name}.git"
        set_remote(project_path, safe_url)
        log_message(f"Push failed: {err}", project_name)
        return False


# ============================================
# SETUP COMMAND
# ============================================

def setup_projects():
    """First-time setup: create repos, init git, set remotes."""
    config = load_config()
    token = get_github_token()
    if not token:
        return

    username = config["github_username"]

    print("\nSETUP MODE")
    print("=" * 50)

    for project in config["projects"]:
        if not project.get("enabled", True):
            continue

        project_path = project["local_path"]
        repo_name = project["repo_name"]
        description = project.get("description", "")
        private = project.get("private", False)

        print(f"\nSetting up: {repo_name}")
        print(f"   Path: {project_path}")

        # Check if path exists
        if not os.path.exists(project_path):
            print(f"   Path does not exist: {project_path}")
            continue

        # Initialize git repo
        if not is_git_repo(project_path):
            init_git_repo(project_path, project.get("branch", "main"))
            print(f"   Initialized git repository")
        else:
            print(f"   Git repository already exists")

        # Create GitHub repo
        print(f"   Creating GitHub repo: {repo_name} ({'private' if private else 'public'})")
        success, url = create_github_repo(repo_name, description, private, token)
        if success:
            print(f"   GitHub repo ready: {url}")
        else:
            print(f"   Failed to create repo: {url}")
            continue

        # Set remote
        remote_url = f"https://github.com/{username}/{repo_name}.git"
        set_remote(project_path, remote_url)
        print(f"   Remote set to: {remote_url}")

        # Configure git user
        run_git(["config", "user.email", f"{username}@users.noreply.github.com"], cwd=project_path)
        run_git(["config", "user.name", username], cwd=project_path)
        print(f"   Git user configured")

    print("\nSetup complete! Run 'python auto_commit.py --drip' to start drip-feeding.")


# ============================================
# STATUS COMMAND
# ============================================

def show_status():
    """Show the status of all configured projects."""
    config = load_config()
    drip_state = load_drip_state()

    print("\n📊 PROJECT STATUS")
    print("=" * 60)

    for project in config["projects"]:
        repo_name = project["repo_name"]
        enabled = project.get("enabled", True)
        drip = project.get("drip_feed", False)
        path = project["local_path"]
        exists = os.path.exists(path)
        is_repo = is_git_repo(path) if exists else False
        changes = has_changes(path) if is_repo else False

        print(f"\n📁 {repo_name}")
        print(f"   Path:     {path}")
        print(f"   Exists:   {'Yes' if exists else 'No'}")
        print(f"   Git repo: {'Yes' if is_repo else 'No'}")
        print(f"   Enabled:  {'Yes' if enabled else 'No'}")
        print(f"   Changes:  {'📝 Yes' if changes else 'Clean'}")

        if drip:
            state = drip_state.get(repo_name, {})
            current = state.get("current_day", 0)
            total = state.get("total_days", "?")
            completed = state.get("completed", False)
            committed = len(state.get("committed_files", []))
            if completed:
                print(f"   Drip:     Complete ({total} days, {committed} files)")
            else:
                print(f"   Drip:     📅 Day {current}/{total} ({committed} files committed)")


# ============================================
# MAIN
# ============================================

def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    drip_mode = "--drip" in args
    setup_mode = "--setup" in args
    status_mode = "--status" in args
    no_delay = "--no-delay" in args  # Skip delay for manual runs

    if dry_run:
        print("🧪 DRY-RUN MODE — No changes will be made\n")

    if setup_mode:
        setup_projects()
        return

    if status_mode:
        show_status()
        return

    # ── Random Delay ──────────────────────────────────────────────
    # When run by Task Scheduler (9:30 PM), wait a random 0-150 minutes
    # so the actual commit happens somewhere between 9:30 PM and ~12:00 AM
    # This makes commit times look natural and human-like
    # Use --no-delay flag to skip (for manual runs)
    if not dry_run and not no_delay:
        delay_minutes = random.randint(0, 15)
        delay_seconds = delay_minutes * 60
        commit_time = datetime.now() + timedelta(minutes=delay_minutes)
        log_message(f"Random delay: {delay_minutes} minutes (commit at ~{commit_time.strftime('%I:%M %p')})")
        print(f"\n  Waiting {delay_minutes} minutes before committing...")
        print(f"  Estimated commit time: {commit_time.strftime('%I:%M %p')}")
        time.sleep(delay_seconds)

    config = load_config()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message(f"Auto-commit started at {timestamp}")

    success_count = 0
    fail_count = 0

    for project in config["projects"]:
        if not project.get("enabled", True):
            continue

        repo_name = project["repo_name"]
        is_drip = project.get("drip_feed", False)

        print(f"\n{'='*50}")
        print(f"Project: {repo_name}")
        print(f"{'='*50}")

        try:
            if drip_mode and is_drip:
                # Drip-feed mode
                result = run_drip_feed(project, dry_run)
            elif not drip_mode and not is_drip:
                # Normal auto-commit mode (for non-drip projects)
                result = auto_commit_project(project, dry_run)
            elif not drip_mode and is_drip:
                # Drip projects also get normal commits after drip is done
                state = load_drip_state()
                if state.get(repo_name, {}).get("completed", False):
                    result = auto_commit_project(project, dry_run)
                else:
                    log_message("Drip-feed in progress — run with --drip flag", repo_name)
                    continue
            else:
                continue

            if result and not dry_run:
                push_result = push_project(project, dry_run)
                if push_result:
                    success_count += 1
                else:
                    fail_count += 1
            elif result:
                success_count += 1
            else:
                fail_count += 1

        except Exception as e:
            log_message(f"Error: {str(e)}", repo_name)
            fail_count += 1

    print(f"\n{'='*50}")
    print(f"Results: {success_count} succeeded, {fail_count} failed")
    print(f"{'='*50}")

    log_message(f"Auto-commit finished: {success_count} succeeded, {fail_count} failed")


if __name__ == "__main__":
    main()
