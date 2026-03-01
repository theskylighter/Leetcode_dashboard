#!/usr/bin/env python3
"""Writes index.css and app.js for LeetDash."""
import os, pathlib

ROOT = pathlib.Path(__file__).parent

# ─── CSS ────────────────────────────────────────────────────────────────────
CSS = r"""
/* ═══════════════════════════════════════════════════════
   LeetDash — Main Stylesheet
   ══════════════════════════════════════════════════════ */

/* ── Variables ─────────────────────────────────────────── */
:root {
  --bg:         #0a0a0f;
  --surface:    #111118;
  --surface2:   #1a1a26;
  --surface3:   #22223a;
  --border:     #2a2a3a;
  --accent:     #f97316;
  --accent2:    #fb923c;
  --accent-g:   rgba(249,115,22,.15);
  --text:       #e8e8f0;
  --muted:      #6b6b8a;
  --easy:       #22c55e;
  --medium:     #f59e0b;
  --hard:       #ef4444;
  --radius:     14px;
  --radius-sm:  8px;
}

[data-theme="light"] {
  --bg:       #f5f5fa;
  --surface:  #ffffff;
  --surface2: #f0f0f8;
  --surface3: #e8e8f5;
  --border:   #d0d0e0;
  --text:     #1a1a2e;
  --muted:    #7070a0;
}

/* ── Reset ──────────────────────────────────────────────── */
*, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
a { text-decoration:none; color:inherit; }
button { cursor:pointer; font-family:inherit; }
input, textarea, select { font-family:inherit; }
ul, ol { list-style:none; }

/* ── Base ───────────────────────────────────────────────── */
html { scroll-behavior:smooth; }

body {
  font-family: 'Syne', sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  overflow-x: hidden;
  line-height: 1.6;
}

/* ambient background glows */
body::before {
  content:'';
  position:fixed; top:-20%; right:-10%;
  width:600px; height:600px;
  background:radial-gradient(circle,rgba(249,115,22,.07) 0%,transparent 70%);
  pointer-events:none; z-index:0;
}
body::after {
  content:'';
  position:fixed; bottom:-10%; left:-10%;
  width:500px; height:500px;
  background:radial-gradient(circle,rgba(99,102,241,.05) 0%,transparent 70%);
  pointer-events:none; z-index:0;
}

/* ── Typography helpers ─────────────────────────────────── */
.mono { font-family:'JetBrains Mono',monospace; }
.muted { color:var(--muted); }
.accent { color:var(--accent); }
.hidden { display:none !important; }
.w-full { width:100%; }

/* ── Scrollbar ──────────────────────────────────────────── */
::-webkit-scrollbar { width:6px; }
::-webkit-scrollbar-track { background:var(--bg); }
::-webkit-scrollbar-thumb { background:var(--border); border-radius:3px; }

/* ── Alert banners ──────────────────────────────────────── */
.alert-banner {
  position:sticky; top:0; z-index:200;
  display:flex; align-items:center; gap:10px;
  padding:10px 1.5rem;
  font-size:.83rem; font-weight:600;
  border-bottom:1px solid var(--border);
}
.alert-warn  { background:#2d1a00; color:#f97316; border-color:#4d2a00; }
.alert-info  { background:#0d1a2d; color:#60a5fa; border-color:#1a3a5c; }
.alert-banner a { color:inherit; text-decoration:underline; }
.alert-close {
  margin-left:auto; background:none; border:none;
  color:inherit; opacity:.6; font-size:1rem;
  cursor:pointer; padding:2px 6px;
}
.alert-close:hover { opacity:1; }

/* ── Navigation ─────────────────────────────────────────── */
#main-nav {
  position:sticky; top:0; z-index:100;
  display:flex; align-items:center; gap:2rem;
  padding:0 2rem; height:60px;
  background:rgba(10,10,15,.88);
  backdrop-filter:blur(18px);
  border-bottom:1px solid var(--border);
}

.nav-logo {
  display:flex; align-items:center; gap:9px;
  font-size:1.15rem; font-weight:800;
  letter-spacing:-.02em;
  color:var(--text);
}
.logo-icon {
  width:30px; height:30px;
  background:linear-gradient(135deg,var(--accent),#fbbf24);
  border-radius:8px;
  display:flex; align-items:center; justify-content:center;
  font-size:15px;
  box-shadow:0 0 18px rgba(249,115,22,.45);
}

.nav-links {
  display:flex; gap:1.5rem; align-items:center;
}
.nav-links a {
  color:var(--muted);
  font-size:.85rem; font-weight:600;
  letter-spacing:.025em;
  transition:color .2s;
  padding:4px 0;
  border-bottom:2px solid transparent;
}
.nav-links a:hover     { color:var(--text); }
.nav-links a.active    { color:var(--accent); border-bottom-color:var(--accent); }

.nav-right { margin-left:auto; display:flex; align-items:center; gap:10px; }

.nav-streak-badge {
  font-size:.78rem; font-weight:700;
  font-family:'JetBrains Mono',monospace;
  color:var(--accent);
  background:var(--accent-g);
  border:1px solid rgba(249,115,22,.3);
  padding:4px 10px; border-radius:100px;
  min-width:40px; text-align:center;
}

.icon-btn {
  background:var(--surface2);
  border:1px solid var(--border);
  color:var(--text);
  width:34px; height:34px;
  border-radius:8px;
  display:flex; align-items:center; justify-content:center;
  font-size:16px;
  transition:all .2s;
}
.icon-btn:hover { border-color:var(--accent); color:var(--accent); }

/* ── Page skeleton ──────────────────────────────────────── */
#app {
  position:relative; z-index:1;
  max-width:1100px; margin:0 auto;
  padding:2rem 2rem 5rem;
  min-height:calc(100vh - 60px);
}

.page-loading {
  display:flex; align-items:center; justify-content:center;
  min-height:60vh;
}
.spinner {
  width:36px; height:36px;
  border:3px solid var(--border);
  border-bottom-color:var(--accent);
  border-radius:50%;
  animation:spin 1s linear infinite;
}
@keyframes spin { to { transform:rotate(360deg); } }

/* ── Shared page layout ─────────────────────────────────── */
.page-header {
  margin-bottom:1.75rem;
}
.page-title {
  font-size:1.6rem; font-weight:800;
  letter-spacing:-.03em;
  margin-bottom:.3rem;
}
.page-subtitle { color:var(--muted); font-size:.9rem; }

/* ── Card ───────────────────────────────────────────────── */
.card {
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:var(--radius);
  overflow:hidden;
  transition:border-color .2s;
}
.card:hover { border-color:#3a3a4a; }

.card-header {
  padding:1.25rem 1.5rem;
  border-bottom:1px solid var(--border);
  display:flex; align-items:center; gap:10px;
}
.card-header h2, .card-header h3 {
  font-size:.8rem; font-weight:700;
  color:var(--muted); text-transform:uppercase;
  letter-spacing:.06em;
}
.card-header .card-icon { font-size:16px; }
.card-header-right { margin-left:auto; }

.card-body { padding:1.5rem; }

/* ── Difficulty badges ──────────────────────────────────── */
.badge {
  display:inline-flex; align-items:center;
  padding:3px 10px; border-radius:100px;
  font-size:.68rem; font-weight:700;
  letter-spacing:.04em; text-transform:uppercase;
  font-family:'JetBrains Mono',monospace;
}
.badge-easy   { background:rgba(34,197,94,.12);  color:var(--easy);   border:1px solid rgba(34,197,94,.3);  }
.badge-medium { background:rgba(245,158,11,.12); color:var(--medium); border:1px solid rgba(245,158,11,.3); }
.badge-hard   { background:rgba(239,68,68,.12);  color:var(--hard);   border:1px solid rgba(239,68,68,.3);  }

/* ── Buttons ────────────────────────────────────────────── */
.btn-primary {
  display:inline-flex; align-items:center; gap:7px;
  background:var(--accent); color:#000;
  padding:10px 22px; border-radius:var(--radius-sm);
  font-weight:700; font-size:.88rem;
  border:none; transition:all .2s;
  box-shadow:0 4px 20px rgba(249,115,22,.3);
}
.btn-primary:hover {
  transform:translateY(-1px);
  box-shadow:0 6px 28px rgba(249,115,22,.5);
}
.btn-secondary {
  display:inline-flex; align-items:center; gap:7px;
  background:var(--surface2); color:var(--text);
  padding:10px 22px; border-radius:var(--radius-sm);
  font-weight:600; font-size:.88rem;
  border:1px solid var(--border); transition:all .2s;
}
.btn-secondary:hover { border-color:var(--muted); background:var(--surface3); }
.btn-sm { padding:6px 14px; font-size:.8rem; }
.btn-danger { background:var(--hard); color:#fff; box-shadow:none; }
.btn-danger:hover { background:#dc2626; }

/* ── Diff bars ──────────────────────────────────────────── */
.diff-row { display:flex; align-items:center; gap:10px; margin-bottom:8px; }
.diff-name { width:56px; font-size:.73rem; font-weight:700; text-transform:uppercase; letter-spacing:.04em; font-family:'JetBrains Mono',monospace; }
.diff-name.easy   { color:var(--easy);   }
.diff-name.medium { color:var(--medium); }
.diff-name.hard   { color:var(--hard);   }
.diff-track { flex:1; height:5px; background:var(--surface2); border-radius:10px; overflow:hidden; }
.diff-fill { height:100%; border-radius:10px; transition:width 1s ease; width:0%; }
.diff-fill.easy   { background:var(--easy);   }
.diff-fill.medium { background:var(--medium); }
.diff-fill.hard   { background:var(--hard);   }
.diff-count { font-family:'JetBrains Mono',monospace; font-size:.73rem; font-weight:600; color:var(--muted); min-width:30px; text-align:right; }

/* ── Animations ─────────────────────────────────────────── */
@keyframes fadeInUp   { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:none} }
@keyframes fadeInDown { from{opacity:0;transform:translateY(-12px)} to{opacity:1;transform:none} }
@keyframes fadeIn     { from{opacity:0} to{opacity:1} }
@keyframes scaleIn    { from{opacity:0;transform:scale(.9)} to{opacity:1;transform:none} }

.fade-in    { animation:fadeIn .35s ease both; }
.fade-in-up { animation:fadeInUp .4s ease both; }

/* ═══════════════════════════════════════════════════════
   DASHBOARD PAGE
   ══════════════════════════════════════════════════════ */

.dashboard-grid {
  display:grid;
  grid-template-columns:1fr 340px;
  gap:1.5rem;
  align-items:start;
}
.dashboard-main  { display:flex; flex-direction:column; gap:1.5rem; }
.dashboard-aside { display:flex; flex-direction:column; gap:1.5rem; }

/* readiness gauge */
.readiness-wrap {
  display:flex; flex-direction:column; align-items:center;
  padding:1.5rem;
}
.gauge-svg { overflow:visible; }
.gauge-track { fill:none; stroke:var(--surface2); }
.gauge-fill  { fill:none; stroke-linecap:round; transition:stroke-dashoffset .8s ease; }
.gauge-num {
  font-family:'JetBrains Mono',monospace;
  font-size:2rem; font-weight:800;
  fill:var(--text);
  dominant-baseline:middle; text-anchor:middle;
}
.gauge-label { fill:var(--muted); font-size:.65rem; dominant-baseline:middle; text-anchor:middle; }
.readiness-level {
  margin-top:.75rem;
  font-size:.8rem; font-weight:700;
  text-align:center;
  padding:4px 14px; border-radius:100px;
}

/* streak section */
.streak-stats {
  display:flex; gap:1.5rem;
  padding:1rem 1.5rem;
  border-top:1px solid var(--border);
  font-size:.82rem;
}
.streak-stat-val {
  font-family:'JetBrains Mono',monospace;
  font-weight:700; font-size:1.2rem;
  color:var(--accent);
}
.streak-stat-label { color:var(--muted); font-size:.72rem; }

/* heat grid */
.heat-grid-wrap {
  padding:1.25rem 1.5rem;
  overflow-x:auto;
}
.heat-grid {
  display:grid;
  grid-template-rows:repeat(7,13px);
  grid-auto-flow:column;
  gap:3px;
  width:max-content;
}
.heat-cell {
  width:13px; height:13px;
  border-radius:3px;
  background:var(--surface2);
  cursor:default;
  transition:opacity .15s;
  position:relative;
}
.heat-cell:hover { opacity:.8; }
.heat-cell[data-count="1"] { background:rgba(249,115,22,.35); }
.heat-cell[data-count="2"] { background:rgba(249,115,22,.6);  }
.heat-cell[data-count="3"] { background:rgba(249,115,22,.85); }
.heat-cell[data-count="4"] { background:var(--accent); }

/* due-today section */
.due-item {
  display:flex; align-items:center; gap:10px;
  padding:.75rem 1.5rem;
  border-bottom:1px solid var(--border);
  transition:background .15s;
}
.due-item:last-child { border-bottom:none; }
.due-item:hover { background:var(--surface2); }
.due-item-info { flex:1; min-width:0; }
.due-item-title { font-weight:600; font-size:.88rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.due-item-meta  { font-size:.73rem; color:var(--muted); margin-top:2px; }
.due-item-actions { display:flex; gap:6px; flex-shrink:0; }
.btn-solve {
  background:var(--accent-g); color:var(--accent);
  border:1px solid rgba(249,115,22,.3);
  padding:4px 12px; border-radius:6px;
  font-size:.75rem; font-weight:700;
  transition:all .2s;
}
.btn-solve:hover { background:var(--accent); color:#000; }
.empty-state {
  padding:2rem 1.5rem;
  text-align:center;
  color:var(--muted);
  font-size:.88rem;
}

/* daily recommendation */
.rec-slots { display:flex; flex-direction:column; gap:0; }
.rec-slot {
  display:flex; align-items:center; gap:12px;
  padding:1rem 1.5rem;
  border-bottom:1px solid var(--border);
}
.rec-slot:last-child { border-bottom:none; }
.rec-slot-icon { font-size:1.4rem; flex-shrink:0; }
.rec-slot-info { flex:1; min-width:0; }
.rec-slot-label { font-size:.7rem; color:var(--muted); font-weight:700; text-transform:uppercase; letter-spacing:.05em; }
.rec-slot-title { font-size:.9rem; font-weight:700; margin-top:2px; }
.rec-slot-tag   { font-size:.73rem; color:var(--accent); }

/* ═══════════════════════════════════════════════════════
   PROGRESS PAGE
   ══════════════════════════════════════════════════════ */

.progress-grid {
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:1.5rem;
}
.progress-full { grid-column:1 / -1; }

/* radar chart */
.radar-wrap {
  display:flex; flex-direction:column; align-items:center;
  padding:1.5rem;
  gap:1rem;
}
.radar-svg { overflow:visible; }
.radar-polygon { transition:all .6s ease; }
.radar-axis-label {
  font-size:.65rem; font-weight:700;
  fill:var(--muted); text-anchor:middle;
  dominant-baseline:middle;
}
.weak-topics { width:100%; }
.weak-topics-title {
  font-size:.72rem; font-weight:700; color:var(--muted);
  text-transform:uppercase; letter-spacing:.05em;
  margin-bottom:.6rem;
}
.weak-row {
  display:flex; align-items:center; gap:8px;
  margin-bottom:6px;
}
.weak-label { font-size:.78rem; font-weight:600; flex:1; text-transform:capitalize; }
.weak-pct   { font-family:'JetBrains Mono',monospace; font-size:.73rem; color:var(--muted); }

/* solve history */
.history-list { display:flex; flex-direction:column; gap:0; }
.history-day {
  display:flex; align-items:center; gap:10px;
  padding:.6rem 1.5rem;
  border-bottom:1px solid var(--border);
  font-size:.82rem;
}
.history-day:last-child { border-bottom:none; }
.history-date { font-family:'JetBrains Mono',monospace; color:var(--muted); width:90px; flex-shrink:0; }
.history-slugs { flex:1; min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; color:var(--muted); }
.history-count { font-family:'JetBrains Mono',monospace; font-weight:700; color:var(--accent); }

/* ═══════════════════════════════════════════════════════
   REVIEW PAGE
   ══════════════════════════════════════════════════════ */

.review-list { display:flex; flex-direction:column; }
.review-item {
  display:flex; align-items:center; gap:12px;
  padding:1rem 1.5rem;
  border-bottom:1px solid var(--border);
  transition:background .15s;
}
.review-item:last-child { border-bottom:none; }
.review-item:hover { background:var(--surface2); }
.review-item-info { flex:1; min-width:0; }
.review-item-title { font-weight:700; font-size:.92rem; }
.review-item-meta  { font-size:.73rem; color:var(--muted); margin-top:3px; }
.review-item-due   { font-size:.73rem; color:var(--hard); }
.review-item-actions { display:flex; gap:6px; align-items:center; }

/* rating section (inline) */
.rating-inline {
  display:flex; gap:4px;
}
.ri-btn {
  width:32px; height:32px;
  border-radius:6px;
  border:1px solid var(--border);
  background:var(--surface2);
  font-size:.78rem; font-weight:700;
  font-family:'JetBrains Mono',monospace;
  transition:all .15s;
  display:flex; align-items:center; justify-content:center;
}
.ri-btn:hover { border-color:var(--accent); color:var(--accent); }
.ri-btn[data-r="1"]:hover { border-color:var(--hard); color:var(--hard); }
.ri-btn[data-r="5"]:hover { border-color:var(--easy); color:var(--easy); }

/* ═══════════════════════════════════════════════════════
   STUDY PATHS PAGE
   ══════════════════════════════════════════════════════ */

.path-tabs {
  display:flex; gap:0;
  border:1px solid var(--border);
  border-radius:var(--radius-sm);
  overflow:hidden;
  margin-bottom:1.5rem;
  width:fit-content;
}
.path-tab {
  padding:8px 20px;
  font-size:.83rem; font-weight:700;
  background:var(--surface); color:var(--muted);
  border:none; border-right:1px solid var(--border);
  transition:all .2s;
}
.path-tab:last-child { border-right:none; }
.path-tab.active { background:var(--accent); color:#000; }
.path-tab:hover:not(.active) { background:var(--surface2); color:var(--text); }

.path-progress-bar-row {
  display:flex; align-items:center; gap:12px;
  margin-bottom:1.5rem;
}
.path-bar-track {
  flex:1; height:8px;
  background:var(--surface2); border-radius:10px; overflow:hidden;
}
.path-bar-fill {
  height:100%; border-radius:10px;
  background:var(--accent);
  transition:width .8s ease;
}
.path-pct {
  font-family:'JetBrains Mono',monospace;
  font-size:.8rem; font-weight:700; color:var(--accent);
  min-width:48px; text-align:right;
}

.path-section-title {
  font-size:.75rem; font-weight:700;
  color:var(--muted); text-transform:uppercase;
  letter-spacing:.06em;
  padding:.75rem 1.5rem .5rem;
  background:var(--surface2);
  border-top:1px solid var(--border);
  border-bottom:1px solid var(--border);
  display:flex; align-items:center; gap:8px;
}
.path-section-done { color:var(--easy); }

.path-problem-row {
  display:flex; align-items:center; gap:12px;
  padding:.65rem 1.5rem;
  border-bottom:1px solid var(--border);
  cursor:pointer;
  transition:background .15s;
}
.path-problem-row:last-child { border-bottom:none; }
.path-problem-row:hover { background:var(--surface2); }
.path-problem-row.solved .path-prob-title { text-decoration:line-through; color:var(--muted); }

.path-checkbox {
  width:17px; height:17px; flex-shrink:0;
  border-radius:4px; border:2px solid var(--border);
  background:var(--surface2);
  display:flex; align-items:center; justify-content:center;
  font-size:.7rem; color:transparent;
  transition:all .2s;
}
.path-problem-row.solved .path-checkbox {
  background:var(--easy); border-color:var(--easy); color:#000;
}
.path-prob-title { flex:1; font-size:.88rem; font-weight:600; }
.path-prob-note-btn {
  background:none; border:none; color:var(--muted);
  font-size:14px; padding:2px 6px;
  transition:color .2s;
}
.path-prob-note-btn:hover { color:var(--accent); }

/* ═══════════════════════════════════════════════════════
   BADGES PAGE
   ══════════════════════════════════════════════════════ */

.badges-grid {
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(190px,1fr));
  gap:1rem;
  padding:1.5rem;
}

.badge-card {
  background:var(--surface2);
  border:1px solid var(--border);
  border-radius:var(--radius);
  padding:1.25rem;
  text-align:center;
  transition:all .2s;
  position:relative;
  overflow:hidden;
}
.badge-card.earned {
  border-color:rgba(249,115,22,.35);
  background:linear-gradient(135deg,rgba(249,115,22,.08),var(--surface2));
}
.badge-card:not(.earned) { opacity:.45; filter:grayscale(1); }
.badge-card.earned:hover { transform:translateY(-2px); box-shadow:0 8px 24px rgba(249,115,22,.15); }

.badge-icon    { font-size:2.2rem; margin-bottom:.6rem; }
.badge-name    { font-size:.82rem; font-weight:700; margin-bottom:.3rem; }
.badge-desc    { font-size:.72rem; color:var(--muted); }
.badge-date    { font-size:.68rem; color:var(--accent); margin-top:.4rem; font-family:'JetBrains Mono',monospace; }

/* Badge popup toast */
.badge-popup {
  position:fixed; bottom:2rem; right:2rem; z-index:500;
  background:var(--surface);
  border:1px solid rgba(249,115,22,.4);
  border-radius:var(--radius);
  padding:1rem 1.25rem;
  box-shadow:0 8px 40px rgba(0,0,0,.5);
  animation:slideInRight .4s ease forwards;
  max-width:280px;
}
.badge-popup-inner { display:flex; align-items:center; gap:12px; }
.badge-popup-icon  { font-size:2rem; flex-shrink:0; }
.badge-popup-label { font-size:.7rem; color:var(--accent); font-weight:700; text-transform:uppercase; letter-spacing:.05em; }
.badge-popup-name  { font-size:.92rem; font-weight:700; }

@keyframes slideInRight {
  from { opacity:0; transform:translateX(60px); }
  to   { opacity:1; transform:none; }
}

/* ═══════════════════════════════════════════════════════
   SETTINGS PAGE
   ══════════════════════════════════════════════════════ */

.settings-section { margin-bottom:2rem; }
.settings-section-title {
  font-size:.75rem; font-weight:700;
  color:var(--muted); text-transform:uppercase;
  letter-spacing:.06em; margin-bottom:1rem;
  padding-bottom:.5rem; border-bottom:1px solid var(--border);
}

.setting-row {
  display:flex; align-items:center; gap:12px;
  padding:.75rem 0;
  border-bottom:1px solid var(--border);
}
.setting-row:last-child { border-bottom:none; }
.setting-label { flex:1; font-size:.88rem; font-weight:600; }
.setting-desc  { font-size:.76rem; color:var(--muted); }

.setting-input {
  background:var(--surface2);
  border:1px solid var(--border);
  color:var(--text);
  padding:8px 12px; border-radius:var(--radius-sm);
  font-size:.83rem; outline:none;
  min-width:160px;
  transition:border-color .2s;
}
.setting-input:focus { border-color:var(--accent); }

.storage-meter {
  margin-top:1rem;
  background:var(--surface2);
  border:1px solid var(--border);
  border-radius:var(--radius-sm);
  padding:1rem;
}
.storage-bar-track { height:8px; background:var(--surface3); border-radius:10px; overflow:hidden; margin:.5rem 0; }
.storage-bar-fill  { height:100%; border-radius:10px; background:var(--accent); transition:width .6s ease; }
.storage-meta { font-size:.75rem; color:var(--muted); display:flex; justify-content:space-between; }

/* ═══════════════════════════════════════════════════════
   PROFILE CARD (shared URL)
   ══════════════════════════════════════════════════════ */

.profile-card-wrap {
  display:flex; justify-content:center; padding:2rem 1rem;
}
.profile-card {
  background:var(--surface);
  border:1px solid rgba(249,115,22,.3);
  border-radius:20px;
  padding:2rem;
  max-width:380px; width:100%;
  text-align:center;
  position:relative;
}
.profile-card::after {
  content:'LeetDash';
  position:absolute; bottom:1rem; right:1.25rem;
  font-size:.65rem; color:var(--muted); opacity:.4;
  font-weight:700; letter-spacing:.06em;
}
.profile-card-user  { font-size:1.4rem; font-weight:800; margin-bottom:.3rem; }
.profile-card-score {
  font-size:4rem; font-weight:800;
  font-family:'JetBrains Mono',monospace;
  background:linear-gradient(135deg,var(--accent),#fbbf24);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  background-clip:text; margin:.5rem 0;
}
.profile-card-stats {
  display:flex; justify-content:center; gap:2rem;
  margin:1rem 0; font-size:.83rem; color:var(--muted);
}
.profile-card-stat-val { font-weight:800; color:var(--text); font-family:'JetBrains Mono',monospace; }
.profile-card-badges { display:flex; flex-wrap:wrap; gap:6px; justify-content:center; margin-top:1rem; }
.profile-badge-chip {
  font-size:.72rem; background:var(--surface2);
  border:1px solid var(--border); padding:3px 10px; border-radius:100px;
}

/* ═══════════════════════════════════════════════════════
   MODALS
   ══════════════════════════════════════════════════════ */

.modal {
  position:fixed; inset:0; z-index:300;
  display:flex; align-items:center; justify-content:center;
}
.modal.hidden { display:none; }

.modal-backdrop {
  position:absolute; inset:0;
  background:rgba(0,0,0,.65);
  backdrop-filter:blur(4px);
}
.modal-panel {
  position:relative; z-index:1;
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:20px;
  width:90%; max-width:540px;
  max-height:90vh; overflow-y:auto;
  animation:scaleIn .25s ease;
}
.modal-sm { max-width:380px; }

.modal-header {
  display:flex; align-items:center;
  padding:1.25rem 1.5rem;
  border-bottom:1px solid var(--border);
  gap:10px;
}
.modal-header h3 { font-size:1rem; font-weight:700; flex:1; }
.modal-actions { display:flex; align-items:center; gap:8px; margin-left:auto; }

.save-indicator { font-size:.72rem; color:var(--easy); font-family:'JetBrains Mono',monospace; }

.modal-body { padding:1.5rem; display:flex; flex-direction:column; gap:1rem; }

/* Note fields */
.note-field { display:flex; flex-direction:column; gap:6px; }
.note-field label { font-size:.75rem; font-weight:700; color:var(--muted); text-transform:uppercase; letter-spacing:.05em; }
.note-field textarea, .note-field input {
  background:var(--surface2);
  border:1px solid var(--border);
  color:var(--text); border-radius:var(--radius-sm);
  padding:10px 12px; font-size:.85rem;
  resize:vertical; outline:none;
  transition:border-color .2s;
}
.note-field textarea { min-height:90px; }
.note-field textarea:focus, .note-field input:focus { border-color:var(--accent); }
.char-count { font-size:.68rem; color:var(--muted); text-align:right; font-family:'JetBrains Mono',monospace; }

.note-row { display:grid; grid-template-columns:1fr 1fr; gap:10px; }

/* Star rating */
.star-rating { display:flex; gap:4px; }
.star {
  font-size:1.5rem; cursor:pointer;
  color:var(--border); transition:color .15s;
}
.star.active, .star:hover { color:#fbbf24; }

/* Solve modal */
.solve-subtitle { font-size:.85rem; color:var(--muted); margin-bottom:8px; }
.rating-buttons { display:flex; gap:6px; margin-bottom:1rem; flex-wrap:wrap; }
.rating-btn {
  flex:1; min-width:52px;
  display:flex; flex-direction:column; align-items:center;
  gap:3px; padding:10px 6px; border-radius:8px;
  border:1px solid var(--border); background:var(--surface2);
  font-size:1rem; font-weight:800; font-family:'JetBrains Mono',monospace;
  color:var(--text); transition:all .15s;
}
.rating-btn span { font-size:.62rem; font-weight:600; color:var(--muted); font-family:'Syne',sans-serif; }
.rating-btn.selected { border-color:var(--accent); background:var(--accent-g); color:var(--accent); }
.rating-btn:hover:not(.selected) { border-color:var(--muted); }

/* ═══════════════════════════════════════════════════════
   CONTEST CARDS
   ══════════════════════════════════════════════════════ */

.contest-list { display:flex; flex-direction:column; gap:1rem; padding:1.5rem; }
.contest-card {
  background:var(--surface2);
  border:1px solid var(--border);
  border-radius:var(--radius-sm);
  padding:1rem 1.25rem;
  display:flex; align-items:center; gap:1rem;
}
.contest-time-block { text-align:center; flex-shrink:0; min-width:70px; }
.contest-countdown { font-family:'JetBrains Mono',monospace; font-size:1rem; font-weight:700; color:var(--accent); }
.contest-countdown-label { font-size:.65rem; color:var(--muted); text-transform:uppercase; letter-spacing:.04em; }
.contest-info { flex:1; min-width:0; }
.contest-title { font-weight:700; font-size:.9rem; }
.contest-date  { font-size:.76rem; color:var(--muted); margin-top:2px; }
.contest-remind { background:none; border:1px solid var(--border); color:var(--muted); padding:5px 12px; border-radius:6px; font-size:.75rem; font-weight:600; transition:all .2s; }
.contest-remind.active { border-color:var(--accent); color:var(--accent); }
.contest-remind:hover  { border-color:var(--accent); color:var(--accent); }

/* ═══════════════════════════════════════════════════════
   COMPANY PREP
   ══════════════════════════════════════════════════════ */

.company-prep-bar {
  background:var(--surface2);
  border:1px solid rgba(249,115,22,.25);
  border-radius:var(--radius-sm);
  padding:1rem 1.5rem;
  display:flex; align-items:center; gap:12px;
  margin-bottom:1.5rem;
}
.company-tag { font-size:.75rem; font-weight:700; color:var(--accent); text-transform:uppercase; letter-spacing:.04em; }
.company-solved { font-family:'JetBrains Mono',monospace; font-size:.85rem; font-weight:700; }

/* ═══════════════════════════════════════════════════════
   RESPONSIVE
   ══════════════════════════════════════════════════════ */

@media (max-width:900px) {
  .dashboard-grid  { grid-template-columns:1fr; }
  .progress-grid   { grid-template-columns:1fr; }
}

@media (max-width:600px) {
  #app { padding:1.25rem 1rem 4rem; }
  #main-nav { padding:0 1rem; }
  .nav-links { display:none; }
  .page-title { font-size:1.3rem; }
  .badges-grid { grid-template-columns:repeat(2,1fr); }
  .rating-buttons { gap:4px; }
}
""".strip()

# ─── JS ─────────────────────────────────────────────────────────────────────
JS = r"""
/* ═══════════════════════════════════════════════════════════════════════════
   LeetDash — app.js
   Single-file SPA. localStorage only. No backend.
   ═══════════════════════════════════════════════════════════════════════════ */

'use strict';

/* ──────────────────────────────────────────────────────────────────────────
   1. CONSTANTS & CONFIG
   ────────────────────────────────────────────────────────────────────────── */

const LS = {
  SOLVE_LOG:    'ld:solveLog',
  REVIEW_QUEUE: 'ld:reviewQueue',
  NOTES:        'ld:notes',
  STREAK_META:  'ld:streakMeta',
  STUDY_PATHS:  'ld:studyPaths',
  BADGES:       'ld:badges',
  PREFS:        'ld:prefs',
};

const BADGE_DEFS = [
  { id:'first-solve',   name:'First Blood',       icon:'🩸', desc:'Solve your first problem'                },
  { id:'streak-7',      name:'Week Warrior',       icon:'🔥', desc:'7-day solving streak'                    },
  { id:'streak-30',     name:'Monthly Grinder',    icon:'💪', desc:'30-day solving streak'                   },
  { id:'streak-100',    name:'Century Streak',     icon:'🏆', desc:'100-day solving streak'                  },
  { id:'solved-50',     name:'Fifty Club',         icon:'5️⃣0️⃣', desc:'Solve 50 problems'                  },
  { id:'solved-100',    name:'Centurion',          icon:'💯', desc:'Solve 100 problems'                      },
  { id:'solved-250',    name:'Quarter Thousand',   icon:'🎯', desc:'Solve 250 problems'                      },
  { id:'solved-500',    name:'Five Hundred',       icon:'🚀', desc:'Solve 500 problems'                      },
  { id:'first-hard',    name:'Hard Mode',          icon:'💀', desc:'Solve your first hard problem'           },
  { id:'hard-10',       name:'Hard Hitter',        icon:'⚡', desc:'Solve 10 hard problems'                  },
  { id:'topic-master',  name:'Topic Master',       icon:'🧠', desc:'80%+ solve rate in any topic'            },
  { id:'blind75-done',  name:'Blind Completed',    icon:'👁', desc:'Complete the Blind 75 path'              },
  { id:'ready-70',      name:'Interview Ready',    icon:'💼', desc:'Readiness score ≥ 70'                    },
  { id:'ready-90',      name:'Dream Offer',        icon:'🌟', desc:'Readiness score ≥ 90'                    },
];

const RADAR_TOPICS = [
  'array','string','hash-table','dynamic-programming',
  'tree','graph','binary-search','two-pointers','stack','greedy',
];

const PATHS = ['blind75','neetcode150','grind169'];

/* ──────────────────────────────────────────────────────────────────────────
   2. DATE UTILITIES
   ────────────────────────────────────────────────────────────────────────── */

function today() {
  return new Date().toISOString().split('T')[0];
}

function addDays(dateStr, n) {
  const d = new Date(dateStr);
  d.setDate(d.getDate() + n);
  return d.toISOString().split('T')[0];
}

function daysAgo(n) {
  return addDays(today(), -n);
}

function daysBetween(a, b) {
  return Math.floor((new Date(b) - new Date(a)) / 86400000);
}

function fmtDate(dateStr) {
  const d = new Date(dateStr + 'T00:00:00');
  return d.toLocaleDateString('en-US', { month:'short', day:'numeric', year:'numeric' });
}

/* ──────────────────────────────────────────────────────────────────────────
   3. LOCALSTORAGE HELPERS
   ────────────────────────────────────────────────────────────────────────── */

function lsGet(key, fallback = {}) {
  try {
    const v = localStorage.getItem(key);
    return v === null ? fallback : (JSON.parse(v) ?? fallback);
  } catch { return fallback; }
}

function lsSet(key, value) {
  try { localStorage.setItem(key, JSON.stringify(value)); } catch(e) {
    console.warn('localStorage write failed:', e);
  }
}

function lsSize() {
  let total = 0;
  for (const k of Object.keys(localStorage)) {
    if (k.startsWith('ld:')) {
      total += (localStorage.getItem(k) || '').length * 2; // UTF-16
    }
  }
  return total; // bytes
}

/* ──────────────────────────────────────────────────────────────────────────
   4. STREAK COMPUTATION
   ────────────────────────────────────────────────────────────────────────── */

function computeStreak(solveLog) {
  const t = today();
  let current = 0, longest = 0, totalDays = 0, temp = 0;
  // total active days
  for (const d of Object.keys(solveLog)) {
    if ((solveLog[d] || []).length > 0) totalDays++;
  }
  // current streak (count back from today; allow yesterday too)
  let d = t;
  let started = false;
  for (let i = 0; i < 1000; i++) {
    const date = addDays(t, -i);
    const count = (solveLog[date] || []).length;
    if (count > 0) {
      started = true;
      current++;
      temp++;
      longest = Math.max(longest, temp);
    } else {
      if (!started) { temp = 0; continue; } // haven't started streak yet
      break;
    }
  }
  // scan all for longest
  const dates = Object.keys(solveLog).filter(d => (solveLog[d]||[]).length > 0).sort();
  temp = 0;
  for (let i = 0; i < dates.length; i++) {
    if (i === 0) { temp = 1; }
    else {
      const diff = daysBetween(dates[i-1], dates[i]);
      if (diff === 1) temp++;
      else temp = 1;
    }
    longest = Math.max(longest, temp);
  }
  const lastActiveDate = dates[dates.length-1] || null;
  return { currentStreak:current, longestStreak:longest, lastActiveDate, totalDays };
}

function updateStreakMeta(solveLog) {
  const meta = computeStreak(solveLog);
  lsSet(LS.STREAK_META, meta);
  return meta;
}

/* ──────────────────────────────────────────────────────────────────────────
   5. SM-2 SPACED REPETITION
   ────────────────────────────────────────────────────────────────────────── */

function sm2Update(item, rating) {
  if (rating <= 2) {
    item.interval = 1;
    item.ease = Math.max(1.3, item.ease - 0.2);
    item.reps = 0;
  } else {
    item.reps += 1;
    if (item.reps === 1)      item.interval = 1;
    else if (item.reps === 2) item.interval = 6;
    else item.interval = Math.round(item.interval * item.ease);
    if (rating === 5) item.ease = Math.min(3.0, item.ease + 0.1);
    if (rating === 3) item.ease = Math.max(1.3, item.ease - 0.14);
    item.ease = Math.max(1.3, item.ease);
  }
  item.lastSolved = today();
  item.nextReview = addDays(today(), item.interval);
  return item;
}

/* ──────────────────────────────────────────────────────────────────────────
   6. TOPIC RADAR
   ────────────────────────────────────────────────────────────────────────── */

function computeTopicRadar(solveLog, problems) {
  const allSolved = new Set(Object.values(solveLog).flat());
  const topicData = {};
  for (const p of problems) {
    for (const t of (p.topics || [])) {
      if (!topicData[t]) topicData[t] = { solved:0, total:0 };
      topicData[t].total++;
      if (allSolved.has(p.slug)) topicData[t].solved++;
    }
  }
  const result = {};
  for (const [t, d] of Object.entries(topicData)) {
    result[t] = d.total ? Math.round((d.solved / d.total) * 100) : 0;
  }
  return result;
}

/* ──────────────────────────────────────────────────────────────────────────
   7. READINESS SCORE
   ────────────────────────────────────────────────────────────────────────── */

function computeReadiness(solveLog, reviewQueue, problems) {
  const allSolvedArr = Object.values(solveLog).flat();
  const allSolved    = new Set(allSolvedArr);
  const totalSolved  = allSolved.size;

  // Component A — volume (40)
  const compA = Math.min(totalSolved / 300, 1) * 40;

  // Component B — difficulty spread (20)
  let easy=0, medium=0, hard=0;
  for (const slug of allSolved) {
    const p = problems.find(x => x.slug === slug);
    if (!p) continue;
    if (p.difficulty === 'easy')   easy++;
    if (p.difficulty === 'medium') medium++;
    if (p.difficulty === 'hard')   hard++;
  }
  const weightedSum = easy*0.3 + medium*0.5 + hard*1.0;
  const compB = totalSolved > 0 ? Math.min(weightedSum / totalSolved, 1) * 20 : 0;

  // Component C — topic breadth (20)
  const radar  = computeTopicRadar(solveLog, problems);
  const topics = RADAR_TOPICS;
  const covered = topics.filter(t => (radar[t] || 0) >= 10).length;
  const compC = (covered / topics.length) * 20;

  // Component D — recency (10)
  const meta = lsGet(LS.STREAK_META, {});
  const lastDate = meta.lastActiveDate || '';
  const daysSince = lastDate ? daysBetween(lastDate, today()) : 999;
  const compD = daysSince < 7 ? 10 : Math.max(0, 10 - daysSince);

  // Component E — review health (10)
  const t = today();
  const queueEntries = Object.values(reviewQueue);
  const overdue = queueEntries.filter(d => d.nextReview <= t).length;
  const total   = queueEntries.length;
  const compE = total > 0 ? (1 - overdue/total) * 10 : 10;

  const score = Math.round(compA + compB + compC + compD + compE);
  return { score, compA, compB, compC, compD, compE };
}

function readinessLevel(score) {
  if (score >= 90) return { label:'Dream Offer Territory', color:'#22c55e' };
  if (score >= 70) return { label:'Interview Ready — Senior', color:'#22c55e' };
  if (score >= 55) return { label:'Interview Ready — Mid-level', color:'#f59e0b' };
  if (score >= 40) return { label:'Intern / Entry Level', color:'#f97316' };
  return { label:'Keep Grinding', color:'#ef4444' };
}

/* ──────────────────────────────────────────────────────────────────────────
   8. BADGE EVALUATION
   ────────────────────────────────────────────────────────────────────────── */

function checkBadges(problems, silent = false) {
  const solveLog    = lsGet(LS.SOLVE_LOG);
  const streakMeta  = lsGet(LS.STREAK_META, {});
  const reviewQueue = lsGet(LS.REVIEW_QUEUE);
  const studyPaths  = lsGet(LS.STUDY_PATHS);
  const badges      = lsGet(LS.BADGES);

  const allSolved     = new Set(Object.values(solveLog).flat());
  const totalSolved   = allSolved.size;
  const currentStreak = streakMeta.currentStreak || 0;

  const hardsSolved = [...allSolved].filter(s => {
    const p = problems.find(x => x.slug === s);
    return p && p.difficulty === 'hard';
  }).length;

  const radar   = computeTopicRadar(solveLog, problems);
  const topicAt80 = Object.values(radar).some(v => v >= 80);

  const blind75done = (() => {
    const bp = studyPaths['blind75'];
    return bp && bp.total && bp.completed.length >= bp.total;
  })();

  const { score } = computeReadiness(solveLog, reviewQueue, problems);

  const conditions = {
    'first-solve':  totalSolved >= 1,
    'streak-7':     currentStreak >= 7,
    'streak-30':    currentStreak >= 30,
    'streak-100':   currentStreak >= 100,
    'solved-50':    totalSolved >= 50,
    'solved-100':   totalSolved >= 100,
    'solved-250':   totalSolved >= 250,
    'solved-500':   totalSolved >= 500,
    'first-hard':   hardsSolved >= 1,
    'hard-10':      hardsSolved >= 10,
    'topic-master': topicAt80,
    'blind75-done': blind75done,
    'ready-70':     score >= 70,
    'ready-90':     score >= 90,
  };

  const newlyEarned = [];
  const t = today();
  for (const [id, met] of Object.entries(conditions)) {
    if (met && !badges[id]) {
      badges[id] = { earned: t };
      newlyEarned.push(id);
    }
  }

  if (newlyEarned.length) {
    lsSet(LS.BADGES, badges);
    if (!silent) {
      let i = 0;
      const showNext = () => {
        if (i < newlyEarned.length) {
          showBadgePopup(newlyEarned[i++]);
          setTimeout(showNext, 3200);
        }
      };
      showNext();
    }
  }

  return badges;
}

/* ──────────────────────────────────────────────────────────────────────────
   9. CORE — onProblemSolved
   ────────────────────────────────────────────────────────────────────────── */

function addToSolveLog(slug) {
  const t = today();
  const log = lsGet(LS.SOLVE_LOG);
  if (!log[t]) log[t] = [];
  if (!log[t].includes(slug)) log[t].push(slug);
  lsSet(LS.SOLVE_LOG, log);
  return log;
}

function onProblemSolved(slug, rating = 3) {
  // 1. Solve log
  const log = addToSolveLog(slug);

  // 2. Spaced repetition
  const queue = lsGet(LS.REVIEW_QUEUE);
  if (!queue[slug]) queue[slug] = { ease:2.5, interval:1, reps:0 };
  sm2Update(queue[slug], rating);
  lsSet(LS.REVIEW_QUEUE, queue);

  // 3. Streak meta
  updateStreakMeta(log);

  // 4. Badges (after all state updated)
  checkBadges(App.problems);

  // 5. Auto-backup reminder milestones
  const allSolved = new Set(Object.values(log).flat()).size;
  const meta = lsGet(LS.STREAK_META, {});
  if (allSolved === 500 || meta.currentStreak === 100) {
    setTimeout(() => exportData(true), 1200);
  }

  // 6. Re-render whatever page is active
  App.render();
}

/* ──────────────────────────────────────────────────────────────────────────
   10. EXPORT / IMPORT
   ────────────────────────────────────────────────────────────────────────── */

function exportData(silent = false) {
  const out = {};
  for (const k of Object.values(LS)) {
    const v = localStorage.getItem(k);
    if (v) out[k] = JSON.parse(v);
  }
  const blob = new Blob([JSON.stringify(out, null, 2)], { type:'application/json' });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href = url;
  a.download = `leetdash-backup-${today()}.json`;
  a.click();
  URL.revokeObjectURL(url);
  // update last backup date
  const prefs = lsGet(LS.PREFS, {});
  prefs.lastBackupReminder = today();
  lsSet(LS.PREFS, prefs);
  if (!silent) toast('Backup downloaded ✓');
}

function importData(file) {
  const reader = new FileReader();
  reader.onload = e => {
    try {
      const data = JSON.parse(e.target.result);
      const valid = Object.keys(data).every(k => k.startsWith('ld:'));
      if (!valid) { toast('Invalid backup file — keys must start with ld:', 'error'); return; }
      for (const [k, v] of Object.entries(data)) {
        lsSet(k, v);
      }
      toast('Restore complete. Reloading…');
      setTimeout(() => window.location.reload(), 1000);
    } catch {
      toast('Failed to parse backup file', 'error');
    }
  };
  reader.readAsText(file);
}

/* ──────────────────────────────────────────────────────────────────────────
   11. CONTEST API
   ────────────────────────────────────────────────────────────────────────── */

const CONTEST_QUERY = `query { topTwoContests { title startTime duration titleSlug } }`;

async function fetchContests() {
  try {
    const r = await fetch('https://leetcode.com/graphql', {
      method:'POST',
      headers:{ 'Content-Type':'application/json' },
      body: JSON.stringify({ query: CONTEST_QUERY }),
    });
    const json = await r.json();
    return json?.data?.topTwoContests || [];
  } catch { return []; }
}

/* ──────────────────────────────────────────────────────────────────────────
   12. SHARE URL
   ────────────────────────────────────────────────────────────────────────── */

function generateShareURL() {
  const solveLog    = lsGet(LS.SOLVE_LOG);
  const streakMeta  = lsGet(LS.STREAK_META, {});
  const reviewQueue = lsGet(LS.REVIEW_QUEUE);
  const badges      = lsGet(LS.BADGES);
  const prefs       = lsGet(LS.PREFS, {});
  const allSolved   = new Set(Object.values(solveLog).flat()).size;
  const { score }   = computeReadiness(solveLog, reviewQueue, App.problems);
  const payload = {
    u: prefs.lcUsername || 'Anonymous',
    s: allSolved,
    streak: streakMeta.currentStreak || 0,
    score,
    badges: Object.keys(badges),
  };
  const encoded = btoa(unescape(encodeURIComponent(JSON.stringify(payload))));
  const url = `${location.origin}${location.pathname}#/profile?s=${encoded}`;
  navigator.clipboard?.writeText(url).then(() => toast('Share URL copied ✓')).catch(() => {
    prompt('Copy your share URL:', url);
  });
}

function parseSharedProfile() {
  const hash = location.hash; // e.g. #/profile?s=...
  const m = hash.match(/[?&]s=([^&]+)/);
  if (!m) return null;
  try {
    return JSON.parse(decodeURIComponent(escape(atob(m[1]))));
  } catch { return null; }
}

/* ──────────────────────────────────────────────────────────────────────────
   13. NOTES MODAL
   ────────────────────────────────────────────────────────────────────────── */

let notesSlug = null;
let notesSaveTimer = null;
let notesRating = 0;

function openNotes(slug, title) {
  notesSlug = slug;
  const notes = lsGet(LS.NOTES);
  const n = notes[slug] || {};
  document.getElementById('notes-modal-title').textContent = title || slug;
  document.getElementById('note-approach').value = n.approach || '';
  document.getElementById('note-time').value     = n.time     || '';
  document.getElementById('note-space').value    = n.space    || '';
  document.getElementById('note-gotcha').value   = n.note     || '';
  notesRating = n.rating || 0;
  renderNoteStars(notesRating);
  updateCharCount('note-approach', 'approach-count');
  updateCharCount('note-gotcha',   'gotcha-count');
  document.getElementById('notes-modal').classList.remove('hidden');
  document.getElementById('notes-save-indicator').textContent = n.updatedAt ? `Saved ${n.updatedAt}` : '';
}

function closeNotes() {
  document.getElementById('notes-modal').classList.add('hidden');
  notesSlug = null;
}

function saveNote() {
  if (!notesSlug) return;
  const notes = lsGet(LS.NOTES);
  if (!notes[notesSlug]) notes[notesSlug] = {};
  notes[notesSlug].approach  = document.getElementById('note-approach').value;
  notes[notesSlug].time      = document.getElementById('note-time').value;
  notes[notesSlug].space     = document.getElementById('note-space').value;
  notes[notesSlug].note      = document.getElementById('note-gotcha').value;
  notes[notesSlug].rating    = notesRating;
  notes[notesSlug].updatedAt = today();
  lsSet(LS.NOTES, notes);
  document.getElementById('notes-save-indicator').textContent = 'Saved ✓';
  setTimeout(() => {
    const el = document.getElementById('notes-save-indicator');
    if (el) el.textContent = '';
  }, 2000);
}

function debouncedSave() {
  clearTimeout(notesSaveTimer);
  notesSaveTimer = setTimeout(saveNote, 500);
}

function updateCharCount(inputId, countId) {
  const el  = document.getElementById(inputId);
  const cnt = document.getElementById(countId);
  if (el && cnt) cnt.textContent = `${el.value.length} / 2000`;
}

function renderNoteStars(val) {
  document.querySelectorAll('#note-stars .star').forEach(s => {
    s.classList.toggle('active', parseInt(s.dataset.v) <= val);
  });
}

/* ──────────────────────────────────────────────────────────────────────────
   14. SOLVE MODAL
   ────────────────────────────────────────────────────────────────────────── */

let solveModalSlug = null;
let solveModalRating = 3;
let solveModalCb = null;

function openSolveModal(slug, title, cb) {
  solveModalSlug   = slug;
  solveModalRating = 3;
  solveModalCb     = cb || null;
  document.getElementById('solve-modal-title').textContent = `Mark Solved — ${title || slug}`;
  document.querySelectorAll('.rating-btn').forEach(b => {
    b.classList.toggle('selected', parseInt(b.dataset.r) === 3);
  });
  document.getElementById('solve-modal').classList.remove('hidden');
}

function closeSolveModal() {
  document.getElementById('solve-modal').classList.add('hidden');
  solveModalSlug = null;
}

/* ──────────────────────────────────────────────────────────────────────────
   15. BADGE POPUP
   ────────────────────────────────────────────────────────────────────────── */

let _popupTimer = null;

function showBadgePopup(badgeId) {
  const def = BADGE_DEFS.find(b => b.id === badgeId);
  if (!def) return;
  const popup = document.getElementById('badge-popup');
  document.getElementById('badge-popup-icon').textContent = def.icon;
  document.getElementById('badge-popup-name').textContent = def.name;
  popup.classList.remove('hidden');
  clearTimeout(_popupTimer);
  _popupTimer = setTimeout(() => popup.classList.add('hidden'), 3000);
}

/* ──────────────────────────────────────────────────────────────────────────
   16. TOAST
   ────────────────────────────────────────────────────────────────────────── */

function toast(msg, type = 'success') {
  let el = document.getElementById('ld-toast');
  if (!el) {
    el = document.createElement('div');
    el.id = 'ld-toast';
    el.style.cssText = `
      position:fixed;bottom:1.5rem;left:50%;transform:translateX(-50%);
      background:var(--surface);border:1px solid var(--border);
      color:var(--text);padding:10px 20px;border-radius:10px;
      font-size:.83rem;font-weight:600;z-index:600;
      box-shadow:0 4px 24px rgba(0,0,0,.4);
      transition:opacity .3s;
    `;
    document.body.appendChild(el);
  }
  el.textContent = msg;
  el.style.borderColor = type === 'error' ? 'var(--hard)' : 'var(--easy)';
  el.style.opacity = '1';
  clearTimeout(el._t);
  el._t = setTimeout(() => { el.style.opacity = '0'; }, 2500);
}

/* ──────────────────────────────────────────────────────────────────────────
   17. RENDERING HELPERS
   ────────────────────────────────────────────────────────────────────────── */

function diffBadge(difficulty) {
  const cls = difficulty === 'easy' ? 'badge-easy' : difficulty === 'medium' ? 'badge-medium' : 'badge-hard';
  return `<span class="badge ${cls}">${difficulty}</span>`;
}

function problemLink(slug, title) {
  return `<a href="https://leetcode.com/problems/${slug}/" target="_blank" rel="noopener">${title}</a>`;
}

/* ──────────────────────────────────────────────────────────────────────────
   18. PAGE — DASHBOARD
   ────────────────────────────────────────────────────────────────────────── */

function renderDashboard() {
  const solveLog    = lsGet(LS.SOLVE_LOG);
  const reviewQueue = lsGet(LS.REVIEW_QUEUE);
  const streakMeta  = lsGet(LS.STREAK_META, { currentStreak:0, longestStreak:0, totalDays:0 });
  const prefs       = lsGet(LS.PREFS, {});
  const problems    = App.problems;

  // due reviews
  const t = today();
  const due = Object.entries(reviewQueue)
    .filter(([,d]) => d.nextReview <= t)
    .sort((a,b) => a[1].nextReview.localeCompare(b[1].nextReview));

  // readiness
  const { score } = computeReadiness(solveLog, reviewQueue, problems);
  const lvl = readinessLevel(score);

  // daily recommendation
  const radar    = computeTopicRadar(solveLog, problems);
  const allSolved = new Set(Object.values(solveLog).flat());
  const sortedTopics = RADAR_TOPICS.slice().sort((a,b) => (radar[a]||0) - (radar[b]||0));
  let newProblem = null;
  for (const topic of sortedTopics) {
    newProblem = problems.find(p => p.topics.includes(topic) && !allSolved.has(p.slug));
    if (newProblem) break;
  }
  const dueTodayFirst = due[0];

  // company prep
  const companyBar = (() => {
    const company = prefs.targetCompany;
    if (!company || !App.companyTags[company]) return '';
    const slugs     = App.companyTags[company];
    const solvedN   = slugs.filter(s => allSolved.has(s)).length;
    return `<div class="company-prep-bar">
      <div>
        <div class="company-tag">🎯 ${company.toUpperCase()} Prep</div>
        <div class="company-solved">${solvedN} / ${slugs.length} tagged problems</div>
      </div>
      <div style="flex:1;margin:0 12px">
        <div class="path-bar-track"><div class="path-bar-fill" style="width:${Math.round(solvedN/slugs.length*100)}%"></div></div>
      </div>
      <span style="font-family:'JetBrains Mono',monospace;font-size:.8rem;color:var(--accent);font-weight:700">
        ${Math.round(solvedN/slugs.length*100)}%
      </span>
    </div>`;
  })();

  // heat grid (364 days = 52 cols × 7 rows)
  const cells = [];
  for (let i = 363; i >= 0; i--) {
    const d = daysAgo(i);
    const cnt = Math.min((solveLog[d] || []).length, 4);
    cells.push(`<div class="heat-cell" data-count="${cnt}" title="${fmtDate(d)} — ${(solveLog[d]||[]).length} solved"></div>`);
  }

  // due list
  const dueHtml = due.length === 0
    ? `<div class="empty-state">✓ All caught up — no reviews due today</div>`
    : due.slice(0,8).map(([slug, d]) => {
        const p = problems.find(x => x.slug === slug);
        const title = p ? p.title : slug;
        const diff  = p ? p.difficulty : '';
        const days = d.lastSolved ? daysBetween(d.lastSolved, today()) : '?';
        return `<div class="due-item">
          <div class="due-item-info">
            <div class="due-item-title">${problemLink(slug, title)}</div>
            <div class="due-item-meta">${diffBadge(diff)} · Last solved ${days}d ago · interval ${d.interval}d</div>
          </div>
          <div class="due-item-actions">
            <button class="btn-solve" onclick="openSolveModal('${slug}','${title.replace(/'/g,"\\'")}')">Review</button>
            <button class="icon-btn btn-sm" onclick="openNotes('${slug}','${title.replace(/'/g,"\\'")}')">📝</button>
          </div>
        </div>`;
      }).join('') + (due.length > 8 ? `<div class="empty-state">${due.length - 8} more due — <a href="#/review">see all →</a></div>` : '');

  // gauge SVG
  const gaugeColor = score >= 70 ? '#22c55e' : score >= 40 ? '#f59e0b' : '#ef4444';
  const r = 52, circ = 2 * Math.PI * r;
  const dash = circ * (score / 100);
  const gaugeSvg = `<svg class="gauge-svg" width="140" height="140" viewBox="0 0 140 140">
    <circle class="gauge-track" cx="70" cy="70" r="${r}" stroke-width="10"/>
    <circle class="gauge-fill" cx="70" cy="70" r="${r}" stroke="${gaugeColor}" stroke-width="10"
      stroke-dasharray="${dash} ${circ - dash}"
      stroke-dashoffset="${circ * 0.25}"
      transform="rotate(-90 70 70)"/>
    <text class="gauge-num" x="70" y="68" style="font-family:'JetBrains Mono',monospace;font-size:22px;font-weight:800;fill:var(--text);dominant-baseline:middle;text-anchor:middle">${score}</text>
    <text x="70" y="88" style="font-size:9px;fill:var(--muted);dominant-baseline:middle;text-anchor:middle">/ 100</text>
  </svg>`;

  // rec slots
  const recHtml = `<div class="rec-slots">
    ${newProblem ? `<div class="rec-slot">
      <div class="rec-slot-icon">📚</div>
      <div class="rec-slot-info">
        <div class="rec-slot-label">New · Weakest Topic</div>
        <div class="rec-slot-title">${problemLink(newProblem.slug, newProblem.title)}</div>
        <div class="rec-slot-tag">${sortedTopics[0].replace('-',' ')}</div>
      </div>
      ${diffBadge(newProblem.difficulty)}
      <button class="btn-solve" onclick="openSolveModal('${newProblem.slug}','${newProblem.title.replace(/'/g,"\\'")}')">Solve</button>
    </div>` : ''}
    ${dueTodayFirst ? (() => {
      const [slug, d] = dueTodayFirst;
      const p = problems.find(x => x.slug === slug);
      const title = p ? p.title : slug;
      return `<div class="rec-slot">
        <div class="rec-slot-icon">🔁</div>
        <div class="rec-slot-info">
          <div class="rec-slot-label">Review · Due Today</div>
          <div class="rec-slot-title">${problemLink(slug, title)}</div>
        </div>
        ${p ? diffBadge(p.difficulty) : ''}
        <button class="btn-solve" onclick="openSolveModal('${slug}','${(title).replace(/'/g,"\\'")}')">Review</button>
      </div>`;
    })() : `<div class="rec-slot"><div class="rec-slot-icon">✅</div><div class="rec-slot-info"><div class="rec-slot-title" style="color:var(--muted)">No reviews due today</div></div></div>`}
  </div>`;

  return `
    <div class="page-header fade-in-up">
      <div class="page-title">Dashboard</div>
      <div class="page-subtitle">${today()}</div>
    </div>
    ${companyBar}
    <div class="dashboard-grid">
      <div class="dashboard-main">

        <div class="card fade-in-up">
          <div class="card-header">
            <span class="card-icon">🔥</span>
            <h2>Streak & Activity</h2>
          </div>
          <div class="heat-grid-wrap">
            <div class="heat-grid">${cells.join('')}</div>
          </div>
          <div class="streak-stats">
            <div>
              <div class="streak-stat-val">${streakMeta.currentStreak || 0}</div>
              <div class="streak-stat-label">Current Streak</div>
            </div>
            <div>
              <div class="streak-stat-val">${streakMeta.longestStreak || 0}</div>
              <div class="streak-stat-label">Longest</div>
            </div>
            <div>
              <div class="streak-stat-val">${streakMeta.totalDays || 0}</div>
              <div class="streak-stat-label">Active Days</div>
            </div>
            <div>
              <div class="streak-stat-val">${allSolved.size}</div>
              <div class="streak-stat-label">Total Solved</div>
            </div>
          </div>
        </div>

        <div class="card fade-in-up">
          <div class="card-header">
            <span class="card-icon">📅</span>
            <h2>Due for Review</h2>
            <span class="card-header-right" style="font-family:'JetBrains Mono',monospace;font-size:.75rem;color:var(--accent)">${due.length} due</span>
          </div>
          ${dueHtml}
        </div>

        <div class="card fade-in-up">
          <div class="card-header">
            <span class="card-icon">💡</span>
            <h2>Today's Focus</h2>
          </div>
          ${recHtml}
        </div>

      </div>
      <div class="dashboard-aside">

        <div class="card fade-in-up">
          <div class="card-header">
            <span class="card-icon">📊</span>
            <h2>Interview Readiness</h2>
          </div>
          <div class="readiness-wrap">
            ${gaugeSvg}
            <div class="readiness-level" style="background:${gaugeColor}22;color:${gaugeColor};border:1px solid ${gaugeColor}44">
              ${lvl.label}
            </div>
          </div>
          <div style="padding:0 1.5rem 1.25rem">
            ${['easy','medium','hard'].map(d => {
              const cnt = [...allSolved].filter(s => {
                const p = problems.find(x => x.slug === s);
                return p && p.difficulty === d;
              }).length;
              const tot = problems.filter(p => p.difficulty === d).length;
              const pct = tot ? Math.round(cnt/tot*100) : 0;
              return `<div class="diff-row">
                <span class="diff-name ${d}">${d}</span>
                <div class="diff-track"><div class="diff-fill ${d}" style="width:${pct}%"></div></div>
                <span class="diff-count">${cnt}</span>
              </div>`;
            }).join('')}
          </div>
        </div>

        <div class="card fade-in-up" id="contest-card">
          <div class="card-header">
            <span class="card-icon">🏆</span>
            <h2>Upcoming Contests</h2>
          </div>
          <div id="contest-list" class="contest-list">
            <div class="empty-state">Loading contests…</div>
          </div>
        </div>

      </div>
    </div>`;
}

/* ──────────────────────────────────────────────────────────────────────────
   19. PAGE — PROGRESS
   ────────────────────────────────────────────────────────────────────────── */

function renderProgress() {
  const solveLog    = lsGet(LS.SOLVE_LOG);
  const reviewQueue = lsGet(LS.REVIEW_QUEUE);
  const problems    = App.problems;
  const allSolved   = new Set(Object.values(solveLog).flat());

  const radar = computeTopicRadar(solveLog, problems);
  const topicPcts = RADAR_TOPICS.map(t => radar[t] || 0);

  // SVG radar
  const CX=140, CY=140, RMAX=110, N=RADAR_TOPICS.length;
  const pts = topicPcts.map((pct, i) => {
    const angle = (i / N) * 2 * Math.PI - Math.PI/2;
    const r = RMAX * (pct/100);
    return [CX + r*Math.cos(angle), CY + r*Math.sin(angle)];
  });
  const polyPts = pts.map(p => p.join(',')).join(' ');

  // rings
  const rings = [25,50,75,100].map(pct => {
    const rpts = RADAR_TOPICS.map((_,i) => {
      const angle = (i/N)*2*Math.PI - Math.PI/2;
      const r = RMAX*(pct/100);
      return `${CX+r*Math.cos(angle)},${CY+r*Math.sin(angle)}`;
    }).join(' ');
    return `<polygon points="${rpts}" fill="none" stroke="var(--border)" stroke-width="1"/>`;
  }).join('');

  // axes + labels
  const axes = RADAR_TOPICS.map((t, i) => {
    const angle = (i/N)*2*Math.PI - Math.PI/2;
    const x2 = CX + RMAX*Math.cos(angle);
    const y2 = CY + RMAX*Math.sin(angle);
    const lx = CX + (RMAX+18)*Math.cos(angle);
    const ly = CY + (RMAX+18)*Math.sin(angle);
    const label = t.replace(/-/g,' ').replace(/\b\w/g,c=>c.toUpperCase());
    const pct = radar[t] || 0;
    return `<line x1="${CX}" y1="${CY}" x2="${x2}" y2="${y2}" stroke="var(--border)" stroke-width="1"/>
      <text x="${lx}" y="${ly}" class="radar-axis-label">${label} ${pct}%</text>`;
  }).join('');

  const weakest = RADAR_TOPICS.slice().sort((a,b) => (radar[a]||0)-(radar[b]||0)).slice(0,5);

  // solve history
  const histDays = Object.keys(solveLog).filter(d => (solveLog[d]||[]).length>0)
    .sort((a,b) => b.localeCompare(a)).slice(0,20);

  const { score } = computeReadiness(solveLog, reviewQueue, problems);

  return `
    <div class="page-header fade-in-up">
      <div class="page-title">Progress</div>
      <div class="page-subtitle">Your solving analysis</div>
    </div>
    <div class="progress-grid">

      <div class="card fade-in-up">
        <div class="card-header"><span class="card-icon">🕸</span><h2>Topic Radar</h2></div>
        <div class="radar-wrap">
          <svg class="radar-svg" width="280" height="280" viewBox="0 0 280 280">
            ${rings}
            ${axes}
            <polygon class="radar-polygon" points="${polyPts}"
              fill="rgba(249,115,22,.2)" stroke="var(--accent)" stroke-width="2"/>
          </svg>
          <div class="weak-topics">
            <div class="weak-topics-title">Weakest Topics</div>
            ${weakest.map(t => `
              <div class="weak-row">
                <span class="weak-label">${t.replace(/-/g,' ')}</span>
                <div class="diff-track" style="flex:1"><div class="diff-fill medium" style="width:${radar[t]||0}%"></div></div>
                <span class="weak-pct">${radar[t]||0}%</span>
              </div>`).join('')}
          </div>
        </div>
      </div>

      <div class="card fade-in-up">
        <div class="card-header"><span class="card-icon">📈</span><h2>Summary</h2></div>
        <div class="card-body">
          <div style="text-align:center;margin-bottom:1.5rem">
            <div style="font-size:3.5rem;font-weight:800;font-family:'JetBrains Mono',monospace;
              background:linear-gradient(135deg,var(--accent),#fbbf24);
              -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">
              ${allSolved.size}
            </div>
            <div style="color:var(--muted);font-size:.8rem;font-weight:600;text-transform:uppercase;letter-spacing:.06em">Problems Solved</div>
          </div>
          ${['easy','medium','hard'].map(d => {
            const cnt = [...allSolved].filter(s => {
              const p = problems.find(x => x.slug === s); return p && p.difficulty === d;
            }).length;
            const tot = problems.filter(p => p.difficulty === d).length;
            const pct = tot ? Math.round(cnt/tot*100) : 0;
            return `<div class="diff-row">
              <span class="diff-name ${d}">${d}</span>
              <div class="diff-track"><div class="diff-fill ${d}" style="width:${pct}%"></div></div>
              <span class="diff-count">${cnt} / ${tot}</span>
            </div>`;
          }).join('')}
          <div style="margin-top:1.25rem;padding-top:1.25rem;border-top:1px solid var(--border)">
            <div style="font-size:.75rem;color:var(--muted);font-weight:700;text-transform:uppercase;letter-spacing:.05em;margin-bottom:.5rem">Readiness</div>
            <div style="font-size:2rem;font-weight:800;font-family:'JetBrains Mono',monospace;color:${readinessLevel(score).color}">${score}<span style="font-size:.9rem;opacity:.6"> / 100</span></div>
            <div style="font-size:.78rem;color:var(--muted);margin-top:3px">${readinessLevel(score).label}</div>
          </div>
        </div>
      </div>

      <div class="card fade-in-up progress-full">
        <div class="card-header"><span class="card-icon">📋</span><h2>Solve History</h2></div>
        <div class="history-list">
          ${histDays.length === 0
            ? `<div class="empty-state">No solves yet — get started!</div>`
            : histDays.map(d => `
              <div class="history-day">
                <span class="history-date">${fmtDate(d)}</span>
                <span class="history-slugs">${(solveLog[d]||[]).join(', ')}</span>
                <span class="history-count">${(solveLog[d]||[]).length}</span>
              </div>`).join('')}
        </div>
      </div>
    </div>`;
}

/* ──────────────────────────────────────────────────────────────────────────
   20. PAGE — REVIEW
   ────────────────────────────────────────────────────────────────────────── */

function renderReview() {
  const queue    = lsGet(LS.REVIEW_QUEUE);
  const problems = App.problems;
  const t        = today();

  const allEntries = Object.entries(queue)
    .sort((a,b) => a[1].nextReview.localeCompare(b[1].nextReview));

  const due     = allEntries.filter(([,d]) => d.nextReview <= t);
  const upcoming = allEntries.filter(([,d]) => d.nextReview > t);

  const renderItem = ([slug, d], isDue) => {
    const p = problems.find(x => x.slug === slug);
    const title = p ? p.title : slug;
    const daysUntil = daysBetween(t, d.nextReview);
    const meta = isDue
      ? `<span class="review-item-due">Overdue by ${daysBetween(d.nextReview, t)}d</span>`
      : `Next in ${daysUntil}d — ${fmtDate(d.nextReview)}`;
    return `<div class="review-item">
      <div class="review-item-info">
        <div class="review-item-title">${problemLink(slug, title)} ${p ? diffBadge(p.difficulty) : ''}</div>
        <div class="review-item-meta">Interval: ${d.interval}d · Ease: ${d.ease.toFixed(2)} · Reps: ${d.reps} · ${meta}</div>
      </div>
      <div class="review-item-actions">
        ${isDue ? `<div class="rating-inline">
          ${[1,2,3,4,5].map(r => `<button class="ri-btn" data-r="${r}" onclick="quickRate('${slug}','${title.replace(/'/g,"\\'")}',${r})" title="${['Blackout','Hard','Ok','Good','Easy'][r-1]}">${r}</button>`).join('')}
        </div>` : ''}
        <button class="icon-btn btn-sm" onclick="openNotes('${slug}','${title.replace(/'/g,"\\'")}')">📝</button>
      </div>
    </div>`;
  };

  return `
    <div class="page-header fade-in-up">
      <div class="page-title">Review Queue</div>
      <div class="page-subtitle">${due.length} due · ${upcoming.length} upcoming</div>
    </div>
    <div class="card fade-in-up">
      <div class="card-header"><span class="card-icon">🔴</span><h2>Due Today (${due.length})</h2></div>
      <div class="review-list">
        ${due.length === 0
          ? `<div class="empty-state">✓ All caught up!</div>`
          : due.map(e => renderItem(e, true)).join('')}
      </div>
    </div>
    ${upcoming.length > 0 ? `
    <div class="card fade-in-up" style="margin-top:1.5rem">
      <div class="card-header"><span class="card-icon">🟡</span><h2>Upcoming (${upcoming.length})</h2></div>
      <div class="review-list">
        ${upcoming.slice(0,30).map(e => renderItem(e, false)).join('')}
      </div>
    </div>` : ''}`;
}

function quickRate(slug, title, rating) {
  onProblemSolved(slug, rating);
}

/* ──────────────────────────────────────────────────────────────────────────
   21. PAGE — PATHS
   ────────────────────────────────────────────────────────────────────────── */

let activePathId = 'blind75';

async function renderPaths() {
  const studyPaths = lsGet(LS.STUDY_PATHS);
  const pathData   = App.pathData;
  const solveLog   = lsGet(LS.SOLVE_LOG);
  const allSolved  = new Set(Object.values(solveLog).flat());

  // Load if not cached
  for (const id of PATHS) {
    if (!pathData[id]) {
      try {
        pathData[id] = await fetch(`data/paths/${id}.json`).then(r => r.json());
      } catch { pathData[id] = []; }
    }
  }

  const data     = pathData[activePathId] || [];
  const progress = studyPaths[activePathId] || { completed:[] };
  const completed = new Set(progress.completed);

  // update total
  const totalProblems = data.reduce((sum, s) => sum + (s.problems||[]).length, 0);
  if (!studyPaths[activePathId]) studyPaths[activePathId] = { completed:[], total:totalProblems, pct:0 };
  studyPaths[activePathId].total = totalProblems;
  studyPaths[activePathId].pct   = totalProblems ? Math.round(completed.size/totalProblems*100) : 0;
  lsSet(LS.STUDY_PATHS, studyPaths);

  const pct = totalProblems ? Math.round(completed.size/totalProblems*100) : 0;

  const sectionsHtml = data.map(section => {
    const sProblems  = section.problems || [];
    const sCompleted = sProblems.filter(p => completed.has(p.slug)).length;
    const allDone    = sCompleted === sProblems.length && sProblems.length > 0;
    return `
      <div class="path-section-title ${allDone ? 'path-section-done' : ''}">
        ${allDone ? '✓ ' : ''}${section.section}
        <span style="margin-left:auto;font-family:'JetBrains Mono',monospace;font-size:.7rem">${sCompleted}/${sProblems.length}</span>
      </div>
      ${sProblems.map(p => {
        const done = completed.has(p.slug);
        const cls  = done ? 'path-problem-row solved' : 'path-problem-row';
        return `<div class="${cls}" onclick="togglePathProblem('${activePathId}','${p.slug}','${(p.title||p.slug).replace(/'/g,"\\'")}')">
          <div class="path-checkbox">${done ? '✓' : ''}</div>
          <span class="path-prob-title">${problemLink(p.slug, p.title || p.slug)}</span>
          ${diffBadge(p.difficulty || 'medium')}
          <button class="path-prob-note-btn" onclick="event.stopPropagation();openNotes('${p.slug}','${(p.title||p.slug).replace(/'/g,"\\'")}')">📝</button>
        </div>`;
      }).join('')}`;
  }).join('');

  return `
    <div class="page-header fade-in-up">
      <div class="page-title">Study Paths</div>
      <div class="page-subtitle">Track your curated list progress</div>
    </div>
    <div class="path-tabs">
      ${PATHS.map(id => `<button class="path-tab ${id===activePathId?'active':''}" onclick="switchPath('${id}')">${id}</button>`).join('')}
    </div>
    <div class="path-progress-bar-row">
      <span style="font-size:.85rem;font-weight:700">${completed.size} / ${totalProblems} solved</span>
      <div class="path-bar-track"><div class="path-bar-fill" style="width:${pct}%"></div></div>
      <span class="path-pct">${pct}%</span>
    </div>
    <div class="card fade-in-up">
      ${sectionsHtml || '<div class="empty-state">Loading path data…</div>'}
    </div>`;
}

function switchPath(id) {
  activePathId = id;
  App.render();
}

function togglePathProblem(pathId, slug, title) {
  const paths = lsGet(LS.STUDY_PATHS);
  if (!paths[pathId]) paths[pathId] = { completed:[], total:0, pct:0 };
  const idx = paths[pathId].completed.indexOf(slug);
  if (idx === -1) {
    paths[pathId].completed.push(slug);
    addToSolveLog(slug);
    updateStreakMeta(lsGet(LS.SOLVE_LOG));
    checkBadges(App.problems);
    toast(`✓ ${title}`);
  } else {
    paths[pathId].completed.splice(idx, 1);
  }
  lsSet(LS.STUDY_PATHS, paths);
  App.render();
}

/* ──────────────────────────────────────────────────────────────────────────
   22. PAGE — BADGES
   ────────────────────────────────────────────────────────────────────────── */

function renderBadges() {
  const earned = lsGet(LS.BADGES);

  const cards = BADGE_DEFS.map(b => {
    const e = earned[b.id];
    return `<div class="badge-card ${e ? 'earned' : ''}">
      <div class="badge-icon">${b.icon}</div>
      <div class="badge-name">${b.name}</div>
      <div class="badge-desc">${b.desc}</div>
      ${e ? `<div class="badge-date">${fmtDate(e.earned)}</div>` : ''}
    </div>`;
  }).join('');

  const totalEarned = Object.keys(earned).length;

  return `
    <div class="page-header fade-in-up">
      <div class="page-title">Achievements</div>
      <div class="page-subtitle">${totalEarned} / ${BADGE_DEFS.length} earned</div>
    </div>
    <div class="card fade-in-up">
      <div class="badges-grid">${cards}</div>
    </div>`;
}

/* ──────────────────────────────────────────────────────────────────────────
   23. PAGE — SETTINGS
   ────────────────────────────────────────────────────────────────────────── */

function renderSettings() {
  const prefs    = lsGet(LS.PREFS, {});
  const companies = Object.keys(App.companyTags).sort();
  const sizeKB   = Math.round(lsSize() / 1024);
  const pct      = Math.min(Math.round(sizeKB / 5120 * 100), 100);

  return `
    <div class="page-header fade-in-up">
      <div class="page-title">Settings</div>
    </div>

    <div class="card fade-in-up">
      <div class="card-body">

        <div class="settings-section">
          <div class="settings-section-title">Profile</div>
          <div class="setting-row">
            <div><div class="setting-label">LeetCode Username</div><div class="setting-desc">Used for your shareable profile</div></div>
            <input class="setting-input" id="pref-username" type="text" placeholder="your_username" value="${prefs.lcUsername||''}"/>
          </div>
          <div class="setting-row">
            <div><div class="setting-label">Daily Goal</div><div class="setting-desc">Problems per day target</div></div>
            <input class="setting-input" id="pref-daily-goal" type="number" min="1" max="20" value="${prefs.dailyGoal||2}" style="max-width:80px"/>
          </div>
          <div class="setting-row">
            <div><div class="setting-label">Target Company</div><div class="setting-desc">Filter problems to company questions</div></div>
            <select class="setting-input" id="pref-company">
              <option value="">None</option>
              ${companies.map(c => `<option value="${c}" ${prefs.targetCompany===c?'selected':''}>${c.charAt(0).toUpperCase()+c.slice(1)}</option>`).join('')}
            </select>
          </div>
          <div style="margin-top:1rem">
            <button class="btn-primary btn-sm" onclick="savePrefs()">Save Settings</button>
            <button class="btn-secondary btn-sm" style="margin-left:8px" onclick="generateShareURL()">🔗 Share Profile</button>
          </div>
        </div>

        <div class="settings-section">
          <div class="settings-section-title">Backup & Restore</div>
          <div class="setting-row">
            <div><div class="setting-label">Download Backup</div><div class="setting-desc">Export all your data as JSON</div></div>
            <button class="btn-primary btn-sm" onclick="exportData()">⬇ Download</button>
          </div>
          <div class="setting-row">
            <div><div class="setting-label">Restore from File</div><div class="setting-desc">Import a previously downloaded backup</div></div>
            <label class="btn-secondary btn-sm" style="cursor:pointer">
              ⬆ Choose file
              <input type="file" accept=".json" style="display:none" onchange="importData(this.files[0])"/>
            </label>
          </div>
        </div>

        <div class="settings-section">
          <div class="settings-section-title">Storage</div>
          <div class="storage-meter">
            <div style="display:flex;justify-content:space-between;font-size:.78rem">
              <span>Used: <strong>${sizeKB} KB</strong></span>
              <span>Limit: <strong>5,120 KB</strong></span>
            </div>
            <div class="storage-bar-track">
              <div class="storage-bar-fill" style="width:${pct}%"></div>
            </div>
            <div class="storage-meta"><span>${pct}% used</span><span>${5120-sizeKB} KB free</span></div>
          </div>
        </div>

        <div class="settings-section">
          <div class="settings-section-title">Danger Zone</div>
          <div class="setting-row">
            <div><div class="setting-label">Reset All Data</div><div class="setting-desc" style="color:var(--hard)">This cannot be undone</div></div>
            <button class="btn-primary btn-sm btn-danger" onclick="resetAllData()">🗑 Reset</button>
          </div>
        </div>

      </div>
    </div>`;
}

function savePrefs() {
  const prefs = lsGet(LS.PREFS, {});
  prefs.lcUsername    = document.getElementById('pref-username')?.value.trim() || '';
  prefs.dailyGoal     = parseInt(document.getElementById('pref-daily-goal')?.value) || 2;
  prefs.targetCompany = document.getElementById('pref-company')?.value || '';
  lsSet(LS.PREFS, prefs);
  toast('Settings saved ✓');
  App.render();
}

function resetAllData() {
  if (!confirm('This will permanently delete ALL your LeetDash data. Are you sure?')) return;
  for (const k of Object.values(LS)) localStorage.removeItem(k);
  toast('Data cleared');
  App.render();
}

/* ──────────────────────────────────────────────────────────────────────────
   24. PAGE — PROFILE (shared read-only)
   ────────────────────────────────────────────────────────────────────────── */

function renderProfile() {
  const data = parseSharedProfile();
  if (!data) {
    return `<div class="page-header fade-in-up"><div class="page-title">Profile</div></div>
      <div class="card fade-in-up"><div class="card-body" style="text-align:center;padding:3rem">
        <p style="color:var(--muted)">No profile data found.</p>
        <p style="margin-top:.5rem;font-size:.83rem">Share your profile from <a href="#/settings">Settings →</a></p>
      </div></div>`;
  }

  const badgeChips = (data.badges || []).map(id => {
    const def = BADGE_DEFS.find(b => b.id === id);
    return def ? `<div class="profile-badge-chip">${def.icon} ${def.name}</div>` : '';
  }).join('');

  const scoreColor = data.score >= 70 ? '#22c55e' : data.score >= 40 ? '#f59e0b' : '#ef4444';

  return `
    <div class="page-header fade-in-up">
      <div class="page-title">Shared Profile</div>
    </div>
    <div class="profile-card-wrap fade-in-up">
      <div class="profile-card">
        <div class="profile-card-user">@${data.u}</div>
        <div class="profile-card-score" style="-webkit-text-fill-color:${scoreColor};color:${scoreColor}">${data.score}</div>
        <div style="font-size:.76rem;color:var(--muted);margin-top:-.5rem">Interview Readiness Score</div>
        <div class="profile-card-stats">
          <div><div class="profile-card-stat-val">${data.s}</div><div>Problems Solved</div></div>
          <div><div class="profile-card-stat-val">${data.streak}</div><div>Day Streak</div></div>
        </div>
        ${badgeChips ? `<div class="profile-card-badges">${badgeChips}</div>` : ''}
      </div>
    </div>`;
}

/* ──────────────────────────────────────────────────────────────────────────
   25. ROUTER & APP SHELL
   ────────────────────────────────────────────────────────────────────────── */

const App = {
  problems:    [],
  companyTags: {},
  pathData:    {},

  async init() {
    // Load static data
    try { App.problems    = await fetch('data/problems.json').then(r => r.json()); } catch(e) { console.error('problems.json load failed', e); }
    try { App.companyTags = await fetch('data/company-tags.json').then(r => r.json()); } catch(e) { console.error('company-tags.json load failed', e); }

    // Check private browsing
    try {
      const est = await navigator.storage.estimate();
      if (est.quota < 120_000_000) {
        document.getElementById('private-banner').classList.remove('hidden');
      }
    } catch {}

    // Backup reminder
    const prefs = lsGet(LS.PREFS, {});
    if (prefs.lastBackupReminder) {
      const d = daysBetween(prefs.lastBackupReminder, today());
      if (d >= 7) document.getElementById('backup-banner').classList.remove('hidden');
    }

    // Recompute streak on load (in case of rebuild)
    const solveLog = lsGet(LS.SOLVE_LOG);
    updateStreakMeta(solveLog);

    // Check badges silently on load
    checkBadges(App.problems, true);

    // Wire up global event listeners
    App.wireEvents();

    // Router
    window.addEventListener('hashchange', () => App.route());
    App.route();
  },

  route() {
    const hash = location.hash || '#/';
    let route  = hash.split('?')[0].replace('#/', '') || 'dashboard';
    if (route === '') route = 'dashboard';
    if (route.startsWith('profile')) route = 'profile';

    // Update nav active state
    document.querySelectorAll('.nav-links a').forEach(a => {
      a.classList.toggle('active', a.dataset.route === route ||
        (route === 'dashboard' && a.dataset.route === 'dashboard'));
    });

    App.render(route);
  },

  async render(route) {
    if (!route) {
      const hash = location.hash || '#/';
      route = hash.split('?')[0].replace('#/', '') || 'dashboard';
      if (route === '') route = 'dashboard';
      if (route.startsWith('profile')) route = 'profile';
    }

    const container = document.getElementById('app');
    container.innerHTML = '';

    // Update nav streak badge
    const meta = lsGet(LS.STREAK_META, {});
    const nb   = document.getElementById('nav-streak');
    if (nb) nb.textContent = `🔥 ${meta.currentStreak || 0}`;

    let html = '';
    switch (route) {
      case 'dashboard': html = renderDashboard(); break;
      case 'progress':  html = renderProgress();  break;
      case 'review':    html = renderReview();     break;
      case 'paths':     html = await renderPaths(); break;
      case 'badges':    html = renderBadges();     break;
      case 'settings':  html = renderSettings();   break;
      case 'profile':   html = renderProfile();    break;
      default:          html = renderDashboard();
    }
    container.innerHTML = html;

    // Post-render: load contests on dashboard
    if (route === 'dashboard') App.loadContests();
  },

  async loadContests() {
    const listEl = document.getElementById('contest-list');
    if (!listEl) return;
    const prefs = lsGet(LS.PREFS, {});
    try {
      const contests = await fetchContests();
      if (!contests.length) {
        listEl.innerHTML = `<div class="empty-state">No upcoming contests found</div>`;
        return;
      }
      listEl.innerHTML = contests.map(c => {
        const start = new Date(c.startTime * 1000);
        const now   = Date.now();
        const diff  = start - now;
        const active = prefs.contestReminders && prefs[`remind_${c.titleSlug}`];
        let countdownStr = '';
        if (diff > 0) {
          const h = Math.floor(diff/3600000);
          const m = Math.floor((diff%3600000)/60000);
          countdownStr = h > 24 ? `${Math.floor(h/24)}d ${h%24}h` : `${h}h ${m}m`;
        } else {
          countdownStr = 'Live!';
        }
        return `<div class="contest-card">
          <div class="contest-time-block">
            <div class="contest-countdown">${countdownStr}</div>
            <div class="contest-countdown-label">${diff > 0 ? 'to start' : ''}</div>
          </div>
          <div class="contest-info">
            <div class="contest-title">${c.title}</div>
            <div class="contest-date">${start.toLocaleDateString('en-US',{weekday:'short',month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'})}</div>
          </div>
          <button class="contest-remind ${active?'active':''}"
            onclick="toggleContestReminder('${c.titleSlug}','${c.title.replace(/'/g,"\\'")}',${c.startTime})">
            🔔 Remind
          </button>
        </div>`;
      }).join('');

      // Live countdown update every minute
      clearInterval(App._contestTimer);
      App._contestTimer = setInterval(() => App.loadContests(), 60000);
    } catch {
      listEl.innerHTML = `<div class="empty-state">Could not load contests</div>`;
    }
  },

  wireEvents() {
    // Theme toggle
    const themeBtn = document.getElementById('theme-toggle');
    if (themeBtn) themeBtn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme');
      const next    = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      themeBtn.textContent = next === 'dark' ? '☀' : '🌙';
      const prefs = lsGet(LS.PREFS, {});
      prefs.theme = next; lsSet(LS.PREFS, prefs);
    });

    // Set initial theme
    const savedTheme = lsGet(LS.PREFS, {}).theme || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    if (themeBtn) themeBtn.textContent = savedTheme === 'dark' ? '☀' : '🌙';

    // Backup banner dismiss
    document.getElementById('dismiss-backup-banner')?.addEventListener('click', () => {
      document.getElementById('backup-banner').classList.add('hidden');
      const prefs = lsGet(LS.PREFS, {});
      prefs.lastBackupReminder = today();
      lsSet(LS.PREFS, prefs);
    });

    // Notes modal
    document.getElementById('close-notes-modal')?.addEventListener('click', closeNotes);
    document.getElementById('notes-backdrop')?.addEventListener('click', closeNotes);

    document.getElementById('note-approach')?.addEventListener('input', function() {
      updateCharCount('note-approach','approach-count'); debouncedSave();
    });
    document.getElementById('note-gotcha')?.addEventListener('input', function() {
      updateCharCount('note-gotcha','gotcha-count'); debouncedSave();
    });
    document.getElementById('note-time')?.addEventListener('input',  debouncedSave);
    document.getElementById('note-space')?.addEventListener('input', debouncedSave);

    document.querySelectorAll('#note-stars .star').forEach(s => {
      s.addEventListener('click', () => {
        notesRating = parseInt(s.dataset.v);
        renderNoteStars(notesRating);
        debouncedSave();
      });
    });

    // Solve modal
    document.getElementById('close-solve-modal')?.addEventListener('click', closeSolveModal);
    document.getElementById('solve-backdrop')?.addEventListener('click', closeSolveModal);

    document.querySelectorAll('.rating-btn').forEach(b => {
      b.addEventListener('click', () => {
        solveModalRating = parseInt(b.dataset.r);
        document.querySelectorAll('.rating-btn').forEach(x => x.classList.remove('selected'));
        b.classList.add('selected');
      });
    });

    document.getElementById('confirm-solve-btn')?.addEventListener('click', () => {
      if (!solveModalSlug) return;
      const slug   = solveModalSlug;
      const rating = solveModalRating;
      const cb     = solveModalCb;
      closeSolveModal();
      onProblemSolved(slug, rating);
      if (cb) cb(slug, rating);
      toast(`Marked solved! Next review in ${lsGet(LS.REVIEW_QUEUE)[slug]?.interval || 1}d`);
    });
  },
};

/* ──────────────────────────────────────────────────────────────────────────
   26. GLOBAL HELPERS (called inline from HTML)
   ────────────────────────────────────────────────────────────────────────── */

function toggleContestReminder(slug, title, startTime) {
  const prefs = lsGet(LS.PREFS, {});
  const key   = `remind_${slug}`;
  if (prefs[key]) {
    prefs[key] = false;
    toast(`Reminder cancelled for ${title}`);
  } else {
    Notification.requestPermission().then(perm => {
      if (perm === 'granted') {
        const ms = (startTime * 1000) - Date.now() - 15 * 60 * 1000;
        if (ms > 0) {
          setTimeout(() => new Notification('LeetCode Contest Starting Soon', {
            body: `${title} starts in 15 minutes!`,
            icon: '/favicon.ico',
          }), ms);
          prefs[key] = true;
          toast(`🔔 Reminder set for ${title}`);
        } else {
          toast('Contest starts too soon', 'error');
        }
      } else {
        toast('Notification permission denied', 'error');
      }
    });
  }
  lsSet(LS.PREFS, prefs);
  App.loadContests();
}

/* ──────────────────────────────────────────────────────────────────────────
   27. BOOT
   ────────────────────────────────────────────────────────────────────────── */

document.addEventListener('DOMContentLoaded', () => App.init());
""".strip()

# Write files
(ROOT / 'index.css').write_text(CSS, encoding='utf-8')
print(f"index.css  written — {len(CSS):,} chars")

(ROOT / 'app.js').write_text(JS, encoding='utf-8')
print(f"app.js     written — {len(JS):,} chars")
