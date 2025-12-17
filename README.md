# TradeShift Atlas

Interactive world choropleth for exploring changes in normalized bilateral trade coupling between two periods (e.g., 2015 → 2024). Hover a country to select it as the **source**; the map colors every **target** by the signed change in that target’s share of the source country’s total bilateral trade weight.

- **Green**: target became a larger share of the source’s external trade coupling
- **Red**: target became a smaller share
- **White**: little / no change

## Data model

The frontend expects `data/data.json`:

```json
{
  "countries": ["DEU", "FRA", "..."],
  "matrix": {
    "DEU": { "DEU": 0.0, "FRA": -0.0012, "...": 0.0003 },
    "FRA": { "DEU": 0.0009, "FRA": 0.0,  "...": -0.0001 }
  }
}
````

Interpretation:

* `matrix[target][source]` is the change in **target share** of the **source** country’s total bilateral trade coupling between period1 and period0.
* Values are typically small; the UI clamps to `[-1, 1]` for display.

## Repo structure

```text
.
├── index.html
└── data/
    └── data.json
```

## Run locally

Because the page uses `fetch()`, you must serve it over HTTP (opening `index.html` directly from disk will be blocked by CORS in most browsers).

### Python (recommended)

```bash
python3 -m http.server 8000
```

Open:

* `http://localhost:8000/`


## UI behavior

* Hovering any country sets it as the new source and redraws `z` values for all targets.
* Color scale is diverging with `zmid = 0`:

  * `#a50026` (red) → decrease
  * `#ffffff` (white) → neutral
  * `#006837` (green) → increase

## License

MIT