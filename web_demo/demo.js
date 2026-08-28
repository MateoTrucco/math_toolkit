import { bootPython } from './pyodide-helper.js';

let py;
let history = [];
const tool = document.querySelector('#tool');
const a = document.querySelector('#a');
const b = document.querySelector('#b');
const fieldB = document.querySelector('#fieldB');
const labelA = document.querySelector('#labelA');
const labelB = document.querySelector('#labelB');
const out = document.querySelector('#output');
const run = document.querySelector('#run');
const config = {
  d2b: ['Decimal integer', false, '42', '', 'Uses Python integer formatting and preserves the sign.'],
  b2d: ['Binary value', false, '101010', '', 'Validates every digit before converting base 2 to base 10.'],
  root: ['Non-negative integer', false, '180', '', 'Extracts repeated square factors from the radicand.'],
  avg: ['Numbers separated by commas', false, '10, 20, 35', '', 'Rejects empty and non-finite datasets before computing the mean.'],
  imag: ['Integer exponent', false, '7', '', 'Reduces the exponent modulo four across the i cycle.'],
  pct: ['Base amount', true, '100', 'Percentage', 'Applies the rate as base × (1 + percentage / 100).'],
};

const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (character) => ({
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
  "'": '&#039;',
})[character]);

function renderHistory() {
  document.querySelector('#history').innerHTML = history.map((item) => `<div class="demo-row"><div><strong>${escapeHtml(item.tool)}</strong><small>${escapeHtml(item.input)}</small></div><code>${escapeHtml(item.result)}</code></div>`).join('') || '<p class="muted">Your recent calculations will appear here.</p>';
}

function refresh() {
  const current = config[tool.value];
  labelA.textContent = current[0];
  fieldB.classList.toggle('hide', !current[1]);
  a.value = current[2];
  labelB.textContent = current[3] || 'Value';
  document.querySelector('#explanation').textContent = current[4];
}

async function init() { py = await bootPython(['operations.py']); run.disabled = false; calc(); }

function calc() {
  if (!py) return;
  py.globals.set('a', a.value);
  py.globals.set('b', b.value);
  let code = '';
  switch (tool.value) {
    case 'd2b': code = `from operations import decimal_to_binary\nstr(decimal_to_binary(int(a)))`; break;
    case 'b2d': code = `from operations import binary_to_decimal\nstr(binary_to_decimal(a))`; break;
    case 'root': code = `from operations import simplify_square_root\nstr(simplify_square_root(int(a)))`; break;
    case 'avg': code = `from operations import finite_average\nstr(finite_average([float(x.strip()) for x in a.split(',') if x.strip()]))`; break;
    case 'imag': code = `from operations import imaginary_power\nstr(imaginary_power(int(a)))`; break;
    case 'pct': code = `from operations import apply_percentage\nstr(apply_percentage(float(a),float(b)))`; break;
  }
  try {
    const result = String(py.runPython(code));
    out.textContent = result;
    history = [{ tool: tool.options[tool.selectedIndex].text, input: b.value && !fieldB.classList.contains('hide') ? `${a.value}, ${b.value}` : a.value, result }, ...history].slice(0, 6);
    renderHistory();
  } catch (error) { out.textContent = `Validation error: ${error.message}`; }
}

run.disabled = true;
tool.addEventListener('change', () => { refresh(); calc(); });
run.addEventListener('click', calc);
a.addEventListener('input', calc);
b.addEventListener('input', calc);
document.querySelector('#clearHistory').addEventListener('click', () => { history = []; renderHistory(); });
refresh();
renderHistory();
init().catch(() => {});
