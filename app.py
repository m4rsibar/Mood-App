from flask import Flask, request, jsonify, render_template, redirect, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import datetime
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# if os.environ.get('PROD'):
#     app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# else:
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/MoodApp'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY')

db = SQLAlchemy(app)
ma = Marshmallow(app)


# Classes
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


# Schemas
class MoodSchema(ma.Schema):
    class Meta:
        fields = ('id', 'date', 'moodrating', 'comment')


mood_schema = MoodSchema()
moods_schema = MoodSchema(many=True)


def tableExists(tableName):
    exists = db.session.execute(
        f"SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_schema = 'public'AND table_name = '{tableName}');"
    )
    return (exists.first()[0])


def isTableEmpty(tableName):
    IsEmpty = db.session.execute(
        f"SELECT CASE WHEN EXISTS(SELECT 1 FROM {tableName}) THEN 0 ELSE 1 END;"
    )
    return (IsEmpty.first()[0])


def FillCalendar():
    db.session.execute(
        f" INSERT INTO calendar (day_id, year, month, day, day_of_week, day_of_year, week_of_year)(SELECT ts,EXTRACT(YEAR FROM ts),EXTRACT(MONTH FROM ts),EXTRACT(DAY FROM ts),EXTRACT(DOW FROM ts),EXTRACT(DOY FROM ts),EXTRACT(WEEK FROM ts)FROM generate_series('2019-01-01'::timestamp, '2038-01-01', '1day'::interval) AS t(ts));"
    )
    db.session.commit()
    print('populated')


if tableExists('calendar') is True:
    if isTableEmpty('calendar') == 1:
        FillCalendar()
    else:
        print("Calendar table is populated.")


# Routes
@app.route('/', methods=['GET'])
def week():
    return render_template("home.html")


@app.route('/thisWeeksGraph', methods=['GET'])
def this_weeks_graph():
    return render_template("week.html")


@app.route('/moodForm', methods=['GET'])
def form():
    return render_template("form.html")


@app.route('/getmoods', methods=['GET'])
def get_moods():
    all_moods = Mood.query.all()
    result = moods_schema.dump(all_moods)
    return jsonify(result)


@app.route('/month', methods=['GET', 'POST'])
def get_month_moods():

    userInputMonth = request.cookies.get('userMonth')
    dt = datetime.datetime.today()
    year = dt.year
    month = dt.month

    if userInputMonth is not None:
        month = userInputMonth

    data = db.session.execute(
        f"SELECT * FROM mood m JOIN calendar c ON m.date=c.day_id and month={month} and year={year} order by c.day "
    )
    return jsonify({'result': [dict(row) for row in data]})


@app.route('/monthgraph', methods=['GET'])
def month_graph():

    if request.args.get('month'):
        resp = make_response(render_template("month.html"))
        resp.set_cookie('userMonth', request.args.get('month'))
        return resp
    else:
        return render_template("month.html")


@app.route('/thisweek', methods=['GET'])
def get_weeks_moods():

    dt = datetime.datetime.today()
    week = dt.isocalendar()[1]
    start = dt - datetime.timedelta(days=dt.weekday() + 1)
    end = start + datetime.timedelta(days=6)

    if start.month != end.month:
        month = (str(start.month) + "," + str(end.month))
    else:
        month = (start.month)


# Raw sql requirement
    data = db.session.execute(
        f"SELECT m.id, m.date, coalesce(m.moodrating, 0) as moodrating, m.comment, c.day_of_week FROM mood m RIGHT JOIN calendar c ON m.date=c.day_id WHERE c.week_of_year={week} AND c.day_of_week <> 0 AND month IN ({month}) AND year={dt.year} UNION (SELECT m.id, m.date, coalesce(m.moodrating, 0) AS moodrating, m.comment, c.day_of_week FROM mood m RIGHT JOIN calendar c on m.date=c.day_id WHERE c.week_of_year={week - 1} AND c.day_of_week={0} AND c.month IN ({month}) AND c.year={dt.year}) ORDER BY day_of_week"
    )

    return jsonify({'result': [dict(row) for row in data]})


@app.route('/mood', methods=['POST'])
def add_mood():
    date = request.form['date']
    moodrating = request.form['moodrating']
    moodratingDivided = int(moodrating) / 10
    comment = request.form['comment']

    if date == '' or moodrating == '':
        flash("Required input: date and mood rating.")
        return redirect('/moodForm')

    exists = db.session.query(db.exists().where(Mood.date == date)).scalar()
    if (exists):
        flash("You've already entered a mood for this date.")
        return redirect('/moodForm')
    else:
        new_mood = Mood(date, moodratingDivided, comment)
        db.session.add(new_mood)
        db.session.commit()
    return redirect('/thisWeeksGraph')


# Run server
if __name__ == '__main__':
    app.run(debug=True)
