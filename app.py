
from flask import Flask, render_template, request

app = Flask(__name__)

def check_diagonal_dominance(a, b, c):
    n = len(b)
    violations = []
    
    for i in range(n):
        sub_val = abs(a[i]) if i > 0 else 0.0
        super_val = abs(c[i]) if i < n - 1 else 0.0
        diag_val = abs(b[i])
        
        if diag_val < (sub_val + super_val):
            violations.append("Row %d (|%.2f| < |%.2f| + |%.2f|)" % (i+1, b[i], sub_val, super_val))
            
    if violations:
        msg = "Warning: The system is not strictly diagonally dominant at: " + ", ".join(violations) + ". The algorithm may become unstable."
        return False, msg
    return True, "Success: Matrix passes strict diagonal dominance checks."

def thomas_algorithm_with_steps(a, b, c, r):
    n = len(b)
    gamma = [0.0] * n
    rho = [0.0] * n
    x = [0.0] * n
    steps = []

    is_dominant, dominance_msg = check_diagonal_dominance(a, b, c)
    steps.append({"type": "info", "text": dominance_msg})

    steps.append({"type": "header", "text": "Stage 1: Forward Sweep (Computing Gamma and Rho vectors)"})
    steps.append({"type": "sub-header", "text": "Processing Row 1"})
    
    if b[0] == 0.0:
        raise ValueError("Calculation Halt: Diagonal element b_1 is exactly zero. Cannot initialize forward substitution sweep.")
        
    gamma[0] = c[0] / b[0]
    rho[0] = r[0] / b[0]
    
    # Changed delimiters to $$ for flawless MathJax parsing
    steps.append({"type": "equation", "text": r"$$\gamma_1 = \frac{c_1}{b_1} = \frac{%.2f}{%.2f} = %.4f$$" % (c[0], b[0], gamma[0])})
    steps.append({"type": "equation", "text": r"$$\rho_1 = \frac{r_1}{b_1} = \frac{%.2f}{%.2f} = %.4f$$" % (r[0], b[0], rho[0])})

    for i in range(1, n - 1):
        steps.append({"type": "sub-header", "text": "Processing Row %d" % (i+1)})
        denom = b[i] - a[i] * gamma[i-1]
        
        if denom == 0.0:
            raise ValueError("Halt: Division by zero encountered at diagonal position %d." % (i+1))
            
        gamma[i] = c[i] / denom
        rho[i] = (r[i] - a[i] * rho[i-1]) / denom
        
        # Changed delimiters to $$ for flawless MathJax parsing
        steps.append({"type": "equation", "text": r"$$\gamma_{%d} = \frac{c_{%d}}{b_{%d} - a_{%d} \gamma_{%d}} = \frac{%.2f}{%.2f - (%.2f \times %.2f)} = %.4f$$" % (i+1, i+1, i+1, i+1, i, c[i], b[i], a[i], gamma[i-1], gamma[i])})
        steps.append({"type": "equation", "text": r"$$\rho_{%d} = \frac{r_{%d} - a_{%d} \rho_{%d}}{b_{%d} - a_{%d} \gamma_{%d}} = \frac{%.2f - (%.2f \times %.2f)}{%.2f - (%.2f \times %.2f)} = %.4f$$" % (i+1, i+1, i+1, i, i+1, i+1, i, r[i], a[i], rho[i-1], b[i], a[i], gamma[i-1], rho[i])})

    steps.append({"type": "sub-header", "text": "Processing Final Row %d" % n})
    denom_n = b[n-1] - a[n-1] * gamma[n-2]
    if denom_n == 0.0:
        raise ValueError("Halt: Division by zero encountered at the final row.")
    
    gamma[n-1] = 0.0
    rho[n-1] = (r[n-1] - a[n-1] * rho[n-2]) / denom_n
    
    # Changed delimiters to $$ for flawless MathJax parsing
    steps.append({"type": "equation", "text": r"$$\rho_{%d} = \frac{r_{%d} - a_{%d} \rho_{%d}}{b_{%d} - a_{%d} \gamma_{%d}} = \frac{%.2f - (%.2f \times %.2f)}{%.2f - (%.2f \times %.2f)} = %.4f$$" % (n, n, n, n-1, n, n, n-1, r[n-1], a[n-1], rho[n-2], b[n-1], a[n-1], gamma[n-2], rho[n-1])})

    steps.append({"type": "header", "text": "Stage 2: Backward Substitution (Upward Sweep)"})
    
    x[n-1] = rho[n-1]
    steps.append({"type": "equation", "text": r"$$x_{%d} = \rho_{%d} = %.4f$$" % (n, n, x[n-1])})

    for i in range(n - 2, -1, -1):
        x[i] = rho[i] - gamma[i] * x[i+1]
        steps.append({"type": "equation", "text": r"$$x_{%d} = \rho_{%d} - \gamma_{%d} x_{%d} = %.2f - (%.2f \times %.4f) = %.4f$$" % (i+1, i+1, i+1, i+2, rho[i], gamma[i], x[i+1], x[i])})

    return gamma, rho, x, steps

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    error = None
    steps = None
    
    inputs = {
        'b1': 2.0,  'c1': -1.0, 'r1': 1.0,
        'a2': -1.0, 'b2': 2.0,  'c2': -1.0, 'r2': 0.0,
        'a3': -1.0, 'b3': 2.0,  'c3': -1.0, 'r3': 0.0,
        'a4': -1.0, 'b4': 2.0,  'r4': 1.0
    }

    if request.method == 'POST':
        try:
            for key in inputs.keys():
                inputs[key] = float(request.form.get(key, 0.0))
            
            a = [0.0, inputs['a2'], inputs['a3'], inputs['a4']]
            b = [inputs['b1'], inputs['b2'], inputs['b3'], inputs['b4']]
            c = [inputs['c1'], inputs['c2'], inputs['c3'], 0.0]
            r = [inputs['r1'], inputs['r2'], inputs['r3'], inputs['r4']]
            
            gamma, rho, x, calculated_steps = thomas_algorithm_with_steps(a, b, c, r)
            result = {'gamma': gamma, 'rho': rho, 'x': x}
            steps = calculated_steps
            
        except ValueError as ve:
            error = str(ve)
        except Exception as e:
            error = "Calculation Error: " + str(e)

    return render_template('index.html', result=result, error=error, inputs=inputs, steps=steps)

if __name__ == '__main__':
    app.run(debug=True)