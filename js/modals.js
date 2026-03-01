/* ============================================================
   modals.js — solve modal (rating), badge popup
   ============================================================ */

let solveModalSlug   = null;
let solveModalRating = 3;
let solveModalCb     = null;

function openSolveModal(slug, title, cb) {
  solveModalSlug   = slug;
  solveModalRating = 3;
  solveModalCb     = cb || null;
  document.getElementById('solve-modal-title').textContent = `Mark Solved — ${title || slug}`;
  document.querySelectorAll('.rating-btn').forEach(b => {
    b.classList.toggle('selected', parseInt(b.dataset.r) === 3);
  });
  document.getElementById('solve-modal').classList.remove('hidden');
}

function closeSolveModal() {
  document.getElementById('solve-modal').classList.add('hidden');
  solveModalSlug = null;
}
