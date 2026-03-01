// Encapsulate behavior so DOM queries happen after load
// Daily question & leaderboard + stars management

async function fetchJson(url) {
    const res = await fetch(url);
    if (!res.ok) {
        const text = await res.text().catch(() => '');
        const message = text || res.statusText || `HTTP ${res.status}`;
        const err = new Error(message);
        err.status = res.status;
        throw err;
    }
    return res.json();
}

function createRowElement(user, rank) {
    const tr = document.createElement('tr');

    // Rank cell
    const tdRank = document.createElement('td');
    const rankSpan = document.createElement('span');
    rankSpan.className = 'rank-num' + (rank === 1 ? ' gold' : rank === 2 ? ' silver' : rank === 3 ? ' bronze' : '');
    rankSpan.textContent = rank;
    tdRank.appendChild(rankSpan);

    // Username cell
    const tdUser = document.createElement('td');
    const userCell = document.createElement('div');
    userCell.className = 'username-cell';
    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.textContent = (user.username || '?')[0].toUpperCase();
    const nameSpan = document.createElement('span');
    nameSpan.textContent = user.username;
    userCell.appendChild(avatar);
    userCell.appendChild(nameSpan);
    tdUser.appendChild(userCell);

    // Stats cells
    const tdTotal = document.createElement('td');
    tdTotal.className = 'td-mono';
    tdTotal.textContent = user.solved ?? 0;

    const tdEasy = document.createElement('td');
    tdEasy.className = 'td-mono';
    tdEasy.style.color = 'var(--easy)';
    tdEasy.textContent = user.easySolved ?? 0;

    const tdMedium = document.createElement('td');
    tdMedium.className = 'td-mono';
    tdMedium.style.color = 'var(--medium)';
    tdMedium.textContent = user.mediumSolved ?? 0;

    const tdHard = document.createElement('td');
    tdHard.className = 'td-mono';
    tdHard.style.color = 'var(--hard)';
    tdHard.textContent = user.hardSolved ?? 0;

    // Profile link cell
    const tdAction = document.createElement('td');
    const a = document.createElement('a');
    a.href = `https://leetcode.com/${encodeURIComponent(user.username)}`;
    a.target = '_blank';
    a.rel = 'noopener';
    a.className = 'profile-link';
    a.textContent = '→';
    tdAction.appendChild(a);

    tr.appendChild(tdRank);
    tr.appendChild(tdUser);
    tr.appendChild(tdTotal);
    tr.appendChild(tdEasy);
    tr.appendChild(tdMedium);
    tr.appendChild(tdHard);
    tr.appendChild(tdAction);

    return tr;
}

document.addEventListener('DOMContentLoaded', () => {
    const checkBtn = document.querySelector('.btn-check');
    const dailyBtn = document.querySelector('#daily-btn');
    const checkOutput = document.querySelector('.check-output');
    const usernameInput = document.querySelector('.username-input');
    const numPara = document.querySelector('.total-number');
    const tableBody = document.getElementById('leaderboard-body');
    const stars = document.querySelector('.stars');

    // Difficulty bar elements
    const easyBar = document.getElementById('easy-bar');
    const mediumBar = document.getElementById('medium-bar');
    const hardBar = document.getElementById('hard-bar');
    const easyCount = document.getElementById('easy-count');
    const mediumCount = document.getElementById('medium-count');
    const hardCount = document.getElementById('hard-count');

    // Status message element (pre-exists in new HTML)
    let statusEl = checkOutput.querySelector('.status');
    if (!statusEl) {
        statusEl = document.createElement('div');
        statusEl.className = 'status';
        statusEl.setAttribute('aria-live', 'polite');
        checkOutput.appendChild(statusEl);
    }

    // Leaderboard persisted in localStorage
    let leaderboard = [];
    try {
        const raw = localStorage.getItem('leetdash_leaderboard');
        if (raw) leaderboard = JSON.parse(raw);
    } catch (e) {
        leaderboard = [];
    }

    function saveLeaderboard() {
        try { localStorage.setItem('leetdash_leaderboard', JSON.stringify(leaderboard)); } catch (e) {}
    }

    function renderLeaderboard() {
        tableBody.innerHTML = '';
        if (!leaderboard.length) {
            const placeholder = document.createElement('tr');
            const tdEmpty = document.createElement('td');
            tdEmpty.colSpan = 7;
            tdEmpty.style.cssText = 'text-align:center;padding:1.5rem;color:var(--muted);font-family:\'JetBrains Mono\',monospace;font-size:0.8rem';
            tdEmpty.textContent = 'No entries yet — check a username above';
            placeholder.appendChild(tdEmpty);
            tableBody.appendChild(placeholder);
            return;
        }

        // sort by total solved desc
        const sorted = leaderboard.slice().sort((a, b) => (b.solved || 0) - (a.solved || 0));
        sorted.forEach((u, i) => tableBody.appendChild(createRowElement(u, i + 1)));
    }

    async function dailyUpdate() {
        const URL = `https://alfa-leetcode-api.onrender.com/daily`;
        try {
            const data = await fetchJson(URL);
            if (dailyBtn) dailyBtn.href = data.questionLink || '#';

            const dailyTitle = document.querySelector('.question-title');
            const dailyDifficulty = document.querySelector('.daily-difficulty');
            const dailyDescription = document.querySelector('.daily-description');
            const dailyLink = document.querySelector('.daily-link');

            if (dailyTitle) {
                // Title may contain markup — render plain text for title
                dailyTitle.textContent = (data.questionTitle || data.question || 'Daily Question');
            }
            if (dailyDifficulty) {
                dailyDifficulty.textContent = data.difficulty || '-';
                dailyDifficulty.className = 'badge daily-difficulty';
                if (data.difficulty === 'Easy') {
                    dailyDifficulty.classList.add('badge-easy');
                } else if (data.difficulty === 'Medium') {
                    dailyDifficulty.classList.add('badge-medium');
                } else if (data.difficulty === 'Hard') {
                    dailyDifficulty.classList.add('badge-hard');
                }
            }
            if (dailyDescription) {
                // The API may return HTML for the question body. Render a sanitized subset of tags.
                const raw = data.questionBody || data.question || '';
                dailyDescription.innerHTML = sanitizeAllowedHtml(raw, ['p','code','strong','em','ol','ul','li','br']);
            }
            if (dailyLink) dailyLink.href = data.questionLink || '#';
        } catch (error) {
            console.error('Error fetching daily question:', error);
            const dailyTitle = document.querySelector('.daily-title');
            if (dailyTitle) dailyTitle.textContent = 'Failed to load daily question';
        }
    }

    // Very small sanitizer that keeps only a whitelist of tags and strips attributes.
    // Not a replacement for a full sanitizer library, but reasonable for simple content.
    function sanitizeAllowedHtml(htmlString, allowedTags = []) {
        if (!htmlString) return '';
        const template = document.createElement('template');
        template.innerHTML = htmlString;

        function walk(node) {
            const nodeType = node.nodeType;
            if (nodeType === Node.TEXT_NODE) return;

            if (nodeType === Node.ELEMENT_NODE) {
                const tag = node.tagName.toLowerCase();
                if (!allowedTags.includes(tag)) {
                    // replace node with its children (effectively stripping the tag)
                    const parent = node.parentNode;
                    while (node.firstChild) parent.insertBefore(node.firstChild, node);
                    parent.removeChild(node);
                    return; // children already moved — no need to recurse here
                }

                // remove all attributes for safety
                const attrs = Array.from(node.attributes || []);
                attrs.forEach(a => node.removeAttribute(a.name));
            }

            // recurse into children
            const children = Array.from(node.childNodes);
            children.forEach(child => walk(child));
        }

        walk(template.content);
        return template.innerHTML;
    }

    async function checkUser(usernameRaw) {
        const username = String(usernameRaw || '').trim().toLowerCase();
        if (!username) {
            statusEl.textContent = 'Please enter a username.';
            return;
        }
        statusEl.textContent = '';

        const URL = `https://alfa-leetcode-api.onrender.com/${encodeURIComponent(username)}/solved`;
        checkOutput.classList.add('loading');
        try {
            const data = await fetchJson(URL);
            const solved = data.solvedProblem || 0;
            const easy = data.easySolved || 0;
            const medium = data.mediumSolved || 0;
            const hard = data.hardSolved || 0;

            numPara.textContent = solved;

            // Update difficulty bars
            if (easyBar) easyBar.style.width = `${solved ? Math.round((easy / solved) * 100) : 0}%`;
            if (mediumBar) mediumBar.style.width = `${solved ? Math.round((medium / solved) * 100) : 0}%`;
            if (hardBar) hardBar.style.width = `${solved ? Math.round((hard / solved) * 100) : 0}%`;
            if (easyCount) easyCount.textContent = easy;
            if (mediumCount) mediumCount.textContent = medium;
            if (hardCount) hardCount.textContent = hard;

            // update leaderboard data structure
            const idx = leaderboard.findIndex(u => (u.username || '').toLowerCase() === username);
            const entry = {
                username: username,
                solved: solved,
                easySolved: easy,
                mediumSolved: medium,
                hardSolved: hard
            };

            if (idx >= 0) leaderboard[idx] = entry; else leaderboard.push(entry);
            saveLeaderboard();
            renderLeaderboard();
        } catch (error) {
            console.error('Error fetching solved count:', error);
            statusEl.textContent = 'Failed to fetch user data. Please try again.';
            numPara.textContent = 'Error occurred';
        } finally {
            checkOutput.classList.remove('loading');
        }
    }

    function createStars() {
        if (!stars) return;
        // avoid duplicating stars
        if (stars.children.length) return;

        // responsive count
        const viewportWidth = window.innerWidth || document.documentElement.clientWidth;
        let count = 90;
        if (viewportWidth < 480) count = 30;
        else if (viewportWidth < 768) count = 60;

        const minSize = 0.3;
        const maxSize = 3.5;
        const minDuration = 2;
        const maxDuration = 5;

        for (let i = 0; i < count; i++) {
            const star = document.createElement('div');
            star.className = 'star';
            const x = Math.random() * 100;
            const y = Math.random() * 100;
            const size = minSize + Math.random() * (maxSize - minSize);
            const duration = minDuration + Math.random() * (maxDuration - minDuration);
            star.style.cssText = `left: ${x}%; top: ${y}%; width: ${size}px; height: ${size}px; --duration: ${duration}s`;
            stars.appendChild(star);
        }
    }

    // Initial render & hooks
    renderLeaderboard();
    createStars();
    dailyUpdate();

    checkBtn.addEventListener('click', () => checkUser(usernameInput.value));
    // trigger initial check if value present
    if (usernameInput && usernameInput.value && usernameInput.value.trim()) {
        checkUser(usernameInput.value);
    }
});