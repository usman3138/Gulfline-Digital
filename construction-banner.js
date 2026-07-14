(function(){
  var STORAGE_KEY = 'gdConstructionBannerHiddenUntil';
  var HIDE_MS = 2 * 60 * 1000;

  var style = document.createElement('style');
  style.textContent =
    '#gd-construction-banner{background:#8a4a12;color:#fff;font-family:"Inter",sans-serif;' +
    'padding:12px 44px;font-size:0.85rem;line-height:1.5;text-align:center;position:relative;}' +
    '#gd-construction-banner .gd-banner-close{position:absolute;top:50%;right:14px;transform:translateY(-50%);' +
    'background:none;border:none;color:#fff;font-size:1.4rem;line-height:1;cursor:pointer;padding:4px 8px;}' +
    'html[dir="rtl"] #gd-construction-banner .gd-banner-close{right:auto;left:14px;}' +
    '#gd-construction-banner .gd-banner-close:hover{opacity:0.75;}';
  document.head.appendChild(style);

  function showBanner(){
    if(document.getElementById('gd-construction-banner')) return;
    var banner = document.createElement('div');
    banner.id = 'gd-construction-banner';
    banner.innerHTML =
      '<span data-lang="en">This website is under construction &mdash; we\'re still finalizing our business license, so content, pricing and services are subject to change.</span>' +
      '<span data-lang="ar">هذا الموقع قيد الإنشاء &mdash; ما زلنا في طور استكمال الرخصة التجارية، لذا قد يتغيّر المحتوى والأسعار والخدمات.</span>' +
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
