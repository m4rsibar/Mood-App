from flask import Flask, request, jsonify, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
from flask_cors import CORS
import os

# App
app = Flask(__name__)
CORS(app)

if os.environ.get('PROD'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('LOCAL_URI')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY')

db = SQLAlchemy(app)
# Marshmallow
ma = Marshmallow(app)

# Mood Class


class Mood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    moodrating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)

    def __init__(self, date, moodrating, comment):
        self.date = date
        self.moodrating = moodrating
        self.comment = comment


class Calendar(db.Model):

    day_id = db.Column(db.Date, primary_key=True)
    year = db.Column(db.SmallInteger, nullable=False)
    month = db.Column(db.SmallInteger, nullable=False)
    day = db.Column(db.SmallInteger, nullable=False)
    day_of_week = db.Column(db.SmallInteger, nullable=False)
    day_of_year = db.Column(db.SmallInteger, nullable=False)
    week_of_year = db.Column(db.SmallInteger, nullable=False)


# Mood Schema
class MoodSchema(ma.Schema):
    class Meta:
        fields = ('id', 'date', 'moodrating', 'comment')


mood_schema = MoodSchema()
moods_schema = MoodSchema(many=True)


# Routes


@app.route('/', methods=['GET'])
def index():
    return render_template("home.html")


@app.route('/thisWeeksGraph', methods=['GET'])
def thisWeeksGraph():
    return render_template("index.html")


@app.route('/moodForm', methods=['GET'])
def form():
    return render_template("form.html")


@app.route('/mood', methods=['POST'])
def add_mood():
    date = request.form['date']
    moodrating = request.form['moodrating']
    moodratingDivided = int(moodrating)/10
    comment = request.form['comment']

    if date == '' or moodrating == '':
        flash("Required input: date and mood rating.")
        return redirect('/moodForm')

    exists = db.session.query(db.exists().where(Mood.date == date)).scalar()
    if(exists):
        flash("You've already entered a mood for this date.")
        return redirect('/moodForm')
    else:
        new_mood = Mood(date, moodratingDivided, comment)
        db.session.add(new_mood)
        db.session.commit()
        flash("Mood successfully entered.")
    return redirect('/thisWeeksGraph')


# Fetch all moods
@app.route('/getmoods', methods=['GET'])
def get_moods():
    all_moods = Mood.query.all()
    result = moods_schema.dump(all_moods)
    return jsonify(result)

# Fetch moods for a month


@app.route('/month', methods=['GET'])
# month = request.form['month']
# year = request.form['year']
def get_month_moods():
    month = 3
    year = 2020

    data = db.session.execute(
        f"SELECT * FROM mood m JOIN calendar c ON m.date=c.day_id and month={month} and year={year} order by c.day ")
    return jsonify({'result': [dict(row) for row in data]})


@app.route('/monthgraph', methods=['GET'])
def month_graph():
    return render_template("month.html")


# Fetch moods for current week
@app.route('/thisweek', methods=['GET'])
def get_weeks_moods():
    today = datetime.today()
    week = today.isocalendar()[1]
    month = today.month
    year = today.year

# Raw sql requirement
    data = db.session.execute(
        f"SELECT m.id, m.date, coalesce(m.moodrating, 0) as moodrating, m.comment, c.day_of_week FROM mood m RIGHT JOIN calendar c ON m.date=c.day_id where c.week_of_year={week} and c.day_of_week <> 0 and month={month} and year={year} union (SELECT m.id, m.date, coalesce(m.moodrating, 0) as moodrating, m.comment, c.day_of_week  FROM mood m RIGHT JOIN calendar c on m.date=c.day_id where c.week_of_year={week - 1} and c.day_of_week={0} and c.month={month} and c.year={year}) order by day_of_week")
    return jsonify({'result': [dict(row) for row in data]})


# Run server
if __name__ == '__main__':
    app.run(debug=True)
