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
            violations.append(f"Row {i+1} (|{b[i]}| < |{sub_val}| + |{super_val}|)")
    if violations:
        msg = "Warning: The system is not strictly diagonally dominant at: " + ", ".join(violations) + ". The algorithm may become unstable or fail due to division by zero."
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

    # --- STAGE 1: Forward Sweep ---
    steps.append({"type": "header", "text": "Stage 1: Forward Sweep (Computing Gamma and Rho vectors)"})
    steps.append({"type": "sub-header", "text": "Processing Row 1"})
    
    if b[0] == 0.0:
        raise ValueError("Calculation Halt: Diagonal element b_1 is exactly zero.")
        
    gamma[0] = c[0] / b[0]
    rho[0] = r[0] / b[0]
    
    steps.append({"type": "equation", "text": f"\\\\[ \\\\gamma_1 = \\\\frac{{c_1}}{{b_1}} = \\\\frac{{{c[0]:.2f}}}{{{b[0]:.2f}}} = {gamma[0]:.4f} \\\\]"})
    steps.append({"type": "equation", "text": f"\\\\[ \\\\rho_1 = \\\\frac{{r_1}}{{b_1}} = \\\\frac{{{r[0]:.2f}}}{{{b[0]:.2f}}} = {rho[0]:.4f} \\\\]"})

    for i in range(1, n - 1):
        steps.append({"type": "sub-header", "text": f"Processing Row {i+1}"})
        denom = b[i] - a[i] * gamma[i-1]
        if denom == 0.0:
            raise ValueError(f"Halt: Division by zero encountered at diagonal position {i+1}.")
        gamma[i] = c[i] / denom
        rho[i] = (r[i] - a[i] * rho[i-1]) / denom
        
        steps.append({"type": "equation", "text": f"\\\\[ \\\\gamma_{{{i+1}}} = \\\\frac{{c_{{{i+1}}}}}{{b_{{{i+1}}} - a_{{{i+1}}} \\\\gamma_{{{i}}}}} = \\\\frac{{{c[i]:.2f}}}{{{b[i]:.2f}} - ({a[i]:.2f} \\\\times {gamma[i-1]:.2f})} = {gamma[i]:.4f} \\\\]"})
        steps.append({"type": "equation", "text": f"\\\\[ \\\\rho_{{{i+1}}} = \\\\frac{{r_{{{i+1}}} - a_{{{i+1}}} \\\\rho_{{{i}}}}}{{b_{{{i+1}}} - a_{{{i+1}}} \\\\gamma_{{{i}}}}} = \\\\frac{{{r[i]:.2f} - ({a[i]:.2f} \\\\times {rho[i-1]:.2f})}}{{{b[i]:.2f} - ({a[i]:.2f} \\\\times {gamma[i-1]:.2f})}} = {rho[i]:.4f} \\\\]"})

    steps.append({"type": "sub-header", "text": f"Processing Final Row {n}"})
    denom_n = b[n-1] - a[n-1] * gamma[n-2]
    if denom_n == 0.0:
        raise ValueError("Halt: Division by zero encountered at final row.")
    gamma[n-1] = 0.0  
    rho[n-1] = (r[n-1] - a[n-1] * rho[n-2]) / denom_n
    
    steps.append({"type": "equation", "text": f"\\\\[ \\\\rho_{{{n}}} = \\\\frac{{r_{{{n}}} - a_{{{n}}} \\\\rho_{{{n-1}}}}}{{b_{{{n}}} - a_{{{n}}} \\\\gamma_{{{n-1}}}}} = \\\\frac{{{r[n-1]:.2f} - ({a[n-1]:.2f} \\\\times {rho[n-2]:.2f})}}{{{b[n-1]:.2f} - ({a[n-1]:.2f} \\\\times {gamma[n-2]:.2f})}} = {rho[n-1]:.4f} \\\\]"})

    # --- STAGE 2: Backward Substitution ---
    steps.append({"type": "header", "text": "Stage 2: Backward Substitution (Upward Sweep)"})
    x[n-1] = rho[n-1]
    steps.append({"type": "equation", "text": f"\\\\[ x_{{{n}}} = \\\\rho_{{{n}}} = {x[n-1]:.4f} \\\\]"})

    for i in range(n - 2, -1, -1):
        x[i] = rho[i] - gamma[i] * x[i+1]
        steps.append({"type": "equation", "text": f"\\\\[ x_{{{i+1}}} = \\\\rho_{{{i+1}}} - \\\\gamma_{{{i+1}}} x_{{{i+2}}} = {rho[i]:.2f} - ({gamma[i]:.2f} \\\\times {x[i+1]:.2f}) = {x[i]:.4f} \\\\]"})

    # PRE-FORMAT STRINGS HERE TO AVOID JINJA COMPILATION ERRORS
    formatted_gamma = [f"{v:.4f}" for v in gamma]
    formatted_rho = [f"{v:.4f}" for v in rho]
    formatted_x = [f"{v:.4f}" for v in x]

    return formatted_gamma, formatted_rho, formatted_x, steps

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
        except Exception:
            error = "Invalid numerical configuration setup!"
    return render_template('index.html', result=result, error=error, inputs=inputs, steps=steps)

# ... keep all your code above exactly the same ...

# Make sure this is explicitly exposed for Vercel
app = app

if __name__ == '__main__':
    app.run(debug=True)
