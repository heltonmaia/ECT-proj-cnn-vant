from object_trackers.centroidTracker import *
from yolov4.tf import YOLOv4
from math import sqrt
from progress.bar import Bar
from utils import *

import numpy as np
import pandas as pd
import cv2 as cv
import argparse
import time
import os


def parse_args():
    parser = argparse.ArgumentParser(
        description='Process a video with the YOLO object detector'
    )

    parser.add_argument(
        'data', type=str,
        help='Path to network data file'
    )
    parser.add_argument(
        'weight', type=str,
        help='Path to the weights file'
    )

    parser.add_argument(
        'video', type=str,
        help='Path to source video'
    )

    parser.add_argument(
        'output', type=str,
        help='Name of the log file to be produced'
    )

    parser.add_argument(
        '--debug', action='store_true',
        help='Shows a window with debugging information during video classification.'
    )

    parser.add_argument(
        '--save-video', action='store_true',
        help='Create a video file with the analysis result.'
    )

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    # Init the object tracker
    tracker = CentroidTracker()

    # Init the model
    yolo = YOLOv4(isTiny(bytes(args.weight, encoding="utf-8")))
    yolo.classes = namePath(bytes(args.data, encoding="utf-8"))
    yolo.make_model()
    yolo.load_weights(bytes(args.weight, encoding="utf-8"), weights_type="yolo")
    
    cap = cv.VideoCapture(args.video)
    bar = Bar('Processing Frames', max=int(cap.get(cv.CAP_PROP_FRAME_COUNT)))
    width  = int(cap.get(3))
    height = int(cap.get(4))

    if(not cap.isOpened()):
        print('Error opening video stream!')
        exit()

    print(f'\nAnalysing {args.video}...')

    # with open(f'{args.output}.csv', 'w') as file:
    #     file.write('class,score,x,y,w,h\n')

    if(args.save_video):
        outWriter = cv.VideoWriter(
            f'result_{args.output}.avi',
            cv.VideoWriter_fourcc('M', 'J', 'P', 'G'),
            30, (width, height)
        )

    # Selection of the ROI
    ret, frame = cap.read()

    if(not ret):
        print('Error reading video stream')
        exit()

    roi_win = 'Select ROI for proximity detection'
    cv.namedWindow(roi_win, cv.WINDOW_KEEPRATIO)
    cv.resizeWindow(roi_win, 1685, 988)
    roiX, roiY, roiW, roiH = cv.selectROI(roi_win, frame, False)
    cv.destroyWindow(roi_win)

    #roiX, roiY, roiW, roiH = (380, 565, 1329, 317)
    
    if(args.debug):
        main_win = 'Safe Distance Tool'
        cv.namedWindow(main_win, cv.WINDOW_KEEPRATIO)
        cv.resizeWindow(main_win, 1685, 988)
    first = True
    while(cap.isOpened()):
        
        ret, frame = cap.read()
        bar.next()
        if(not ret):
            break

        # results shape like (n_boxes, (x, y, w, h, class_id, prob))
        results = infer(yolo, frame)

        # values in float between [0, 1] to int values
        results[:, [0, 2]] = results[:, [0, 2]] * width
        results[:, [1, 3]] = results[:, [1, 3]] * height

        # with open(f'{args.output}.txt', 'a') as file:
        #     file.write(str(results) + '\n')

        # Drawing the ROI
        cv.rectangle(
            frame, 
            (roiX, roiY),
            (roiX + roiW, roiY + roiH),
            (80, 80, 80), 2
            #(237, 147, 78), 2
        )

        resultsInsideRoi = []
        for result in results:
            x, y, w, h, _, _ = result

            if(roiX <= x <= roiX+roiW and roiY <= y <= roiY+roiH):
                resultsInsideRoi.append(result)

        # Tracking
        centroids = [(int(x), int(y)) for (x, y, _, _, _, _) in resultsInsideRoi]  
        tracker.update(centroids)

        for index, (x, y, w, h, class_id, score) in enumerate(resultsInsideRoi):

            # Getting the object id, from tracker
            for obj_id, (centroid, dissapeared) in enumerate(zip(tracker.objects.values(), tracker.disappeared.values())):
                if int(x) == centroid[0] and int(y) == centroid[1] and dissapeared == 0:
                    className = class_name(class_id) + '-' + str(obj_id) 

            # Bounding box
            cv.rectangle(
                frame,
                (int(x - w/2), int(y - h/2)),
                (int(x + w/2), int(y + h/2)),
                (91, 249, 77), 2
            )

            # Bounding box center
            cv.circle(
                frame, (int(x), int(y)),
                5, (91, 249, 77), -1
            )

            for result in resultsInsideRoi:
                nextX, nextY, nextW, nextH, _, _ = result

                if(int(nextY) in list(range(int(y) - 50, int(y) + 50))):
                    
                    dist = int(sqrt((x - nextX)**2 + (y - nextY)**2))

                    cv.putText(
                        frame,
                        className + f' {dist}',
                        (int(x - w/2) - 3, int(y - w/2)),
                        cv.FONT_HERSHEY_COMPLEX,
                        0.7, (255, 255, 255)
                    )

                    if(dist < 200):
                        cv.line(
                            frame,
                            (int(x), int(y)),
                            (int(nextX), int(nextY)),
                            (0, 0, 255), 2
                        )
                    else: 
                        cv.line(
                            frame,
                            (int(x), int(y)),
                            (int(nextX), int(nextY)),
                            (91, 249, 77), 2
                        )

                    break


        if(args.debug):
            cv.imshow(main_win, frame)
        
        if(args.save_video):
            outWriter.write(frame)

        key = cv.waitKey(5)
        # esc or q key pressed
        if(key == 27 or key == 113):
            cv.destroyAllWindows()
            cap.release()
            
            if(args.save_video):
                outWriter.release()
            
            exit()
        # Space key pressed
        if(key == 32):
            while True:
                cv.imshow(main_win, frame)

                key2 = cv.waitKey(5)
                if(key2 == 32):
                    break
                elif(key2 == 27 or key2 == 113):
                    cv.destroyAllWindows()
                    cap.release()

                    if(args.save_video):
                        outWriter.release()

                    exit()
    bar.finish()
    print('Done!')
