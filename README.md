# Price Tracker

A simple, static **6-Month Historical Electronics Price Report** website for 500 popular electronics products. Built with plain HTML, CSS, and JavaScript — no frameworks, no build step, no backend.

> **Demo historical data — replace with verified prices.**
> The dataset shipped in `data.js` is clearly-marked placeholder/demo data, not real recorded prices. See "Using real data" below before publishing anything as fact.

## What this is

- A static site that shows, for ~500 electronics products (smartphones, laptops, TVs, cameras, appliances, etc.), the **lowest and highest recorded price for each of the last 6 months**.
- Search by product name, brand, model, or category.
- Filter by category.
- Click a product to see its full 6-month table, a low/high/range summary, and a simple line chart.

## What this is **not**

- Not a live price tracker. It does not fetch current prices.
- Does not call any external API or scrape any retailer.
- Has no backend, database, login, or admin panel.
- Makes no claim about the current price of anything.

## Files

```
index.html   — page structure
style.css    — all styling (mobile + desktop responsive)
script.js    — search, filtering, product detail view, chart rendering
data.js      — the 500-product dataset (const PRODUCTS = [...])
README.md    — this file
```

`data.js` was generated once from `gen_data.py` (not required for deployment — the generated `data.js` is what the site actually reads). You do not need Python or any build tool to run or deploy the site.

## How the data is structured

Each product in `data.js` looks like this:

```js
{
  "id": 1,
  "brand": "Samsung",
  "name": "Galaxy S24",
  "category": "Smartphones",
  "model": "Galaxy S24",
  "history": [
    { "month": "March 2026", "low": 64999, "high": 71999 },
    { "month": "April 2026", "low": 63999, "high": 72499 },
    { "month": "May 2026",   "low": 62999, "high": 70999 },
    { "month": "June 2026",  "low": 61999, "high": 69999 },
    { "month": "July 2026",  "low": 60999, "high": 68999 },
    { "month": "August 2026","low": 59999, "high": 67999 }
  ]
}
```

`history` always holds the 6 most recent completed months in the dataset. `low` / `high` are in whole rupees; the site formats them using Indian digit grouping (e.g. `₹1,24,999`).

## Using real data

To replace the demo prices with verified real prices:

1. Open `data.js`.
2. For each product, update the `low` / `high` values under `history` with prices you have verified yourself (e.g. from your own price-tracking records, invoices, or a source you trust).
3. Once every product's data is verified, update the banner text in `index.html` (the `<div class="demo-banner">`) and the dataset comment at the top of `data.js` to reflect that the data is real, and cite where it came from.
4. Do not publish demo/placeholder numbers as if they were real recorded prices.

You can also add, remove, or edit products directly in the `PRODUCTS` array — no other file needs to change, since `script.js` reads everything dynamically from `data.js`.

## Deploying to GitHub Pages

1. Create a new GitHub repository (public, so Pages can serve it on a free plan).
2. Upload all five files (`index.html`, `style.css`, `script.js`, `data.js`, `README.md`) to the root of the repository.
3. In the repository, go to **Settings → Pages**.
4. Under **Build and deployment**, choose **Deploy from a branch**.
5. Select your branch (e.g. `main`) and the `/ (root)` folder, then save.
6. Wait a minute or two — GitHub will give you a URL like `https://<your-username>.github.io/<repo-name>/`.

No `npm install`, no build command, no config file. It's plain static files.

## Local preview

You can just open `index.html` directly in a browser, or serve the folder locally, e.g.:

```
python3 -m http.server 8000
```

then visit `http://localhost:8000`.

## Notes on the chart

The line chart on each product page uses [Chart.js](https://www.chartjs.org/) loaded from a CDN (`cdnjs.cloudflare.com`). If the CDN script fails to load (e.g. no internet access, or the CDN is blocked), the page detects this and shows a note under the chart area — the 6-month price **table** above it still works normally, so no functionality is lost.

## Accessibility & responsiveness

- Large tap targets for the search box, dropdown, and product cards (Android-friendly).
- No horizontal scrolling on the page; only the price table scrolls horizontally on very small screens, inside its own contained box.
- No unnecessary animations.
- Keyboard-focusable product cards and a visible focus outline.
- Works the same after a refresh — reopening a product's URL (with its `#product-<id>` hash) reopens that product's detail view directly.
