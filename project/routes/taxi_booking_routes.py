"""Just a simple Route File.
Kinda dirty, a blueprint would have been better
"""
from project.models.taxi import Taxi
from project.models.tick_tracker import Tick
from project.models.base import db
from project.pathfinder_algo.rectilinear_no_blocks import Pathfinder
from flask import request, jsonify
from project.load import app
from flask import render_template

DEFAULT_TAXI_COUNT=3
   
@app.route('/api/add_taxi', methods = ["GET", 'PUT'])
def add_taxi():
    """API call to increase number of available taxis
    
    ENDPOINT: /api/add_taxi
    METHOD: PUT or GET    

    Returns:
        json -- A simple message
    """
    Taxi((0,0))
    count=len(Taxi.query.all())
    return jsonify(
        {"message":f"Added a new Taxi", \
         "taxi_count":count})

@app.route('/api/reset',  methods = ['PUT'])
def reset():
    """Resets the taxis and states to initial position

    This will also create the initial tables if it's blank
    You can specify the number of taxis you want to spawn on reset
    If no taxi_count param, default is 3 taxis

    METHOD: PUT
    ENDPOINT: /api/reset
    PARAMS: taxi_count {optional integer} -- number of taxis to spawn

    Returns:
        json -- A simple message
    """
    t_count = request.args.get('taxi_count')
    if not t_count:
        t_count = DEFAULT_TAXI_COUNT
    t_count=int(t_count)

    if not db.engine.dialect.has_table(db.engine, "taxis"):
        Taxi.__table__.create(db.engine)
    else: #destroy table and create it again. This way we reset index to 0
        Taxi.__table__.drop(db.engine)
        Taxi.__table__.create(db.engine)
        for _ in range(0, t_count):
            Taxi((0,0))

    if not db.engine.dialect.has_table(db.engine, "tick"):
        Tick.__table__.create(db.engine)
    else:
        Tick.__table__.drop(db.engine)
        Tick.__table__.create(db.engine)
        Tick()

    count=len(Taxi.query.all())

    return jsonify(
        {"message":f"State Reset", \
         "taxi_count":count})

@app.route('/api/tick',  methods = ['POST'])
def tick():
    """Moves the time unit one step

    METHOD: post
    ENDPOINT: /api/tick

    Returns:
        json -- A simple message
    """
    taxis = Taxi.query.all()
    tick = Tick.query.first()
    tick.move_time()
    for taxi in taxis:
        taxi.move_time()        
    return jsonify(
        {"message":f"Time Has Moved", \
         "tick_count":tick.tick})

@app.route('/api/book',  methods = ['POST'])
def book():    
    """Make a car booking

    METHOD: POST
    ENDPOINT: /api/book
    Parameters: JSON
    {"source": {"x": x,"y": y},"destination": {"x": x,"y": -y}}

    Returns:
        json --  { "car_id": id, "total_time":time_unit_to_finish}
    """
    req = request.get_json(silent=True)
    source = (req['source']['x'] or 0,req['source']['y'] or 0)
    destination = (req['destination']['x'] or 0,req['destination']['y'] or 0)
    available_taxis = Taxi.query.filter(Taxi.state==0).all()
    if len(available_taxis) == 0:
       return jsonify({})
    first_nearest_taxi = None
    for taxi in available_taxis: 
        taxi.set_pathfinder(Pathfinder)       
        if first_nearest_taxi == None:
            first_nearest_taxi = taxi
        if taxi.calculate_steps(source) < first_nearest_taxi.calculate_steps(source):
            first_nearest_taxi = taxi
    
    first_nearest_taxi.book(source,destination)         
    data = { "car_id": first_nearest_taxi.id, "total_time": first_nearest_taxi.time_unit}
    return jsonify(data)

@app.route('/api/get_all_data',  methods = ['POST', 'GET'])
def getAllData():
    """Gets all the data for the taxis and the tick time
    METHOD: GET
    ENDPOINT: /api/get_all_data
    

    Returns:
        json --  {"taxis":{1:<taxi_data>, 2:<taxi_data>, 3:<taxi_data>}, "tick":7}
    """
    taxis = Taxi.query.order_by(Taxi.id).all()
    tick = Tick.query.first()
    data = {}
    taxi_data = {}
    for taxi in taxis:
        taxi_data[taxi.id]=taxi.get_taxi_data()
    data["taxis"]=taxi_data
    data["tick"]=tick.tick
    return jsonify(data)

@app.route('/player/')
def player():    
    return render_template('player.html')