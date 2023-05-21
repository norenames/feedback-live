from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# Initialize a Flask App
app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True

    # Pointing to local database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Forestwoods7818@localhost/feedback'

else:
    app.debug = False

    # Pointing to the remote database hosted in Render.com
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://feedback_live_jaqi_user:bU2oKTSgrmya0ccSp8KNIS7DPGsATK4g@dpg-chg3m6bhp8u065vsm4d0-a.oregon-postgres.render.com/feedback_live_jaqi'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Create a database object
db = SQLAlchemy(app)

# Define the structure of a database table
class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True) #primary_key --> unique indentifier of a row
    user = db.Column(db.String(200), unique=True)
    trainers = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    # Constructor (Used to create an object/clone of the Feedback Table Class)
    def __init__(self, user, trainers, rating, comments):
        self.user = user
        self.trainers = trainers
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        user = request.form['user']
        trainers = request.form['trainers']
        rating = request.form['rating']
        comments = request.form['comments']
        # print(user, trainers, rating, comments)
        if user == '' or trainers == '' or rating == '':
            return render_template('index.html', message='Please enter required fields!')
        
        if db.session.query(Feedback).filter(Feedback.user == user).count() == 0:
            data = Feedback(user, trainers, rating, comments)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')
        
        return render_template('index.html', message='You have already submitted feedback! Thank you')
    

if __name__ == '__main__':
    app.run()