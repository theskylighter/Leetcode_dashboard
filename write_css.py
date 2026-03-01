"""Write the full index.css for LeetDash."""
import os
css = r"""
/* ═══════════════════════════════════════════════════════════
   LEETDASH — Global Design System
   Dark theme by default, light via [data-theme="light"]
═══════════════════════════════════════════════════════════ */

/* ─── CSS Variables ──────────────────────────────────────── */
:root {
  --bg:          #0a0a0f;
  --surface:     #111118;
  --surface2:    #1a1a26;
  --surface3:    #242434;
  --border:      #2a2a3a;
  --accent:      #f97316;
  --accent2:     #fb923c;
  --accent-dim:  rgba(249,115,22,0.15);
  --accent-glow: rgba(249,115,22,0.3);
  --text:        #e8e8f0;
  --text-muted:  #8888aa;
  --easy:        #22c55e;
  --medium:      #f59e0b;
  --hard:        #ef4444;
  --green:       #22c55e;
  --amber:       #f59e0b;
  --red:         #ef4444;
  --blue:        #3b82f6;
  --radius:      12px;
  --radius-sm:   8px;
  --shadow:      0 4px 24px rgba(0,0,0,0.4);
  --font-mono:   'JetBrains Mono', monospace;
  --font-main:   'Syne', sans-serif;
  --nav-h:       64px;
  --transition:  0.18s ease;
}
[data-theme="light"] {
  --bg:       #f4f4f8;
  --surface:  #ffffff;
  --surface2: #eeeef5;
  --surface3: #e0e0ec;
  --border:   #d0d0e0;
  --text:     #18181e;
  --text-muted: #6060808;
  --shadow:   0 4px 24px rgba(0,0,0,0.10);
}

/* ─── Reset & Base ───────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--font-main);
  font-size: 15px;
  line-height: 1.6;
  min-height: 100vh;
  overflow-x: hidden;
}
a { color: var(--accent); text-decoration: none; }
a:hover { color: var(--accent2); }
button { cursor: pointer; border: none; outline: none; font-family: inherit; }
textarea, input, select {
  font-family: inherit;
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--text);
  padding: 8px 12px;
  width: 100%;
  font-size: 14px;
  transition: border var(--transition);
}
textarea:focus, input:focus, select:focus {
  outline: none;
  border-color: var(--accent);
}
select option { background: var(--surface2); }

/* ─── Alert Banners ──────────────────────────────────────── */
.alert-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 20px;
  font-size: 13px;
  position: relative;
  z-index: 200;
}
.alert-warn { background: rgba(245,158,11,0.18); color: #fbbf24; border-bottom: 1px solid rgba(245,158,11,0.3); }
.alert-info { background: rgba(59,130,246,0.12); color: #60a5fa; border-bottom: 1px solid rgba(59,130,246,0.25); }
.alert-close {
  margin-left: auto;
  background: none;
  border: none;
  color: inherit;
  font-size: 16px;
  opacity: 0.7;
  cursor: pointer;
}
.alert-close:hover { opacity: 1; }

/* ─── Navigation ─────────────────────────────────────────── */
#main-nav {
  height: var(--nav-h);
  background: rgba(10,10,15,0.92);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  padding: 0 24px;
  gap: 24px;
  position: sticky;
  top: 0;
  z-index: 100;
}
.nav-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 800;
  font-size: 1.2rem;
  color: var(--text);
  text-decoration: none;
  white-space: nowrap;
}
.logo-icon { font-size: 1.3rem; }
.nav-links {
  display: flex;
  list-style: none;
  gap: 4px;
  flex: 1;
}
.nav-links a {
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-muted);
  transition: all var(--transition);
  white-space: nowrap;
}
.nav-links a:hover,
.nav-links a.active {
  background: var(--accent-dim);
  color: var(--accent);
}
.nav-right { display: flex; align-items: center; gap: 10px; }
.nav-streak-badge {
  font-size: 13px;
  font-weight: 700;
  color: var(--accent);
  background: var(--accent-dim);
  padding: 4px 10px;
  border-radius: 20px;
  min-width: 40px;
  text-align: center;
}
.icon-btn {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--text);
  width: 34px;
  height: 34px;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition);
}
.icon-btn:hover { border-color: var(--accent); color: var(--accent); }

/* ─── Page Loading ───────────────────────────────────────── */
.page-loading {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}
.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ─── Page Container ─────────────────────────────────────── */
#app { max-width: 1280px; margin: 0 auto; padding: 28px 20px 60px; }

/* ─── Page Header ────────────────────────────────────────── */
.page-header { margin-bottom: 28px; }
.page-title { font-size: 1.8rem; font-weight: 800; }
.page-subtitle { color: var(--text-muted); font-size: 14px; margin-top: 4px; }

/* ─── Card ───────────────────────────────────────────────── */
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px 24px;
  box-shadow: var(--shadow);
}
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}
.card-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  font-size: 1rem;
}

/* ─── Grid Layouts ───────────────────────────────────────── */
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.grid-3 { display: grid; grid-template-columns: repeat(3,1fr); gap: 20px; }
.grid-4 { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; }
@media (max-width:1024px) { .grid-4 { grid-template-columns: repeat(2,1fr); } }
@media (max-width:768px)  { .grid-2,.grid-3,.grid-4 { grid-template-columns: 1fr; } }

.dashboard-layout {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 20px;
  align-items: start;
}
@media (max-width:900px) {
  .dashboard-layout { grid-template-columns: 1fr; }
}

/* ─── Buttons ────────────────────────────────────────────── */
.btn-primary {
  background: var(--accent);
  color: #fff;
  padding: 10px 22px;
  border-radius: var(--radius-sm);
  font-weight: 700;
  font-size: 14px;
  border: none;
  transition: all var(--transition);
}
.btn-primary:hover { background: var(--accent2); transform: translateY(-1px); }
.btn-secondary {
  background: var(--surface2);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 10px 22px;
  border-radius: var(--radius-sm);
  font-weight: 600;
  font-size: 14px;
  transition: all var(--transition);
}
.btn-secondary:hover { border-color: var(--accent); color: var(--accent); }
.btn-sm { padding: 6px 14px; font-size: 13px; }
.w-full { width: 100%; }

/* ─── Badges/Pills ───────────────────────────────────────── */
.badge {
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.badge-easy   { background: rgba(34,197,94,0.15); color: var(--easy); }
.badge-medium { background: rgba(245,158,11,0.15); color: var(--medium); }
.badge-hard   { background: rgba(239,68,68,0.15); color: var(--hard); }

/* ─── Progress Bar ───────────────────────────────────────── */
.progress-bar-track {
  background: var(--surface2);
  border-radius: 99px;
  height: 8px;
  overflow: hidden;
}
.progress-bar-fill {
  height: 100%;
  border-radius: 99px;
  background: var(--accent);
  transition: width 0.6s ease;
}

/* ─── DASHBOARD ──────────────────────────────────────────── */
.daily-question-card { }
.daily-meta { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
.daily-num { font-family: var(--font-mono); color: var(--text-muted); font-size: 13px; }
.daily-title { font-size: 1.3rem; font-weight: 800; margin-bottom: 8px; }
.daily-title a { color: var(--text); }
.daily-title a:hover { color: var(--accent); }
.daily-topics { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 16px; }
.topic-tag {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 20px;
  font-size: 11px;
  padding: 2px 10px;
  color: var(--text-muted);
}
.daily-footer { display: flex; gap: 10px; align-items: center; }

/* Readiness Score Gauge */
.readiness-card { text-align: center; }
.gauge-wrap { position: relative; display: inline-block; margin: 12px 0; }
.gauge-svg { display: block; }
.gauge-score {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 2.2rem;
  font-weight: 800;
  font-family: var(--font-mono);
  line-height: 1;
}
.gauge-label {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 2px;
}
.readiness-meta { font-size: 12px; color: var(--text-muted); margin-top: 8px; }

/* Today's Focus */
.focus-card-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px;
  background: var(--surface2);
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
  margin-bottom: 10px;
}
.focus-card-item:last-child { margin-bottom: 0; }
.focus-icon { font-size: 1.4rem; flex-shrink: 0; margin-top: 2px; }
.focus-info { flex: 1; min-width: 0; }
.focus-label { font-size: 11px; text-transform: uppercase; color: var(--text-muted); letter-spacing: .05em; margin-bottom: 3px; }
.focus-title { font-weight: 700; font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.focus-meta { font-size: 12px; color: var(--text-muted); margin-top: 2px; }
.focus-action { flex-shrink: 0; }

/* Streak summary */
.streak-summary {
  display: flex;
  gap: 20px;
  margin-top: 12px;
  font-size: 13px;
  color: var(--text-muted);
}
.streak-summary strong { color: var(--text); }

/* Due Reviews list */
.review-list { list-style: none; }
.review-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 0;
  border-bottom: 1px solid var(--border);
}
.review-item:last-child { border-bottom: none; }
.review-info { flex: 1; min-width: 0; }
.review-title { font-weight: 600; font-size: 14px; }
.review-due { font-size: 11px; color: var(--text-muted); }
.review-actions { display: flex; gap: 6px; }

/* Empty state */
.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: var(--text-muted);
}
.empty-state .empty-icon { font-size: 2.5rem; margin-bottom: 10px; }
.empty-state p { font-size: 14px; }

/* ─── STREAK GRID ────────────────────────────────────────── */
.streak-grid-wrap { overflow-x: auto; padding-bottom: 8px; }
.streak-grid {
  display: grid;
  grid-template-rows: repeat(7, 14px);
  grid-auto-flow: column;
  gap: 3px;
  width: max-content;
}
.streak-cell {
  width: 14px;
  height: 14px;
  border-radius: 3px;
  background: var(--surface2);
  cursor: pointer;
  transition: opacity 0.15s, transform 0.1s;
  position: relative;
}
.streak-cell:hover { transform: scale(1.15); }
.streak-cell[data-count="0"] { background: var(--surface2); }
.streak-cell[data-count="1"] { background: rgba(249,115,22,0.35); }
.streak-cell[data-count="2"] { background: rgba(249,115,22,0.60); }
.streak-cell[data-count="3"],
.streak-cell[data-count="4"],
.streak-cell[data-count="5"] { background: rgba(249,115,22,0.85); }
.streak-cell.today { box-shadow: 0 0 0 2px var(--accent); }

.streak-months { display: flex; width: max-content; margin-bottom: 4px; font-size: 10px; color: var(--text-muted); }
.streak-weekdays {
  display: grid;
  grid-template-rows: repeat(7, 14px);
  gap: 3px;
  margin-right: 6px;
  font-size: 9px;
  color: var(--text-muted);
  align-items: center;
}

/* Tooltip */
.tooltip {
  position: fixed;
  background: var(--surface3);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 6px 10px;
  font-size: 12px;
  pointer-events: none;
  z-index: 999;
  white-space: nowrap;
  transition: opacity 0.12s;
}

/* ─── RADAR CHART ────────────────────────────────────────── */
.radar-wrap { display: flex; justify-content: center; }
.radar-svg text { fill: var(--text-muted); font-family: var(--font-main); }
.radar-polygon { fill: rgba(249,115,22,0.2); stroke: var(--accent); stroke-width: 2; }
.radar-bg-poly { fill: none; stroke: var(--border); stroke-width: 1; }
.radar-axis { stroke: var(--border); stroke-width: 1; }
.weakness-list { margin-top: 14px; }
.weakness-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 7px 0;
  border-bottom: 1px solid var(--border);
  font-size: 13px;
}
.weakness-item:last-child { border-bottom: none; }
.weakness-rank { font-weight: 700; color: var(--text-muted); width: 18px; }
.weakness-topic { flex: 1; text-transform: capitalize; }
.weakness-pct { font-family: var(--font-mono); font-size: 12px; }
.weakness-pct.danger { color: var(--red); }
.weakness-pct.warn   { color: var(--amber); }
.weakness-pct.good   { color: var(--green); }

/* ─── PATHS PAGE ─────────────────────────────────────────── */
.path-tabs { display: flex; gap: 8px; margin-bottom: 20px; }
.path-tab {
  padding: 8px 20px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
  background: var(--surface2);
  color: var(--text-muted);
  font-weight: 600;
  font-size: 13px;
  cursor: pointer;
  transition: all var(--transition);
}
.path-tab:hover, .path-tab.active {
  background: var(--accent-dim);
  color: var(--accent);
  border-color: var(--accent);
}
.path-progress-bar { margin-bottom: 20px; }
.path-progress-label {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  margin-bottom: 6px;
  color: var(--text-muted);
}
.path-section { margin-bottom: 20px; }
.path-section-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  background: var(--surface2);
  border-radius: var(--radius-sm);
  font-weight: 700;
  font-size: 14px;
  margin-bottom: 8px;
  cursor: pointer;
  user-select: none;
}
.path-section-header .section-check { color: var(--green); }
.path-section-header .section-pct { margin-left: auto; font-size: 12px; color: var(--text-muted); font-weight: 400; }
.path-problem-list { list-style: none; padding-left: 0; }
.path-problem-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 14px;
  border-radius: var(--radius-sm);
  transition: background var(--transition);
  font-size: 14px;
}
.path-problem-item:hover { background: var(--surface2); }
.path-problem-item input[type="checkbox"] {
  width: 16px;
  height: 16px;
  accent-color: var(--accent);
  cursor: pointer;
  flex-shrink: 0;
  background: var(--surface2);
  border: 1px solid var(--border);
}
.path-problem-item.solved .path-problem-title { text-decoration: line-through; color: var(--text-muted); }
.path-problem-title { flex: 1; }
.path-problem-actions { display: flex; gap: 6px; }

/* ─── BADGES PAGE ────────────────────────────────────────── */
.badges-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px,1fr)); gap: 16px; }
.badge-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px 16px;
  text-align: center;
  transition: all var(--transition);
}
.badge-card.earned { border-color: var(--accent); background: linear-gradient(135deg,var(--surface) 0%,rgba(249,115,22,0.06) 100%); }
.badge-card.locked { opacity: 0.45; }
.badge-card:hover { transform: translateY(-2px); box-shadow: var(--shadow); }
.badge-emoji { font-size: 2.4rem; margin-bottom: 10px; display: block; }
.badge-name { font-weight: 700; font-size: 14px; margin-bottom: 4px; }
.badge-desc { font-size: 11px; color: var(--text-muted); line-height: 1.4; }
.badge-date { font-size: 10px; color: var(--accent); margin-top: 6px; font-family: var(--font-mono); }

/* Badge Popup */
.badge-popup {
  position: fixed;
  bottom: 30px;
  right: 30px;
  z-index: 1000;
  animation: slideUp 0.4s ease;
}
.badge-popup.hidden { display: none; }
.badge-popup-inner {
  display: flex;
  align-items: center;
  gap: 16px;
  background: var(--surface);
  border: 1px solid var(--accent);
  border-radius: var(--radius);
  padding: 16px 22px;
  box-shadow: 0 8px 32px rgba(249,115,22,0.25);
  min-width: 260px;
}
.badge-popup-icon { font-size: 2.2rem; }
.badge-popup-label { font-size: 11px; color: var(--accent); text-transform: uppercase; letter-spacing: .06em; font-weight: 700; }
.badge-popup-name { font-weight: 800; font-size: 16px; margin-top: 2px; }
@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to   { transform: translateY(0); opacity: 1; }
}

/* ─── REVIEW PAGE ────────────────────────────────────────── */
.review-filter-row { display: flex; gap: 10px; margin-bottom: 20px; align-items: center; }
.review-full-item {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 18px 20px;
  margin-bottom: 12px;
  transition: border-color var(--transition);
}
.review-full-item:hover { border-color: var(--accent); }
.review-full-header { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
.review-full-title { flex: 1; font-weight: 700; font-size: 15px; }
.review-full-meta { display: flex; gap: 16px; font-size: 12px; color: var(--text-muted); }
.review-full-actions { display: flex; gap: 8px; margin-top: 12px; }
.rating-btn-sm {
  padding: 5px 12px;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: var(--surface2);
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition);
}
.rating-btn-sm:hover { border-color: var(--accent); color: var(--accent); }
.rating-btn-sm.rated { background: var(--accent); color: #fff; border-color: var(--accent); }

/* ─── SETTINGS PAGE ──────────────────────────────────────── */
.settings-section { margin-bottom: 28px; }
.settings-section-title { font-size: 12px; text-transform: uppercase; letter-spacing: .08em; color: var(--text-muted); font-weight: 700; margin-bottom: 12px; }
.setting-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 0;
  border-bottom: 1px solid var(--border);
}
.setting-row:last-child { border-bottom: none; }
.setting-label { font-size: 14px; font-weight: 600; }
.setting-desc { font-size: 12px; color: var(--text-muted); margin-top: 2px; }
.setting-control { flex-shrink: 0; }
.select-input {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--text);
  padding: 7px 12px;
  font-size: 13px;
}
.toggle {
  position: relative;
  width: 44px;
  height: 24px;
}
.toggle input { opacity: 0; width: 0; height: 0; }
.toggle-slider {
  position: absolute;
  inset: 0;
  background: var(--surface3);
  border-radius: 12px;
  cursor: pointer;
  transition: background 0.2s;
}
.toggle-slider::before {
  content: '';
  position: absolute;
  width: 18px;
  height: 18px;
  left: 3px;
  top: 3px;
  background: #fff;
  border-radius: 50%;
  transition: transform 0.2s;
}
.toggle input:checked + .toggle-slider { background: var(--accent); }
.toggle input:checked + .toggle-slider::before { transform: translateX(20px); }
.storage-meter { margin-top: 8px; }
.storage-text { font-size: 12px; color: var(--text-muted); margin-bottom: 6px; }

/* Backup area */
.backup-area { display: flex; gap: 12px; flex-wrap: wrap; padding: 16px 0; }
.file-input-label {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
  background: var(--surface2);
  color: var(--text);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition);
}
.file-input-label:hover { border-color: var(--accent); color: var(--accent); }
.file-input-label input { display: none; }

/* ─── NOTES MODAL ────────────────────────────────────────── */
.modal {
  position: fixed;
  inset: 0;
  z-index: 500;
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal.hidden { display: none; }
.modal-backdrop {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.65);
  backdrop-filter: blur(4px);
}
.modal-panel {
  position: relative;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  width: 100%;
  max-width: 560px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.5);
  margin: 16px;
}
.modal-sm { max-width: 420px; }
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 22px;
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  background: var(--surface);
  z-index: 1;
}
.modal-header h3 { font-size: 16px; font-weight: 800; }
.modal-actions { display: flex; align-items: center; gap: 10px; }
.modal-body { padding: 22px; }
.save-indicator { font-size: 12px; color: var(--text-muted); font-family: var(--font-mono); }
.note-field { margin-bottom: 18px; }
.note-field label { display: block; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: .06em; color: var(--text-muted); margin-bottom: 6px; }
.note-field textarea { resize: vertical; min-height: 90px; }
.note-row { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.note-field.half {}
.char-count { font-size: 11px; color: var(--text-muted); font-family: var(--font-mono); display: block; text-align: right; margin-top: 4px; }
.star-rating { display: flex; gap: 6px; }
.star {
  font-size: 1.6rem;
  cursor: pointer;
  color: var(--surface3);
  transition: color 0.1s, transform 0.1s;
  line-height: 1;
}
.star.active, .star:hover { color: var(--accent); transform: scale(1.1); }

/* ─── SOLVE MODAL ────────────────────────────────────────── */
.solve-subtitle { color: var(--text-muted); font-size: 13px; margin-bottom: 14px; }
.rating-buttons { display: flex; gap: 8px; margin-bottom: 18px; }
.rating-btn {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  padding: 10px 4px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
  background: var(--surface2);
  color: var(--text-muted);
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all var(--transition);
  font-family: var(--font-mono);
}
.rating-btn span { font-size: 10px; font-family: var(--font-main); font-weight: 600; text-transform: uppercase; }
.rating-btn:hover, .rating-btn.selected {
  border-color: var(--accent);
  color: var(--accent);
  background: var(--accent-dim);
}

/* ─── CONTEST CARD ───────────────────────────────────────── */
.contest-card { }
.contest-item {
  padding: 14px 0;
  border-bottom: 1px solid var(--border);
}
.contest-item:last-child { border-bottom: none; }
.contest-title { font-weight: 700; font-size: 14px; margin-bottom: 4px; }
.contest-time { font-size: 12px; color: var(--text-muted); margin-bottom: 8px; }
.contest-countdown {
  font-family: var(--font-mono);
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--accent);
  letter-spacing: .02em;
}
.contest-meta { display: flex; align-items: center; justify-content: space-between; }

/* ─── PROGRESS PAGE ──────────────────────────────────────── */
.progress-stat-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; margin-bottom: 24px; }
@media (max-width:768px) { .progress-stat-grid { grid-template-columns: repeat(2,1fr); } }
.stat-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 18px;
  text-align: center;
}
.stat-number { font-size: 2rem; font-weight: 800; font-family: var(--font-mono); color: var(--accent); }
.stat-label { font-size: 12px; color: var(--text-muted); margin-top: 4px; }
.diff-breakdown { display: flex; gap: 8px; margin-top: 12px; }
.diff-item { flex: 1; text-align: center; padding: 10px; border-radius: 8px; }
.diff-item.easy   { background: rgba(34,197,94,0.1); }
.diff-item.medium { background: rgba(245,158,11,0.1); }
.diff-item.hard   { background: rgba(239,68,68,0.1);  }
.diff-item .diff-n { font-size: 1.4rem; font-weight: 800; font-family: var(--font-mono); }
.diff-item.easy   .diff-n { color: var(--easy); }
.diff-item.medium .diff-n { color: var(--medium); }
.diff-item.hard   .diff-n { color: var(--hard); }
.diff-item .diff-l { font-size: 11px; color: var(--text-muted); margin-top: 2px; }

/* ─── PROFILE CARD  (shared URL view) ───────────────────── */
.profile-card-wrap { display: flex; justify-content: center; padding: 40px 0; }
.profile-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 32px;
  max-width: 400px;
  width: 100%;
  text-align: center;
  box-shadow: var(--shadow);
  position: relative;
}
.profile-watermark {
  font-size: 11px;
  color: var(--text-muted);
  margin-bottom: 16px;
  text-transform: uppercase;
  letter-spacing: .1em;
}
.profile-username { font-size: 1.8rem; font-weight: 800; margin-bottom: 8px; }
.profile-stats { display: flex; justify-content: center; gap: 30px; margin-bottom: 20px; font-family: var(--font-mono); }
.profile-stat-num { font-size: 1.6rem; font-weight: 800; color: var(--accent); }
.profile-stat-label { font-size: 11px; color: var(--text-muted); }
.profile-badges { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; }
.profile-badge-chip {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 4px 12px;
  font-size: 12px;
}

/* ─── Misc helpers ───────────────────────────────────────── */
.hidden { display: none !important; }
.text-muted { color: var(--text-muted); }
.text-accent { color: var(--accent); }
.text-green { color: var(--green); }
.text-red { color: var(--red); }
.mt-1 { margin-top: 4px; }
.mt-2 { margin-top: 8px; }
.mt-3 { margin-top: 12px; }
.mt-4 { margin-top: 16px; }
.mb-4 { margin-bottom: 16px; }
.flex { display: flex; }
.flex-center { display: flex; align-items: center; justify-content: center; }
.gap-2 { gap: 8px; }
.gap-3 { gap: 12px; }
.font-mono { font-family: var(--font-mono); }
hr.divider { border: none; border-top: 1px solid var(--border); margin: 20px 0; }

/* username input settings */
.username-row { display: flex; gap: 8px; }
.username-row input { flex: 1; }
"""

path = os.path.join(os.path.dirname(__file__), 'index.css')
with open(path, 'w') as f:
    f.write(css.strip())
print(f"Wrote {len(css.strip())} chars to index.css")
