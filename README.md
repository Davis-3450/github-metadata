# github-metadata scraper

Github metadata downloader is a tool written in Python that allows you to retrieve metadata from your GitHub repositories. It uses the GitHub API to fetch information about your repositories, such as their names, descriptions, languages, stars, and more.

returns a JSON file with the following structure:

```json
[
  {
    "name": "username/repo-name",
    "private": false,
    "desc": "Repository description",
    "lang": "Python",
    "stars": 42,
    "updated": "2023-01-01",
    "archived": false,
    "tags": ["tag1", "tag2"]
  },
  ...
]
```

## Clone

```bash
git clone https://github.com/Davis-3450/github-metadata.git
```

## Usage

```bash
uv sync # install deps
uv run main.py # Run the script
```

General access token is expected to be stored in a `.env` file in the root directory of the project, with the following format

## Environment Variables

```bash
GITHUB_TOKEN=your_personal_access_token
```