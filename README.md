# Daily Forum Auto Login

Automates daily forum login using cloudscraper and GitHub Actions.

## How It Works

The script runs automatically every day at **08:00 WIB** via GitHub Actions. Login is performed using [cloudscraper](https://github.com/VeNoMouS/cloudscraper) — a lightweight requests-based library that bypasses Cloudflare's JS challenge without needing a browser. All credentials are read from environment variables so no sensitive data is stored in the code.

## Project Structure

```
daily-login/
├── .github/
│   └── workflows/
│       └── daily-login.yml   # GitHub Actions workflow
├── login.py                  # Main login script
├── requirements.txt          # Python dependencies
├── .gitignore
└── README.md
```

## Setup

### 1. Fork / Clone the Repository

```bash
git clone <repo-url>
cd daily-login
```

### 2. Add GitHub Secrets

Go to **Settings → Secrets and variables → Actions → New repository secret** and add the following three secrets:

| Secret Name      | Description                                                     |
|------------------|-----------------------------------------------------------------|
| `FORUM_USERNAME` | Forum account username or email                                 |
| `FORUM_PASSWORD` | Forum account password                                          |
| `FORUM_URL`      | Login page URL (e.g. `https://forum.example.com/member.php?mod=logging&action=login`) |

### 3. Enable GitHub Actions

Make sure the **Actions** tab in your repository is enabled. The workflow will run automatically on schedule, or you can trigger it manually via **Run workflow**.

## Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FORUM_USERNAME="your_username"
export FORUM_PASSWORD="your_password"
export FORUM_URL="https://forum.example.com/member.php?mod=logging&action=login"

# Run the script
python login.py
```

On Windows (PowerShell):

```powershell
$env:FORUM_USERNAME = "your_username"
$env:FORUM_PASSWORD = "your_password"
$env:FORUM_URL      = "https://forum.example.com/member.php?mod=logging&action=login"
python login.py
```

## Schedule

| Cron Expression | Time                        |
|-----------------|-----------------------------|
| `0 1 * * *`     | 08:00 WIB (01:00 UTC) daily |

To change the schedule, edit the `cron:` line in [.github/workflows/daily-login.yml](.github/workflows/daily-login.yml).

## Troubleshooting

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| `FORUM_USERNAME, FORUM_PASSWORD, dan FORUM_URL harus di-set.` | Secrets not added | Add secrets in Settings |
| `formhash tidak ditemukan` | Still blocked by Cloudflare | Check if the forum uses a stricter Cloudflare plan (Turnstile/CAPTCHA) |
| `Login GAGAL` | Wrong credentials or form selectors changed | Verify credentials and forum structure |

## Security

- **No** credentials or URLs are hardcoded anywhere in the codebase.
- All sensitive values are read from GitHub Secrets (in CI) or environment variables (locally).
- `.env` is listed in `.gitignore` to prevent accidental commits.
