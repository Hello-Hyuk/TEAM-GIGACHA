;; Auto-generated. Do not edit!


(when (boundp 'planner_and_control::Ego)
  (if (not (find-package "PLANNER_AND_CONTROL"))
    (make-package "PLANNER_AND_CONTROL"))
  (shadow 'Ego (find-package "PLANNER_AND_CONTROL")))
(unless (find-package "PLANNER_AND_CONTROL::EGO")
  (make-package "PLANNER_AND_CONTROL::EGO"))

(in-package "ROS")
;;//! \htmlinclude Ego.msg.html


(defclass planner_and_control::Ego
  :super ros::object
  :slots (_x _y _heading _index _speed _steer _brake _gear _target_speed _global_path _auto_manual ))

(defmethod planner_and_control::Ego
  (:init
   (&key
    ((:x __x) 0.0)
    ((:y __y) 0.0)
    ((:heading __heading) 0.0)
    ((:index __index) 0)
    ((:speed __speed) 0.0)
    ((:steer __steer) 0.0)
    ((:brake __brake) 0)
    ((:gear __gear) 0)
    ((:target_speed __target_speed) 0.0)
    ((:global_path __global_path) ())
    ((:auto_manual __auto_manual) 0)
    )
   (send-super :init)
   (setq _x (float __x))
   (setq _y (float __y))
   (setq _heading (float __heading))
   (setq _index (round __index))
   (setq _speed (float __speed))
   (setq _steer (float __steer))
   (setq _brake (round __brake))
   (setq _gear (round __gear))
   (setq _target_speed (float __target_speed))
   (setq _global_path __global_path)
   (setq _auto_manual (round __auto_manual))
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
  (:index
   (&optional __index)
   (if __index (setq _index __index)) _index)
  (:speed
   (&optional __speed)
   (if __speed (setq _speed __speed)) _speed)
  (:steer
   (&optional __steer)
   (if __steer (setq _steer __steer)) _steer)
  (:brake
   (&optional __brake)
   (if __brake (setq _brake __brake)) _brake)
  (:gear
   (&optional __gear)
   (if __gear (setq _gear __gear)) _gear)
  (:target_speed
   (&optional __target_speed)
   (if __target_speed (setq _target_speed __target_speed)) _target_speed)
  (:global_path
   (&rest __global_path)
   (if (keywordp (car __global_path))
       (send* _global_path __global_path)
     (progn
       (if __global_path (setq _global_path (car __global_path)))
       _global_path)))
  (:auto_manual
   (&optional __auto_manual)
   (if __auto_manual (setq _auto_manual __auto_manual)) _auto_manual)
  (:serialization-length
   ()
   (+
    ;; float64 _x
    8
    ;; float64 _y
    8
    ;; float64 _heading
    8
    ;; int32 _index
    4
    ;; float32 _speed
    4
    ;; float32 _steer
    4
    ;; int32 _brake
    4
    ;; int16 _gear
    2
    ;; float32 _target_speed
    4
    ;; planner_and_control/Path[] _global_path
    (apply #'+ (send-all _global_path :serialization-length)) 4
    ;; int16 _auto_manual
    2
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
     ;; int32 _index
       (write-long _index s)
     ;; float32 _speed
       (sys::poke _speed (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _steer
       (sys::poke _steer (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; int32 _brake
       (write-long _brake s)
     ;; int16 _gear
       (write-word _gear s)
     ;; float32 _target_speed
       (sys::poke _target_speed (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; planner_and_control/Path[] _global_path
     (write-long (length _global_path) s)
     (dolist (elem _global_path)
       (send elem :serialize s)
       )
     ;; int16 _auto_manual
       (write-word _auto_manual s)
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
   ;; int32 _index
     (setq _index (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; float32 _speed
     (setq _speed (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _steer
     (setq _steer (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; int32 _brake
     (setq _brake (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int16 _gear
     (setq _gear (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; float32 _target_speed
     (setq _target_speed (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; planner_and_control/Path[] _global_path
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _global_path (let (r) (dotimes (i n) (push (instance planner_and_control::Path :init) r)) r))
     (dolist (elem- _global_path)
     (send elem- :deserialize buf ptr-) (incf ptr- (send elem- :serialization-length))
     ))
   ;; int16 _auto_manual
     (setq _auto_manual (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;;
   self)
  )

(setf (get planner_and_control::Ego :md5sum-) "258a1134fe7ea402fb7a013bfa91a320")
(setf (get planner_and_control::Ego :datatype-) "planner_and_control/Ego")
(setf (get planner_and_control::Ego :definition-)
      "float64 x
float64 y
float64 heading
int32 index
float32 speed
float32 steer
int32 brake
int16 gear
float32 target_speed
planner_and_control/Path[] global_path
int16 auto_manual
================================================================================
MSG: planner_and_control/Path
float64[] x
float64[] y
float64[] heading
float64[] k
")



(provide :planner_and_control/Ego "258a1134fe7ea402fb7a013bfa91a320")


