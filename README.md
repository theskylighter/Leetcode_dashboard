# LeetDash — LeetCode Progress Dashboard

A lightweight, client-side web dashboard that tracks your LeetCode solving progress and displays a daily challenge. Built with vanilla HTML/CSS/JS, Tailwind CSS, and Flowbite components.

## Features

- **Daily Question** — Automatically fetches and displays today's LeetCode Daily Challenge (title, difficulty badge, description, and direct link).
- **Username Lookup** — Enter any LeetCode username to see their total solved count (easy / medium / hard breakdown).
- **Local Leaderboard** — Every checked user is added to a persistent leaderboard stored in `localStorage`, sorted by total problems solved.
- **Animated Starfield** — Decorative twinkling-star background that adapts its density to viewport size.
- **Dark Mode Ready** — Uses Tailwind's `dark:` variants throughout; respects system/browser preference.
- **Responsive** — Mobile-first layout with collapsible navbar, scrollable table, and stacked input controls on small screens.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Markup | HTML5 |
| Styling | Tailwind CSS v4 (CDN browser build) + custom CSS |
| Components | Flowbite 3.1.1 (navbar, buttons, table) |
| Logic | Vanilla JavaScript (ES2020+) |
| API | [alfa-leetcode-api](https://github.com/alfaarghya/alfa-leetcode-api) (hosted on Render) |

## Project Structure

```
├── index.html   # Single-page HTML shell (navbar, hero, daily card, form, leaderboard table, footer)
├── app.js       # All application logic (API calls, DOM updates, leaderboard persistence, starfield)
├── index.css    # Custom styles (starfield animation, loader, responsive overrides, layout helpers)
└── README.md
```

## How It Works

1. On page load, `app.js` fires three actions:
   - **Renders the leaderboard** from `localStorage`.
   - **Creates the starfield** background (`div.star` elements with randomised position, size, and animation duration).
   - **Fetches the daily challenge** from `https://alfa-leetcode-api.onrender.com/daily` and populates the Daily Question card.
2. The user enters a LeetCode username and clicks **Check**.
3. The app calls `https://alfa-leetcode-api.onrender.com/<username>/solved`, displays the result, and upserts the user into the leaderboard.
4. The leaderboard is saved to `localStorage` so it persists across sessions.

## Getting Started

No build step required — just serve the files with any static server:

```bash
# Python
python3 -m http.server 8000

# Node (npx)
npx serve .

# Or simply open index.html in a browser
```

Then navigate to `http://localhost:8000`.

## API Dependency

All data comes from the **alfa-leetcode-api** public instance at `https://alfa-leetcode-api.onrender.com`. The free Render tier may cold-start, so the first request can take 30–60 seconds.

## License

This project currently has no explicit license. Contact the repository owner for usage terms.
