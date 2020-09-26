import os, json, unittest
from project.load import app, db
 
 
class BasicTests(unittest.TestCase):
    #Some basic Setup and Tear Downs

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test/testdb.sqlite'
        self.app = app.test_client()
        with  app.app_context():
            db.drop_all()
            db.create_all()

        self.assertEqual(app.debug, False)
 
    # executed after each test
    def tearDown(self):
        with app.app_context():
            db.drop_all()
 
 
#Here are the tests
 
    def test_add_taxi(self):
        """Let's test if we can add one taxi
        """        
        response = self.app.get('/api/add_taxi', follow_redirects=True)    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["taxi_count"], 1)        
    
    def test_add_2_taxi(self):
        """Let's test if we can add two taxis
        """        
        self.app.get('/api/add_taxi', follow_redirects=True)    
        response = self.app.get('/api/add_taxi', follow_redirects=True)    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["taxi_count"], 2)
    
    def test_reset_data_default(self):
        """Let's test if resetting data without params work
        Reset without params will have 3 taxis by default        
        """
        response = self.app.put('/api/reset', follow_redirects=True) 
        self.assertEqual(response.json["taxi_count"], 3)        
 
    def test_reset_data_10_taxis(self):
        """Let's test if resetting data with taxi_count params work          
        """
        response = self.app.put('/api/reset?taxi_count=10', follow_redirects=True) 
        self.assertEqual(response.json["taxi_count"], 10)
    
    def test_tick(self):
        """Let's now test if the tick number moves when tick is called
        """
        response = self.app.put('/api/reset', follow_redirects=True) 
        response = self.app.post('/api/tick', follow_redirects=True) 
        self.assertEqual(response.json["tick_count"], 1)
        response = self.app.post('/api/tick', follow_redirects=True) 
        self.assertEqual(response.json["tick_count"], 2)
    
    def test_book(self):
        """Let's now test booking is working
        We will do a 17 step booking        
        {"source": {"x": -1,"y": -1},"destination": {"x": 5,"y": -10}}
        """
        self.app.put('/api/reset', follow_redirects=True) 
        response=self.app.post('/api/book', 
                       data=json.dumps({"source": {"x": -1,"y": -1},"destination": {"x": 5,"y": -10}}),
                       content_type='application/json')        
        self.assertEqual(response.json["total_time"], 17)
    
    def test_basic_solution_checker(self):
        """Let's test using the basic solution checker as well
         reset()
        book({'x': 1, 'y': 0}, {'x': 1, 'y': 1}, {'car_id': 1, 'total_time': 2})
        book({'x': 1, 'y': 1}, {'x': 5, 'y': 5}, {'car_id': 2, 'total_time': 10})
        tick()
        book({'x': -1, 'y': 1}, {'x': 5, 'y': 10}, {'car_id': 3, 'total_time': 17})

        """
        self.app.put('/api/reset', follow_redirects=True)
        #test 1st booking
        response=self.app.post('/api/book', 
                       data=json.dumps({"source": {"x": 1,"y": 0},"destination": {"x": 1,"y": 1}}),
                       content_type='application/json')
        self.assertEqual(response.json["car_id"], 1)               
        self.assertEqual(response.json["total_time"], 2)

        #test 2nd booking
        response=self.app.post('/api/book', 
                       data=json.dumps({"source": {"x": 1,"y": 1},"destination": {"x": 5,"y": 5}}),
                       content_type='application/json')
        self.assertEqual(response.json["car_id"], 2)               
        self.assertEqual(response.json["total_time"], 10)

        #test if we tick
        response = self.app.post('/api/tick', follow_redirects=True) 
        self.assertEqual(response.json["tick_count"], 1)

        #test 3rd booking
        response=self.app.post('/api/book', 
                       data=json.dumps({"source": {"x": -1,"y": 1},"destination": {"x": 5,"y": 10}}),
                       content_type='application/json')        
        self.assertEqual(response.json["car_id"], 3)               
        self.assertEqual(response.json["total_time"], 17)
    
    def test_movement_and_get_all_data(self):
        """Let's test if ticking actually moves a car to it's destination
        This will also check get_all_data if it is working correctly
        """
        #car States
        AVAILABLE = 0
        PICKING_UP = 1
        DROPPING_OFF = 2

        self.app.put('/api/reset', follow_redirects=True)
        response = self.app.get('/api/get_all_data', follow_redirects=True)        
        #let's see if car 1 is available, in [0,0] and tick is in 0
        self.assertEqual(response.json["taxis"]['1']["state"], AVAILABLE)
        self.assertEqual(response.json["taxis"]['1']["position"], [0,0])
        self.assertEqual(response.json["tick"], 0)

        #let's now book and check
        response=self.app.post('/api/book', 
                       data=json.dumps({"source": {"x": 1,"y": 1},"destination": {"x": 2,"y": 2}}),
                       content_type='application/json')
        self.assertEqual(response.json["car_id"], 1)
        self.assertEqual(response.json["total_time"], 4)

        #Let's tick once and see if the car moved from [0,0], we use X first in our algo, so it should be [1,0]
        #Let's also see if taxi is in PICKING_UP mode
        #Tick should have moved as well
        self.app.post('/api/tick', follow_redirects=True)         
        response = self.app.get('/api/get_all_data', follow_redirects=True)        
        self.assertEqual(response.json["taxis"]['1']["state"], PICKING_UP)
        self.assertEqual(response.json["taxis"]['1']["position"], [1,0])
        self.assertEqual(response.json["tick"], 1)

        #Let's tick again and see if the car has picked up the passenger and status has changed to DROPPING_OFF
        #Tick should be 2
        #Position should be [1,1]
        self.app.post('/api/tick', follow_redirects=True)         
        response = self.app.get('/api/get_all_data', follow_redirects=True)        
        self.assertEqual(response.json["taxis"]['1']["state"], DROPPING_OFF)
        self.assertEqual(response.json["taxis"]['1']["position"], [1,1])
        self.assertEqual(response.json["tick"], 2)

        #Lastly, let's tick twice. Taxi should have reached the destination [2,2]
        #Tick should be 4
        #Taxi should be in AVAILABLE state again
        self.app.post('/api/tick', follow_redirects=True)         
        self.app.post('/api/tick', follow_redirects=True)         
        response = self.app.get('/api/get_all_data', follow_redirects=True)        
        self.assertEqual(response.json["taxis"]['1']["state"], AVAILABLE)
        self.assertEqual(response.json["taxis"]['1']["position"], [2,2])
        self.assertEqual(response.json["tick"], 4)
        
 
if __name__ == "__main__":
    unittest.main()