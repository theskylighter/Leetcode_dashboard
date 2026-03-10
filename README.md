# LeetDash — LeetCode Progress Dashboard

A fully client-side, multi-page SPA that helps you track LeetCode solving progress, manage spaced-repetition reviews, follow curated study paths, and share your stats. Built with vanilla HTML/CSS/JS — no framework, no build step.

## Features

- **Dashboard** — At-a-glance readiness score, 52-week activity heat map, daily review queue, smart next-problem recommendation, company prep bar, and live contest/daily-challenge cards.
- **Progress** — SVG topic radar chart across 10 key topics, weakest-topic highlights, solve history, and difficulty breakdown.
- **Review Queue** — SM-2 spaced-repetition scheduler. Rate each review 1–5 to automatically schedule the next repetition date; overdue and upcoming items shown separately.
- **Study Paths** — Track completion of Blind 75, NeetCode 150, and Grind 169 with per-section progress indicators.
- **Achievements** — 14 unlockable badges (streak milestones, volume targets, difficulty goals, readiness thresholds, path completion).
- **Notes Modal** — Per-problem notes (approach, time/space complexity, gotchas) with a 1–5 confidence star rating; auto-saves to `localStorage`.
- **Settings** — LeetCode username, daily goal, target-company filter, one-click LeetCode profile fetch (solved counts, contest rating, recent submissions), and full JSON backup/restore.
- **Shared Profile** — Shareable read-only profile URL encoding username, score, streak, and earned badges in the URL hash.
- **Smart Banners** — Private/incognito mode warning and a 7-day backup reminder.
- **Theme Toggle** — Light/dark mode switch persistent across sessions.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Markup | HTML5 |
| Styling | Custom CSS (CSS variables, responsive, light/dark themes) |
| Fonts | Syne + JetBrains Mono (Google Fonts) |
| Logic | Vanilla JavaScript (ES2020+, no framework) |
| Storage | `localStorage` (all data stored client-side) |
| API | [alfa-leetcode-api](https://github.com/alfaarghya/alfa-leetcode-api) (hosted on Render) |

## Project Structure

```
├── index.html              # App shell: nav, banners, router mount point, modals
├── index.css               # All styles (layout, components, animations, themes)
├── build_data.py           # Script to build/update data/problems.json
├── data/
│   ├── problems.json       # Problem metadata (slug, title, difficulty, topics)
│   ├── company-tags.json   # Company → problem slug mapping
│   └── paths/
│       ├── blind75.json    # Blind 75 path definition
│       ├── neetcode150.json
│       └── grind169.json
└── js/
    ├── utils.js            # Constants (LS keys, ALFA_API), date helpers, localStorage wrappers, toast
    ├── compute.js          # Pure functions: topic radar, readiness score
    ├── storage.js          # Streak, SM-2 algorithm, onProblemSolved, export/import
    ├── api.js              # alfa-leetcode-api calls (profile, daily challenge, contests, calendar import)
    ├── badges.js           # Badge definitions, evaluation logic, popup
    ├── notes.js            # Notes modal open/save/close
    ├── modals.js           # Solve/rate modal
    ├── router.js           # App init, hash-based routing, event wiring
    └── pages/
        ├── dashboard.js    # Dashboard page render
        ├── progress.js     # Progress page render
        ├── review.js       # Review queue page render
        ├── paths.js        # Study paths page render
        ├── badges.js       # Achievements page render
        ├── settings.js     # Settings page render
        └── profile.js      # Shared profile page render
```

## How It Works

1. On load, `router.js` fetches `data/problems.json` and `data/company-tags.json`, checks storage health (private mode, backup reminder), recomputes streak and badges, then routes to the current hash.
2. The hash-based router (`#/`, `#/progress`, `#/review`, etc.) swaps the `<main id="app">` content by calling the relevant `render*()` function.
3. All user data (solve log, review queue, notes, badges, preferences) lives in `localStorage` under `ld:*` keys.
4. The SM-2 algorithm in `storage.js` schedules review intervals; rating a problem (1–5) updates its ease factor and next-review date.
5. The Settings page can fetch live stats from `alfa-leetcode-api` (solved counts, contest rating, recent AC submissions, submission calendar) and auto-import activity days into the solve log.

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

Optional live stats come from the **alfa-leetcode-api** public instance at `https://alfa-leetcode-api.onrender.com`. The free Render tier may cold-start, so the first fetch can take 30–60 seconds. The app is fully functional offline without it.

## License

This project currently has no explicit license. Contact the repository owner for usage terms.
