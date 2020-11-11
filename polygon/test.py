import cv2 as cv
import numpy as np

polygons = []
points = []
img = np.zeros((480, 640, 3), dtype=np.uint8)

def distance(pt1, pt2):
    return abs(pt1[0]-pt2[0]) + abs(pt1[1] - pt2[1])

def draw_polygon(event, x, y, flags, param):
    global mouseX, mouseY
    if event == cv.EVENT_LBUTTONDOWN:
        print("x :{}, y: {}".format(x, y))
        points.append((x, y))

        if len(points) > 1:
            if distance(points[0], points[-1]) > 10:
                cv.line(img, points[-2], points[-1], (255, 0, 0), 4)
                cv.circle(img, points[-1], 10, (255, 0, 0), 4)
            else:
                polygons.append(points)
                for point in points[1:]:
                    cv.circle(img, point, 10, (255, 255, 0), 4)
                    cv.line(img, point, points[points.index(point)-1], (255, 255, 0), 4)
                points.clear()

        else:
            cv.circle(img, (x, y), 10, (255, 0, 0), 4)

        cv.imshow('window', img)
        mouseX, mouseY = x, y

cv.putText(img, 'click to start recording the polygon', 
        (10, 30), cv.FONT_ITALIC, 1, (70, 255, 70), 2)
cv.putText(img, 'press esc to quit', 
        (10, 50), cv.FONT_ITALIC, 1, (70, 255, 70), 2)

cv.namedWindow('window')
cv.setMouseCallback('window', draw_polygon)

while(1):
    cv.imshow("window", img)
    
    c = cv.waitKey(0)

    if c == 27:
        break
