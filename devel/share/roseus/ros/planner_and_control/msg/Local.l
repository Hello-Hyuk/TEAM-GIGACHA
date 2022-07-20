;; Auto-generated. Do not edit!


(when (boundp 'planner_and_control::Local)
  (if (not (find-package "PLANNER_AND_CONTROL"))
    (make-package "PLANNER_AND_CONTROL"))
  (shadow 'Local (find-package "PLANNER_AND_CONTROL")))
(unless (find-package "PLANNER_AND_CONTROL::LOCAL")
  (make-package "PLANNER_AND_CONTROL::LOCAL"))

(in-package "ROS")
;;//! \htmlinclude Local.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(defclass planner_and_control::Local
  :super ros::object
  :slots (_x _y _heading _dr_x _dr_y _dr_vel _orientation ))

(defmethod planner_and_control::Local
  (:init
   (&key
    ((:x __x) 0.0)
    ((:y __y) 0.0)
    ((:heading __heading) 0.0)
    ((:dr_x __dr_x) 0.0)
    ((:dr_y __dr_y) 0.0)
    ((:dr_vel __dr_vel) 0.0)
    ((:orientation __orientation) (instance geometry_msgs::Quaternion :init))
    )
   (send-super :init)
   (setq _x (float __x))
   (setq _y (float __y))
   (setq _heading (float __heading))
   (setq _dr_x (float __dr_x))
   (setq _dr_y (float __dr_y))
   (setq _dr_vel (float __dr_vel))
   (setq _orientation __orientation)
   self)
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:heading
   (&optional __heading)
   (if __heading (setq _heading __heading)) _heading)
  (:dr_x
   (&optional __dr_x)
   (if __dr_x (setq _dr_x __dr_x)) _dr_x)
  (:dr_y
   (&optional __dr_y)
   (if __dr_y (setq _dr_y __dr_y)) _dr_y)
  (:dr_vel
   (&optional __dr_vel)
   (if __dr_vel (setq _dr_vel __dr_vel)) _dr_vel)
  (:orientation
   (&rest __orientation)
   (if (keywordp (car __orientation))
       (send* _orientation __orientation)
     (progn
       (if __orientation (setq _orientation (car __orientation)))
       _orientation)))
  (:serialization-length
   ()
   (+
    ;; float64 _x
    8
    ;; float64 _y
    8
    ;; float64 _heading
    8
    ;; float64 _dr_x
    8
    ;; float64 _dr_y
    8
    ;; float64 _dr_vel
    8
    ;; geometry_msgs/Quaternion _orientation
    (send _orientation :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _x
       (sys::poke _x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _y
       (sys::poke _y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _heading
       (sys::poke _heading (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _dr_x
       (sys::poke _dr_x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _dr_y
       (sys::poke _dr_y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _dr_vel
       (sys::poke _dr_vel (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; geometry_msgs/Quaternion _orientation
       (send _orientation :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _x
     (setq _x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _y
     (setq _y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _heading
     (setq _heading (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _dr_x
     (setq _dr_x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _dr_y
     (setq _dr_y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _dr_vel
     (setq _dr_vel (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; geometry_msgs/Quaternion _orientation
     (send _orientation :deserialize buf ptr-) (incf ptr- (send _orientation :serialization-length))
   ;;
   self)
  )

(setf (get planner_and_control::Local :md5sum-) "5482e65cb9b89e47309bd05fd67914ba")
(setf (get planner_and_control::Local :datatype-) "planner_and_control/Local")
(setf (get planner_and_control::Local :definition-)
      "float64 x
float64 y
float64 heading
float64 dr_x
float64 dr_y
float64 dr_vel
geometry_msgs/Quaternion orientation
================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w

")



(provide :planner_and_control/Local "5482e65cb9b89e47309bd05fd67914ba")


