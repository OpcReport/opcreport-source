/* apply-legacy-redirects.js — rebuilt from gh-pages artifacts
 *
 * Pure generator approach (no after_generate route patching):
 * 1. 404.html: build the true-case path map (tags/categories + pagination)
 *    and inject it into the rendered page via an after_render filter that
 *    only touches the 404.html route.
 * 2. Legacy dated permalinks /2026/:year/:month/:day/:slug/ get meta-refresh
 *    stubs pointing to the flat canonical URLs.
 */

hexo.extend.generator.register('legacy-redirects', function(locals){
  var routes = [];

  // ---- legacy dated permalink stubs (meta refresh) ----
  var pad = function(n){ return (n < 10 ? '0' : '') + n; };
  locals.posts.each(function(post){
    var d = post.date; // moment in site timezone (Asia/Shanghai)
    var legacyPath = d.year() + '/' + pad(d.month() + 1) + '/' + pad(d.date()) + '/' + post.slug + '/index.html';
    var target = hexo.config.url + '/' + post.path;
    var stub = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n' +
      '<meta http-equiv="refresh" content="0; url=' + target + '">\n' +
      '<link rel="canonical" href="' + target + '">\n' +
      '<title>' + post.slug + ' | OPC Report</title>\n' +
      '</head>\n<body>\n<p>This page has moved to <a href="' + target + '">' + target + '</a>.</p>\n</body>\n</html>\n';
    routes.push({ path: legacyPath, data: stub });
  });

  return routes;
});

// ---- inject MAP into 404.html at render time ----
hexo.extend.filter.register('after_render:html', function(result, data){
  // only patch the 404 page (contains the placeholder marker)
  if (typeof result !== 'string' || result.indexOf('/*__LEGACY_MAP__*/') < 0) return result;

  var map = {};
  hexo.locals.get('tags').each(function(tag){
    if (!tag.length) return;
    var p = tag.path.replace(/^\/?/, '');
    map[p.toLowerCase()] = p;
  });
  hexo.locals.get('categories').each(function(cat){
    if (!cat.length) return;
    var p = cat.path.replace(/^\/?/, '');
    map[p.toLowerCase()] = p;
    var perPage = (hexo.config.category_generator && hexo.config.category_generator.per_page) || 10;
    var pages = Math.ceil(cat.posts.length / perPage);
    for (var i = 2; i <= pages; i++) {
      var pp = p + 'page/' + i + '/';
      map[pp.toLowerCase()] = pp;
    }
  });

  hexo.log.info('apply-legacy-redirects: injected ' + Object.keys(map).length + ' path mappings into 404.html');
  return result.replace('/*__LEGACY_MAP__*/{}', '/*__LEGACY_MAP__*/' + JSON.stringify(map));
});
