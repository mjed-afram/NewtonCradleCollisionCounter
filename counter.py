import cv2 as cv
import math


class CollisionCounter():
    def __init__(self) -> None:
        self.total_hits = 0
        self.collision1 = False
        self.collision2 = False
        self.initial_state = False
        self.hit_sequence = []

    
    def countCollisions(self, f, coordinates):

        # Calculate distances between first and second ball, 
        # and between the last and second-last ball (visualization purposes only) 
        first_distance = math.sqrt((coordinates[1][0] - coordinates[0][0])**2 + (coordinates[1][1] - coordinates[0][1])**2)
        last_distance = math.sqrt((coordinates[-1][0] - coordinates[-2][0])**2 + (coordinates[-1][1] - coordinates[-2][1])**2)
        # Draw lines between the first and second, and the last and second-last balls for visualization.
        cv.line(f, (coordinates[1][0], coordinates[1][1]), (coordinates[0][0], coordinates[0][1]), (255, 0, 0), 2)
        cv.line(f, (coordinates[-1][0], coordinates[-1][1]), (coordinates[-2][0], coordinates[-2][1]), (255, 0, 0), 2)

        # Check for collision1: Occurs if the first distance is within a threshold 
        # and the last distance is not.
        if self.collision1 == False:
            if  first_distance <= 47 and last_distance > 47: # the threshold 47 is based on the video frame size
                if len(self.hit_sequence) == 0 or self.hit_sequence[-1] != 1:              
                    self.hit_sequence.append(1)
                    self.total_hits += 1
                    self.collision1 = True
                    self.initial_state = True

                elif self.hit_sequence[-1] == 1:
                    pass
        # Reset collision1 state if the first distance is beyond the threshold.
        elif self.collision1 == True:
            if first_distance > 47:
                self.collision1 = False

        # Check for collision2: Occurs if the last distance is within a threshold 
        # and the first distance is not, after an initial state is set.
        if self.collision2 == False and self.initial_state == True:
            if last_distance <= 47 and first_distance > 47:
                if self.hit_sequence[-1] != 2:
                    self.collision2 = True
                    self.total_hits += 1
                    self.hit_sequence.append(2)
                if self.hit_sequence[-1] == 2:
                    pass
        # Reset collision2 state if the last distance is beyond the threshold.
        elif self.collision2 == True:
            if last_distance > 47:
                self.collision2 = False

        return self.total_hits
    