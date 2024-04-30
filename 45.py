import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

road=cv2.imread("road.jpeg")
road_copy=np.copy(road)
marker_img=np.zeros(road.shape[:2],np.int32)
segment=np.zeros(road.shape,np.int8)
cm.tab10(0)
def create_rgb(i):
    return tuple(np.array(cm.tab10(i)[:3])*255)
colors=[]
for i in range(10):
    colors.append(create_rgb(i))
current_marker=1
marker_update=False
n_markers=10

def mouse_callback(evenet, x, y,z,t):
    global marker_update

    if evenet == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(marker_img, (x, y), 10, (current_marker), -1)
        cv2.circle(road_copy, (x, y), 10, colors[current_marker], -1)
        marker_update = True


cv2.namedWindow('Road Image')
cv2.setMouseCallback('Road Image', mouse_callback)

while True:
    cv2.imshow("Watershed segment",segment)
    cv2.imshow('Road Image', road_copy)

    k=cv2.waitKey(1)
    if k==27:
        break
    elif k==ord('c'):
        road_copy=road.copy()
        marker_img = np.zeros(road.shape[:2], np.int32)
        segment = np.zeros(road.shape, np.int8)
    elif k>0 and chr(k).isdigit():
        current_marker=int(chr((k)))

    if marker_update:
        marker_img_copy=marker_img.copy()
        cv2.watershed(road,marker_img_copy)
        segment=np.zeros(road.shape, np.int8)
        for color_ind in range(n_markers):
            segment[marker_img_copy==(color_ind)]=colors[color_ind]

cv2.destroyAllWindows()
