// vim: set ts=2 sw=2 sts=2 et ff=unix fenc=utf-8 ai :
//
//  ccocr.js    250730  cy
//  updated:    260320  clone linkage, L&F, sticky fix, i18n
//
//-------1---------2---------3---------4---------5---------6---------7--------#

/* ------------------------------------------------------------------- i18n */
const JA = (navigator.language || '').startsWith('ja');

const MSG = {
  instruction: JA
    ? '誤読があれば修正して、ページ下端の「確認終了」を押してください。'
    : 'Correct any misreadings, then click "Confirm" at the bottom left.',
  sheet: JA ? 'シート：' : 'Sheet:',
  post:  JA ? '確認終了' : 'Confirm',
};

document.addEventListener('DOMContentLoaded', () => {
  const instr = document.getElementById('instruction');
  if (instr) instr.textContent = MSG.instruction;
  const lbl = document.querySelector('#toolbar .label');
  if (lbl) lbl.textContent = MSG.sheet;
  const postBtn = document.getElementById('post');
  if (postBtn) postBtn.textContent = MSG.post;
});

/* ------------------------------------------------------------------ init */
const btns = document.querySelectorAll('.btn');
const tbls = document.querySelectorAll('table');

/* --------------------------------------------------------- clone linkage */
function bindCloneLinkage(tbl) {
  const txtRows = Array.from(tbl.querySelectorAll('tr.txt'));
  txtRows.forEach((row) => {
    row.querySelectorAll('td input').forEach((input) => {
      if (input.dataset.clone === 'true') return;
      const cells  = Array.from(row.querySelectorAll('th, td'));
      const colIdx = cells.indexOf(input.closest('td'));
      input.addEventListener('input', () => {
        const newVal = input.value;
        txtRows.forEach((r) => {
          const rcells = Array.from(r.querySelectorAll('th, td'));
          const target = rcells[colIdx];
          if (!target) return;
          const cloneInput = target.querySelector('input[data-clone="true"]');
          if (cloneInput) cloneInput.value = newVal;
        });
      });
    });
  });
}

/* -------------------------------------------------- sticky left columns
   Fix left positions for ALL rows (thead + tbody) consistently.
   The first 4 columns (doc#, pdf, page, i#) are <th> and must be sticky.
*/
function applyStickyHeaders(tbl) {
  // Compute column widths from the header row (most reliable)
  const hdrCells = Array.from(
    tbl.querySelector('thead tr')?.querySelectorAll('th') || []
  );
  const stickyCount = 4; // doc#, pdf, page, i#
  const stickyWidths = [];
  let acc = 0;
  hdrCells.forEach((th, i) => {
    if (i < stickyCount) {
      stickyWidths.push(acc);
      acc += th.offsetWidth;
    }
  });

  // Apply sticky style to every cell in sticky columns across ALL rows
  tbl.querySelectorAll('tr').forEach((row) => {
    const cells = Array.from(row.querySelectorAll('th, td'));
    cells.forEach((cell, i) => {
      if (i >= stickyCount) return;
      cell.style.position   = 'sticky';
      cell.style.left       = `${stickyWidths[i]}px`;
      cell.style.zIndex     = '2';
      // ensure background so content behind doesn't bleed through
      if (cell.tagName === 'TH') {
        cell.style.background = '#3a3a3a';
        cell.style.color      = '#fff';
      } else {
        cell.style.background = '#fff';
      }
    });
  });

  // thead th z-index higher so it sits above tbody sticky cells
  tbl.querySelectorAll('thead th').forEach((th, i) => {
    th.style.zIndex = i < stickyCount ? '4' : '3';
  });
}

/* -------------------------------------------------------------- tab click */
btns.forEach((btn) => {
  btn.addEventListener('click', () => {
    const name = btn.innerText.trim();
    btns.forEach((b) => b.removeAttribute('disabled'));
    btn.setAttribute('disabled', true);
    tbls.forEach((t) => { t.style.display = 'none'; });
    const tbl = document.querySelector(`#${CSS.escape(name)}`);
    if (!tbl) return;
    tbl.style.display = 'table';
    applyStickyHeaders(tbl);
    bindCloneLinkage(tbl);
  });
});

/* ------------------------------------------------------------ on page load */
if (btns.length >= 1) btns[0].click();

/* ----------------------------------------------------------------- submit */
const dict = {};
document.querySelector('#post').addEventListener('click', () => {
  tbls.forEach((tbl) => {
    dict[tbl.getAttribute('id')] = [];
    tbl.querySelectorAll('tr.txt').forEach((row) => {
      const ary = [];
      row.querySelectorAll('td, th').forEach((cell) => {
        const inp = cell.querySelector('input');
        ary.push(inp ? inp.value : cell.innerText);
      });
      dict[tbl.getAttribute('id')].push(ary);
    });
  });
  fetch('/post', {
    method:  'POST',
    headers: { 'content-type': 'application/json' },
    body:    JSON.stringify(dict),
  })
  .then((res) => { if (res.status === 200) window.location.href = '/bye'; })
  .catch((err) => console.error(err));
});
