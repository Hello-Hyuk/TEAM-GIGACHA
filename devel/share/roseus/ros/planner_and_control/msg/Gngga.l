;; Auto-generated. Do not edit!


(when (boundp 'planner_and_control::Gngga)
  (if (not (find-package "PLANNER_AND_CONTROL"))
    (make-package "PLANNER_AND_CONTROL"))
  (shadow 'Gngga (find-package "PLANNER_AND_CONTROL")))
(unless (find-package "PLANNER_AND_CONTROL::GNGGA")
  (make-package "PLANNER_AND_CONTROL::GNGGA"))

(in-package "ROS")
;;//! \htmlinclude Gngga.msg.html


(defclass planner_and_control::Gngga
  :super ros::object
  :slots (_latitude _longitude _quality_indicator _noise _satellite ))

(defmethod planner_and_control::Gngga
  (:init
   (&key
    ((:latitude __latitude) 0.0)
    ((:longitude __longitude) 0.0)
    ((:quality_indicator __quality_indicator) 0.0)
    ((:noise __noise) 0.0)
    ((:satellite __satellite) 0.0)
    )
   (send-super :init)
   (setq _latitude (float __latitude))
   (setq _longitude (float __longitude))
   (setq _quality_indicator (float __quality_indicator))
   (setq _noise (float __noise))
   (setq _satellite (float __satellite))
   self)
  (:latitude
   (&optional __latitude)
   (if __latitude (setq _latitude __latitude)) _latitude)
  (:longitude
   (&optional __longitude)
   (if __longitude (setq _longitude __longitude)) _longitude)
  (:quality_indicator
   (&optional __quality_indicator)
   (if __quality_indicator (setq _quality_indicator __quality_indicator)) _quality_indicator)
  (:noise
   (&optional __noise)
   (if __noise (setq _noise __noise)) _noise)
  (:satellite
   (&optional __satellite)
   (if __satellite (setq _satellite __satellite)) _satellite)
  (:serialization-length
   ()
   (+
    ;; float64 _latitude
    8
    ;; float64 _longitude
    8
    ;; float32 _quality_indicator
    4
    ;; float32 _noise
    4
    ;; float32 _satellite
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _latitude
       (sys::poke _latitude (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _longitude
       (sys::poke _longitude (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float32 _quality_indicator
       (sys::poke _quality_indicator (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _noise
       (sys::poke _noise (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _satellite
       (sys::poke _satellite (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _latitude
     (setq _latitude (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _longitude
     (setq _longitude (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float32 _quality_indicator
     (setq _quality_indicator (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _noise
     (setq _noise (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _satellite
     (setq _satellite (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get planner_and_control::Gngga :md5sum-) "63e398a035d41ac999d8966a3c9d2faa")
(setf (get planner_and_control::Gngga :datatype-) "planner_and_control/Gngga")
(setf (get planner_and_control::Gngga :definition-)
      "float64 latitude
float64 longitude

float32 quality_indicator # 0 - fix not available, 1 - GPS fix, 2 - Differential GPS fix
float32 noise
float32 satellite

")



(provide :planner_and_control/Gngga "63e398a035d41ac999d8966a3c9d2faa")


