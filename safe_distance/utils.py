from yolov4.tf import YOLOv4

import tensorflow as tf
import cv2 as cv
import numpy as np
import time

def isTiny(weight):
    if 'tiny' in str(weight):
        return True
    return False

def namePath(data):
    arq = open(data, 'r')
    while(1):
        line = arq.readline()
        if 'names' in line:
            return line.split('=')[1][0:-1]

def infer(model, frame, iou_thresh=0.5, score_thresh=0.75, show_time=False):
    resized_image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    resized_image = model.resize_image(resized_image)

    resized_image = resized_image / 255.

    input_data = resized_image[tf.newaxis, ...].astype(np.float32)
    if show_time:
        start_time = time.time()

    # x_pred == Dim(1, output_size, output_size, anchors, (bbox))
    candidates = model.model.predict(input_data)
    _candidates = []

    for candidate in candidates:
        batch_size = candidate.shape[0]
        grid_size = candidate.shape[1]
        _candidates.append(tf.reshape(candidate, shape=(1, grid_size * grid_size * 3, -1)))

    # candidates == Dim(batch, candidates, (bbox))
    candidates = np.concatenate(_candidates, axis=1)

    # pred_bboxes == Dim(candidates, (x, y, w, h, class_id, prob))
    pred_bboxes = model.candidates_to_pred_bboxes(candidates[0], iou_thresh, score_thresh)
    pred_bboxes = model.fit_pred_bboxes_to_original(pred_bboxes, frame.shape)

    if show_time:
        exec_time = time.time() - start_time
        print("time: {:.2f} ms".format(exec_time * 1000))

    return pred_bboxes

def class_name(class_id):
    if class_id == 0:
        return 'car'
    if class_id == 1:
        return 'bus'
    if class_id == 2:
        return 'motorcycle'
