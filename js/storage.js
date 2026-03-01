/* ============================================================
   storage.js — streak, SM-2, onProblemSolved, export/import
   ============================================================ */

function computeStreak(solveLog) {
  const t = today();
  let current = 0, longest = 0, totalDays = 0, temp = 0;
  for (const d of Object.keys(solveLog)) {
    if ((solveLog[d] || []).length > 0) totalDays++;
  }
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
      if (!started) { temp = 0; continue; }
      break;
    }
  }
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
  return { currentStreak: current, longestStreak: longest, lastActiveDate, totalDays };
}

function updateStreakMeta(solveLog) {
  const meta = computeStreak(solveLog);
  lsSet(LS.STREAK_META, meta);
  return meta;
}

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

function addToSolveLog(slug) {
  const t   = today();
  const log = lsGet(LS.SOLVE_LOG);
  if (!log[t]) log[t] = [];
  if (!log[t].includes(slug)) log[t].push(slug);
  lsSet(LS.SOLVE_LOG, log);
  return log;
}

function onProblemSolved(slug, rating = 3) {
  const log   = addToSolveLog(slug);
  const queue = lsGet(LS.REVIEW_QUEUE);
  if (!queue[slug]) queue[slug] = { ease: 2.5, interval: 1, reps: 0 };
  sm2Update(queue[slug], rating);
  lsSet(LS.REVIEW_QUEUE, queue);
  updateStreakMeta(log);
  checkBadges(App.problems);
  const allSolved = new Set(Object.values(log).flat()).size;
  const meta = lsGet(LS.STREAK_META, {});
  if (allSolved === 500 || meta.currentStreak === 100) {
    setTimeout(() => exportData(true), 1200);
  }
  App.render();
}

function exportData(silent = false) {
  const out = {};
  for (const k of Object.values(LS)) {
    const v = localStorage.getItem(k);
    if (v) out[k] = JSON.parse(v);
  }
  const blob = new Blob([JSON.stringify(out, null, 2)], { type: 'application/json' });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href     = url;
  a.download = `leetdash-backup-${today()}.json`;
  a.click();
  URL.revokeObjectURL(url);
  const prefs = lsGet(LS.PREFS, {});
  prefs.lastBackupReminder = today();
  lsSet(LS.PREFS, prefs);
  if (!silent) toast('Backup downloaded ✓');
}

function importData(file) {
  const reader = new FileReader();
  reader.onload = e => {
    try {
      const data  = JSON.parse(e.target.result);
      const valid = Object.keys(data).every(k => k.startsWith('ld:'));
      if (!valid) { toast('Invalid backup file — keys must start with ld:', 'error'); return; }
      for (const [k, v] of Object.entries(data)) lsSet(k, v);
      toast('Restore complete. Reloading…');
      setTimeout(() => window.location.reload(), 1000);
    } catch {
      toast('Failed to parse backup file', 'error');
    }
  };
  reader.readAsText(file);
}
