/* ============================================================
   notes.js — per-problem notes modal
   ============================================================ */

let notesSlug      = null;
let notesSaveTimer = null;
let notesRating    = 0;

function openNotes(slug, title) {
  notesSlug = slug;
  const notes = lsGet(LS.NOTES);
  const n     = notes[slug] || {};
  document.getElementById('notes-modal-title').textContent = title || slug;
  document.getElementById('note-approach').value = n.approach || '';
  document.getElementById('note-time').value     = n.time     || '';
  document.getElementById('note-space').value    = n.space    || '';
  document.getElementById('note-gotcha').value   = n.note     || '';
  notesRating = n.rating || 0;
  renderNoteStars(notesRating);
  updateCharCount('note-approach', 'approach-count');
  updateCharCount('note-gotcha',   'gotcha-count');
  document.getElementById('notes-modal').classList.remove('hidden');
  document.getElementById('notes-save-indicator').textContent = n.updatedAt ? `Saved ${n.updatedAt}` : '';
}

function closeNotes() {
  document.getElementById('notes-modal').classList.add('hidden');
  notesSlug = null;
}

function saveNote() {
  if (!notesSlug) return;
  const notes = lsGet(LS.NOTES);
  if (!notes[notesSlug]) notes[notesSlug] = {};
  notes[notesSlug].approach  = document.getElementById('note-approach').value;
  notes[notesSlug].time      = document.getElementById('note-time').value;
  notes[notesSlug].space     = document.getElementById('note-space').value;
  notes[notesSlug].note      = document.getElementById('note-gotcha').value;
  notes[notesSlug].rating    = notesRating;
  notes[notesSlug].updatedAt = today();
  lsSet(LS.NOTES, notes);
  document.getElementById('notes-save-indicator').textContent = 'Saved ✓';
  setTimeout(() => {
    const el = document.getElementById('notes-save-indicator');
    if (el) el.textContent = '';
  }, 2000);
}

function debouncedSave() {
  clearTimeout(notesSaveTimer);
  notesSaveTimer = setTimeout(saveNote, 500);
}

function updateCharCount(inputId, countId) {
  const el  = document.getElementById(inputId);
  const cnt = document.getElementById(countId);
  if (el && cnt) cnt.textContent = `${el.value.length} / 2000`;
}

function renderNoteStars(val) {
  document.querySelectorAll('#note-stars .star').forEach(s => {
    s.classList.toggle('active', parseInt(s.dataset.v) <= val);
  });
}
