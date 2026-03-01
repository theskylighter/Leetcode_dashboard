/* ============================================================
   api.js — LC profile, daily challenge, contests, submissions,
            calendar import (alfa-leetcode-api)
   ============================================================ */

/* ── Fetch LC profile bundle (all endpoints in parallel) ── */
async function fetchLCProfile(username) {
  if (!username) { toast('Enter a LeetCode username first', 'error'); return null; }
  const btn    = document.getElementById('lc-fetch-btn');
  const status = document.getElementById('lc-fetch-status');
  if (btn) { btn.disabled = true; btn.textContent = 'Fetching…'; }
  if (status) status.textContent = '';

  try {
    const safe = async (url) => {
      try {
        const r = await fetch(url);
        if (!r.ok) return null;
        return await r.json();
      } catch { return null; }
    };

    const [profile, solved, contest, acSub, calendar, badges] = await Promise.all([
      safe(`${ALFA_API}/${encodeURIComponent(username)}`),
      safe(`${ALFA_API}/${encodeURIComponent(username)}/solved`),
      safe(`${ALFA_API}/${encodeURIComponent(username)}/contest`),
      safe(`${ALFA_API}/${encodeURIComponent(username)}/acSubmission?limit=10`),
      safe(`${ALFA_API}/${encodeURIComponent(username)}/calendar`),
      safe(`${ALFA_API}/${encodeURIComponent(username)}/badges`),
    ]);

    if (!profile && !solved) throw new Error('User not found or API down');

    // Merge solved fields into profile-level for backwards compat
    const merged = {
      ...(profile || {}),
      ...(solved  || {}),
      contest,
      acSubmission: acSub,
      calendar,
      lcBadges: badges,
      fetchedAt: today(),
      username,
    };

    const prefs = lsGet(LS.PREFS, {});
    prefs.lcProfile  = merged;
    prefs.lcUsername = username;
    lsSet(LS.PREFS, prefs);

    if (status) status.textContent = `✓ Fetched ${today()}`;
    toast(`LeetCode profile loaded for @${username} ✓`);

    // Auto-import activity days from calendar into solveLog
    if (calendar?.submissionCalendar) {
      importCalendarToSolveLog(calendar.submissionCalendar);
    }

    renderLCProfileCard(merged);
    renderContestRatingCard(contest);
    renderRecentSubmissionsCard(acSub);
    return merged;
  } catch(e) {
    const msg = e.message || 'Failed to fetch';
    if (status) status.textContent = `✗ ${msg}`;
    toast(`Could not fetch: ${msg}`, 'error');
    return null;
  } finally {
    if (btn) { btn.disabled = false; btn.textContent = '↺ Refresh'; }
  }
}

/* ── Import submission calendar into solveLog (adds activity days) ── */
function importCalendarToSolveLog(submissionCalendar) {
  try {
    const cal = typeof submissionCalendar === 'string'
      ? JSON.parse(submissionCalendar)
      : submissionCalendar;

    const log = lsGet(LS.SOLVE_LOG);
    let imported = 0;

    for (const [ts, count] of Object.entries(cal)) {
      if (!count) continue;
      const date = new Date(parseInt(ts) * 1000).toISOString().split('T')[0];
      if (!log[date]) {
        log[date] = [`lc-imported-${date}`];
        imported++;
      }
    }

    if (imported > 0) {
      lsSet(LS.SOLVE_LOG, log);
      updateStreakMeta(log);
      toast(`📥 Imported ${imported} active days from LC calendar`);
    }
  } catch(e) {
    console.warn('Calendar import failed', e);
  }
}

/* ── Render LC profile card (works in both dashboard sidebar & settings) ── */
function renderLCProfileCard(data) {
  document.querySelectorAll('.lc-profile-body').forEach(el => {
    if (!el || !data) return;
    el.innerHTML = `
      <div class="lc-profile-card">
        <div class="lc-profile-username">@${data.username || '—'}
          <span style="font-size:.72rem;font-weight:600;color:var(--muted);margin-left:6px">Ranking #${(data.ranking||0).toLocaleString()}</span>
        </div>
        <div class="lc-profile-stats">
          <div class="lc-stat">
            <div class="lc-stat-num" style="color:var(--accent)">${data.totalSolved ?? data.solvedProblem ?? '—'}</div>
            <div class="lc-stat-label">Total</div>
          </div>
          <div class="lc-stat">
            <div class="lc-stat-num easy">${data.easySolved ?? '—'}</div>
            <div class="lc-stat-label">Easy</div>
          </div>
          <div class="lc-stat">
            <div class="lc-stat-num medium">${data.mediumSolved ?? '—'}</div>
            <div class="lc-stat-label">Medium</div>
          </div>
          <div class="lc-stat">
            <div class="lc-stat-num hard">${data.hardSolved ?? '—'}</div>
            <div class="lc-stat-label">Hard</div>
          </div>
          <div class="lc-stat">
            <div class="lc-stat-num" style="color:var(--muted)">${data.totalEasy ?? '—'}</div>
            <div class="lc-stat-label">/ Easy</div>
          </div>
          <div class="lc-stat">
            <div class="lc-stat-num" style="color:var(--muted)">${data.totalMedium ?? '—'}</div>
            <div class="lc-stat-label">/ Med</div>
          </div>
        </div>
        ${data.ranking ? `<div style="font-size:.72rem;color:var(--muted)">Reputation: ${data.reputation ?? 0} · Contributions: ${data.contributionPoint ?? 0}</div>` : ''}
      </div>`;
  });
}

/* ── Render contest rating card ── */
function renderContestRatingCard(contest) {
  const el = document.getElementById('contest-rating-body');
  if (!el) return;
  if (!contest || contest.errors) {
    el.innerHTML = '<div class="empty-state">No contest data yet</div>';
    return;
  }
  const rating  = Math.round(contest.contestRating || 0);
  const rank    = (contest.contestGlobalRanking || 0).toLocaleString();
  const topPct  = contest.contestTopPercentage?.toFixed(1) ?? '—';
  const attended = contest.contestAttend || 0;
  const badge   = contest.contestBadge;

  el.innerHTML = `
    <div class="contest-rating-card">
      ${badge ? `<div class="contest-badge-img"><img src="${badge.icon||''}" alt="${badge.name||''}" style="height:48px" onerror="this.style.display='none'"></div>` : ''}
      <div class="cr-stats">
        <div class="cr-stat"><span class="cr-val">${rating}</span><span class="cr-lbl">Rating</span></div>
        <div class="cr-stat"><span class="cr-val">#${rank}</span><span class="cr-lbl">Global Rank</span></div>
        <div class="cr-stat"><span class="cr-val">Top ${topPct}%</span><span class="cr-lbl">Percentile</span></div>
        <div class="cr-stat"><span class="cr-val">${attended}</span><span class="cr-lbl">Contests</span></div>
      </div>
    </div>`;
}

/* ── Render recent accepted submissions card ── */
function renderRecentSubmissionsCard(acSub) {
  const el = document.getElementById('recent-submissions-body');
  if (!el) return;
  const list = acSub?.submission || acSub?.acSubmission || [];
  if (!list.length) {
    el.innerHTML = '<div class="empty-state">No recent submissions</div>';
    return;
  }
  el.innerHTML = `
    <div class="submissions-list">
      ${list.slice(0, 8).map(s => {
        const date = s.timestamp
          ? new Date(parseInt(s.timestamp) * 1000).toLocaleDateString('en-US',{month:'short',day:'numeric'})
          : '';
        return `<div class="submission-row">
          <a href="https://leetcode.com/problems/${s.titleSlug}/" target="_blank" rel="noopener" class="sub-title">${s.title}</a>
          <span class="sub-lang">${s.lang || ''}</span>
          <span class="sub-date muted">${date}</span>
        </div>`;
      }).join('')}
    </div>`;
}

/* ── Fetch upcoming contests ── */
async function fetchContests() {
  try {
    const r    = await fetch(`${ALFA_API}/contests/upcoming`);
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const json = await r.json();
    return Array.isArray(json) ? json : (json.contests || []);
  } catch { return []; }
}

/* ── Fetch today's daily challenge ── */
async function fetchDailyChallenge() {
  try {
    const r    = await fetch(`${ALFA_API}/daily`);
    if (!r.ok) return null;
    return await r.json();
  } catch { return null; }
}

/* ── Render daily challenge card ── */
function renderDailyCard(data) {
  const el = document.getElementById('daily-challenge-body');
  if (!el) return;
  if (!data || data.errors || data.error) {
    el.innerHTML = '<div class="empty-state">Could not load daily challenge</div>';
    return;
  }
  const slug   = data.titleSlug || data.slug || '';
  const title  = data.title || 'Daily Challenge';
  const diff   = (data.difficulty || '').toLowerCase();
  const topics = (data.topicTags || data.topics || []).map(t => t.name || t).join(', ');
  const url    = `https://leetcode.com/problems/${slug}/`;

  el.innerHTML = `
    <div class="daily-problem">
      <div class="daily-problem-header">
        ${diffBadge(diff)}
        ${topics ? `<span class="daily-topics muted">${topics}</span>` : ''}
      </div>
      <div class="daily-problem-title">${problemLink(slug, title)}</div>
      <div class="daily-problem-actions">
        <a href="${url}" target="_blank" rel="noopener" class="btn-primary btn-sm">Open ↗</a>
        <button class="btn-secondary btn-sm"
          onclick="onProblemSolved('${slug}', 3); toast('✓ Marked solved!')">
          ✓ Mark Solved
        </button>
      </div>
    </div>`;
}

/* ── Share URL helpers ── */
function generateShareURL() {
  const solveLog    = lsGet(LS.SOLVE_LOG);
  const streakMeta  = lsGet(LS.STREAK_META, {});
  const reviewQueue = lsGet(LS.REVIEW_QUEUE);
  const badges      = lsGet(LS.BADGES);
  const prefs       = lsGet(LS.PREFS, {});
  const allSolved   = new Set(Object.values(solveLog).flat()).size;
  const { score }   = computeReadiness(solveLog, reviewQueue, App.problems);
  const payload = {
    u:      prefs.lcUsername || 'Anonymous',
    s:      allSolved,
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
  const hash = location.hash;
  const m    = hash.match(/[?&]s=([^&]+)/);
  if (!m) return null;
  try {
    return JSON.parse(decodeURIComponent(escape(atob(m[1]))));
  } catch { return null; }
}
