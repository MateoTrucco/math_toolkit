import {bootPython} from './pyodide-helper.js';let py;const tool=document.querySelector('#tool'),a=document.querySelector('#a'),b=document.querySelector('#b'),fieldB=document.querySelector('#fieldB'),labelA=document.querySelector('#labelA'),labelB=document.querySelector('#labelB'),out=document.querySelector('#output'),run=document.querySelector('#run');
const config={d2b:['Decimal integer',false,'42',''],b2d:['Binary value',false,'101010',''],root:['Non-negative integer',false,'180',''],avg:['Numbers separated by commas',false,'10, 20, 35',''],imag:['Integer exponent',false,'7',''],pct:['Base amount',true,'100','Percentage']};
function refresh(){const c=config[tool.value];labelA.textContent=c[0];fieldB.classList.toggle('hide',!c[1]);a.value=c[2];labelB.textContent=c[3]||'Value';}
async function init(){py=await bootPython(['operations.py']);run.disabled=false;calc();}
function calc(){if(!py)return;py.globals.set('a',a.value);py.globals.set('b',b.value);let code='';switch(tool.value){case'd2b':code=`from operations import decimal_to_binary
str(decimal_to_binary(int(a)))`;break;case'b2d':code=`from operations import binary_to_decimal
str(binary_to_decimal(a))`;break;case'root':code=`from operations import simplify_square_root
str(simplify_square_root(int(a)))`;break;case'avg':code=`from operations import finite_average
str(finite_average([float(x.strip()) for x in a.split(',') if x.strip()]))`;break;case'imag':code=`from operations import imaginary_power
str(imaginary_power(int(a)))`;break;case'pct':code=`from operations import apply_percentage
str(apply_percentage(float(a),float(b)))`;break;}try{out.textContent=String(py.runPython(code));}catch(e){out.textContent='Error: '+e.message;}}
run.disabled=true;tool.addEventListener('change',()=>{refresh();calc()});run.addEventListener('click',calc);refresh();init().catch(()=>{});
