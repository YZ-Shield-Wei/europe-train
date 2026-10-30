/* Collected notices are never interpreted as proof of normal train operation. */
(function (root) {
  'use strict';
  const DAY = 24 * 60 * 60 * 1000;
  function classify(payload, now) {
    if (!payload || typeof payload !== 'object' || payload.success === false) throw new Error('invalid-feed');
    const source = Array.isArray(payload.data) ? payload.data : payload.disruptions;
    if (!Array.isArray(source)) throw new Error('invalid-feed');
    const records = source.filter(x => x && typeof x === 'object' && typeof x.title === 'string' && x.title.trim()).map(x => {
      const stamp = x.updatedAt || x.updated_at || x.createdAt || x.publishedAt;
      const time = typeof stamp === 'string' ? Date.parse(stamp) : NaN;
      return {title: x.title.slice(0, 500), operator: String(x.operatorCode || x.operator || '').slice(0, 80),
        status: String(x.status || '').slice(0, 80), time: Number.isFinite(time) && time <= now + 300000 ? time : null,
        id: /^\d+$/.test(String(x.id)) && Number(x.id) >= 1 && Number(x.id) <= 1000 ? Number(x.id) : null};
    }).sort((a, b) => (b.time || 0) - (a.time || 0));
    const latest = records.find(x => x.time !== null);
    return {kind: !records.length ? 'empty' : latest && now - latest.time <= DAY ? 'fresh' : 'stale',
      records: records.slice(0, 20), latest: latest ? latest.time : null, retrieved: now};
  }
  function failure(previous) { return {kind: previous ? 'cached' : 'unavailable', previous: previous || null}; }
  const api = {classify, failure};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (!root.document) return;
  const document = root.document;
  const button = document.getElementById('check-feed');
  if (!button) return;
  const copy = JSON.parse(document.getElementById('status-copy').textContent);
  const message = document.getElementById('feed-message');
  const timing = document.getElementById('feed-timing');
  const list = document.getElementById('feed-records');
  let previous = null;
  let pending = false;
  function text(tag, value, parent) { const el = document.createElement(tag); el.textContent = value; parent.appendChild(el); return el; }
  function date(value) { return new Date(value).toLocaleString(document.documentElement.lang || 'en'); }
  function render(state) {
    message.textContent = copy[state.kind];
    const data = state.previous || state;
    timing.textContent = data.retrieved ? copy.retrieved + ': ' + date(data.retrieved) + ' · ' + copy.sourceDate + ': ' + (data.latest ? date(data.latest) : copy.undated) : '';
    list.replaceChildren();
    (data.records || []).forEach(item => {
      const article = document.createElement('article');
      text('h3', item.title, article);
      text('p', [item.operator, item.status].filter(Boolean).join(' · '), article);
      const time = text('time', item.time ? date(item.time) : copy.undated, article);
      if (item.time) time.dateTime = new Date(item.time).toISOString();
      if (item.id) { const p = document.createElement('p'); const a = text('a', copy.history + ' →', p); a.href = '/disruption/' + item.id + '.html'; article.appendChild(p); }
      list.appendChild(article);
    });
  }
  button.addEventListener('click', async function () {
    if (pending) return;
    pending = true; button.disabled = true; message.textContent = copy.loading;
    const controller = new AbortController();
    const timeout = root.setTimeout(() => controller.abort(), 8000);
    try {
      const response = await root.fetch('https://traini.ainchina.com/api/disruptions?limit=100', {signal: controller.signal, credentials: 'omit', cache: 'no-store'});
      if (!response.ok) throw new Error('unavailable');
      const result = classify(await response.json(), Date.now());
      previous = result; render(result);
    } catch (_) { render(failure(previous)); }
    finally { root.clearTimeout(timeout); pending = false; button.disabled = false; }
  });
})(typeof window === 'undefined' ? globalThis : window);
