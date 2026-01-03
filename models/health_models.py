'''Model definitions'''
from datetime import datetime
'''Don't need to do models.__init__ because '''
from models import db # Import the db object from models package

'''
db.Model is the base class for all models in SQLAlchemy.
db.Column is used to define columns in the database table.
db.Integer, db.String, db.Date, db.Float are data types for the columns.
datetime.utcnow().date is used to set the default date to the current date.
'''
class Meal(db.Model): # Inherit from db.Model
    __tablename__ = 'meals'  # Specify table name
    id = db.Column(db.Integer, primary_key=True) # Primary key column
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date) # Date column with default value
    food = db.Column(db.String(100), nullable=False) # Food item column
    calories = db.Column(db.Integer, nullable=False) # Calories column

    def __repr__(self): # String representation of the model
        return f'<Meal {self.food}: {self.calories} cal>'

class Sleep(db.Model):
    __tablename__ = 'sleep'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    hours = db.Column(db.Float, nullable=False)

    def __repr__ (self):
        return f'<Sleep {self.date}: {self.hours} hours>'

class Steps(db.Model):
    __tablename__ = 'steps'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    count = db.Column(db.Integer, nullable=False)

    def __repr__ (self):
        return f'<Steps {self.date}: {self.count} steps>'


class Weight(db.Model):
    __tablename__ = 'weight'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    value = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Weight {self.date}: {self.value} lbs>'



