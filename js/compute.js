/* ============================================================
   compute.js — topic radar, readiness score (pure, no side effects)
   ============================================================ */

const RADAR_TOPICS = [
  'array', 'string', 'hash-table', 'dynamic-programming',
  'tree', 'graph', 'binary-search', 'two-pointers', 'stack', 'greedy',
];

function computeTopicRadar(solveLog, problems) {
  const allSolved = new Set(Object.values(solveLog).flat());
  const topicData = {};
  for (const p of problems) {
    for (const t of (p.topics || [])) {
      if (!topicData[t]) topicData[t] = { solved: 0, total: 0 };
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

function computeReadiness(solveLog, reviewQueue, problems) {
  const allSolvedArr = Object.values(solveLog).flat();
  const allSolved    = new Set(allSolvedArr);
  const totalSolved  = allSolved.size;

  // A — volume (40)
  const compA = Math.min(totalSolved / 300, 1) * 40;

  // B — difficulty spread (20)
  let easy = 0, medium = 0, hard = 0;
  for (const slug of allSolved) {
    const p = problems.find(x => x.slug === slug);
    if (!p) continue;
    if (p.difficulty === 'easy')   easy++;
    if (p.difficulty === 'medium') medium++;
    if (p.difficulty === 'hard')   hard++;
  }
  const weightedSum = easy * 0.3 + medium * 0.5 + hard * 1.0;
  const compB = totalSolved > 0 ? Math.min(weightedSum / totalSolved, 1) * 20 : 0;

  // C — topic breadth (20)
  const radar   = computeTopicRadar(solveLog, problems);
  const covered = RADAR_TOPICS.filter(t => (radar[t] || 0) >= 10).length;
  const compC   = (covered / RADAR_TOPICS.length) * 20;

  // D — recency (10)
  const meta      = lsGet(LS.STREAK_META, {});
  const lastDate  = meta.lastActiveDate || '';
  const daysSince = lastDate ? daysBetween(lastDate, today()) : 999;
  const compD     = daysSince < 7 ? 10 : Math.max(0, 10 - daysSince);

  // E — review health (10)
  const t             = today();
  const queueEntries  = Object.values(reviewQueue);
  const overdue       = queueEntries.filter(d => d.nextReview <= t).length;
  const total         = queueEntries.length;
  const compE         = total > 0 ? (1 - overdue / total) * 10 : 10;

  const score = Math.round(compA + compB + compC + compD + compE);
  return { score, compA, compB, compC, compD, compE };
}

function readinessLevel(score) {
  if (score >= 90) return { label: 'Dream Offer Territory', color: '#22c55e' };
  if (score >= 70) return { label: 'Interview Ready — Senior', color: '#22c55e' };
  if (score >= 55) return { label: 'Interview Ready — Mid-level', color: '#f59e0b' };
  if (score >= 40) return { label: 'Intern / Entry Level', color: '#f97316' };
  return { label: 'Keep Grinding', color: '#ef4444' };
}
