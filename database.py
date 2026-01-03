'''Database initialization & utilities'''
from models import db

'''
app parameter is the Flask application instance.
This function initializes the database with the Flask app context.
app_context is used to ensure that the database tables are created within the application context. 
It allows access to application-specific resources.
'''
def init_app(app): # Function to initialize database with Flask app
    db.init_app(app) # Initialize the db with the app

    with app.app_context(): # Use app context to create tables
        db.create_all() # Create all database tables
        print("Database initialized!")

def sample_data(): # Function to add sample data to the database
    from models.health_models import Meal, Sleep, Steps, Weight
    from datetime import datetime

    # Only if tables are empty
    if Meal.query.first() is None:
        meal = Meal(food='Apple', calories=95)
        db.session.add(meal) # Add single entry

        sleep = Sleep(hours=7.5)
        steps = Steps(count=8000)
        weight = Weight(value=162.3)
        db.session.add_all([sleep, steps, weight]) # Add multiple entries

        meals_data = [ # Define sample data as a list of dictionaries
            {'food': 'Banana', 'calories': 105},
            {'food': 'Chicken Breast', 'calories': 165},
            {'food': 'Salad', 'calories': 150},
            {'food': 'Brown Rice', 'calories': 215}
        ]

        sleep_data = [
            {'hours': 6.0},
            {'hours': 8.0},
            {'hours': 7.0}
        ]

        steps_data = [
            {'count': 5000},
            {'count': 10000},
            {'count': 7500}
        ]

        weight_data = [
            {'value': 160.0},
            {'value': 161.5},
            {'value': 163.0}
        ]

        meal1 = [Meal(**data) for data in meals_data] # Create Meal instances from dictionaries
        sleep1 = [Sleep(**data) for data in sleep_data]
        steps1 = [Steps(**data) for data in steps_data]
        weight1 = [Weight(**data) for data in weight_data]

        db.session.add_all(meal1 + sleep1 + steps1 + weight1) # Add all sample data to session
        db.session.commit() # Commit the changes
        print("Sample data added!")