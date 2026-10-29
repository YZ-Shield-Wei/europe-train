/* Chinese homepage progressive enhancement; shared English script remains unchanged. */
(() => {
  'use strict';
  const tools = document.getElementById('guide-tools');
  const search = document.getElementById('guide-search');
  const clear = document.getElementById('clear-search');
  const reset = document.getElementById('reset-guides');
  const status = document.getElementById('guide-count');
  const empty = document.getElementById('no-guides');
  const cards = Array.from(document.querySelectorAll('.guide-card'));
  const buttons = Array.from(document.querySelectorAll('[data-filter]'));
  if (!tools || !search || !cards.length) return;

  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const indexedCards = cards.map(card => ({ card, text: normalize(card.textContent + ' ' + card.dataset.keywords) }));
  let category = 'all';

  function filterGuides() {
    const terms = normalize(search.value).trim().split(/\s+/).filter(Boolean);
    let count = 0;
    indexedCards.forEach(({ card, text }) => {
      const visible = (category === 'all' || card.dataset.category === category) && terms.every(term => text.includes(term));
      card.hidden = !visible;
      if (visible) count += 1;
    });
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
    clear.hidden = search.value.length === 0;
    empty.hidden = count !== 0;
    status.textContent = `显示 ${count} 篇指南，共 ${cards.length} 篇`;
  }
  function resetGuides() {
    search.value = '';
    category = 'all';
    filterGuides();
  }
  search.addEventListener('input', filterGuides);
  clear.addEventListener('click', () => { search.value = ''; filterGuides(); search.focus(); });
  buttons.forEach(button => button.addEventListener('click', () => { category = button.dataset.filter; filterGuides(); }));
  reset.addEventListener('click', () => { resetGuides(); search.focus(); });

  // A direct reservation link must work even when an earlier filter hid its card.
  function revealLinkedGuide() {
    if (window.location.hash !== '#reservation-guide') return;
    resetGuides();
    const guide = document.getElementById('reservation-guide');
    guide.querySelector('details').open = true;
    guide.scrollIntoView({ block: 'start' });
  }
  window.addEventListener('hashchange', revealLinkedGuide);
  document.querySelectorAll('a[href="#reservation-guide"]').forEach(link => {
    link.addEventListener('click', revealLinkedGuide);
  });
  tools.hidden = false;
  status.hidden = false;
  filterGuides();
  revealLinkedGuide();
})();
