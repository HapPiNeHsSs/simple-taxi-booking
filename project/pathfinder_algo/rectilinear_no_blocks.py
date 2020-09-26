from collections import deque

class Pathfinder:
    
    """A Rectilinear No Block Pathfinding Class"""
    def __init__(self):
        """Initiates the Algorithm
        """        
        pass
    def path(self, origin, destination, coordinates):
        """Find the path origin coordinate to destination coordinate

        Arguments:
            pathfinder {Pathfinder} -- pathfinding class that contains the algorithm
        """
        o_x, o_y = origin
        d_x, d_y = destination

        #let's do X coords first
        #calculating steps in rectilinear without blocks should be easy, just add/subtract o_x from d_x        
        steps = int(d_x-o_x) #can be negative steps or positive steps

        #to get steps direction, we use abs to get the absolute steps value (remove sign) and divide that from steps
        try:    
            step = steps/int(abs(steps)) #1 for positve direction, -1 for negative direction
        except:
            step = 0
        #here we just make a loop of abs(steps) count
        for _ in range(0, abs(int(steps))):
            #then add (or subtact) 1 to o_x until it is equalt to d_x
            o_x=int(o_x+step)
            coordinates.appendleft((o_x,o_y))
        
        #Let's repeat that for o_y and d_y
        steps = int(d_y-o_y) #can be negative steps or positive steps

        #to get steps direction, we use abs to get the absolute steps value (remove sign) and divide that from steps
        try:
            step = steps/int(abs(steps)) #1 for positve direction, -1 for negative direction
        except:
            step = 0
        for _ in range(0, abs(int(steps))):
            #then add (or subtact) 1 to o_y until it is equalt to d_y
            o_y=int(o_y+step)
            coordinates.appendleft((o_x,o_y))

        return coordinates
   
    

