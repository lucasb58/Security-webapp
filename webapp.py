import os
import json
from markupsafe import Markup
from flask import Flask, url_for, render_template, request
from flask import redirect
from flask import session

app = Flask(__name__)

# In order to use "sessions",you need a "secret key".
# This is something random you generate.  
# For more info see: https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY

app.secret_key=os.environ["SECRET_KEY"]; #This is an environment variable.  
                                     #The value should be set on the server. 
                                     #To run locally, set in env.bat (env.sh on Macs) and include that file in gitignore so the secret key is not made public.

@app.route('/')
def renderMain():
    return render_template('home.html')

@app.route('/startOver')
def startOver():
    session.clear() #clears variable values and creates a new session
    return redirect(url_for('renderMain')) # url_for('renderMain') could be replaced with '/'

@app.route('/page1')
def renderPage1():
    return render_template('page1.html')

@app.route('/page2',methods=['GET','POST'])
def renderPage2():
    if "firstName" not in session:   
        session["firstName"]=request.form['firstName']
    if "lastName" not in session:   
        session["lastName"]=request.form['lastName']    
    states = get_state_options()
    return render_template('page2.html', state_options=states)

@app.route('/page3',methods=['GET','POST'])
def renderPage3():
    if "state" not in session:  
        session["state"]=request.form['state']
    return render_template('page3.html')
    
@app.route('/page4',methods=['GET','POST'])
def renderPage4():
    if "entry" not in session:  
        session["entry"]=request.form['entry']
    questionare = check_answer(session["state"] , session["entry"] )
    if questionare == 1:
        line = " Your answer was correct"
    elif questionare == 0: 
        line = "Your answer was wrong"    
    return render_template('page4.html', qoute = line)    

# select state
def get_state_options():
    with open('state.json') as states_data:
        state = json.load(states_data)
    states=[]
    for c in state:
        if c["Code"] not in states:
            states.append(c["Code"])       
    options=""
    for s in states:
        options += Markup("<option value=\"" + s + "\">" + s + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options
 
 # checks answer   
def check_answer(state, entry):
    with open('state.json') as states_data:
        states = json.load(states_data)  
    answer = 0
    for a in states:
    	if a["Code"] == state and int(a["Admission"]) == int(entry):
            answer = 1
    print(answer)        
    return answer
    	
if __name__=="__main__":
    app.run(debug=False)
