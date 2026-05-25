from flask import Flask, render_template, request

app = Flask(__name__)

def check_diagonal_dominance(a, b, c):
<<<<<<< HEAD

=======
>>>>>>> 14cab41ee89479e8f7c23f794cae3c3a573a2974
    n = len(b)
    violations = []

    for i in range(n):

        sub_val = abs(a[i]) if i > 0 else 0.0
        super_val = abs(c[i]) if i < n - 1 else 0.0
        diag_val = abs(b[i])

        if diag_val < (sub_val + super_val):
<<<<<<< HEAD

=======
>>>>>>> 14cab41ee89479e8f7c23f794cae3c3a573a2974
            violations.append(
                f"Row {i+1} (|{b[i]}| < |{sub_val}| + |{super_val}|)"
            )

    if violations:
<<<<<<< HEAD

        msg = (
            "Warning: The system is not strictly diagonally dominant at: "
            + ", ".join(violations)
            + ". The algorithm may become unstable or fail."
        )

=======
        msg = (
            "Warning: The system is not strictly diagonally dominant at: "
            + ", ".join(violations)
            + ". The algorithm may become unstable or fail due to division by zero."
        )
>>>>>>> 14cab41ee89479e8f7c23f794cae3c3a573a2974
        return False, msg

    return True, "Success: Matrix passes strict diagonal dominance checks."


def thomas_algorithm_with_steps(a, b, c, r):
<<<<<<< HEAD

=======
>>>>>>> 14cab41ee89479e8f7c23f794cae3c3a573a2974
    n = len(b)

    gamma = [0.0] * n
    rho = [0.0] * n
    x = [0.0] * n

    steps = []

    is_dominant, dominance_msg = check_diagonal_dominance(a, b, c)

    steps.append({
        "type": "info",
        "text": dominance_msg
    })

    # =========================
<<<<<<< HEAD
    # FORWARD SWEEP
=======
    # STAGE 1: Forward Sweep
>>>>>>> 14cab41ee89479e8f7c23f794cae3c3a573a2974
    # =========================

    steps.append({
        "type": "header",
<<<<<<< HEAD
        "text": "Stage 1: Forward Sweep"
    })

    if b[0] == 0.0:

        raise ValueError(
            "Division by zero encountered!"
=======
        "text": "Stage 1: Forward Sweep (Computing Gamma and Rho vectors)"
    })

    steps.append({
        "type": "sub-header",
        "text": "Processing Row 1"
    })

    if b[0] == 0.0:
        raise ValueError(
            "Calculation Halt: Diagonal element b_1 is exactly zero."
>>>>>>> 14cab41ee89479e8f7c23f794cae3c3a573a2974
        )

    gamma[0] = c[0] / b[0]
    rho[0] = r[0] / b[0]

    steps.append({
        "type": "equation",
        "text": (
            f"\\\\[ "
<<<<<<< HEAD
            f"\\\\gamma_1 = \\\\frac{{{c[0]}}}{{{b[0]}}} = {gamma[0]:.4f}"
=======
            f"\\\\gamma_1 = \\\\frac{{c_1}}{{b_1}} "
            f"= \\\\frac{{{c[0]:.2f}}}{{{b[0]:.2f}}} "
            f"= {gamma[0]:.4f} "
>>>>>>> 14cab41ee89479e8f7c23f794cae3c3a573a2974
            f"\\\\]"
        )
    })

    steps.append({
        "type": "equation",
        "text": (
            f"\\\\[ "
<<<<<<< HEAD
            f"\\\\rho_1 = \\\\frac{{{r[0]}}}{{{b[0]}}} = {rho[0]:.4f}"
=======
            f"\\\\rho_1 = \\\\frac{{r_1}}{{b_1}} "
            f"= \\\\frac{{{r[0]:.2f}}}{{{b[0]:.2f}}} "
            f"= {rho[0]:.4f} "
>>>>>>> 14cab41ee89479e8f7c23f794cae3c3a573a2974
            f"\\\\]"
        )
    })

    for i in range(1, n - 1):

<<<<<<< HEAD
        denom = b[i] - a[i] * gamma[i - 1]

        if denom == 0.0:

            raise ValueError(
                f"Division by zero at row {i+1}"
=======
        steps.append({
            "type": "sub-header",
            "text": f"Processing Row {i+1}"
        })

        denom = b[i] - a[i] * gamma[i - 1]

        if denom == 0.0:
            raise ValueError(
                f"Halt: Division by zero encountered at diagonal position {i+1}."
>>>>>>> 14cab41ee89479e8f7c23f794cae3c3a573a2974
            )

        gamma[i] = c[i] / denom

        rho[i] = (
            r[i] - a[i] * rho[i - 1]
        ) / denom

        steps.append({
            "type": "equation",
            "text": (
                f"\\\\[ "
<<<<<<< HEAD
                f"\\\\gamma_{{{i+1}}} = {gamma[i]:.4f}"
=======
                f"\\\\gamma_{{{i+1}}} "
                f"= \\\\frac{{c_{{{i+1}}}}}"
                f"{{b_{{{i+1}}} - a_{{{i+1}}} \\\\gamma_{{{i}}}}} "
                f"= \\\\frac{{{c[i]:.2f}}}"
                f"{{{b[i]:.2f} - ({a[i]:.2f} \\\\times {gamma[i-1]:.2f})}} "
                f"= {gamma[i]:.4f} "
>>>>>>> 14cab41ee89479e8f7c23f794cae3c3a573a2974
                f"\\\\]"
            )
        })

        steps.append({
            "type": "equation",
            "text": (
                f"\\\\[ "
<<<<<<< HEAD
                f"\\\\rho_{{{i+1}}} = {rho[i]:.4f}"
=======
                f"\\\\rho_{{{i+1}}} "
                f"= \\\\frac{{r_{{{i+1}}} - a_{{{i+1}}} \\\\rho_{{{i}}}}}"
                f"{{b_{{{i+1}}} - a_{{{i+1}}} \\\\gamma_{{{i}}}}} "
                f"= \\\\frac{{{r[i]:.2f} - ({a[i]:.2f} \\\\times {rho[i-1]:.2f})}}"
                f"{{{b[i]:.2f} - ({a[i]:.2f} \\\\times {gamma[i-1]:.2f})}} "
                f"= {rho[i]:.4f} "
>>>>>>> 14cab41ee89479e8f7c23f794cae3c3a573a2974
                f"\\\\]"
            )
        })

    # =========================
    # FINAL ROW
    # =========================

<<<<<<< HEAD
    denom_n = b[n - 1] - a[n - 1] * gamma[n - 2]

    if denom_n == 0.0:

        raise ValueError(
            "Division by zero at final row."
        )

=======
    steps.append({
        "type": "sub-header",
        "text": f"Processing Final Row {n}"
    })

    denom_n = b[n - 1] - a[n - 1] * gamma[n - 2]

    if denom_n == 0.0:
        raise ValueError(
            "Halt: Division by zero encountered at final row."
        )

>>>>>>> 14cab41ee89479e8f7c23f794cae3c3a573a2974
    gamma[n - 1] = 0.0

    rho[n - 1] = (
        r[n - 1] - a[n - 1] * rho[n - 2]
    ) / denom_n

    steps.append({
        "type": "equation",
        "text": (
            f"\\\\[ "
<<<<<<< HEAD
            f"\\\\rho_{{{n}}} = {rho[n-1]:.4f}"
=======
            f"\\\\rho_{{{n}}} "
            f"= \\\\frac{{r_{{{n}}} - a_{{{n}}} \\\\rho_{{{n-1}}}}}"
            f"{{b_{{{n}}} - a_{{{n}}} \\\\gamma_{{{n-1}}}}} "
            f"= \\\\frac{{{r[n-1]:.2f} - ({a[n-1]:.2f} \\\\times {rho[n-2]:.2f})}}"
            f"{{{b[n-1]:.2f} - ({a[n-1]:.2f} \\\\times {gamma[n-2]:.2f})}} "
            f"= {rho[n-1]:.4f} "
>>>>>>> 14cab41ee89479e8f7c23f794cae3c3a573a2974
            f"\\\\]"
        )
    })

    # =========================
<<<<<<< HEAD
    # BACKWARD SUBSTITUTION
=======
    # STAGE 2: Backward Substitution
>>>>>>> 14cab41ee89479e8f7c23f794cae3c3a573a2974
    # =========================

    steps.append({
        "type": "header",
<<<<<<< HEAD
        "text": "Stage 2: Backward Substitution"
    })

    x[n - 1] = rho[n - 1]
=======
        "text": "Stage 2: Backward Substitution (Upward Sweep)"
    })

    x[n - 1] = rho[n - 1]

    steps.append({
        "type": "equation",
        "text": (
            f"\\\\[ "
            f"x_{{{n}}} = \\\\rho_{{{n}}} "
            f"= {x[n-1]:.4f} "
            f"\\\\]"
        )
    })
>>>>>>> 14cab41ee89479e8f7c23f794cae3c3a573a2974

    for i in range(n - 2, -1, -1):

        x[i] = rho[i] - gamma[i] * x[i + 1]

        steps.append({
            "type": "equation",
            "text": (
                f"\\\\[ "
<<<<<<< HEAD
                f"x_{{{i+1}}} = {x[i]:.4f}"
=======
                f"x_{{{i+1}}} "
                f"= \\\\rho_{{{i+1}}} - \\\\gamma_{{{i+1}}}x_{{{i+2}}} "
                f"= {rho[i]:.2f} - ({gamma[i]:.2f} \\\\times {x[i+1]:.2f}) "
                f"= {x[i]:.4f} "
>>>>>>> 14cab41ee89479e8f7c23f794cae3c3a573a2974
                f"\\\\]"
            )
        })

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
<<<<<<< HEAD

=======
>>>>>>> 14cab41ee89479e8f7c23f794cae3c3a573a2974
        'b1': 2.0,
        'c1': -1.0,
        'r1': 1.0,

        'a2': -1.0,
        'b2': 2.0,
        'c2': -1.0,
        'r2': 0.0,

        'a3': -1.0,
        'b3': 2.0,
        'c3': -1.0,
        'r3': 0.0,

        'a4': -1.0,
        'b4': 2.0,
        'r4': 1.0
    }

    if request.method == 'POST':

        try:

            for key in inputs.keys():
<<<<<<< HEAD

                inputs[key] = float(
                    request.form.get(key, 0.0)
                )
=======
                inputs[key] = float(request.form.get(key, 0.0))
>>>>>>> 14cab41ee89479e8f7c23f794cae3c3a573a2974

            a = [
                0.0,
                inputs['a2'],
                inputs['a3'],
                inputs['a4']
            ]

            b = [
                inputs['b1'],
                inputs['b2'],
                inputs['b3'],
                inputs['b4']
            ]

            c = [
                inputs['c1'],
                inputs['c2'],
                inputs['c3'],
                0.0
            ]

            r = [
                inputs['r1'],
                inputs['r2'],
                inputs['r3'],
                inputs['r4']
            ]

            gamma, rho, x, calculated_steps = (
                thomas_algorithm_with_steps(a, b, c, r)
            )

            result = {
                'gamma': gamma,
                'rho': rho,
                'x': x
            }

            steps = calculated_steps

        except ValueError as ve:

            error = str(ve)

<<<<<<< HEAD
        except Exception as e:

            error = f"Unexpected Error: {str(e)}"

    return render_template(
        'index.html',
        result=result,
        error=error,
        inputs=inputs,
        steps=steps
    )


# =========================
# IMPORTANT FOR VERCEL
# =========================

handler = app
=======
        except Exception:
            error = "Invalid numerical configuration setup!"

    return render_template(
        'index.html',
        result=result,
        error=error,
        inputs=inputs,
        steps=steps
    )


# =========================
# VERCEL ENTRY POINT
# =========================

handler = app


if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> 14cab41ee89479e8f7c23f794cae3c3a573a2974
