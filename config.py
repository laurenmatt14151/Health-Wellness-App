'''Database configuration settings'''
import os

class Config:
    '''Base configurations'''
    '''
    URI is set to use SQLite database located in the instance folder.
    Track modifications is disabled to improve performance.
    '''
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:\\Users\\laroc\\OneDrive\\Documents\\GitHub\\Web Developer\\Health Wellness App\\instance\\wellness.db' # SQLite database URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Disable modification tracking for performance