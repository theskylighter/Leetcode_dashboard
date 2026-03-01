/* ============================================================
   router.js — App shell, routing, event wiring, boot
   ============================================================ */

const App = {
  problems:    [],
  companyTags: {},
  pathData:    {},
  _contestTimer: null,

  async init() {
    try { App.problems    = await fetch('data/problems.json').then(r => r.json()); }    catch(e) { console.error('problems.json load failed', e); }
    try { App.companyTags = await fetch('data/company-tags.json').then(r => r.json()); } catch(e) { console.error('company-tags.json load failed', e); }

    // Private browsing warning
    try {
      const est = await navigator.storage.estimate();
      if (est.quota < 120_000_000) {
        document.getElementById('private-banner')?.classList.remove('hidden');
      }
    } catch {}

    // Backup reminder
    const prefs = lsGet(LS.PREFS, {});
    if (prefs.lastBackupReminder) {
      if (daysBetween(prefs.lastBackupReminder, today()) >= 7) {
        document.getElementById('backup-banner')?.classList.remove('hidden');
      }
    }

    // Recompute streak + silent badge check
    updateStreakMeta(lsGet(LS.SOLVE_LOG));
    checkBadges(App.problems, true);

    App.wireEvents();
    window.addEventListener('hashchange', () => App.route());
    App.route();
  },

  route() {
    const hash = location.hash || '#/';
    let route  = hash.split('?')[0].replace('#/', '') || 'dashboard';
    if (route === '') route = 'dashboard';
    if (route.startsWith('profile')) route = 'profile';

    document.querySelectorAll('.nav-links a').forEach(a => {
      a.classList.toggle('active', a.dataset.route === route ||
        (route === 'dashboard' && a.dataset.route === 'dashboard'));
    });

    App.render(route);
  },

  async render(route) {
    if (!route) {
      const hash = location.hash || '#/';
      route = hash.split('?')[0].replace('#/', '') || 'dashboard';
      if (route === '') route = 'dashboard';
      if (route.startsWith('profile')) route = 'profile';
    }

    const container = document.getElementById('app');
    container.innerHTML = '';

    // Update streak badge in nav
    const meta = lsGet(LS.STREAK_META, {});
    const nb   = document.getElementById('nav-streak');
    if (nb) nb.textContent = `🔥 ${meta.currentStreak || 0}`;

    let html = '';
    switch (route) {
      case 'dashboard': html = renderDashboard();       break;
      case 'progress':  html = renderProgress();        break;
      case 'review':    html = renderReview();          break;
      case 'paths':     html = await renderPaths();     break;
      case 'badges':    html = renderBadges();          break;
      case 'settings':  html = renderSettings();        break;
      case 'profile':   html = renderProfile();         break;
      default:          html = renderDashboard();
    }
    container.innerHTML = html;

    // Post-render hooks
    if (route === 'dashboard') {
      App.loadContests();
      App.loadDashboardApiCards();
    }
    if (route === 'settings') {
      const cached = lsGet(LS.PREFS, {}).lcProfile;
      if (cached) renderLCProfileCard(cached);
    }
  },

  /* Load API-dependent cards on dashboard (non-blocking) */
  async loadDashboardApiCards() {
    const cached = lsGet(LS.PREFS, {}).lcProfile;
    if (cached) {
      renderLCProfileCard(cached);
      renderContestRatingCard(cached.contest);
      renderRecentSubmissionsCard(cached.acSubmission);
    }
    // Always fetch fresh daily challenge
    fetchDailyChallenge().then(data => renderDailyCard(data));
  },

  async loadContests() {
    const listEl = document.getElementById('contest-list');
    if (!listEl) return;
    const prefs = lsGet(LS.PREFS, {});
    try {
      const contests = await fetchContests();
      if (!contests.length) {
        listEl.innerHTML = `<div class="empty-state">No upcoming contests found</div>`;
        return;
      }
      listEl.innerHTML = contests.map(c => {
        const start = new Date(c.startTime * 1000);
        const now   = Date.now();
        const diff  = start - now;
        const active = prefs[`remind_${c.titleSlug}`];
        let countdownStr = '';
        if (diff > 0) {
          const h = Math.floor(diff/3600000);
          const m = Math.floor((diff%3600000)/60000);
          countdownStr = h > 24 ? `${Math.floor(h/24)}d ${h%24}h` : `${h}h ${m}m`;
        } else {
          countdownStr = 'Live!';
        }
        return `<div class="contest-card">
          <div class="contest-time-block">
            <div class="contest-countdown">${countdownStr}</div>
            <div class="contest-countdown-label">${diff > 0 ? 'to start' : ''}</div>
          </div>
          <div class="contest-info">
            <div class="contest-title">${c.title}</div>
            <div class="contest-date">${start.toLocaleDateString('en-US',{weekday:'short',month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'})}</div>
          </div>
          <button class="contest-remind ${active?'active':''}"
            onclick="toggleContestReminder('${c.titleSlug}','${(c.title||'').replace(/'/g,"\\'")}',${c.startTime})">
            🔔 Remind
          </button>
        </div>`;
      }).join('');

      clearInterval(App._contestTimer);
      App._contestTimer = setInterval(() => App.loadContests(), 60000);
    } catch {
      listEl.innerHTML = `<div class="empty-state">Could not load contests</div>`;
    }
  },

  wireEvents() {
    // Theme toggle
    const themeBtn = document.getElementById('theme-toggle');
    if (themeBtn) themeBtn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme');
      const next    = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      themeBtn.textContent = next === 'dark' ? '☀' : '🌙';
      const prefs = lsGet(LS.PREFS, {});
      prefs.theme = next; lsSet(LS.PREFS, prefs);
    });

    const savedTheme = lsGet(LS.PREFS, {}).theme || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    if (themeBtn) themeBtn.textContent = savedTheme === 'dark' ? '☀' : '🌙';

    // Backup banner
    document.getElementById('dismiss-backup-banner')?.addEventListener('click', () => {
      document.getElementById('backup-banner')?.classList.add('hidden');
      const prefs = lsGet(LS.PREFS, {});
      prefs.lastBackupReminder = today();
      lsSet(LS.PREFS, prefs);
    });

    // Notes modal
    document.getElementById('close-notes-modal')?.addEventListener('click', closeNotes);
    document.getElementById('notes-backdrop')?.addEventListener('click', closeNotes);
    document.getElementById('note-approach')?.addEventListener('input', function() {
      updateCharCount('note-approach', 'approach-count'); debouncedSave();
    });
    document.getElementById('note-gotcha')?.addEventListener('input', function() {
      updateCharCount('note-gotcha', 'gotcha-count'); debouncedSave();
    });
    document.getElementById('note-time')?.addEventListener('input',  debouncedSave);
    document.getElementById('note-space')?.addEventListener('input', debouncedSave);
    document.querySelectorAll('#note-stars .star').forEach(s => {
      s.addEventListener('click', () => {
        notesRating = parseInt(s.dataset.v);
        renderNoteStars(notesRating);
        debouncedSave();
      });
    });

    // Solve modal
    document.getElementById('close-solve-modal')?.addEventListener('click', closeSolveModal);
    document.getElementById('solve-backdrop')?.addEventListener('click',  closeSolveModal);
    document.querySelectorAll('.rating-btn').forEach(b => {
      b.addEventListener('click', () => {
        solveModalRating = parseInt(b.dataset.r);
        document.querySelectorAll('.rating-btn').forEach(x => x.classList.remove('selected'));
        b.classList.add('selected');
      });
    });
    document.getElementById('confirm-solve-btn')?.addEventListener('click', () => {
      if (!solveModalSlug) return;
      const slug   = solveModalSlug;
      const rating = solveModalRating;
      const cb     = solveModalCb;
      closeSolveModal();
      onProblemSolved(slug, rating);
      if (cb) cb(slug, rating);
      toast(`Marked solved! Next review in ${lsGet(LS.REVIEW_QUEUE)[slug]?.interval || 1}d`);
    });
  },
};

/* ── Global inline helpers ── */

function toggleContestReminder(slug, title, startTime) {
  const prefs = lsGet(LS.PREFS, {});
  const key   = `remind_${slug}`;
  if (prefs[key]) {
    prefs[key] = false;
    toast(`Reminder cancelled for ${title}`);
    lsSet(LS.PREFS, prefs);
    App.loadContests();
    return;
  }
  Notification.requestPermission().then(perm => {
    if (perm === 'granted') {
      const ms = (startTime * 1000) - Date.now() - 15 * 60 * 1000;
      if (ms > 0) {
        setTimeout(() => new Notification('LeetCode Contest Starting Soon', {
          body: `${title} starts in 15 minutes!`,
          icon: '/favicon.ico',
        }), ms);
        prefs[key] = true;
        toast(`🔔 Reminder set for ${title}`);
      } else {
        toast('Contest starts too soon', 'error');
      }
    } else {
      toast('Notification permission denied', 'error');
    }
    lsSet(LS.PREFS, prefs);
    App.loadContests();
  });
}

/* ── Boot ── */
document.addEventListener('DOMContentLoaded', () => App.init());
