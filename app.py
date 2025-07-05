from flask import Flask, render_template, request, redirect, url_for, flash, session
import joblib

app=Flask(__name__)
app.secret_key="abc"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/quiz',methods=['GET','POST'])
def quiz():
    if request.method =='POST':
        try:
            time_spent_alone=float(request.form['time_spent_alone'])
            stage_fear=request.form['stage_fear']
            social_event_attendance=float(request.form['social_event_attendance'])
            going_outside=float(request.form['going_outside'])
            drained_after_socializing=request.form['drained_after_socializing']
            friends_circle_size=float(request.form['friends_circle_size'])
            post_frequency=float(request.form['post_frequency'])
            en=joblib.load('enc.pkl','rb')
            enc=joblib.load('encode.pkl', 'rb')
            model=joblib.load('personality.pkl')
            stage_fear=en.transform([stage_fear])[0]
            drained_after_socializing=enc.transform([drained_after_socializing])[0]
            features = [[
                time_spent_alone,
                stage_fear,
                social_event_attendance,
                going_outside,
                drained_after_socializing,
                friends_circle_size,
                post_frequency
            ]]
            prediction = model.predict(features)
            if prediction[0] == 0:
                result = "You are an extrovert."
            else:
                result = " You are an introvert."
            return render_template('quiz.html',result=f"{result}")
        except Exception as e:
            return render_template("quiz.html", result=f"Error occurred: {str(e)}")
    else:
        return render_template("quiz.html")
        
if __name__ == '__main__':
    app.run(debug=True)