from project.models.base import db
from sqlalchemy import Column, String, Integer, Date, PickleType, JSON

#STATE tables

class Tick(db.Model):    
    """A Class representing a Tick
    We are using SQLAlchemy BaseDescriptor to store this in SQLite as well
    """
    __tablename__ = 'tick'
    id = Column(Integer, primary_key=True)
    tick = Column(Integer)
    

    def __init__(self):
        """Initiates the Ticker

        Just sets it to 0.
        """                
        self.tick = 0
        db.session.add(self)
        db.session.commit()

    def move_time(self):
        """Advances the Time Unit 

        Just adds one to tick
        """   
        self.tick = self.tick+1
        db.session.commit()
    
    def reset(self):
        """Resets time to 0
        
        """   
        self.tick = 0
        db.session.commit()