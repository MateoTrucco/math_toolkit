# Math Utility Toolkit

Five small learning projects consolidated into one application:

- Decimal/binary conversion
- Square-root simplification
- Average calculator
- Powers of the imaginary unit `i`
- Percentage/tax-style calculation

The logic is separated from the interface, validates finite/range-safe values and has automated tests.

```bash
python main.py
python -m pytest tests
```

---

## Live demo

**[Open the live demo](https://mateotrucco.github.io/math_toolkit/)**

The demo runs the repository’s original Python logic directly in the browser with Pyodide 314.0.4. The desktop Tkinter interface remains available through `main.py`.

## Repository setup

This separated repository also includes:

- MIT license
- project-specific `.gitignore`
- automated tests / CI
- GitHub Pages deployment for the demo
- `screenshots/` placeholder for portfolio images

The source files from the cleaned portfolio base were preserved unless a web-demo integration file had to be added.

