/* ============================================================
   pages/dashboard.js — dashboard layout + post-render API calls
   ============================================================ */

function renderDashboard() {
  const solveLog    = lsGet(LS.SOLVE_LOG);
  const reviewQueue = lsGet(LS.REVIEW_QUEUE);
  const streakMeta  = lsGet(LS.STREAK_META, { currentStreak:0, longestStreak:0, totalDays:0 });
  const prefs       = lsGet(LS.PREFS, {});
  const problems    = App.problems;

  const t = today();
  const due = Object.entries(reviewQueue)
    .filter(([,d]) => d.nextReview <= t)
    .sort((a,b) => a[1].nextReview.localeCompare(b[1].nextReview));

  const { score } = computeReadiness(solveLog, reviewQueue, problems);

  const radar    = computeTopicRadar(solveLog, problems);
  const allSolved = new Set(Object.values(solveLog).flat());
  const sortedTopics = RADAR_TOPICS.slice().sort((a,b) => (radar[a]||0) - (radar[b]||0));
  let newProblem = null;
  for (const topic of sortedTopics) {
    newProblem = problems.find(p => p.topics.includes(topic) && !allSolved.has(p.slug));
    if (newProblem) break;
  }
  const dueTodayFirst = due[0];

  const companyBar = (() => {
    const company = prefs.targetCompany;
    if (!company || !App.companyTags[company]) return '';
    const slugs   = App.companyTags[company];
    const solvedN = slugs.filter(s => allSolved.has(s)).length;
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

  // heat grid (364 days = 52 × 7)
  const cells = [];
  for (let i = 363; i >= 0; i--) {
    const d = daysAgo(i);
    const cnt = Math.min((solveLog[d] || []).length, 4);
    cells.push(`<div class="heat-cell" data-count="${cnt}" title="${fmtDate(d)} — ${(solveLog[d]||[]).length} solved"></div>`);
  }

  const dueHtml = due.length === 0
    ? `<div class="empty-state">✓ All caught up — no reviews due today</div>`
    : due.slice(0,8).map(([slug, d]) => {
        const p = problems.find(x => x.slug === slug);
        const title = p ? p.title : slug;
        const diff  = p ? p.difficulty : '';
        const days  = d.lastSolved ? daysBetween(d.lastSolved, today()) : '?';
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
      }).join('')
    + (due.length > 8 ? `<div class="empty-state">${due.length - 8} more due — <a href="#/review">see all →</a></div>` : '');

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
        <button class="btn-solve" onclick="openSolveModal('${slug}','${title.replace(/'/g,"\\'")}')">Review</button>
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
          <div class="card-header"><span class="card-icon">🔥</span><h2>Streak &amp; Activity</h2></div>
          <div class="heat-grid-wrap">
            <div class="heat-grid">${cells.join('')}</div>
          </div>
          <div class="streak-stats">
            <div><div class="streak-stat-val">${streakMeta.currentStreak || 0}</div><div class="streak-stat-label">Current Streak</div></div>
            <div><div class="streak-stat-val">${streakMeta.longestStreak || 0}</div><div class="streak-stat-label">Longest</div></div>
            <div><div class="streak-stat-val">${streakMeta.totalDays || 0}</div><div class="streak-stat-label">Active Days</div></div>
            <div><div class="streak-stat-val">${allSolved.size}</div><div class="streak-stat-label">Total Solved</div></div>
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
          <div class="card-header"><span class="card-icon">💡</span><h2>Today's Focus</h2></div>
          ${recHtml}
        </div>

        <div class="card fade-in-up">
          <div class="card-header">
            <span class="card-icon">📆</span>
            <h2>Daily Challenge</h2>
          </div>
          <div id="daily-challenge-body"><div class="empty-state">Loading…</div></div>
        </div>

      </div>
      <div class="dashboard-aside">

        <div class="card fade-in-up" id="lc-profile-card">
          <div class="card-header">
            <span class="card-icon">👤</span>
            <h2>LeetCode Profile</h2>
            <div class="card-header-right">
              <button class="icon-btn btn-sm" onclick="fetchLCProfile(lsGet(LS.PREFS,{}).lcUsername)" title="Refresh" id="lc-fetch-btn">↺</button>
            </div>
          </div>
          <div class="lc-profile-body"><div class="empty-state">Set your username in Settings →</div></div>
          <span class="lc-fetch-status" id="lc-fetch-status"></span>
        </div>

        <div class="card fade-in-up">
          <div class="card-header"><span class="card-icon">🏆</span><h2>Contest Rating</h2></div>
          <div id="contest-rating-body"><div class="empty-state">Fetch LC profile to see rating</div></div>
        </div>

        <div class="card fade-in-up">
          <div class="card-header"><span class="card-icon">⚡</span><h2>Recent AC</h2></div>
          <div id="recent-submissions-body"><div class="empty-state">Fetch LC profile to see submissions</div></div>
        </div>

        <div class="card fade-in-up" id="contest-card">
          <div class="card-header"><span class="card-icon">🗓</span><h2>Upcoming Contests</h2></div>
          <div id="contest-list" class="contest-list"><div class="empty-state">Loading contests…</div></div>
        </div>

      </div>
    </div>`;
}
