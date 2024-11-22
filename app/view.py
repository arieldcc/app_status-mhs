from flask import render_template, request
import pickle
import numpy as np
from app import app
import os
from app import DB

@app.route('/')
def home():
    return render_template('index.html')

# Load the trained Naive Bayes model
MODEL_NB = os.path.join(os.path.dirname(__file__), 'data', 'model', 'naive_bayes_model.pkl')
MODEL_DT = os.path.join(os.path.dirname(__file__), 'data', 'model', 'decision_tree_model.pkl')

with open(MODEL_NB, 'rb') as file:
    naive_bayes_model = pickle.load(file)

with open(MODEL_DT, 'rb') as file:
    decision_tree_model = pickle.load(file, fix_imports=True)

@app.route('/naivebayes',  methods=['GET', 'POST'])
def naivebayes():
    if request.method == 'POST':
        # Get form data
        jenis_kelamin = request.form['jenis_kelamin']
        umur = request.form['umur']
        kelas = request.form['kelas']
        ips1 = request.form['ips1']
        ips2 = request.form['ips2']
        ips3 = request.form['ips3']
        ips4 = request.form['ips4']
        ips5 = request.form['ips5']

        # Convert categorical variables to numerical
        jenis_kelamin_encoded = 0 if jenis_kelamin == 'Laki-laki' else 1
        kelas_encoded = 0 if kelas == 'Reguler Pagi' else 1

        # Prepare input for the model
        input_features = np.array([jenis_kelamin_encoded, int(umur), kelas_encoded,
                                    float(ips1), float(ips2), float(ips3),
                                    float(ips4), float(ips5)]).reshape(1, -1)

        # Perform prediction
        prediction = naive_bayes_model.predict(input_features)[0]

        # Map prediction to output labels
        status = 'Lulus' if prediction == 1 else 'Drop Out'

        # Simpan ke database
        DB.insert_history(jenis_kelamin, umur, kelas, ips1, ips2, ips3, ips4, ips5, status, 'Naive Bayes')

        # Render template with input values and prediction result
        return render_template(
            'naivebayes.html',
            status=status,
            form_data={
                'jenis_kelamin': jenis_kelamin,
                'umur': umur,
                'kelas': kelas,
                'ips1': ips1,
                'ips2': ips2,
                'ips3': ips3,
                'ips4': ips4,
                'ips5': ips5
            }
        )

    # Default form rendering
    return render_template('naivebayes.html', status=None, form_data={})

@app.route('/decisiontree', methods=['GET', 'POST'])
def decisiontree():
    if request.method == 'POST':
        # Get form data
        jenis_kelamin = request.form['jenis_kelamin']
        umur = request.form['umur']
        kelas = request.form['kelas']
        ips1 = request.form['ips1']
        ips2 = request.form['ips2']
        ips3 = request.form['ips3']
        ips4 = request.form['ips4']
        ips5 = request.form['ips5']

        # Convert categorical variables to numerical (assume encoding is known)
        jenis_kelamin_encoded = 0 if jenis_kelamin == 'Laki-laki' else 1
        kelas_encoded = 0 if kelas == 'Reguler Pagi' else 1

        # Prepare input for the model
        input_features = np.array([jenis_kelamin_encoded, int(umur), kelas_encoded,
                                    float(ips1), float(ips2), float(ips3),
                                    float(ips4), float(ips5)]).reshape(1, -1)

        # Perform prediction
        prediction = decision_tree_model.predict(input_features)[0]

        # # Simpan ulang dengan joblib
        # dump(decision_tree_model, 'decision_tree_model.joblib')

        # # Muat model dengan joblib
        # model = load('decision_tree_model.joblib')

        # print(model)

        # Map prediction to output labels
        status = 'Lulus' if prediction == 1 else 'Drop Out'
        # status = 'Lulus'

        # Simpan ke database
        DB.insert_history(jenis_kelamin, umur, kelas, ips1, ips2, ips3, ips4, ips5, status, 'Decision Tree')

        # Render template with input values and prediction result
        return render_template(
            'decisiontree.html',
            status=status,
            form_data={
                'jenis_kelamin': jenis_kelamin,
                'umur': umur,
                'kelas': kelas,
                'ips1': ips1,
                'ips2': ips2,
                'ips3': ips3,
                'ips4': ips4,
                'ips5': ips5
            }
        )

    # Default form rendering
    return render_template('decisiontree.html', status=None, form_data={})

@app.route('/profil')
def profil():
    return render_template('profil.html')

@app.route('/history')
def history():
    # Ambil data menggunakan fungsi fetch_history
    data = DB.fetch_history()

    # Kirim data ke template
    return render_template(
        'history.html',
        data=data["history_data"],        # Data tabel
        gender_data=data["gender_data"], # Data grafik jenis kelamin
        class_data=data["class_data"],   # Data grafik kelas
        status_data=data["status_data"],  # Data grafik status
        model_data=data["model_data"],
        date_data=data["date_data"]
    )