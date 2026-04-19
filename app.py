from flask import Flask, render_template, request, redirect, session
import numpy as np
import pickle

app = Flask(__name__)
app.secret_key = 'secret123'   # required for login session

# Load model
model = pickle.load(open("model.pkl", "rb"))

# ---------------- LOGIN ---------------- #

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # simple login (you can change credentials)
        if username == 'crop' and password == '1234':
            session['user'] = username
            return redirect('/home')
        else:
            return render_template('login.html', error="Invalid Credentials")

    return render_template('login.html')


# ---------------- HOME PAGE ---------------- #

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect('/')
    return render_template('index.html')


# ---------------- PREDICTION ---------------- #

@app.route('/predict', methods=['POST'])
def predict():
    if 'user' not in session:
        return redirect('/')

    rainfall = float(request.form['rainfall'])
    temperature = float(request.form['temperature'])
    humidity = float(request.form['humidity'])
    fertilizer = float(request.form['fertilizer'])
    soil_type = int(request.form['soil_type'])

    data = np.array([[rainfall, temperature, humidity, fertilizer, soil_type]])

    prediction = float(model.predict(data)[0])

    return render_template('result.html',
                           prediction=round(prediction, 2),
                           rainfall=rainfall,
                           temperature=temperature,
                           humidity=humidity,
                           fertilizer=fertilizer,
                           soil_type=soil_type)


# ---------------- LOGOUT ---------------- #

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)