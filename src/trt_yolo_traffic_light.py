#! /usr/bin/env python3
"""trt_yolo.py
This script demonstrates how to do real-time object detection with
TensorRT optimized YOLO engine.
"""


import os
import time
import argparse
import numpy as np
import cv2
import pycuda.autoinit  # This is needed for initializing CUDA driver
import sys

from utils.yolo_classes import get_cls_dict
from utils.camera import add_camera_args, Camera
from utils.display import open_window, set_display, show_fps
from utils.visualization import BBoxVisualization
from utils.yolo_with_plugins import TrtYOLO
import rospy
from std_msgs.msg import Float32MultiArray # for sending msg class, confidence inform 
from vision_msgs.msg import Detection2D # for sending bouding box
from vision_msgs.msg import Detection2DArray # for sending bounding box
from vision_msgs.msg import BoundingBox2D # for sending bounding box
from vision_msgs.msg import ObjectHypothesisWithPose # for sending bounding box
from sensor_msgs.msg import Image

WINDOW_NAME = 'Esens Detection'

def parse_args():
    """Parse input arguments."""
    desc = ('Capture and display live camera video, while doing '
            'real-time object detection with TensorRT optimized '
            'YOLO model on Jetson')
    parser = argparse.ArgumentParser(description=desc)
    parser = add_camera_args(parser)
    parser.add_argument(
        '-c', '--category_num', type=int, default=80,
        help='number of object categories [80]')
    parser.add_argument(
        '-m', '--model', type=str, required=True,
        help=('[yolov3-tiny|yolov3|yolov3-spp|yolov4-tiny|yolov4|'
              'yolov4-csp|yolov4x-mish]-[{dimension}], where '
              '{dimension} could be either a single number (e.g. '
              '288, 416, 608) or 2 numbers, WxH (e.g. 416x256)'))
    parser.add_argument(
        '-l', '--letter_box', action='store_true',
        help='inference with letterboxed image [False]')
    args = parser.parse_args()
    return args


def loop_and_detect(pub, pub2, cam, trt_yolo, conf_th, vis):
    """Continuously capture images from camera and do object detection.
    # Arguments
      cam: the camera instance (video source).
      trt_yolo: the TRT YOLO object detector instance.
      conf_th: confidence/score threshold for object detection.
      vis: for visualization.
    """
    r = rospy.Rate(10) #to downgrade FPS
    full_scrn = False
    fps = 0.0
    tic = time.time()

    while True:
        if cv2.getWindowProperty(WINDOW_NAME, 0) < 0:
            break
        frame = cam.read()
        if frame is None:
            break
        ######### img
        img_msg = Image()
        img_msg.height = frame.shape[0]
        img_msg.width = frame.shape[1]
        img_msg.encoding = "bgr8"
        img_msg.is_bigendian = 0
        img_msg.data = frame.tostring()
        img_msg.step = 1920
        ######## tnwjdwn
        #img_msg = bridge.cv2_to_imgmsg(img, "bgr8")
        #print(img_msg)
        
        boxes, confs, clss = trt_yolo.detect(frame, conf_th)
        img = vis.draw_bboxes(frame, boxes, confs, clss)
        img = show_fps(img, fps)
        cv2.imshow(WINDOW_NAME, img)
        toc = time.time()
        curr_fps = 1.0 / (toc - tic)
        # calculate an exponentially decaying average of fps number
        fps = curr_fps if fps == 0.0 else (fps*0.95 + curr_fps*0.05)
        tic = toc
        
        # publish msg        
        detection2d = Detection2DArray() # create Detection2DArray ros msg (vision_msg)
        detection2d.header.stamp = rospy.Time.now()
        detection2d.header.frame_id = "camera"
        idx = int()
        box_size = float()
        box_arr = []

        for i in range(len(boxes)):
            detection = Detection2D()
            obj_info = ObjectHypothesisWithPose()
            detection.header.stamp = rospy.Time.now()
            detection.header.frame_id="camera"
                
            detection.bbox.center.x = boxes[i][0] + (boxes[i][2] - boxes[i][0])/2 # get bounding center x
            detection.bbox.center.y = boxes[i][1] + (boxes[i][3] - boxes[i][1])/2 # get bounding cetner y
            detection.bbox.center.theta = 0.0
               
            detection.bbox.size_x = abs(boxes[i][0] - boxes[i][2]) # get bounding x size
            detection.bbox.size_y = abs(boxes[i][1] - boxes[i][3]) # get bounding y size
                
            #box size
            box_size = detection.bbox.size_x * detection.bbox.size_y
                
            #cls conf
            
            traffic_clss = int(clss[i])
            if (traffic_clss == 0 or traffic_clss == 1): ## RED
                traffic_clss = 0
            elif (traffic_clss == 2 or traffic_clss == 3): ## YELLOW
                traffic_clss = 1
            elif (traffic_clss == 4 or traffic_clss == 5): ## GREEN
                traffic_clss = 2
            elif (traffic_clss == 6): ## RED LEFT
                traffic_clss = 3
            elif (traffic_clss == 7): ## GREEN LEFT
                traffic_clss = 4


            obj_info.id = traffic_clss
            obj_info.score = confs[i]

            if (i==0):
                box_arr = np.append(box_arr, box_size)
            else:
                box_arr = np.append(box_arr, box_size)
                box_arr = np.sort(box_arr)[::-1]
                idxar = np.where(box_arr == box_size)
                idx = idxar[0][0]
            
            detection.results.append(obj_info)
            

            detection2d.detections.insert(idx, detection)
            
            print(sys.getsizeof(detection))
        
        pub2.publish(img_msg) # send msg confidence
        pub.publish(detection2d) # send msg bounding box
        # print("------------------")
        # print("top_left |\nx : ", detection2d.detections[0].bbox.center.x - (detection2d.detections[0].bbox.size_x/2),
        #                 "\ny : ",detection2d.detections[0].bbox.center.y - (detection2d.detections[0].bbox.size_y/2))
        # print("bottom_right |\nx : ", detection2d.detections[0].bbox.center.x + (detection2d.detections[0].bbox.size_x/2),
        #                     "\ny : ",detection2d.detections[0].bbox.center.y + (detection2d.detections[0].bbox.size_y/2))
        # print("real box : ",  boxes)
        # print("class : ", detection2d.detections[0].results[0].id)
        # print("confidence : ", detection2d.detections[0].results[0].score)
        # print("===================")
        # print(sys.getsizeof(detection2d))
        # print(detection.results)
        r.sleep() # to downgrade FPS
        
        ###################
        key = cv2.waitKey(1)
        if key == 27:  # ESC key: quit program
            break
        elif key == ord('F') or key == ord('f'):  # Toggle fullscreen
            full_scrn = not full_scrn
            set_display(WINDOW_NAME, full_scrn)


def main(publisher, publisher2):
    pub = publisher
    pub2 = publisher2
    args = parse_args()
    if args.category_num <= 0:
        raise SystemExit('ERROR: bad category_num (%d)!' % args.category_num)
    if not os.path.isfile('yolo/%s.trt' % args.model):
        raise SystemExit('ERROR: file (yolo/%s.trt) not found!' % args.model)

    cam = Camera(args)
    if not cam.isOpened():
        raise SystemExit('ERROR: failed to open camera!')

    cls_dict = get_cls_dict(args.category_num)
    vis = BBoxVisualization(cls_dict)
    trt_yolo = TrtYOLO(args.model, args.category_num, args.letter_box)

    open_window(
        WINDOW_NAME, 'Camera TensorRT YOLO Demo',
        cam.img_width, cam.img_height)
    loop_and_detect(pub,pub2, cam, trt_yolo, conf_th=0.9, vis=vis)

    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    rospy.init_node('VisionYOLO', anonymous=False) # create node
    pub = rospy.Publisher('/bbox', Detection2DArray , queue_size=1) # create bbox msg 
    pub2 = rospy.Publisher('/usb_cam/image_raw', Image , queue_size=1) # create confs msg
    main(pub, pub2)