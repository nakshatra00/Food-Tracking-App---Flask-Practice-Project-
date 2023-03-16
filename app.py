#Importing libraries 
from flask import Flask, render_template, g, request
import sqlite3

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
@app.route('/')
def index():
  return render_template('home.html') 


#view_day route 
@app.route('/view')
def view():
  return render_template('day.html')

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
    return '<h1> Name: {} Protein: {} Carbs: {} Fats: {}'.format(request.form['food-name'],            request.form['protein'], request.form['carbohydrates'], request.form['fat']        )
  cur = db.execute('select name, protein, carbohydrates, fat, calories from food')
  results = cur.fetchall()
  return render_template('add_food.html', results = results)



#running the app
if __name__ == '__main__':
  app.run(
    host = '0.0.0.0',
    debug = True
  )
