/* ============================================================
   utils.js — constants, date helpers, localStorage, toast
   ============================================================ */
'use strict';

const LS = {
  SOLVE_LOG:    'ld:solveLog',
  REVIEW_QUEUE: 'ld:reviewQueue',
  NOTES:        'ld:notes',
  STREAK_META:  'ld:streakMeta',
  STUDY_PATHS:  'ld:studyPaths',
  BADGES:       'ld:badges',
  PREFS:        'ld:prefs',
};

const PATHS = ['blind75', 'neetcode150', 'grind169'];
const ALFA_API = 'https://alfa-leetcode-api.onrender.com';

/* ── Date helpers ── */
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
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

/* ── localStorage helpers ── */
function lsGet(key, fallback = {}) {
  try {
    const v = localStorage.getItem(key);
    return v === null ? fallback : (JSON.parse(v) ?? fallback);
  } catch { return fallback; }
}

function lsSet(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch(e) {
    console.warn('localStorage write failed:', e);
  }
}

function lsSize() {
  let total = 0;
  for (const k of Object.keys(localStorage)) {
    if (k.startsWith('ld:')) {
      total += (localStorage.getItem(k) || '').length * 2;
    }
  }
  return total; // bytes
}

/* ── Toast ── */
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

/* ── Rendering helpers ── */
function diffBadge(difficulty) {
  const cls = difficulty === 'easy' ? 'badge-easy' : difficulty === 'medium' ? 'badge-medium' : 'badge-hard';
  return `<span class="badge ${cls}">${difficulty}</span>`;
}

function problemLink(slug, title) {
  return `<a href="https://leetcode.com/problems/${slug}/" target="_blank" rel="noopener">${title}</a>`;
}
