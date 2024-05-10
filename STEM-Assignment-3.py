import numpy as np
import cv2 
from MusicAnalyser import MusicAnalyser
from Animator import Animator

file_path = "/Users/yinshuodi/Desktop/Assignment/audio/bgm.mp3" 
mus = MusicAnalyser(file_path)
an = Animator()
 
class MySketch:

    #define an empty list
    balls = []
    #define the width and height of the drawing window(consistent with Animator.py)
    width= 640
    height=480

    def __init__(self):
        #call the setup method for initial settings and start the main loop to process subsequent mouse events
        self.setup()
        self.start_loop()

    def setup(self):
        print("setup")
        #initialize the number of balls
        self.number_balls = 10
        #use a placeholder loop '_', as I only need to loop without using variable
        for _ in range(self.number_balls):
            #define the initial x and y axis position of the ball
            ball_x = np.random.randint(0, self.width)
            ball_y = np.random.randint(0, self.height)
            #define the initial moving speed and direction of the ball
            ball_dx = np.random.randint(2, 6) * np.random.randint(-1, 2)
            ball_dy = np.random.randint(2, 6) * np.random.randint(-1, 2)
            #define the initial color of the ball
            ball_color = (0,0,0)
            #add the above five pieces of information to the ball list
            self.balls.append([ball_x, ball_y, ball_dx, ball_dy, ball_color])

    def draw(self):
        #optional to use
        an.background(0)
        #check if mus.fft_vals has data
        if mus.fft_vals.size > 0:
            #calculate the average FFT value
            average_fft_val = np.mean(mus.fft_vals)
            #the average FFT value * 10 as the ball radius
            ball_radius = int(average_fft_val * 10)

            #loop through the balls in the ball list
            for ball in self.balls:
                #add the speed variable to the position variable to update the position
                ball[0] += ball[2]
                ball[1] += ball[3]

                #check if the ball hits the boundary, reverse if so
                if ball[0] - ball_radius < 0 or ball[0] + ball_radius > self.width:
                    ball[2] *= -1
                if ball[1] - ball_radius < 0 or ball[1] + ball_radius > self.height:
                    ball[3] *= -1
                #draw the ball, update the new information to the ball list
                cv2.circle(an.canvas, (int(ball[0]), int(ball[1])), ball_radius, ball[4], -1)

    def mouse_moved(self, event, x, y, flags, param):
        #1 indicates the mouse was clicked
        if event == 1:
            #update the ball color
            self.ball_color = (np.random.randint(0, 100), np.random.randint(0, 100), np.random.randint(0, 100))       
            
            #calculate the current number of balls in the list
            number = len(self.balls)
            #add an equal number of new balls through the loop
            for _ in range(number):
                #generate position and speed for each new ball
                new_ball = [np.random.randint(0, self.width), np.random.randint(0, self.height), np.random.randint(2, 6) * np.random.randint(-1, 2), np.random.randint(2, 6) * np.random.randint(-1, 2), self.ball_color]
                #add the newly created ball to the list
                self.balls.append(new_ball)

    def start_loop(self):
        #initialize a variable to control the loop
        done = False
        #create a window named 'drawing'
        cv2.namedWindow('drawing')
        #set the mouse callback function
        cv2.setMouseCallback('drawing',self.mouse_moved)

        #start the main loop
        while not done:
            #draw the balls
            self.draw()
            #display the current canvas in the window
            cv2.imshow("drawing", an.canvas)
            #check every 1 millisecond for a key press event, end the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF==ord('q'): 
                #set done to True to end the loop
                done = True
                break

        #close all windows created by OpenCV
        cv2.destroyAllWindows() 

MySketch()
