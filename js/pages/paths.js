/* ============================================================
   pages/paths.js
   ============================================================ */

let activePathId = 'blind75';

async function renderPaths() {
  const studyPaths = lsGet(LS.STUDY_PATHS);
  const pathData   = App.pathData;
  const solveLog   = lsGet(LS.SOLVE_LOG);
  const allSolved  = new Set(Object.values(solveLog).flat());

  for (const id of PATHS) {
    if (!pathData[id]) {
      try {
        pathData[id] = await fetch(`data/paths/${id}.json`).then(r => r.json());
      } catch { pathData[id] = []; }
    }
  }

  const data      = pathData[activePathId] || [];
  const progress  = studyPaths[activePathId] || { completed:[] };
  const completed = new Set(progress.completed);

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
        return `<div class="${done ? 'path-problem-row solved' : 'path-problem-row'}"
          onclick="togglePathProblem('${activePathId}','${p.slug}','${(p.title||p.slug).replace(/'/g,"\\'")}')">
          <div class="path-checkbox">${done ? '✓' : ''}</div>
          <span class="path-prob-title">${problemLink(p.slug, p.title || p.slug)}</span>
          ${diffBadge(p.difficulty || 'medium')}
          <button class="path-prob-note-btn"
            onclick="event.stopPropagation();openNotes('${p.slug}','${(p.title||p.slug).replace(/'/g,"\\'")}')">📝</button>
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
