import numpy as np
import cv2
from cv2 import rectangle
import time
from PIL import Image

class Animator:
    
    width = 640
    height = 480
    frame = 0
    mouse_x = 1
    mouse_y = 1
    mouse_down = False
    start_time_millis = int(round(time.time() * 1000))
    millis = 0
    layers = []
    
    def __init__(self, width = 640, height = 480):
        self.width = width
        self.height = height
        self.canvas = np.ones((height,width,3), np.uint8)*255
        print("init")

    def push_layer(self):
        return np.zeros((self.height,self.width,3), np.uint8)
    
    def translate(self, c, dx=0, dy=0):
        w, h, _ = c.shape
        translated_array = np.zeros_like(c)
        x_indices = np.arange(w) + dx
        y_indices = np.arange(h) + dy
        x_indices = np.clip(x_indices, 0, w - 1)
        y_indices = np.clip(y_indices, 0, h - 1)
        translated_array = np.zeros_like(c)
        translated_array[x_indices[:, np.newaxis], y_indices, :] = c
        return np.round(translated_array).astype(np.uint8)
    
    def pop_layer(self, c):
        self.layers.append([c,1])
        self.update_canvas()

    def to_alpha(self, alpha=1):
        new_canvas = np.zeros((self.height,self.width,3), np.uint8)
        self.layers.append([new_canvas,alpha])
        return self.layers[-1][0]
    
    def linear_transformation(self, src, a, origin =(0,0)):
        
        rows, cols = src.shape[:2]
        
        translate_to_origin = np.array([[1, 0, -origin[0]],
                                        [0, 1, -origin[1]],
                                        [0, 0, 1]])
        
        translate_back = np.array([[1, 0, origin[0]],
                                [0, 1, origin[1]],
                                [0, 0, 1]])
        
        transformation_matrix = np.array([[a[0,0], a[0,1], 0],
                                        [a[1,0],a[1,1], 0],
                                        [0, 0, 1]])
        
        transformation_matrix = translate_back @ transformation_matrix @ translate_to_origin

        transformed_image = cv2.warpAffine(src, transformation_matrix[:2, :], (cols, rows))

        return transformed_image

    
    def transform(self, canvas, m, origin = (0,0)):
        return self.linear_transformation(canvas, m, origin)
    
    def mouse_moved(self, event, x, y, flags, param):
        self.mouse_x = x
        self.mouse_y = y
        if event == 1:
            self.mouse_down = True
        elif event == 4:
            self.mouse_down = False

    def background(self,col):
        rectangle(self.canvas, (0,0),(self.width,self.height),col,-1)

    def paste(self, canvas, to_paste, coords = (0,0)):
        canvas = Image.fromarray(canvas)
        canvas.paste(Image.fromarray(to_paste), coords)
        canvas = np.array(canvas)
        return canvas

    #Some complicated stuff to try and do alpha blending
    def update_canvas(self):
        self.layers.insert(0, [self.canvas,1])
        for i in range(len(self.layers)-1):
            c1 = self.layers[i]
            c2 = self.layers[i+1]
            _,mask = cv2.threshold(cv2.cvtColor(c2[0], cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_BINARY)
            #Dont blend into parts of lower layer where there isnt stuff in the upper layer
            masked_image = cv2.bitwise_and(c1[0], c1[0], mask=mask)
            #Blend appropriate bits
            c2[0] = (c2[0]*c2[1]) + (masked_image*(1-c2[1]))
            inverted_mask = cv2.bitwise_not(mask)
            inverted_masked = cv2.bitwise_and(c1[0], c1[0], mask=inverted_mask)
            #Add in blended stuff (not over unblended stuff)
            c2[0] = np.array(c2[0] + inverted_masked, dtype = np.uint8)
        self.canvas = self.layers[-1][0]
        self.layers = []

    def start_loop(self, 
                   setup = lambda *args: None, 
                   draw = lambda *args: None
                   ):
        done = False
        setup()
        cv2.namedWindow('drawing')
        cv2.setMouseCallback('drawing',self.mouse_moved)

        while not done:

            draw()
            self.update_canvas()
            self.millis = int(round(time.time() * 1000)) - self.start_time_millis
            canvas_rgb = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2RGB)
            #Draw to window
            cv2.imshow("drawing", canvas_rgb)

            if cv2.waitKey(1) & 0xFF==ord('q'): # quit when 'q' is pressed
                done = True
                break

            self.frame += 1

        cv2.destroyAllWindows() 
        cv2.waitKey(1)
