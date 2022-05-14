;; Auto-generated. Do not edit!


(when (boundp 'planner_and_control::SegmentObstacle)
  (if (not (find-package "PLANNER_AND_CONTROL"))
    (make-package "PLANNER_AND_CONTROL"))
  (shadow 'SegmentObstacle (find-package "PLANNER_AND_CONTROL")))
(unless (find-package "PLANNER_AND_CONTROL::SEGMENTOBSTACLE")
  (make-package "PLANNER_AND_CONTROL::SEGMENTOBSTACLE"))

(in-package "ROS")
;;//! \htmlinclude SegmentObstacle.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(defclass planner_and_control::SegmentObstacle
  :super ros::object
  :slots (_first_point _mid_point _last_point ))

(defmethod planner_and_control::SegmentObstacle
  (:init
   (&key
    ((:first_point __first_point) (instance geometry_msgs::Point :init))
    ((:mid_point __mid_point) (instance geometry_msgs::Point :init))
    ((:last_point __last_point) (instance geometry_msgs::Point :init))
    )
   (send-super :init)
   (setq _first_point __first_point)
   (setq _mid_point __mid_point)
   (setq _last_point __last_point)
   self)
  (:first_point
   (&rest __first_point)
   (if (keywordp (car __first_point))
       (send* _first_point __first_point)
     (progn
       (if __first_point (setq _first_point (car __first_point)))
       _first_point)))
  (:mid_point
   (&rest __mid_point)
   (if (keywordp (car __mid_point))
       (send* _mid_point __mid_point)
     (progn
       (if __mid_point (setq _mid_point (car __mid_point)))
       _mid_point)))
  (:last_point
   (&rest __last_point)
   (if (keywordp (car __last_point))
       (send* _last_point __last_point)
     (progn
       (if __last_point (setq _last_point (car __last_point)))
       _last_point)))
  (:serialization-length
   ()
   (+
    ;; geometry_msgs/Point _first_point
    (send _first_point :serialization-length)
    ;; geometry_msgs/Point _mid_point
    (send _mid_point :serialization-length)
    ;; geometry_msgs/Point _last_point
    (send _last_point :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; geometry_msgs/Point _first_point
       (send _first_point :serialize s)
     ;; geometry_msgs/Point _mid_point
       (send _mid_point :serialize s)
     ;; geometry_msgs/Point _last_point
       (send _last_point :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; geometry_msgs/Point _first_point
     (send _first_point :deserialize buf ptr-) (incf ptr- (send _first_point :serialization-length))
   ;; geometry_msgs/Point _mid_point
     (send _mid_point :deserialize buf ptr-) (incf ptr- (send _mid_point :serialization-length))
   ;; geometry_msgs/Point _last_point
     (send _last_point :deserialize buf ptr-) (incf ptr- (send _last_point :serialization-length))
   ;;
   self)
  )

(setf (get planner_and_control::SegmentObstacle :md5sum-) "bdb4bb46c5b808de9ab8a895007f4603")
(setf (get planner_and_control::SegmentObstacle :datatype-) "planner_and_control/SegmentObstacle")
(setf (get planner_and_control::SegmentObstacle :definition-)
      "geometry_msgs/Point first_point
geometry_msgs/Point mid_point
geometry_msgs/Point last_point


================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

")



(provide :planner_and_control/SegmentObstacle "bdb4bb46c5b808de9ab8a895007f4603")


