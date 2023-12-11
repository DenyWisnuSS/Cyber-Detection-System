from flask import Flask,request,render_template
import numpy as np
import pandas
import sklearn
import pickle

# importing model
model = pickle.load(open('model_gdb.pkl','rb'))

# creating flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/predict",methods=['POST'])
def predict():
    attack_cat_Normal = bool(request.form['Attack Cat Normal'])
    sttl = float(request.form['sttl'])
    attack_cat_Exploits = bool(request.form['Attack Cat Exploits'])
    attack_cat_Fuzzers = bool(request.form['Attack Cat Fuzzers'])
    ct_state_ttl = float(request.form['ct state ttl'])
    dttl = float(request.form['dttl'])
    state_5 = bool(request.form['state 5'])
    dload = float(request.form['dload'])
    state_2 = bool(request.form['state 2'])

    feature_list = [attack_cat_Normal, sttl, attack_cat_Exploits, attack_cat_Fuzzers, ct_state_ttl, dttl, state_5, dload, state_2]
    single_pred = np.array(feature_list).reshape(1, -1)

    prediction = model.predict(single_pred)

    df1_resampled = {0: "Aman", 1: "Bahaya"}

    if prediction[0] in df1_resampled:
        data = df1_resampled[prediction[0]]
        result = "Status Serangan Adalah {}".format(data)
    else:
        result = "Maaf tidak diketahui."
    return render_template('index.html',result = result)




# python main
if __name__ == "__main__":
    app.run(debug=True)