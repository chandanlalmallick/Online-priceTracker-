/* Price Tracker — vanilla JS, no build step, no live data.
   Reads PRODUCTS from data.js and renders everything client-side. */

(function () {
  "use strict";

  // Map the simplified dropdown categories to the actual category strings
  // used in data.js, so the filter stays simple for users while the
  // dataset can have more specific categories underneath.
  var CATEGORY_GROUPS = {
    "All": null,
    "Smartphones": ["Smartphones"],
    "Laptops": ["Laptops"],
    "Televisions": ["Televisions"],
    "Cameras": ["Cameras", "Lenses"],
    "Gaming": ["Gaming", "Graphics Cards", "CPUs"],
    "Tablets": ["Tablets"],
    "Audio": ["Headphones", "Earbuds"],
    "Monitors": ["Monitors", "Projectors"],
    "Appliances": ["Air Conditioners", "Refrigerators", "Washing Machines"],
    "Other": ["Smartwatches", "Other"]
  };

  var allProducts = [];
  var chartInstance = null;

  var els = {};

  function cacheElements() {
    els.mainView = document.getElementById("main-view");
    els.detailView = document.getElementById("detailView");
    els.detailContent = document.getElementById("detailContent");
    els.backButton = document.getElementById("backButton");
    els.searchInput = document.getElementById("searchInput");
    els.categorySelect = document.getElementById("categorySelect");
    els.productGrid = document.getElementById("productGrid");
    els.resultCount = document.getElementById("resultCount");
    els.noResults = document.getElementById("noResults");
  }

  function formatINR(amount) {
    if (typeof amount !== "number" || isNaN(amount)) {
      return "—";
    }
    try {
      return "\u20B9" + amount.toLocaleString("en-IN");
    } catch (err) {
      return "\u20B9" + String(amount);
    }
  }

  function escapeHtml(str) {
    if (typeof str !== "string") return "";
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function safeProducts() {
    if (!window.PRODUCTS || !Array.isArray(window.PRODUCTS)) {
      return [];
    }
    return window.PRODUCTS.filter(function (p) {
      return p && typeof p === "object" && p.name && p.brand;
    });
  }

  function matchesSearch(product, query) {
    if (!query) return true;
    var q = query.toLowerCase();
    var fields = [product.name, product.brand, product.model, product.category];
    for (var i = 0; i < fields.length; i++) {
      var f = fields[i];
      if (typeof f === "string" && f.toLowerCase().indexOf(q) !== -1) {
        return true;
      }
    }
    return false;
  }

  function matchesCategory(product, groupValue) {
    var group = CATEGORY_GROUPS[groupValue];
    if (!group) return true; // "All"
    return group.indexOf(product.category) !== -1;
  }

  function getFilteredProducts() {
    var query = (els.searchInput.value || "").trim();
    var group = els.categorySelect.value;

    return allProducts.filter(function (p) {
      return matchesCategory(p, group) && matchesSearch(p, query);
    });
  }

  function renderCard(product) {
    var card = document.createElement("button");
    card.type = "button";
    card.className = "product-card";
    card.setAttribute("data-id", String(product.id));

    var brand = escapeHtml(product.brand || "Unknown brand");
    var name = escapeHtml(product.name || "Unnamed product");
    var category = escapeHtml(product.category || "Uncategorized");

    card.innerHTML =
      '<p class="card-brand">' + brand + '</p>' +
      '<h2 class="card-name">' + name + '</h2>' +
      '<p class="card-category">' + category + '</p>' +
      '<span class="card-link">View price history &rarr;</span>';

    card.addEventListener("click", function () {
      showDetail(product.id);
    });

    return card;
  }

  function renderGrid() {
    var filtered;
    try {
      filtered = getFilteredProducts();
    } catch (err) {
      filtered = [];
    }

    els.productGrid.innerHTML = "";

    if (filtered.length === 0) {
      els.noResults.hidden = false;
      els.resultCount.textContent = "";
      return;
    }

    els.noResults.hidden = true;
    els.resultCount.textContent = filtered.length + " product" + (filtered.length === 1 ? "" : "s");

    var fragment = document.createDocumentFragment();
    filtered.forEach(function (product) {
      try {
        fragment.appendChild(renderCard(product));
      } catch (err) {
        // Skip a single broken product card rather than breaking the whole grid.
      }
    });
    els.productGrid.appendChild(fragment);
  }

  function computeLowHigh(history) {
    if (!Array.isArray(history) || history.length === 0) {
      return { low: null, high: null };
    }
    var low = null;
    var high = null;
    history.forEach(function (entry) {
      if (entry && typeof entry.low === "number") {
        if (low === null || entry.low < low) low = entry.low;
      }
      if (entry && typeof entry.high === "number") {
        if (high === null || entry.high > high) high = entry.high;
      }
    });
    return { low: low, high: high };
  }

  function buildPriceTable(history) {
    if (!Array.isArray(history) || history.length === 0) {
      return '<p class="data-unavailable">Data unavailable</p>';
    }

    var rows = history.map(function (entry) {
      if (!entry) {
        return '<tr><td colspan="3" class="data-unavailable">Data unavailable</td></tr>';
      }
      var month = escapeHtml(entry.month || "—");
      return (
        "<tr>" +
        "<td>" + month + "</td>" +
        "<td>" + formatINR(entry.low) + "</td>" +
        "<td>" + formatINR(entry.high) + "</td>" +
        "</tr>"
      );
    }).join("");

    return (
      '<div class="table-wrap">' +
      '<table class="price-table">' +
      "<thead><tr><th>Month</th><th>Lowest</th><th>Highest</th></tr></thead>" +
      "<tbody>" + rows + "</tbody>" +
      "</table>" +
      "</div>"
    );
  }

  function renderDetail(product) {
    var history = Array.isArray(product.history) ? product.history : [];
    var stats = computeLowHigh(history);
    var range = (stats.low !== null && stats.high !== null) ? (stats.high - stats.low) : null;

    var html = "";

    html += '<div class="detail-header">';
    html += '<h2 class="detail-name">' + escapeHtml(product.name || "Unnamed product") + "</h2>";
    html += '<p class="detail-meta">' +
      escapeHtml(product.brand || "Unknown brand") + " &middot; " +
      escapeHtml(product.category || "Uncategorized") + " &middot; Model: " +
      escapeHtml(product.model || "—") +
      "</p>";
    html += "</div>";

    html += '<h3 class="section-heading">6-Month Price History</h3>';
    html += buildPriceTable(history);

    html += '<div class="summary-cards">';
    html += '<div class="summary-card"><p class="summary-label">6-Month Lowest Price</p><p class="summary-value low">' + formatINR(stats.low) + "</p></div>";
    html += '<div class="summary-card"><p class="summary-label">6-Month Highest Price</p><p class="summary-value high">' + formatINR(stats.high) + "</p></div>";
    html += '<div class="summary-card"><p class="summary-label">Price Range</p><p class="summary-value">' + (range !== null ? formatINR(range) : "—") + "</p></div>";
    html += "</div>";

    html += '<h3 class="section-heading">6-Month Price Chart</h3>';
    html += '<div class="chart-wrap">';
    if (history.length > 0) {
      html += '<canvas id="priceChart" role="img" aria-label="Line chart of monthly lowest and highest prices" height="220"></canvas>';
      html += '<p class="chart-fallback-note" id="chartFallbackNote" hidden>Chart could not be loaded — showing the table above instead.</p>';
    } else {
      html += '<p class="data-unavailable">Data unavailable</p>';
    }
    html += "</div>";

    els.detailContent.innerHTML = html;

    if (history.length > 0) {
      drawChart(history);
    }
  }

  function drawChart(history) {
    var canvas = document.getElementById("priceChart");
    var note = document.getElementById("chartFallbackNote");

    if (!canvas) return;

    if (typeof window.Chart === "undefined") {
      // Chart.js failed to load from the CDN — table above still works.
      canvas.hidden = true;
      if (note) note.hidden = false;
      return;
    }

    try {
      if (chartInstance) {
        chartInstance.destroy();
        chartInstance = null;
      }

      var labels = history.map(function (h) { return h && h.month ? h.month : "—"; });
      var lows = history.map(function (h) { return h && typeof h.low === "number" ? h.low : null; });
      var highs = history.map(function (h) { return h && typeof h.high === "number" ? h.high : null; });

      var ctx = canvas.getContext("2d");
      chartInstance = new window.Chart(ctx, {
        type: "line",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Lowest price",
              data: lows,
              borderColor: "#1f6f4f",
              backgroundColor: "#1f6f4f",
              tension: 0.15,
              spanGaps: true
            },
            {
              label: "Highest price",
              data: highs,
              borderColor: "#a3492b",
              backgroundColor: "#a3492b",
              tension: 0.15,
              spanGaps: true
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: "bottom" }
          },
          scales: {
            y: {
              ticks: {
                callback: function (value) { return formatINR(value); }
              }
            }
          }
        }
      });
    } catch (err) {
      canvas.hidden = true;
      if (note) note.hidden = false;
    }
  }

  function showDetail(productId) {
    var product = allProducts.find(function (p) { return p.id === productId; });
    if (!product) return;

    try {
      renderDetail(product);
    } catch (err) {
      els.detailContent.innerHTML = '<p class="data-unavailable">Data unavailable</p>';
    }

    els.mainView.hidden = true;
    els.detailView.hidden = false;
    window.scrollTo(0, 0);

    // Keep the view restorable on refresh via the URL hash.
    try {
      history.replaceState(null, "", "#product-" + productId);
    } catch (err) {
      /* ignore */
    }
  }

  function showList() {
    els.detailView.hidden = true;
    els.mainView.hidden = false;
    window.scrollTo(0, 0);
    try {
      history.replaceState(null, "", window.location.pathname + window.location.search);
    } catch (err) {
      /* ignore */
    }
  }

  function restoreFromHash() {
    var hash = window.location.hash || "";
    var match = hash.match(/^#product-(\d+)$/);
    if (match) {
      var id = parseInt(match[1], 10);
      var exists = allProducts.some(function (p) { return p.id === id; });
      if (exists) {
        showDetail(id);
        return true;
      }
    }
    return false;
  }

  function attachEvents() {
    els.searchInput.addEventListener("input", renderGrid);
    els.categorySelect.addEventListener("change", renderGrid);
    els.backButton.addEventListener("click", showList);
  }

  function init() {
    cacheElements();
    allProducts = safeProducts();
    attachEvents();
    renderGrid();
    restoreFromHash();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
