#Importing libraries
from flask import Flask, render_template, g, request
import sqlite3
from datetime import datetime

#configuring the app
app = Flask(__name__)


#sqlite3 connection
def connect_db():
  sql = sqlite3.connect('food_log.db')
  sql.row_factory = sqlite3.Row
  return sql


def get_db():
  if not hasattr(g, 'sqlite_db'):
    g.sqlite_db = connect_db()
  return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
  if hasattr(g, 'sqlite_db'):
    g.sqlite_db.close()


#index route
@app.route('/', methods=['GET', 'POST'])
def index():
  db = get_db()

  if request.method == 'POST':
    date = request.form['date']

    dt = datetime.strptime(date, '%Y-%m-%d')
    database_date = datetime.strftime(dt, '%Y%m%d')
    db.execute('insert into log_date (entry_date) values (?)', [database_date])
    db.commit()

  cur = db.execute('select entry_date from log_date order by entry_date desc')
  results = cur.fetchall()

  pretty_results = []
  for i in results:
    single_date = {}

    d = datetime.strptime(str(i['entry_date']), '%Y%m%d')
    single_date['entrydate'] = datetime.strftime(d, '%B %d, %Y')
    pretty_results.append(single_date)

  return render_template('home.html', results=pretty_results)


#view_day route
@app.route('/view/<date>', methods=['GET', 'POST'])
def view(date):
  db = get_db()
  cur = db.execute('select id, entry_date from log_date where entry_date = ?',
                   [date])
  date_result = cur.fetchone()
  log_cur = db.execute('select food.name, food.protein, food.carbohydrates, food.fat, food.calories from log_date join food_date on food_date.log_date_id = log_date.id join food on food.id = food_date.food_id where   log_date.entry_date = ?', [date])
  log_results = log_cur.fetchall()

  if request.method == 'POST':
    db.execute('insert into food_date (food_id, log_date_id) values (?,?)',             [request.form['food-select'], date_result['id']])
  db.commit()

  d = datetime.strptime(str(date_result['entry_date']), '%Y%m%d')
  pretty_date = datetime.strftime(d, '%B %d, %Y')
  food_cur = db.execute('select id, name from food')
  food_results = food_cur.fetchall()
  return render_template('day.html',
                         date=pretty_date,
                         food_results=food_results, log_results = log_results)


#Add food route
@app.route('/food', methods=['GET', 'POST'])
def food():
  db = get_db()
  if request.method == 'POST':
    name = request.form['food-name']
    protein = int(request.form['protein'])
    carbohydrates = int(request.form['carbohydrates'])
    fat = int(request.form['fat'])
    calories = protein * 4 + carbohydrates * 4 + fat * 9
    #initializing the database
    db.execute('insert into food (name, protein, carbohydrates, fat, calories) values (?,?,?,?,?)',\
              [name, protein, carbohydrates, fat, calories])
    db.commit()
    return '<h1> Name: {} Protein: {} Carbs: {} Fats: {}'.format(
      request.form['food-name'], request.form['protein'],
      request.form['carbohydrates'], request.form['fat'])
  cur = db.execute(
    'select name, protein, carbohydrates, fat, calories from food')
  results = cur.fetchall()
  return render_template('add_food.html', results=results)


#running the app
if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True, port=4000)
