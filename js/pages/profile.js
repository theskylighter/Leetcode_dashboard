/* ============================================================
   pages/profile.js — shared read-only profile view
   ============================================================ */

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
