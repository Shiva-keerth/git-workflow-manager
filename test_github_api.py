"""Quick test to check if the GitHub PAT can create a new repository."""
import urllib.request
import urllib.error
import json
import os

token = os.environ.get("GITHUB_PAT")

# Step 1: Test authentication
print("=" * 50)
print("Step 1: Testing GitHub API Authentication...")
req = urllib.request.Request(
    "https://api.github.com/user",
    headers={"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"},
)
try:
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read().decode())
    username = data["login"]
    print(f"  OK - Authenticated as: {username}")
    print(f"  OK - Public repos: {data['public_repos']}")
except urllib.error.HTTPError as e:
    print(f"  FAIL - Authentication failed: HTTP {e.code}")
    print(f"  Error: {e.read().decode()}")
    exit(1)

# Step 2: Test repo creation
print()
print("Step 2: Testing repo creation (Workforce-Readiness-AI)...")
url = "https://api.github.com/user/repos"
payload = json.dumps({
    "name": "Workforce-Readiness-AI",
    "description": "AI-powered workforce analytics platform with Random Forest performance prediction",
    "private": False,
    "auto_init": False,
}).encode("utf-8")

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json",
    "Content-Type": "application/json",
}

req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
try:
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read().decode())
    print(f"  OK - Repository created successfully!")
    print(f"  OK - URL: {result.get('html_url', 'N/A')}")
except urllib.error.HTTPError as e:
    error_body = e.read().decode()
    if "already exists" in error_body.lower():
        print(f"  OK - Repository already exists (this is fine!)")
    else:
        print(f"  FAIL - Repo creation FAILED: HTTP {e.code}")
        print(f"  Error: {error_body}")
        # Check token scopes
        print()
        print("Step 3: Checking token permissions...")
        scope_req = urllib.request.Request(
            "https://api.github.com/user",
            headers={"Authorization": f"token {token}"},
        )
        scope_resp = urllib.request.urlopen(scope_req)
        scopes = scope_resp.headers.get("X-OAuth-Scopes", "NONE")
        print(f"  Token scopes: {scopes}")
        print("  WARNING: You need the 'repo' scope to create repositories!")
except Exception as e:
    print(f"  FAIL - Unexpected error: {e}")
