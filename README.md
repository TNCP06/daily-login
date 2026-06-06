# Daily Forum Auto Login

Automates daily forum login using Playwright and GitHub Actions.

## How It Works

The script runs automatically every day at **08:00 WIB** via GitHub Actions. Login is performed using Playwright with headless Chromium, reading all credentials from environment variables so no sensitive data is stored in the code.

## Project Structure

```
auto-login/
├── .github/
│   └── workflows/
│       └── daily-login.yml   # GitHub Actions workflow
├── login.py                  # Main Playwright script
├── requirements.txt          # Python dependencies
├── .gitignore
└── README.md
```

## Setup

### 1. Fork / Clone the Repository

```bash
git clone <repo-url>
cd auto-login
```

### 2. Add GitHub Secrets

Go to **Settings → Secrets and variables → Actions → New repository secret** and add the following three secrets:

| Secret Name      | Description                                                        |
|------------------|--------------------------------------------------------------------|
| `FORUM_USERNAME` | Forum account username or email                                    |
| `FORUM_PASSWORD` | Forum account password                                             |
| `FORUM_URL`      | Login page URL (e.g. `https://forum.example.com/login`)            |

### 3. Enable GitHub Actions

Make sure the **Actions** tab in your repository is enabled. The workflow will run automatically on schedule, or you can trigger it manually via **Run workflow**.

## Running Locally

```bash
# Install dependencies
pip install -r requirements.txt
playwright install chromium --with-deps

# Set environment variables
export FORUM_USERNAME="your_username"
export FORUM_PASSWORD="your_password"
export FORUM_URL="https://forum.example.com/login"

# Run the script
python login.py
```

On Windows (PowerShell):

```powershell
$env:FORUM_USERNAME = "your_username"
$env:FORUM_PASSWORD = "your_password"
$env:FORUM_URL      = "https://forum.example.com/login"
python login.py
```

## Schedule

| Cron Expression | Time                     |
|-----------------|--------------------------|
| `0 1 * * *`     | 08:00 WIB (01:00 UTC) daily |

To change the schedule, edit the `cron:` line in [.github/workflows/daily-login.yml](.github/workflows/daily-login.yml).

## Troubleshooting

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| `Error: FORUM_USERNAME, FORUM_PASSWORD, and FORUM_URL must be set.` | Secrets not added | Add secrets in Settings |
| `Timeout opening page` | URL unreachable | Check the `FORUM_URL` value |
| `Login failed` | Selector changed or wrong credentials | Verify selectors and credentials |

## Security

- **No** credentials or URLs are hardcoded anywhere in the codebase.
- All sensitive values are read from GitHub Secrets (in CI) or environment variables (locally).
- `.env` is listed in `.gitignore` to prevent accidental commits.
