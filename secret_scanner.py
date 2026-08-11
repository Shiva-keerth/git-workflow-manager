"""
Secret Scanner — Scans files for API keys, passwords, and sensitive data.
Prevents accidental exposure of secrets in Git commits.
"""

import re
import os

# Dangerous patterns that indicate secrets/credentials
SECRET_PATTERNS = {
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "AWS Secret Key": r"(?i)aws[_\s]*secret[_\s]*access[_\s]*key.{0,20}['\"][0-9a-zA-Z/+]{40}['\"]",
    "OpenAI API Key": r"sk-[a-zA-Z0-9]{20,}",
    "GitHub Token": r"ghp_[a-zA-Z0-9]{36}",
    "GitHub OAuth": r"gho_[a-zA-Z0-9]{36}",
    "Google API Key": r"AIza[0-9A-Za-z\-_]{35}",
    "Stripe Live Key": r"sk_live_[a-zA-Z0-9]{24,}",
    "Stripe Test Key": r"sk_test_[a-zA-Z0-9]{24,}",
    "Private Key Block": r"-----BEGIN\s*(RSA|DSA|EC|OPENSSH|PGP)?\s*PRIVATE KEY-----",
    "MongoDB URI": r"mongodb(\+srv)?://[^\s]+",
    "PostgreSQL URI": r"postgres(ql)?://[^\s]*:[^\s]*@",
    "MySQL URI": r"mysql://[^\s]*:[^\s]*@",
    "Generic Password": r"(?i)(password|passwd|pwd)\s*[=:]\s*['\"][^'\"]{8,}['\"]",
    "Generic Secret": r"(?i)(secret|token|api_key|apikey)\s*[=:]\s*['\"][^'\"]{8,}['\"]",
    "Slack Token": r"xox[baprs]-[0-9a-zA-Z]{10,}",
    "Telegram Bot Token": r"[0-9]+:AA[0-9A-Za-z\-_]{33}",
    "Groq API Key": r"gsk_[a-zA-Z0-9]{20,}",
    "Hugging Face Token": r"hf_[a-zA-Z0-9]{20,}",
}

# File extensions that should NEVER be committed
DANGEROUS_EXTENSIONS = {
    ".env", ".pem", ".key", ".p12", ".pfx", ".jks",
    ".secret", ".credentials", ".keystore"
}

# Filenames that should NEVER be committed
DANGEROUS_FILENAMES = {
    ".env", ".env.local", ".env.production", ".env.development",
    "credentials.json", "secrets.json", "service-account.json",
    "token.json", "auth.json", ".htpasswd", "id_rsa", "id_ed25519"
}

# Maximum file size to scan (skip large files)
MAX_SCAN_SIZE_BYTES = 1_000_000  # 1 MB


def scan_file(filepath):
    """
    Scan a single file for secret patterns.
    Returns a list of (pattern_name, line_number, matched_text) tuples.
    """
    findings = []

    # Check filename
    basename = os.path.basename(filepath).lower()
    if basename in DANGEROUS_FILENAMES:
        findings.append(("Dangerous Filename", 0, f"File '{basename}' should never be committed"))
        return findings

    # Check extension
    _, ext = os.path.splitext(filepath)
    if ext.lower() in DANGEROUS_EXTENSIONS:
        findings.append(("Dangerous Extension", 0, f"File with extension '{ext}' should never be committed"))
        return findings

    # Skip binary/large files
    try:
        file_size = os.path.getsize(filepath)
        if file_size > MAX_SCAN_SIZE_BYTES:
            return findings  # Skip large files silently

        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line_num, line in enumerate(f, 1):
                for pattern_name, pattern in SECRET_PATTERNS.items():
                    if re.search(pattern, line):
                        # Mask the actual secret for logging
                        masked = line.strip()[:80] + "..." if len(line.strip()) > 80 else line.strip()
                        findings.append((pattern_name, line_num, masked))
    except (IOError, OSError):
        pass  # Skip files we can't read

    return findings


def scan_directory(directory, gitignore_patterns=None):
    """
    Scan all files in a directory for secrets.
    Returns a dict of {filepath: [(pattern_name, line_number, matched_text), ...]}
    """
    all_findings = {}

    for root, dirs, files in os.walk(directory):
        # Skip hidden directories and common non-code directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in
                   {'node_modules', '__pycache__', 'venv', '.venv', '.git',
                    '.idea', '.vscode', 'dist', 'build', 'eggs'}]

        for filename in files:
            filepath = os.path.join(root, filename)
            findings = scan_file(filepath)
            if findings:
                all_findings[filepath] = findings

    return all_findings


def scan_staged_files(repo_path):
    """
    Scan only git-staged files for secrets.
    Returns findings dict and a boolean indicating if it's safe to commit.
    """
    import subprocess

    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            cwd=repo_path,
            capture_output=True, text=True, timeout=30
        )
        staged_files = [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]
    except Exception:
        # If we can't get staged files, scan the whole directory
        return scan_directory(repo_path), False

    all_findings = {}
    for rel_path in staged_files:
        filepath = os.path.join(repo_path, rel_path)
        if os.path.exists(filepath):
            findings = scan_file(filepath)
            if findings:
                all_findings[filepath] = findings

    is_safe = len(all_findings) == 0
    return all_findings, is_safe


def print_findings(findings):
    """Pretty-print scan findings."""
    if not findings:
        print("  No secrets detected — safe to commit!")
        return

    print("  SECRETS DETECTED — COMMIT BLOCKED!")
    print("  " + "=" * 50)
    for filepath, file_findings in findings.items():
        print(f"\n  File: {filepath}")
        for pattern_name, line_num, text in file_findings:
            if line_num > 0:
                print(f"     [{pattern_name}] Line {line_num}: {text}")
            else:
                print(f"     [{pattern_name}]: {text}")
    print("  " + "=" * 50)


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    print(f"Scanning: {target}")
    findings = scan_directory(target)
    print_findings(findings)
    if findings:
        print(f"\n Found secrets in {len(findings)} file(s). DO NOT COMMIT!")
        sys.exit(1)
    else:
        print("\n All clear!")
        sys.exit(0)
