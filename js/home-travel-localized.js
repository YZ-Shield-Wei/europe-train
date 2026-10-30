/* Browser-local guide filtering only: no fare/availability API or affiliate code. */
(() => {
  'use strict';
  const form = document.getElementById('route-form');
  if (!form) return;
  const origin = document.getElementById('origin');
  const destination = document.getElementById('destination');
  const cards = Array.from(document.querySelectorAll('.route-card'));
  const filters = Array.from(document.querySelectorAll('[data-region-filter]'));
  const status = document.getElementById('route-status');
  const error = document.getElementById('route-error');
  const empty = document.getElementById('empty-routes');
  const errorSame = form.dataset.errorSame;
  const resultFormat = form.dataset.resultFormat;
  if (!errorSame || !resultFormat) return;
  let region = 'all';
  const cityName = select => select.selectedOptions[0].textContent;
  function clearError() {
    error.hidden = true;
    origin.removeAttribute('aria-invalid');
    destination.removeAttribute('aria-invalid');
  }
  function showRoutes({ scroll = false, expand = false } = {}) {
    const from = origin.value;
    const to = destination.value;
    if (from && from === to) {
      error.textContent = errorSame;
      error.hidden = false;
      destination.setAttribute('aria-invalid', 'true');
      destination.focus();
      return;
    }
    clearError();
    let visible = [];
    cards.forEach(card => {
      const a = card.dataset.from, b = card.dataset.to;
      const match = (!from || from === a || from === b) && (!to || to === a || to === b) && (region === 'all' || card.dataset.region === region);
      card.hidden = !match;
      if (match) visible.push(card);
      else card.querySelector('details').open = false;
    });
    filters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.regionFilter === region)));
    const query = from && to ? `${cityName(origin)} → ${cityName(destination)} · ` : from ? `${cityName(origin)} · ` : to ? `${cityName(destination)} · ` : '';
    status.textContent = query + resultFormat.replace('{shown}', String(visible.length)).replace('{total}', String(cards.length));
    empty.hidden = visible.length !== 0;
    if (expand && visible.length === 1) visible[0].querySelector('details').open = true;
    if (scroll) {
      const section = document.getElementById('routes');
      section.scrollIntoView({ block: 'start' });
      document.getElementById('routes-title').setAttribute('tabindex', '-1');
      document.getElementById('routes-title').focus({ preventScroll: true });
    }
  }
  function resetRoutes(scroll = false) {
    origin.value = ''; destination.value = ''; region = 'all';
    cards.forEach(card => { card.querySelector('details').open = false; });
    showRoutes({scroll});
  }
  form.addEventListener('submit', event => { event.preventDefault(); region = 'all'; showRoutes({scroll: true, expand: true}); });
  document.getElementById('swap-route').addEventListener('click', () => {
    [origin.value, destination.value] = [destination.value, origin.value];
    clearError();
  });
  [origin, destination].forEach(select => select.addEventListener('change', clearError));
  document.querySelectorAll('[data-preset]').forEach(button => button.addEventListener('click', () => {
    [origin.value, destination.value] = button.dataset.preset.split(',');
    region = 'all'; showRoutes({scroll: true, expand: true});
  }));
  filters.forEach(button => button.addEventListener('click', () => {
    origin.value = ''; destination.value = ''; region = button.dataset.regionFilter;
    cards.forEach(card => { card.querySelector('details').open = false; });
    showRoutes();
  }));
  document.getElementById('reset-routes').addEventListener('click', () => resetRoutes());
  document.getElementById('empty-reset').addEventListener('click', () => resetRoutes(true));
  function revealReservation() {
    if (window.location.hash === '#reservation-guide') document.querySelector('#reservation-guide details').open = true;
  }
  window.addEventListener('hashchange', revealReservation);
  document.querySelectorAll('a[href="#reservation-guide"]').forEach(link => link.addEventListener('click', () => {
    document.querySelector('#reservation-guide details').open = true;
  }));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') document.querySelectorAll('.language-menu[open]').forEach(menu => { menu.open = false; menu.querySelector('summary').focus(); });
  });
  form.hidden = false;
  document.getElementById('route-filters').hidden = false;
  document.getElementById('reset-routes').hidden = false;
  status.hidden = false;
  showRoutes(); revealReservation();
})();
