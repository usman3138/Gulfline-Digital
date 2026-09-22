(function(){
  var STORAGE_KEY = 'gdConstructionBannerHiddenUntil';
  var HIDE_MS = 2 * 60 * 1000;

  var style = document.createElement('style');
  style.textContent =
    '#gd-construction-banner{background:var(--sand,#EFE7D8);color:var(--teal-deep,#0D1B2A);font-family:"Inter",sans-serif;' +
    'padding:10px 44px;font-size:0.8rem;line-height:1.5;text-align:center;position:relative;' +
    'border-bottom:1px solid rgba(13,27,42,0.1);}' +
    '#gd-construction-banner .gd-banner-close{position:absolute;top:50%;right:14px;transform:translateY(-50%);' +
    'background:none;border:none;color:inherit;font-size:1.3rem;line-height:1;cursor:pointer;padding:4px 8px;opacity:0.6;}' +
    'html[dir="rtl"] #gd-construction-banner .gd-banner-close{right:auto;left:14px;}' +
    '#gd-construction-banner .gd-banner-close:hover{opacity:1;}';
  document.head.appendChild(style);

  function showBanner(){
    if(document.getElementById('gd-construction-banner')) return;
    var banner = document.createElement('div');
    banner.id = 'gd-construction-banner';
    banner.innerHTML =
      '<span data-lang="en">Gulfline Digital is a new UAE-based business, currently completing trade licence registration.</span>' +
      '<span data-lang="ar">جلف لاين ديجيتال شركة إماراتية جديدة، بصدد استكمال إجراءات الرخصة التجارية.</span>' +
      '<button type="button" class="gd-banner-close" aria-label="Close">&times;</button>';
    document.body.insertBefore(banner, document.body.firstChild);
    banner.querySelector('.gd-banner-close').addEventListener('click', function(){
      banner.remove();
      var hideUntil = Date.now() + HIDE_MS;
      localStorage.setItem(STORAGE_KEY, String(hideUntil));
      setTimeout(showBanner, HIDE_MS);
    });
  }

  var hideUntil = parseInt(localStorage.getItem(STORAGE_KEY), 10);
  if(hideUntil && Date.now() < hideUntil){
    setTimeout(showBanner, hideUntil - Date.now());
  } else {
    showBanner();
  }
})();
