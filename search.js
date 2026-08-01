(function () {
  var input = document.getElementById("searchInput");
  var btn = document.getElementById("searchBtn");
  var results = document.getElementById("searchResults");
  if (!input || !btn || !results) return;

  var data = [];
  var loaded = false;

  function loadData() {
    if (loaded) return Promise.resolve(data);
    return fetch("search.json")
      .then(function (r) { return r.json(); })
      .then(function (d) { data = d; loaded = true; return data; })
      .catch(function () { return []; });
  }

  var tags = { article: "[A]", note: "[N]", link: "[L]" };

  function render(rows, query) {
    if (!rows.length) {
      results.innerHTML = '<div class="search-no-results">No results for "' + esc(query) + '"</div>';
      return;
    }
    var html = "";
    rows.forEach(function (r) {
      var title = hilit(r.title, query);
      var text = hilit(r.text.slice(0, 140), query);
      var tag = tags[r.type] || "";
      html +=
        '<a href="' + r.slug + '.html" class="search-result-item">' +
        '<div class="search-result-title">[' + tag + "] " + title + "</div>" +
        '<div class="search-result-meta">' + r.date + " — " + text + "</div>" +
        "</a>";
    });
    results.innerHTML = html;
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

  function doSearch() {
    var q = input.value.trim();
    if (!q) {
      results.classList.remove("active");
      results.innerHTML = "";
      return;
    }
    loadData().then(function (rows) {
      var qs = q.toLowerCase().split(/\s+/);
      var filtered = rows.filter(function (r) {
        var hay = r.title.toLowerCase() + " " + r.text.toLowerCase();
        return qs.every(function (w) { return hay.indexOf(w) !== -1; });
      });
      render(filtered.slice(0, 8), q);
      results.classList.add("active");
    });
  }

  // Click Search button
  btn.addEventListener("click", function () {
    doSearch();
  });

  // Press Enter in input
  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      doSearch();
    }
  });

  // Click elsewhere → close
  document.addEventListener("click", function (e) {
    if (!input.contains(e.target) && !btn.contains(e.target) && !results.contains(e.target)) {
      results.classList.remove("active");
    }
  });

  // ESC → close
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      results.classList.remove("active");
      input.blur();
    }
  });
})();

