import cv2 as cv
import numpy as np

def selectPolygon(win, frame):
    firstFrame = frame.copy()
    polygons = []
    points = []
    cv.putText(frame, 'click to start recording the polygon', 
            (10, 20), cv.FONT_HERSHEY_DUPLEX, 1.2, (70, 255, 70), 2)
    cv.putText(frame, 'press esc to quit', 
            (10, 60), cv.FONT_HERSHEY_DUPLEX, 1.2, (70, 255, 70), 2)

    def capture_points(event, x, y, flags, param):
        global mouseX, mouseY
        if event == cv.EVENT_LBUTTONDOWN:
            print("x :{}, y: {}".format(x, y))
            points.append((x, y))

            if len(points) > 1:
                if distance(points[0], points[-1]) < 10:
                    # polygon recorded !

                    points.remove(points[-1])
                    polygons.append(points.copy())
                    points.clear()

            frame_new = drawPolygons(firstFrame, polygons)
            if len(points) > 0:
                frame_new = drawPoints(frame_new, points)

            cv.imshow(win, frame_new)
            mouseX, mouseY = x, y

    cv.setMouseCallback(win, capture_points)

    while True:
        cv.imshow(win, frame)
        c = cv.waitKey(0)

        if c == 27 or c == 13:
            break
        if c == ord('z'):
            frame = undo(firstFrame, frame, points, polygons)

        if c == ord('c'):
            frame = clearAll(frame, firstFrame, points, polygons)

    return polygons

def clearAll(frame, firstFrame, points, polygons):
    frame = firstFrame.copy()
    points.clear()
    polygons.clear()

    cv.putText(frame, 'click to start recording the polygon', 
            (10, 20), cv.FONT_HERSHEY_DUPLEX, 1.2, (70, 255, 70), 2)
    cv.putText(frame, 'press esc to quit', 
            (10, 60), cv.FONT_HERSHEY_DUPLEX, 1.2, (70, 255, 70), 2)

    return frame

def drawPolygons(firstFrame, polygons):

    tmp_frame = firstFrame.copy()

    cv.putText(tmp_frame, 'press esc to quit', 
            (10, 20), cv.FONT_HERSHEY_DUPLEX, 1.2, (70, 255, 70), 2)
    cv.putText(tmp_frame, 'press z to undo a point', 
            (10, 60), cv.FONT_HERSHEY_DUPLEX, 1.2, (70, 255, 70), 2)
    cv.putText(tmp_frame, 'press c to clear', 
            (10, 100), cv.FONT_HERSHEY_DUPLEX, 1.2, (70, 255, 70), 2)
    cv.putText(tmp_frame, 'polygons recorded: {}'.format(len(polygons)), 
            (10, 140), cv.FONT_HERSHEY_DUPLEX, 1.2, (70, 255, 70), 2)

    if len(polygons) < 1:
        return tmp_frame

    else:
        for polygon in polygons:
            drawPoints(tmp_frame, polygon, True)

    return tmp_frame

def drawPoints(frame, points, isPolygon=False):
    if isPolygon:
        color = (255, 255, 0)
    else:
        color = (255, 0, 0)

    cv.circle(frame, points[0], 10, color, 4)
    for idx, point in enumerate(points[1:]):
        cv.circle(frame, point, 10, color, 4)
        cv.line(frame, point, points[idx], color, 4)
    if isPolygon:
        cv.line(frame, points[0], points[len(points) - 1], color, 4)

    return frame

def undo(firstFrame, frame, points, polygons):
    if len(points) < 2:
        return frame

    frame = drawPolygons(firstFrame, polygons)

    points.remove(points[-1])
    
    frame = drawPoints(frame, points)

    return frame


def distance(pt1, pt2):
    return abs(pt1[0]-pt2[0]) + abs(pt1[1] - pt2[1])

def mean_pos(polygon):
    x = 0
    y = 0
    for point in polygon:
        x += point[0]
        y += point[1]
    return [ x//len(polygon), y//len(polygon) ]

