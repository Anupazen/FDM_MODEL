from math import ceil, floor
from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__, template_folder='templetes')
model = pickle.load(open('model_pickle.pkl', 'rb'))  # loading the model

@app.route('/')
def home():
    return render_template('home.html')
  
@app.route('/predict',methods=['POST'])
def predict():
    """Grabs the input values and uses them to make prediction"""

    inputs=[]
    purpose_new=[]

    IsFirst = int(request.form["IsFirst"])

    if(IsFirst==1):
        Previous_loan_paid=-1
    else:
        Previous_loan_paid = int(request.form["Previous_loan_paid"])

    if(IsFirst==1):
        Current_other_loans=-1
    else:
        Current_other_loans = int(request.form["Current_other_loans"])

   
    Is_employeed = int(request.form["Is_employeed"])

    Dependents = int(request.form["Dependents"])
    Credit_card_limit = int(request.form["Credit_card_limit"])
    Credit_card_limit = ceil(Credit_card_limit/1000.0)

    Yearly_salary = int(request.form["Yearly_salary"])
    Yearly_salary = ceil(Yearly_salary/10000)

    Age = int(request.form["Age"])
    Age = floor((Age/5.0)-2)

    Saving_amount = int(request.form["Saving_amount"])
    Saving_amount = ceil((Saving_amount/1000)+1)

    Checking_amount = int(request.form["Checking_amount"])
    Checking_amount = ceil((Checking_amount/1000)+1)
 
    Purpose= int(request.form["Purpose"])

    inputs=[IsFirst,Previous_loan_paid,Current_other_loans,Is_employeed,Dependents,Credit_card_limit,Yearly_salary,Age,Saving_amount,Checking_amount]
    if(Purpose==1):
        purpose_new=[1,0,0,0,0]
    elif(Purpose==2):
        purpose_new=[0,1,0,0,0]
    elif(Purpose==3):
        purpose_new=[0,0,1,0,0]
    elif(Purpose==4):
        purpose_new=[0,0,0,1,0]
    elif(Purpose==5):
        purpose_new=[0,0,0,0,1]

    inputs = np.concatenate((inputs, purpose_new))

    prediction = model.predict([inputs])
    print(Current_other_loans)
    print(Previous_loan_paid)
    print(prediction)

    if(prediction[0]==0):
        prediction_text="This person won't be able to pay the loan amount"
    else:
        prediction_text="This person is capable of paying the loan amount"

    return render_template('index.html', prediction_text=f'{prediction_text}')

if __name__ == "__main__":
    app.run()