from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import random

app = Flask(__name__)
app.secret_key = 'cems_full_system_key'

USERS = {"admin": "1234"}

@app.route('/')
def index():
    return redirect(url_for('dashboard')) if 'user' in session else redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if USERS.get(request.form['username']) == request.form['password']:
            session['user'] = request.form['username']
            return redirect(url_for('dashboard'))
        error = "Login Failed!"
    return render_template('login.html', error=error)

# --- จุดที่ต้องเช็ค 1: Route สำหรับหน้า Dashboard ---
@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('login'))
    return render_template('dashboard.html')

# --- จุดที่ต้องเช็ค 2: Route สำหรับหน้า Trending (ห้ามลืม!) ---
@app.route('/trending')
def trending():
    if 'user' not in session: return redirect(url_for('login'))
    return render_template('trending.html')

@app.route('/api/data')
def get_data():
    # 1. Simulate measured values
    actual_o2 = round(random.uniform(9, 12), 2)
    ref_o2 = 7.0  # Reference Oxygen level per regulations
    
    # Correction Factor Formula
    # If actual O2 is close to 21, it causes error, so cap it
    correction_factor = (21 - ref_o2) / (21 - actual_o2) if actual_o2 < 20 else 1.0

    measured = {
        "SOX": round(random.uniform(290, 305), 2),
        "NOX": round(random.uniform(270, 285), 2),
        "CO": round(random.uniform(415, 430), 2),
        "O2": actual_o2,
        "CO2": round(random.uniform(14, 16), 2),
        "PARTICULATE": round(random.uniform(80, 90), 2),
        "FLOWRATE": round(random.uniform(9500, 10500), 2),
        "OPACITY": round(random.uniform(5, 10), 2),
        "TEMP": round(random.uniform(120, 140), 2)
    }

    # 2. Calculate corrected values (measured x factor)
    corrected = {k: round(v * correction_factor, 2) if k not in ["O2", "CO2"] else v 
                 for k, v in measured.items()}

    return jsonify({
        "measured": measured,
        "corrected": corrected
    })

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)