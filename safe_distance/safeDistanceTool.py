from pydarknet import Detector, Image
from math import sqrt
from veloc import *
from progress.bar import Bar

import pandas as pd
import cv2 as cv
import argparse
import time
import os

os.environ['DARKNET_HOME'] = '/darknet/'

def parse_args():
    parser = argparse.ArgumentParser(
        description='Process a video with the YOLO object detector'
    )

    parser.add_argument(
        'cfg', type=str,
        help='Path to yolo configuration file'
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
    
    # Instanciate the YOLO detector
    net = Detector(
        bytes(args.cfg, encoding='utf-8'),
        bytes(args.weight, encoding='utf-8'),
        0,
        bytes(args.data, encoding='utf-8')
    )

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
        print('Error readning video stream')
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

        dark_frame = Image(frame)
        results = net.detect(dark_frame)
        del dark_frame

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
            _, _, (x, y, w, h) = result

            if(roiX <= x <= roiX+roiW and roiY <= y <= roiY+roiH):
                resultsInsideRoi.append(result)
        listFrame = []
        for index, (className, score, bounds) in enumerate(resultsInsideRoi):
            className = str(className.decode("utf-8")) + str(index)
            x, y, w, h = bounds
            listFrame.append(Veic([className, score, x, y, w, h]))
            
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
                _, _, (nextX, nextY, nextW, nextH) = result

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
        if (not first):
            memory.set_frame(listFrame)
        else:
            memory = List_Veic(listFrame)
            first = False
        for veic in memory.l:
            cv.putText(frame, str(veic.mean_veloc)[0:4], (veic.x, veic.y), cv.FONT_HERSHEY_COMPLEX, 0.9, (0,255,0))

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
