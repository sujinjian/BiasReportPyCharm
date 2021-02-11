from flask import Flask, render_template, request, session, redirect, url_for, g
import pandas as pd
import numpy as np
import psycopg2
import pickle
import math
from scipy.spatial.distance import euclidean

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'


@app.before_request
def before_request():
    g.user = None
    #records g.user as the current user of the session
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: [self.username]>'

#A list of Users(Ignore the password, it doesn't even check for it
#Look to replace with a cfg file in the future
users = [User(id=1, username='willjsu', password="123"),
         User(id=2, username='willjsu2', password="123")
         ]

#Login function
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #Only checks for username, not password
        session.pop('user_id', None)
        username = request.form['username']

        #if username is in list of Users, redirect to profile
        user = [x for x in users if x.username == username][0]
        if user:
            session['user_id'] = user.id
            return redirect(url_for('profile'))

        return redirect(url_for('login'))
    return render_template("login.html")


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    #redirect if wrong user
    if not g.user:
        return redirect(url_for('login'))
    #2 Buttons(DataSet 1, DataSet 2), click on either
    if request.method == "POST":
        if request.method == 'POST':
            if request.form['submit_button'] == 'DataSet 1':
                return redirect(url_for('index'))
            elif request.form['submit_button'] == 'DataSet 2':
                return redirect(url_for('index'))
            else:
                pass  # unknown
    elif request.method == "GET":
        return render_template('profile.html')

    return render_template('profile.html')


@app.route('/index')
def index():
    #Ignore all this commented out code for now
    '''
    baseline_path = "Y:\\Run2\\DATA\\data_hfsmall\\baseline.csv"
    baseline = pd.read_csv(baseline_path, header=[1])
    data_path = "Y:\\Run2\\DATA\\data_hfsmall\\events.csv"
    data = pd.read_csv(data_path, header=[1])

    def format_baseline(df):
        is_icd10 = df['gender'] == "icd10"
        df2 = df[is_icd10]
        df2.columns = ["CodeType", "Code", "Patients_Baseline"]
        is_race = df['gender'] == "race"
        df3 = df[is_race]
        df3.columns = ["CodeType", "Code", "Patients_Baseline"]
        Total = df3["Patients_Baseline"].sum()
        df2["Patients_Baseline_Prob"] = df2["Patients_Baseline"] / Total
        df2 = df2.reset_index(drop=True)
        return df2

    def format_data_baseline(df):
        is_icd10 = df['ALL'] == "ICD10CM"
        df2 = df[is_icd10]
        df2.columns = ["CodeType", "Code", "Patients_Data"]
        is_race = df['ALL'] == "race"
        df3 = df[is_race]
        df3.columns = ["CodeType", "Code", "Patients_Data"]
        Total = df3["Patients_Data"].sum()
        df2["Patients_Data_Prob"] = df2["Patients_Data"] / Total
        df2 = df2.reset_index(drop=True)
        return df2

    _SQRT2 = np.sqrt(2)  # sqrt(2) with default precision np.float64

    def hellinger2(p, q):
        return euclidean(np.sqrt(p), np.sqrt(q)) / _SQRT2


    baseline = format_baseline(baseline)
    data = format_data_baseline(data)
    combined = pd.merge(baseline, data, on=['Code'])
    combined["Difference"] = combined["Patients_Data"] - combined["Patients_Baseline"]
    hellinger_value = hellinger2(combined["Patients_Data_Prob"], combined["Patients_Baseline_Prob"])
    is_icd10 = df['gender'] == "icd10"
    df2 = df[is_icd10]
    df2.columns = ["CodeType", "Code", "Patients"]
    df2 = df2.reset_index(drop=True)
    '''

    #read in pickled file
    combined = pd.read_pickle("C:\\Users\\sujin\\Documents\\College\\VACLAB\\df_Code_hf_combined")

    return render_template('index.html', tables=[combined.to_html()],
                           titles=['na', 'Baseline vs hf', 'Table2'])


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
