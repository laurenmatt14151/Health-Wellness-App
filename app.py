from datetime import datetime
from flask import Flask, request, redirect, render_template
from config import Config # Import configuration settings
from models import db  # Import the database object
from database import init_app, sample_data, empty_db  # Import database initialization and sample data functions
from models.health_models import Meal, Sleep, Steps, Weight  # Import health models
import plotly.graph_objects as go
import plotly.express as px
from sqlalchemy import func

'''
__name__ is a special variable in Python that represents the name of the current module.
app represents the Flask application instance.
'''
app = Flask(__name__) # Initialize the Flask application

'''
. calls the from_object method of the Flask app's config attribute.
.config.from_object(Config) calls the Config class from config.py to load the database settings
'''
app.config.from_object(Config) # Load configurations from Config class

'''
init_app is a function in database.py that initializes the database with the Flask app
'''
init_app(app) # Initialize the database with the Flask app

'''
app_context is a built-in Flask method that provides a context for the application
This is necessary for database operations to ensure they are executed within the app context
app_context allows access to application-specific resources like configuration and database connections
with is used to create a context block
'''
with app.app_context():
    # empty_db() # Clear existing data in the database
    sample_data() # Populate the database with sample data

@app.route('/') # Define root/home route/landing page
def home():
    return render_template('home.html')

'''
Log route for entering health data
GET method displays the log form
POST method processes the submitted form data
'''
@app.route('/log', methods=['GET', 'POST'])
def log():
    '''POST method to handle form submissions'''
    if request.method == 'POST': # Handle form submission
        log_type = request.form.get('type') # Get the type of log from the form
        '''datetime.strptime converts string to date object'''
        date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()  # Get the date from the form

        if log_type == 'meal':
            food = request.form.get('food') # Get food item from the form
            calories = int(request.form.get('calories')) # Get calories from the form
            meal =  Meal(date=date, food=food, calories=calories) # Create Meal instance
            db.session.add(meal) # Add meal to the session

        elif log_type == 'sleep':
            hours = float(request.form.get('hours')) # Get sleep hours from the form
            sleep = Sleep(date=date, hours=hours) # Create Sleep instance
            db.session.add(sleep) # Add sleep to the session

        elif log_type == 'steps':
            count = int(request.form.get('count')) # Get step count from the form
            steps = Steps(date=date, count=count) # Create Steps instance
            db.session.add(steps) # Add steps to the session

        elif log_type == 'weight':
            value = float(request.form.get('value')) # Get weight value from the form
            weight = Weight(date=date, value=value) # Create Weight instance
            db.session.add(weight) # Add weight to the session

        db.session.commit() # Commit the session to save changes
        return redirect('/logs') # Redirect to logs page after submission

    '''GET method to display log form'''
    return render_template('log.html')

'''Display all health logs route'''
@app.route('/logs')
def logs():
    meals = Meal.query.all() # Query all Meal entries
    sleep = Sleep.query.all() # Query all Sleep entries
    steps = Steps.query.all() # Query all Steps entries
    weight = Weight.query.all() # Query all Weight entries

    
    return render_template('logs.html', meals=meals, sleep=sleep, steps=steps, weight=weight)

'''Route to delete specific log entries'''
@app.route('/delete/<log_type>/<int:log_id>') # <log_type> and <log_id> are dynamic URL segments
def delete(log_type, log_id):
    if log_type =='meal':
        meal = Meal.query.get(log_id) # Find meal by ID
        if meal:
            db.session.delete(meal) # Delete meal from session
        else:
            return "Meal not found", 404
    elif log_type == 'sleep':
        sleep = Sleep.query.get(log_id) # Find sleep by ID
        if sleep:
            db.session.delete(sleep) # Delete sleep from session
        else:
            return "Sleep entry not found", 404
    elif log_type == 'steps':
        steps = Steps.query.get(log_id) # Find steps by ID
        if steps:
            db.session.delete(steps) # Delete steps from session
        else:
            return "Steps entry not found", 404
    elif log_type == 'weight':
        weight = Weight.query.get(log_id) # Find weight by ID
        if weight:
            db.session.delete(weight) # Delete weight from session
        else:
            return "Weight entry not found", 404
        
    db.session.commit() # Commit the session to save changes
    return redirect('/logs') # Redirect to logs page after deletion

'''Dashboard route for viewing health statistics'''
@app.route('/dashboard')
def dashboard():
    # Get aggregated data
    calories_by_date = db.session.query(
        Meal.date, # Group by date
        func.sum(Meal.calories) # Sum calories per date
    ).group_by(Meal.date).all() # Group by date

    sleep_data = Sleep.query.all() # Get all sleep data
    steps_data = Steps.query.all() # Get all steps data
    weight_data = Weight.query.all() # Get all weight data

    # Create Charts
    dates = [item[0] for item in calories_by_date] # Extract dates from query result
    calories = [item[1] for item in calories_by_date] # Extract calories from query result

    calories_chart = px.line(
        x=dates,
        y=calories,
        title='Daily Calories',
        labels={'x': 'Date', 'y': 'Calories'}
    ).to_html(full_html=False) # Convert to HTML. full_html=False returns only the div while True returns full HTML document

    sleep_chart = px.scatter(
        x=[s.date for s in sleep_data], # Extract dates
        y=[s.hours for s in sleep_data], # Extract sleep counts
        title='Daily Sleep',
        labels={'x': 'Date', 'y': 'Sleep (hours)'}
    ).to_html(full_html=False) # Convert to HTML

    steps_chart = px.bar(
        x=[s.date for s in steps_data], # Extract dates
        y=[s.count for s in steps_data], # Extract step counts
        title='Daily Steps',
        labels={'x': 'Date', 'y': 'Steps'}
    ).to_html(full_html=False) # Convert to HTML

    weight_chart = px.line(
        x=[w.date for w in weight_data], # Extract dates
        y=[w.value for w in weight_data], # Extract weight values
        title='Weight Trend',
        labels={'x': 'Date', 'y': 'Weight (lbs)'}
    ).to_html(full_html=False) # Convert to HTML

    '''return passes the charts to the dashboard template'''
    return render_template('dashboard.html', 
                           calories_chart=calories_chart, 
                           sleep_chart=sleep_chart, 
                           steps_chart=steps_chart,
                           weight_chart=weight_chart)

if __name__ == '__main__':
    app.run(debug=True) # Run the application in debug mode