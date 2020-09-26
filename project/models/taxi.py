from project.models.base import db
from sqlalchemy import Column, String, Integer, Date, PickleType, JSON
from collections import deque

#STATE tables
AVAILABLE = 0
PICKING_UP = 1
DROPPING_OFF = 2

class Taxi(db.Model):    
    """A Class representing a Taxi
    We are using SQLAlchemy BaseDescriptor to store this in SQLite as well
    """
    __tablename__ = 'taxis'
    id = Column(Integer, primary_key=True)
    position = Column(PickleType)
    coordinate_q = Column(PickleType)
    state = Column(Integer)
    pickup = Column(PickleType)
    destination = Column(PickleType)
    time_unit = Column(Integer)
    time_to_finish = Column(Integer)    

    def __init__(self, position):
        """Initiates the Taxi's position and ID

        Arguments:
            position {integer tuple[x,y]} -- an integer tuple repesenting a coordinate
            id {integer} -- Taxi's id
        """        
        self.position =position
        self.coordinate_q = deque()
        self.state = AVAILABLE
        self.pickup = (0,0)
        self.destination = (0,0)
        self.time_unit = 0
        self.time_to_finish = 0
        db.session.add(self)
        db.session.commit()

    def set_pathfinder(self, pathfinder):
        """Set's the taxi's path finding algorithm

        Arguments:
            pathfinder {Pathfinder} -- pathfinding class that contains the algorithm
        """
        self.pathfinder = pathfinder
        db.session.commit()
    
    def set_booked(self):
        """Books this taxi
        """
        self.state = PICKING_UP
        db.session.commit()
    
    def set_available(self):
        """Makes this taxi available
        """        
        self.pickup = None
        self.destination = None
        self.state = AVAILABLE
        db.session.commit()
    
    def book(self, pickup, destination):
        """
        Book the taxi
        
        Use the pathfinding algorithm to find path to pickup point then to the destination

        This function will also populate the coordinate_q with the coordinates to be traversed

        Arguments:
            pickup {integer tuple[x,y]} -- Pickup the passenger here
            destination {integer tuple[x,y]} -- Bring the passenger here
        
        Returns:
            t_units {integer} = number of time units
        """ 
        self.coordinate_q = deque(self.coordinate_q)
        self.set_booked()
        self.pickup = pickup
        self.destination = destination

        #Use pathfinder to find route from position to pickup point
        self.coordinate_q = (self.pathfinder.path(self, self.position, self.pickup, self.coordinate_q))
        #Use pathfinder to find route from pickup point to destination
        self.coordinate_q = (self.pathfinder.path(self, self.pickup, self.destination, self.coordinate_q))
        if self.position == self.pickup:
            self.state = DROPPING_OFF        
        if len(self.coordinate_q) == 0:            
            self.set_available()        
        self.time_unit = len(self.coordinate_q)
        self.time_to_finish = self.time_unit 
        self.coordinate_q = list(self.coordinate_q)
        db.session.commit()
        return len(self.coordinate_q)
    
    def calculate_steps(self, pickup):
        """This function just calculates steps so we can find which one is closest to user
        Arguments:
            pickup {integer tuple[x,y]} -- Pickup the passenger here

        Returns:
            t_units {integer} = number of time units
        """
        q = deque()        
        #Use pathfinder to find route from position to pickup point
        q = (self.pathfinder.path(self, self.position, pickup, q))        
        return len(q)
    
    def move_time(self):
        """Advances the Time Unit while also updating position and popping off coordinates from queues

        Also changes the Taxi state from PICKING_UP to DROPPING_OFF to AVAILABLE
        """   
        self.coordinate_q = deque(self.coordinate_q)
        if len(self.coordinate_q) == 0:
            self.coordinate_q = list(self.coordinate_q)
            db.session.commit()
            return 0
        self.position = self.coordinate_q.pop()
        self.time_to_finish=self.time_to_finish-1 
        if self.position == self.pickup:
            self.state = DROPPING_OFF
        if self.position == self.destination:
            self.set_available()
            self.time_unit=self.time_to_finish
        self.coordinate_q = list(self.coordinate_q)
        db.session.commit()
        return 1  
    
    def get_taxi_data(self):
        """Returns relevant taxi data so we can store it in DB or memcacche or just view stats
        """
        taxi_data = {}
        taxi_data["position"] = self.position         
        taxi_data["id"] = self.id
        taxi_data["coordinate_q"] = list(self.coordinate_q)
        taxi_data["state"] = self.state
        taxi_data["pickup"] = self.pickup
        taxi_data["destination"] = self.destination
        taxi_data["time_unit"] = self.time_unit
        taxi_data["time_to_finish"] = self.time_to_finish
        return taxi_data
    



