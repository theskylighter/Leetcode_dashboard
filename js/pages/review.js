/* ============================================================
   pages/review.js
   ============================================================ */

function renderReview() {
  const queue    = lsGet(LS.REVIEW_QUEUE);
  const problems = App.problems;
  const t        = today();

  const allEntries = Object.entries(queue)
    .sort((a,b) => a[1].nextReview.localeCompare(b[1].nextReview));

  const due      = allEntries.filter(([,d]) => d.nextReview <= t);
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
          ${[1,2,3,4,5].map(r =>
            `<button class="ri-btn" data-r="${r}" onclick="quickRate('${slug}','${title.replace(/'/g,"\\'")}',${r})"
              title="${['Blackout','Hard','Ok','Good','Easy'][r-1]}">${r}</button>`
          ).join('')}
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
