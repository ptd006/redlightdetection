import cv2
import numpy as np

# initial search boxes
red_box_UL = (307, 16)
red_box_LR = (317, 26)

green_box_UL = (308, 45)
green_box_LR = (318, 55)

# functions to update search box on fly
# how much more intense is col than mean of other (RGB)?
def av_color_intensity(img,x1,y1,x2,y2,col):
    col_intensity = 0
    for x in range(x1,x2+1):
        for y in range(y1,y2+1):
            col_intensity += img[y, x][col] - np.mean(img[y, x])
    # return average
    return col_intensity/( (x2-x1 + 1)*(y2-y1 + 1))

def recentre_av_intensity(img,curr,col):
    max_col_intensity = 0
    max_col_intensity_where = (curr[0] + 5 - 2, curr[1] + 5 - 2)
    sz = 4
    for m in range(0,10):
        for n in range(0,10):
            col_intensity = av_color_intensity(img,curr[0]+m,curr[1]+n,curr[0]+m+sz,curr[1]+n+sz,col)
            #print m,n,col_intensity
            if col_intensity > max_col_intensity: 
                max_col_intensity = col_intensity
                max_col_intensity_where = (m,n)
    # get new upper left
    new_ul = (max_col_intensity_where[0] - 5 + curr[0] + 2, max_col_intensity_where[1] - 5 + curr[1] + 2)
    # ensure shift isn't too big
    max_delta = 1 # alow max 1 px shift in each direction per frame
    new_ul = (max(curr[0] - max_delta, new_ul[0]), max(curr[1] - max_delta, new_ul[1]) 
    new_ul = (min(curr[0] + max_delta, new_ul[0]), min(curr[1] + max_delta, new_ul[1])
    return [max_col_intensity, new_ul]


for im_num in range(1,700):
    img = cv2.imread('/home/peter/redlightdetection/snapshots/out'+str(im_num)+'.png',cv2.IMREAD_COLOR)
    # get red intensity in existing red and green light area based on best 3x3 block (also returns location of best 3x3 block)
    red_box = recentre_av_intensity(img,red_box_UL,2)
    green_box = recentre_av_intensity(img,green_box_UL,1)    
    red_box_intensity = red_box[0]
    green_box_intensity = green_box[0]    
    # if there is at least 33% more red or green then choose that light!
    # update search area and add box
    if red_box_intensity > 1.33*green_box_intensity:        
        red_box_UL = red_box[1]
        red_box_LR = (red_box_UL[0]+10,red_box_UL[1]+10)
        cv2.rectangle(img, red_box_UL, red_box_LR, (0,0,255), 2)
        # cv2.circle(img, (int((red_box_UL[0] + red_box_LR[0])/2.0), int((red_box_UL[1] + red_box_LR[1])/2.0)), 5, (0,0,255), 2)
        #cv2.rectangle(img, green_box_UL, green_box_LR, (255,255,255), 1) # search area for green!
    elif green_box_intensity > 1.33*red_box_intensity:        
        green_box_UL = green_box[1]
        green_box_LR = (green_box_UL[0]+10,green_box_UL[1]+10)    
        cv2.rectangle(img, green_box_UL, green_box_LR, (0,255,0), 2)
        #cv2.rectangle(img, red_box_UL, red_box_LR, (255,255,255), 1) # search area for red
    #else: # just put search boxes
        #cv2.rectangle(img, green_box_UL, green_box_LR, (255,255,255), 1) # search area for green!
        #cv2.rectangle(img, red_box_UL, red_box_LR, (255,255,255), 1) # search area for red
    cv2.imwrite('/home/peter/redlightdetection/snapshots/test/out'+str(im_num)+'.png',img)

