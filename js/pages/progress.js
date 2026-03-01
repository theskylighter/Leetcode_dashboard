/* ============================================================
   pages/progress.js
   ============================================================ */

function renderProgress() {
  const solveLog    = lsGet(LS.SOLVE_LOG);
  const reviewQueue = lsGet(LS.REVIEW_QUEUE);
  const problems    = App.problems;
  const allSolved   = new Set(Object.values(solveLog).flat());

  const radar = computeTopicRadar(solveLog, problems);
  const topicPcts = RADAR_TOPICS.map(t => radar[t] || 0);

  const CX=140, CY=140, RMAX=110, N=RADAR_TOPICS.length;
  const pts = topicPcts.map((pct, i) => {
    const angle = (i / N) * 2 * Math.PI - Math.PI/2;
    const r = RMAX * (pct/100);
    return [CX + r*Math.cos(angle), CY + r*Math.sin(angle)];
  });
  const polyPts = pts.map(p => p.join(',')).join(' ');

  const rings = [25,50,75,100].map(pct => {
    const rpts = RADAR_TOPICS.map((_,i) => {
      const angle = (i/N)*2*Math.PI - Math.PI/2;
      const r = RMAX*(pct/100);
      return `${CX+r*Math.cos(angle)},${CY+r*Math.sin(angle)}`;
    }).join(' ');
    return `<polygon points="${rpts}" fill="none" stroke="var(--border)" stroke-width="1"/>`;
  }).join('');

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
            ${rings}${axes}
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
