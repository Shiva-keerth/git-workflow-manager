# Git Workflow Manager 🚀

A Python-based automation tool designed to help developers maintain a consistent GitHub contribution streak while ensuring sensitive information (like API keys and `.env` files) never accidentally leaks into public repositories. 

## 🌟 Features
- **Automated Drip Deployment:** Schedules and pushes pre-planned commits over a series of days to maintain a steady GitHub contribution graph.
- **Smart Secret Scanning:** Automatically scans your code for hardcoded secrets, API keys, and sensitive tokens before allowing a commit.
- **Global `.gitignore` Management:** Enforces a robust global `.gitignore` strategy to automatically exclude `.env`, `__pycache__`, and other sensitive/unnecessary files across all your projects.
- **Automated Task Scheduler:** Includes batch scripts to easily set up Windows Task Scheduler for fully hands-off daily commits.

---

## 🛠️ Setup Instructions (For Windows)

Follow these steps to set up the Git Workflow Manager on your local machine.

### 1. Prerequisites
- [Python 3.8+](https://www.python.org/downloads/) (Check "Add Python to PATH" during installation)
- [Git for Windows](https://git-scm.com/download/win)

### 2. Clone the Repository
Open Command Prompt (`cmd`) and run:
```cmd
git clone https://github.com/Shiva-keerth/git-workflow-manager.git
cd git-workflow-manager
```

### 3. Set Up the Python Environment
It is highly recommended to use a virtual environment to install the dependencies.
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Configuration 🚨 (Important)
Because this tool interacts with your GitHub account, you need to provide it with secure access. 
1. Go to your GitHub Settings -> Developer Settings -> Personal Access Tokens (Tokens (classic)).
2. Generate a new token with `repo` permissions.
3. In the root directory of this project, create a file named `config.json`.
4. Paste the following into `config.json` and add your specific details:
```json
{
    "GITHUB_TOKEN": "your_personal_access_token_here",
    "REPO_NAME": "your_github_username/your_target_repo"
}
```
*(Note: `config.json` is safely ignored by Git, so your token will never be uploaded to GitHub).*

---

## 🚀 Usage

### Manual Execution
To manually trigger the auto-commit process, ensure your virtual environment is active and run:
```cmd
python auto_commit.py
```

### Scheduling Automated Daily Commits
If you want the tool to run automatically in the background every day:
1. Double-click the `setup_scheduler.bat` file.
2. This will configure the Windows Task Scheduler to run the `run_auto_commit.bat` script daily.

### Global GitIgnore Setup
To apply the strict security rules to all Git repositories on your computer:
1. Run `setup_global_gitignore.bat`.
2. This will apply the `.gitignore_global` rules globally to your Git configuration.

## 🛡️ Security Note
This tool includes a `secret_scanner.py` module. If it detects a potential API key or secret in the files you are trying to commit, it will **abort the commit** and warn you, keeping your accounts safe.
