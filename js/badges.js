/* ============================================================
   badges.js — badge definitions, evaluation, popup
   ============================================================ */

const BADGE_DEFS = [
  { id: 'first-solve',  name: 'First Blood',       icon: '🩸', desc: 'Solve your first problem'         },
  { id: 'streak-7',     name: 'Week Warrior',       icon: '🔥', desc: '7-day solving streak'             },
  { id: 'streak-30',    name: 'Monthly Grinder',    icon: '💪', desc: '30-day solving streak'            },
  { id: 'streak-100',   name: 'Century Streak',     icon: '🏆', desc: '100-day solving streak'           },
  { id: 'solved-50',    name: 'Fifty Club',         icon: '5️⃣0️⃣', desc: 'Solve 50 problems'           },
  { id: 'solved-100',   name: 'Centurion',          icon: '💯', desc: 'Solve 100 problems'               },
  { id: 'solved-250',   name: 'Quarter Thousand',   icon: '🎯', desc: 'Solve 250 problems'               },
  { id: 'solved-500',   name: 'Five Hundred',       icon: '🚀', desc: 'Solve 500 problems'               },
  { id: 'first-hard',   name: 'Hard Mode',          icon: '💀', desc: 'Solve your first hard problem'    },
  { id: 'hard-10',      name: 'Hard Hitter',        icon: '⚡', desc: 'Solve 10 hard problems'           },
  { id: 'topic-master', name: 'Topic Master',       icon: '🧠', desc: '80%+ solve rate in any topic'     },
  { id: 'blind75-done', name: 'Blind Completed',    icon: '👁', desc: 'Complete the Blind 75 path'       },
  { id: 'ready-70',     name: 'Interview Ready',    icon: '💼', desc: 'Readiness score ≥ 70'             },
  { id: 'ready-90',     name: 'Dream Offer',        icon: '🌟', desc: 'Readiness score ≥ 90'             },
];

function checkBadges(problems, silent = false) {
  const solveLog    = lsGet(LS.SOLVE_LOG);
  const streakMeta  = lsGet(LS.STREAK_META, {});
  const reviewQueue = lsGet(LS.REVIEW_QUEUE);
  const studyPaths  = lsGet(LS.STUDY_PATHS);
  const badges      = lsGet(LS.BADGES);

  const allSolved     = new Set(Object.values(solveLog).flat());
  const totalSolved   = allSolved.size;
  const currentStreak = streakMeta.currentStreak || 0;

  const hardsSolved = [...allSolved].filter(s => {
    const p = problems.find(x => x.slug === s);
    return p && p.difficulty === 'hard';
  }).length;

  const radar    = computeTopicRadar(solveLog, problems);
  const topicAt80 = Object.values(radar).some(v => v >= 80);

  const blind75done = (() => {
    const bp = studyPaths['blind75'];
    return bp && bp.total && bp.completed.length >= bp.total;
  })();

  const { score } = computeReadiness(solveLog, reviewQueue, problems);

  const conditions = {
    'first-solve':  totalSolved >= 1,
    'streak-7':     currentStreak >= 7,
    'streak-30':    currentStreak >= 30,
    'streak-100':   currentStreak >= 100,
    'solved-50':    totalSolved >= 50,
    'solved-100':   totalSolved >= 100,
    'solved-250':   totalSolved >= 250,
    'solved-500':   totalSolved >= 500,
    'first-hard':   hardsSolved >= 1,
    'hard-10':      hardsSolved >= 10,
    'topic-master': topicAt80,
    'blind75-done': blind75done,
    'ready-70':     score >= 70,
    'ready-90':     score >= 90,
  };

  const newlyEarned = [];
  const t = today();
  for (const [id, met] of Object.entries(conditions)) {
    if (met && !badges[id]) {
      badges[id] = { earned: t };
      newlyEarned.push(id);
    }
  }

  if (newlyEarned.length) {
    lsSet(LS.BADGES, badges);
    if (!silent) {
      let i = 0;
      const showNext = () => {
        if (i < newlyEarned.length) {
          showBadgePopup(newlyEarned[i++]);
          setTimeout(showNext, 3200);
        }
      };
      showNext();
    }
  }
  return badges;
}

let _popupTimer = null;

function showBadgePopup(badgeId) {
  const def   = BADGE_DEFS.find(b => b.id === badgeId);
  if (!def) return;
  const popup = document.getElementById('badge-popup');
  document.getElementById('badge-popup-icon').textContent = def.icon;
  document.getElementById('badge-popup-name').textContent = def.name;
  popup.classList.remove('hidden');
  clearTimeout(_popupTimer);
  _popupTimer = setTimeout(() => popup.classList.add('hidden'), 3000);
}
