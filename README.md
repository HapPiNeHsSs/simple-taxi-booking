# Simple Taxi Booking System #
Once the service is running, you can also view this README at the service index `/`

## Running via Python3 ##
To run simply type: `python3 run.py`

The service will run on port **8080**

Terminate by `Ctrl+C`

## Running via Docker ##

**Building and Running**

Make sure **docker** is installed and run these commands

1. `docker image build -t simple-taxi-booking .`
2. `docker run --name=simple-taxi-booking-docker -p 8080:8080 -d simple-taxi-booking`

This will run the service on port **8080**

**Stopping the Service**

`docker stop simple-taxi-booking-docker`

**Restarting the Service**

`docker start simple-taxi-booking-docker`

**Removing the container (when you want to start anew)**

1. `docker stop simple-taxi-booking-docker` if it is running, else go to step 2
2. `docker rm simple-taxi-booking-docker`

## Scenario Player ##

I had some time so I made a quick and dirty scenario player at endpoint `/player`.

If you are viewing this README.md as a served page of this project, [click here](/player) to run the player.

The player uses all the APIs below but with a UI (ugly interface haha)

This is a fun tool to view how the scenarios play out.

Be kind with it though, it's very rough

Static file is at `project/templates/player.html` if you need to see the code

## Available APIs ##

**reset:** Resets the taxis and states to initial position
    
This will also create the initial tables if it's blank. You can specify the number of taxis you want to spawn on reset. If no taxi_count param, default is 3 taxis
    
    METHOD: PUT
    ENDPOINT: /api/reset
    PARAMS: taxi_count {optional integer} -- number of taxis to spawn
    
    Returns:
        json -- {"message":f"State Reset", "taxi_count":<taxi_count>}

**book:** Make a car booking
    
    METHOD: POST
    ENDPOINT: /api/book
    Parameters: JSON
    {"source": {"x": x,"y": y},"destination": {"x": x,"y": -y}}
    
    Returns:
        json --  { "car_id": id, "total_time":time_unit_to_finish}

**tick:** Moves the time unit one step
    
    METHOD: post
    ENDPOINT: /api/tick
    
    Returns:
        json -- {"message":"Time Has Moved", "tick_count":<tick_count>})

**get_all_data:** Gets all the data for the taxis and the tick time

    METHOD: GET
    ENDPOINT: /api/get_all_data
    
    Returns:
        json --  {"taxis":{1:<taxi_data>, 2:<taxi_data>, 3:<taxi_data>}, "tick":7}

**add_taxi:** API call to increase number of available taxis
    
    ENDPOINT: /api/add_taxi
    METHOD: PUT or GET    
    
    Returns:
        json -- {"message":"Added a new Taxi", "taxi_count":<taxi_count>}

## Testing ##

The unit tests are in `project/test`.

You can run the unit tests by: `python3 -m unittest project/test/test_taxibooking.py` from the root simple-taxi-booking directory
