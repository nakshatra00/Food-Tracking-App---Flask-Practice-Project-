#Importing libraries 
from flask import Flask, render_template



#configuring the app 
app = Flask(__name__)



#index route 
@app.route('/')
def index():
  return render_template('home.html') 


#view_day route 
@app.route('/view')
def view():
  return render_template('day.html')

#Add food route
@app.route('/food')
def food():
  return render_template('add_food.html')



#running the app
if __name__ == '__main__':
  app.run(
    host = '0.0.0.0',
    debug = True
  )
