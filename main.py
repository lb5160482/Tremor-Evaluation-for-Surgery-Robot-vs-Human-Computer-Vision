import numpy as np
import cv2

mode = 0# 0 for getting point coordinates, 1 for comparing results

def getpoint(event,x,y,flags,param):
    global target
    if event == cv2.EVENT_LBUTTONDBLCLK:
        target.append([x,y])
        print target

with open("810_Part1_left_filteredTip.txt","r") as ins:
    totResult = []
    for line in ins:
    	result = []
        coords = line.strip().split()
        for i in range(len(coords)/2):
	        x, y = int(float(coords[2*i])),int(float(coords[2*i+1]))
	        result.append((x, y))
        totResult.append(result)

cap = cv2.VideoCapture('810_Part1_R.mp4')

# Parameters for lucas kanade optical flo
lk_params = dict( winSize = (15,15),
maxLevel = 2,
criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
# Create some random colors
color = np.random.randint(0,255,(100,3))
# Take first frame and find corners in it
ret, old_frame = cap.read()

b, g, r = cv2.split(old_frame)
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

########
if mode == 0:
    target = []    
    cv2.namedWindow('1')
    cv2.setMouseCallback('1',getpoint)
    while(1):
        cv2.imshow('1',old_gray)
        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            break

    p0 = np.array([target],dtype=np.float32)
    # print p0

else:# comparing mode, enter coordinates in last time 244 100;273 120;305 141
    x_last = 252
    y_last = 106
    p0 = np.array([[279, 281]],dtype=np.float32)

p0 = p0.reshape(-1,1,2)
points = []
points.append(p0.tolist())

# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)
mask2 = np.zeros_like(old_frame)
count = 1
while(1):
    ret,frame = cap.read()
    frame2 = frame.copy()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('pd',frame_gray)
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    # Select good points
    good_new = p1[st==1]
    good_old = p0[st==1]
    # draw the tracks
    for i,(new,old) in enumerate(zip(good_new,good_old)):
        a,b = new.ravel()
        c,d = old.ravel()
        cv2.line(mask, (a,b),(c,d), color[i-1].tolist(), 2)
        cv2.circle(frame,(a,b),4,color[i].tolist(),-1)
    img = cv2.add(frame,mask)
    cv2.imshow('optical flow',img)

    if mode != 0:
        """draw the processed projectory"""
        for i in range(len(totResult[count])):
	        cv2.line(mask2, totResult[count][i],totResult[count-1][i], color[i].tolist(), 2)
        	cv2.circle(frame2,totResult[count][i],4,color[i].tolist(),-1)
        img2 = cv2.add(frame2,mask2)
        cv2.imshow('after aplying filter',img2)
        while(count == len(totResult)-6):
            count = len(totResult)-6
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
        """draw the processed projectory"""

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    # Now update the previous frame and previous points
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1,1,2)

    """output data"""
    points.append(p0.tolist())
    count +=1
    """"""

cv2.destroyAllWindows()
cap.release()