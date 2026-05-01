# Personal Academic Webpage

A clean, static academic website designed for GitHub Pages.

## Preview locally

```bash
python3 -m http.server 8080
```

Then open `http://localhost:8080`.

## Publish on GitHub Pages

1. Create a public repository named `<your-github-username>.github.io`.
2. Upload these files to the repository root.
3. In GitHub, go to **Settings → Pages** and publish from the `main` branch.

GitHub Pages is available for public repositories on GitHub Free.

## Updating publications

Google Scholar does not provide an official public API. This site therefore keeps publications in `data/publications.json`.

For automatic updates:

1. Add your Google Scholar profile ID to `data/profile.json`.
2. Add `SERPAPI_KEY` as a GitHub repository secret.
3. Run the `Update publications` GitHub Action manually or let the weekly schedule run.

Without a SerpAPI key, the site still works from the manually curated JSON file.
