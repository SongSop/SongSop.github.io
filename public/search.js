(function () {
  var input = document.getElementById("searchInput");
  var btn = document.getElementById("searchBtn");
  var results = document.getElementById("searchResults");
  if (!input || !btn || !results) return;

  var data = [];
  var loaded = false;
  var debounceTimer = null;

  function loadData() {
    if (loaded) return Promise.resolve(data);
    return fetch("/search.json")
      .then(function (r) { return r.json(); })
      .then(function (d) {
        // Pre-tokenize posts for faster search
        d.forEach(function (post) {
          post._titleTokens = tokenize(post.title);
          post._bodyTokens = tokenize(post.text);
        });
        data = d;
        loaded = true;
        return data;
      })
      .catch(function () { return []; });
  }

  // Tokenize: Chinese bigrams + single chars + English words
  function tokenize(str) {
    str = str || "";
    var tokens = [];
    // English words
    var en = str.toLowerCase().replace(/[^\w一-鿿]/g, " ").split(/\s+/).filter(function (w) {
      return w.length > 0 && !/^[一-鿿]+$/.test(w);
    });
    tokens = tokens.concat(en);
    // CJK characters
    var cjk = str.match(/[一-鿿]+/g);
    if (cjk) {
      cjk.forEach(function (seg) {
        // Bigrams
        for (var i = 0; i < seg.length - 1; i++) {
          tokens.push(seg.substring(i, i + 2));
        }
        // Single chars
        for (var j = 0; j < seg.length; j++) {
          tokens.push(seg[j]);
        }
      });
    }
    return tokens;
  }

  // Check if a query token matches a document token
  function matches(qt, dt) {
    return dt.indexOf(qt) !== -1;
  }

  function doSearch() {
    var q = input.value.trim();
    if (!q) {
      results.classList.remove("active");
      results.innerHTML = "";
      return;
    }

    loadData().then(function (posts) {
      var queryTokens = tokenize(q);
      if (!queryTokens.length) {
        results.classList.remove("active");
        return;
      }

      var scored = posts.map(function (post) {
        var score = 0;
        var matchedIn = { title: false, body: false };
        queryTokens.forEach(function (qt) {
          // Title matches: weight 5
          post._titleTokens.forEach(function (tt) {
            if (matches(qt, tt)) { score += 5; matchedIn.title = true; }
          });
          // Body matches: weight 1
          post._bodyTokens.forEach(function (bt) {
            if (matches(qt, bt)) { score += 1; matchedIn.body = true; }
          });
        });
        return { post: post, score: score, matchedIn: matchedIn };
      })
      .filter(function (r) { return r.score > 0; })
      .sort(function (a, b) { return b.score - a.score; })
      .slice(0, 10);

      render(scored, q);
      results.classList.add("active");
    });
  }

  function render(scored, query) {
    if (!scored.length) {
      results.innerHTML = '<div class="search-no-results">No results for "' + esc(query) + '"</div>';
      return;
    }
    var tags = { article: "[A]", note: "[N]", link: "[L]" };
    var html = "";
    scored.forEach(function (r) {
      var p = r.post;
      var tag = tags[p.type] || "";
      var title = hilit(p.title, query);
      var snippet = extractSnippet(p.text, query);
      var snipHtml = hilit(snippet, query);
      html +=
        '<a href="' + p.slug + '.html" class="search-result-item">' +
        '<div class="search-result-title">[' + tag + "] " + title + "</div>" +
        '<div class="search-result-meta">' + p.date + " — " + snipHtml + "</div>" +
        "</a>";
    });
    results.innerHTML = html;
  }

  function extractSnippet(text, query) {
    var maxLen = 120;
    var firstTerm = query.trim().split(/\s+/)[0].toLowerCase();
    if (!firstTerm) return text.substring(0, maxLen);
    var pos = text.toLowerCase().indexOf(firstTerm);
    if (pos === -1) pos = 0;
    var start = Math.max(0, pos - 30);
    // Back up to nearest space/CJK char boundary
    while (start > 0 && !/[，,。\s]/.test(text[start - 1]) && start > pos - 40) start--;
    var snippet = text.substring(start, start + maxLen);
    if (start > 0) snippet = "…" + snippet;
    if (start + maxLen < text.length) snippet = snippet + "…";
    return snippet;
  }

  function esc(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function hilit(text, query) {
    if (!query) return esc(text);
    var qs = query.trim().split(/\s+/).filter(function (w) { return w.length > 0; });
    var out = esc(text);
    qs.forEach(function (w) {
      var re = new RegExp("(" + escRe(w) + ")", "gi");
      out = out.replace(re, "<mark>$1</mark>");
    });
    return out;
  }

  function escRe(s) {
    return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  // Real-time search as you type
  input.addEventListener("input", function () {
    clearTimeout(debounceTimer);
    var q = input.value.trim();
    if (!q) {
      results.classList.remove("active");
      results.innerHTML = "";
      return;
    }
    debounceTimer = setTimeout(doSearch, 120);
  });

  // Click Search button
  btn.addEventListener("click", function () {
    doSearch();
  });

  // Press Enter
  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      clearTimeout(debounceTimer);
      doSearch();
    }
  });

  // Click elsewhere -> close
  document.addEventListener("click", function (e) {
    if (!input.contains(e.target) && !btn.contains(e.target) && !results.contains(e.target)) {
      results.classList.remove("active");
    }
  });

  // ESC -> close
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      results.classList.remove("active");
      input.blur();
    }
  });
})();
