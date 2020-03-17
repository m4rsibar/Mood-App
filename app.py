from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime, timedelta
from flask_cors import CORS


# App
app = Flask(__name__)
CORS(app)


# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://grjibwwwdxokwx:f02ad6175a3472e6112f80ed7213b3fbff07f0ac2bf9e3bb186181e70b920d78@ec2-50-17-178-87.compute-1.amazonaws.com:5432/d4icrnr6v2qbm3'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/MoodApp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/mood', methods=['POST'])
def add_mood():
    date = request.json['date']
    moodrating = request.json['moodrating']
    comment = request.json['comment']

    new_mood = Mood(date, moodrating, comment)

    db.session.add(new_mood)
    db.session.commit()

    return mood_schema.jsonify(new_mood)


# Fetch all moods
@app.route('/mood', methods=['GET'])
def get_moods():
    all_moods = Mood.query.all()
    result = moods_schema.dump(all_moods)
    return jsonify(result)


# Fetch moods for current week
@app.route('/thisweek', methods=['GET'])
def get_weeks_moods():
    today = datetime.now().date()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    start = str(start)
    end = str(end)


# Raw sql requirement
    data = db.session.execute(
        f"SELECT m.id, m.date, coalesce(m.moodrating, 0) as moodrating, m.comment, c.day_of_week FROM mood m RIGHT JOIN calendar c ON m.date=c.day_id where c.week_of_year=11 and month=3 and year=2020 order by day_of_week")
    return jsonify({'result': [dict(row) for row in data]})
    # return jsonify(data)


# Run server
if __name__ == '__main__':
    app.run(debug=True)
