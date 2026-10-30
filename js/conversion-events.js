/* First-party interaction metadata only. Uses the existing Google tag; creates no IDs or cookies. */
(function () {
  'use strict';
  if (window.__etConversionEventsBound) return;
  window.__etConversionEventsBound = true;
  function record(event) {
    if (event.type === 'auxclick' && event.button !== 1) return;
    var target = event.target;
    if (!target || typeof target.closest !== 'function') return;
    var link = target.closest('a[data-conversion-entry], a[data-conversion-product]');
    if (!link || typeof window.gtag !== 'function') return;
    var data = link.dataset;
    var affiliate = Boolean(data.conversionProduct);
    var params = {
      content_group: 'swiss_round1',
      entry_point: data.conversionEntry || data.conversionFamily || 'unknown',
      placement: data.conversionPlacement || 'unknown',
      content_language: data.conversionLanguage || document.documentElement.lang,
      page_path: window.location.pathname,
      transport_type: 'beacon'
    };
    if (affiliate) {
      params.affiliate_partner = 'klook';
      params.product = data.conversionProduct;
      params.sub_id = data.conversionSubid || 'unassigned';
    }
    try { window.gtag('event', affiliate ? 'affiliate_product_click' : 'buying_guide_click', params); }
    catch (_) { /* Navigation must work even when analytics is unavailable. */ }
  }
  document.addEventListener('click', record);
  document.addEventListener('auxclick', record);
}());
