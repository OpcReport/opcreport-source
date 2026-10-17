/* Custom generators: dates page, tags index, 404.html — rebuilt from gh-pages artifacts */

var NOT_FOUND_HTML = [
'<!DOCTYPE html>',
'<html lang="en">',
'<head>',
'<meta charset="utf-8">',
'<meta name="viewport" content="width=device-width,initial-scale=1">',
'<title>Page Not Found | OPC Report</title>',
'<script>',
'(function(){',
'  // Path map injected by scripts/apply-legacy-redirects.js after hexo generate.',
'  // Keys are lowercased site-relative paths; values are canonical paths.',
'  var MAP = /*__LEGACY_MAP__*/{}/*__END_LEGACY_MAP__*/;',
'  var raw = window.location.pathname;',
'  var qh = window.location.search + window.location.hash;',
'',
'  // 1. Strip a trailing /index.html (Google-indexed legacy URL form)',
'  var stripped = raw.replace(/index\\.html$/i, \'\');',
'  if (stripped !== raw) {',
'    window.location.replace(stripped + qh);',
'    return;',
'  }',
'',
'  // 2. Look up canonical target for case-variant / renamed tag & category URLs',
'  var p = raw;',
'  try { p = decodeURIComponent(p); } catch (e) {}',
'  if (p.length > 1 && p.charAt(p.length - 1) !== \'/\') p += \'/\';',
'  var target = MAP[p.replace(/^\\//, \'\').toLowerCase()];',
'  if (target && \'/\' + target !== p) {',
'    window.location.replace(\'/\' + target + qh);',
'    return;',
'  }',
'',
'  // 3. Truly missing page — show friendly 404',
'  function show() {',
'    var m = document.getElementById(\'msg\'), d = document.getElementById(\'desc\');',
'    if (m) m.style.display = \'block\';',
'    if (d) d.style.display = \'block\';',
'  }',
'  if (document.readyState === \'loading\') {',
'    document.addEventListener(\'DOMContentLoaded\', show);',
'  } else {',
'    show();',
'  }',
'})();',
'</scr' + 'ipt>',
'<style>',
'  body { font-family: -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; margin: 0; padding: 80px 20px; text-align: center; color: #262a30; background: #f4f6f8; }',
'  h1 { font-size: 48px; margin: 0 0 10px; color: #258fb8; }',
'  p { font-size: 16px; line-height: 1.6; color: #5a6270; max-width: 500px; margin: 0 auto 20px; }',
'  a { color: #258fb8; text-decoration: none; font-weight: 600; }',
'  a:hover { text-decoration: underline; }',
'  .brand { font-size: 20px; font-weight: 700; color: #262a30; margin-bottom: 8px; }',
'</style>',
'</head>',
'<body>',
'  <div class="brand">OPC Report</div>',
'  <h1 id="msg" style="display:none">404</h1>',
'  <p id="desc" style="display:none">The page you\'re looking for doesn\'t exist or has moved. Let\'s get you back on track.</p>',
'  <p><a href="https://opcreport.cn/">&larr; Back to homepage</a></p>',
'</body>',
'</html>'
].join('\n');

hexo.extend.generator.register('dates-page', function(locals){
  var daysMap = {};
  var postsData = [];
  locals.posts.sort('date', -1).each(function(post){
    var iso = post.date.toISOString(); // UTC
    var d = iso.substring(0, 10);
    var t = iso.substring(11, 16);
    daysMap[d] = (daysMap[d] || 0) + 1;
    postsData.push({
      date: d,
      time: t,
      title: post.title,
      path: '/' + post.path,
      tags: post.tags.map(function(x){ return x.name; }).toArray ? post.tags.map(function(x){ return x.name; }).toArray() : post.tags.map(function(x){ return x.name; })
    });
  });
  var days = Object.keys(daysMap).sort().reverse().map(function(d){
    return { date: d, count: daysMap[d] };
  });
  return {
    path: 'dates/index.html',
    layout: 'dates',
    data: {
      title: 'Browse by Date',
      description: 'Pick any date to see all reports published that day. Click a title to read the full report.',
      local_data: { days: days, posts_json: JSON.stringify(postsData) },
      date: new Date('2026-07-18T07:08:16.025Z')
    }
  };
});

hexo.extend.generator.register('tags-index', function(locals){
  var tags = locals.tags.sort('name', 1).filter(function(tag){
    return tag.length; // only tags with posts
  }).map(function(tag){
    return { name: tag.name, slug: tag.slug, count: tag.length };
  });
  // order by count desc (matches live site)
  tags = tags.slice().sort(function(a, b){ return b.count - a.count; });
  return {
    path: 'tags/index.html',
    layout: 'tags-index',
    data: {
      title: undefined,
      local_data: { tags: tags, tag_count: tags.length, post_count: locals.posts.length },
      date: new Date('2026-07-18T07:08:16.025Z')
    }
  };
});

hexo.extend.generator.register('not-found-page', function(locals){
  return {
    path: '404.html',
    layout: 'page',
    data: {
      title: undefined,
      slug: '',
      date: new Date('2026-09-28T05:50:57.130Z'),
      path: '404.html',
      content: NOT_FOUND_HTML,
      _content: NOT_FOUND_HTML
    }
  };
});
