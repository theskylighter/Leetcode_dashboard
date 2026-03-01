/* ============================================================
   pages/badges.js
   ============================================================ */

function renderBadges() {
  const earned = lsGet(LS.BADGES);
  const totalEarned = Object.keys(earned).length;

  const cards = BADGE_DEFS.map(b => {
    const e = earned[b.id];
    return `<div class="badge-card ${e ? 'earned' : ''}">
      <div class="badge-icon">${b.icon}</div>
      <div class="badge-name">${b.name}</div>
      <div class="badge-desc">${b.desc}</div>
      ${e ? `<div class="badge-date">${fmtDate(e.earned)}</div>` : ''}
    </div>`;
  }).join('');

  return `
    <div class="page-header fade-in-up">
      <div class="page-title">Achievements</div>
      <div class="page-subtitle">${totalEarned} / ${BADGE_DEFS.length} earned</div>
    </div>
    <div class="card fade-in-up">
      <div class="badges-grid">${cards}</div>
    </div>`;
}
