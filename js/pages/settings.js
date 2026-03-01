/* ============================================================
   pages/settings.js
   ============================================================ */

function renderSettings() {
  const prefs    = lsGet(LS.PREFS, {});
  const companies = Object.keys(App.companyTags).sort();
  const sizeKB   = Math.round(lsSize() / 1024);
  const pct      = Math.min(Math.round(sizeKB / 5120 * 100), 100);

  return `
    <div class="page-header fade-in-up">
      <div class="page-title">Settings</div>
    </div>

    <div class="card fade-in-up">
      <div class="card-body">

        <div class="settings-section">
          <div class="settings-section-title">Profile</div>
          <div class="setting-row">
            <div><div class="setting-label">LeetCode Username</div><div class="setting-desc">Used for your shareable profile</div></div>
            <input class="setting-input" id="pref-username" type="text" placeholder="your_username" value="${prefs.lcUsername||''}"/>
          </div>
          <div class="setting-row">
            <div><div class="setting-label">Daily Goal</div><div class="setting-desc">Problems per day target</div></div>
            <input class="setting-input" id="pref-daily-goal" type="number" min="1" max="20" value="${prefs.dailyGoal||2}" style="max-width:80px"/>
          </div>
          <div class="setting-row">
            <div><div class="setting-label">Target Company</div><div class="setting-desc">Filter problems to company questions</div></div>
            <select class="setting-input" id="pref-company">
              <option value="">None</option>
              ${companies.map(c => `<option value="${c}" ${prefs.targetCompany===c?'selected':''}>${c.charAt(0).toUpperCase()+c.slice(1)}</option>`).join('')}
            </select>
          </div>
          <div style="margin-top:1rem;display:flex;gap:8px;flex-wrap:wrap;align-items:center">
            <button class="btn-primary btn-sm" onclick="savePrefs()">Save Settings</button>
            <button class="btn-secondary btn-sm" onclick="generateShareURL()">🔗 Share Profile</button>
          </div>
        </div>

        <div class="settings-section">
          <div class="settings-section-title">LeetCode Profile</div>
          <div class="setting-row">
            <div>
              <div class="setting-label">Fetch from LeetCode</div>
              <div class="setting-desc">Pulls your real solved stats from alfa-leetcode-api</div>
            </div>
            <div style="display:flex;flex-direction:column;align-items:flex-end;gap:4px">
              <button class="btn-primary btn-sm" id="lc-fetch-btn"
                onclick="fetchLCProfile(document.getElementById('pref-username').value.trim() || lsGet(LS.PREFS,{}).lcUsername)">
                ↺ Fetch Stats
              </button>
              <span class="lc-fetch-status" id="lc-fetch-status">${prefs.lcProfile ? `✓ Last fetched ${prefs.lcProfile.fetchedAt || ''}` : 'Not fetched yet'}</span>
            </div>
          </div>
          <div class="lc-profile-body"><!-- populated on fetch --></div>
        </div>

        <div class="settings-section">
          <div class="settings-section-title">Backup &amp; Restore</div>
          <div class="setting-row">
            <div><div class="setting-label">Download Backup</div><div class="setting-desc">Export all your data as JSON</div></div>
            <button class="btn-primary btn-sm" onclick="exportData()">⬇ Download</button>
          </div>
          <div class="setting-row">
            <div><div class="setting-label">Restore from File</div><div class="setting-desc">Import a previously downloaded backup</div></div>
            <label class="btn-secondary btn-sm" style="cursor:pointer">
              ⬆ Choose file
              <input type="file" accept=".json" style="display:none" onchange="importData(this.files[0])"/>
            </label>
          </div>
        </div>

        <div class="settings-section">
          <div class="settings-section-title">Storage</div>
          <div class="storage-meter">
            <div style="display:flex;justify-content:space-between;font-size:.78rem">
              <span>Used: <strong>${sizeKB} KB</strong></span>
              <span>Limit: <strong>5,120 KB</strong></span>
            </div>
            <div class="storage-bar-track">
              <div class="storage-bar-fill" style="width:${pct}%"></div>
            </div>
            <div class="storage-meta"><span>${pct}% used</span><span>${5120-sizeKB} KB free</span></div>
          </div>
        </div>

        <div class="settings-section">
          <div class="settings-section-title">Danger Zone</div>
          <div class="setting-row">
            <div><div class="setting-label">Reset All Data</div><div class="setting-desc" style="color:var(--hard)">This cannot be undone</div></div>
            <button class="btn-primary btn-sm btn-danger" onclick="resetAllData()">🗑 Reset</button>
          </div>
        </div>

      </div>
    </div>`;
}

function savePrefs() {
  const prefs = lsGet(LS.PREFS, {});
  prefs.lcUsername    = document.getElementById('pref-username')?.value.trim() || '';
  prefs.dailyGoal     = parseInt(document.getElementById('pref-daily-goal')?.value) || 2;
  prefs.targetCompany = document.getElementById('pref-company')?.value || '';
  lsSet(LS.PREFS, prefs);
  toast('Settings saved ✓');
  App.render();
}

function resetAllData() {
  if (!confirm('This will permanently delete ALL your LeetDash data. Are you sure?')) return;
  for (const k of Object.values(LS)) localStorage.removeItem(k);
  toast('Data cleared');
  App.render();
}
