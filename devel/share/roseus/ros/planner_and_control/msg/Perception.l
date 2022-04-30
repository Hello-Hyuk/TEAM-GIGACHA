;; Auto-generated. Do not edit!


(when (boundp 'planner_and_control::Perception)
  (if (not (find-package "PLANNER_AND_CONTROL"))
    (make-package "PLANNER_AND_CONTROL"))
  (shadow 'Perception (find-package "PLANNER_AND_CONTROL")))
(unless (find-package "PLANNER_AND_CONTROL::PERCEPTION")
  (make-package "PLANNER_AND_CONTROL::PERCEPTION"))

(in-package "ROS")
;;//! \htmlinclude Perception.msg.html


(defclass planner_and_control::Perception
  :super ros::object
  :slots (_objx _objy _signx _signy _objr ))

(defmethod planner_and_control::Perception
  (:init
   (&key
    ((:objx __objx) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:objy __objy) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:signx __signx) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:signy __signy) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:objr __objr) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _objx __objx)
   (setq _objy __objy)
   (setq _signx __signx)
   (setq _signy __signy)
   (setq _objr __objr)
   self)
  (:objx
   (&optional __objx)
   (if __objx (setq _objx __objx)) _objx)
  (:objy
   (&optional __objy)
   (if __objy (setq _objy __objy)) _objy)
  (:signx
   (&optional __signx)
   (if __signx (setq _signx __signx)) _signx)
  (:signy
   (&optional __signy)
   (if __signy (setq _signy __signy)) _signy)
  (:objr
   (&optional __objr)
   (if __objr (setq _objr __objr)) _objr)
  (:serialization-length
   ()
   (+
    ;; float64[] _objx
    (* 8    (length _objx)) 4
    ;; float64[] _objy
    (* 8    (length _objy)) 4
    ;; float64[] _signx
    (* 8    (length _signx)) 4
    ;; float64[] _signy
    (* 8    (length _signy)) 4
    ;; float64[] _objr
    (* 8    (length _objr)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64[] _objx
     (write-long (length _objx) s)
     (dotimes (i (length _objx))
       (sys::poke (elt _objx i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _objy
     (write-long (length _objy) s)
     (dotimes (i (length _objy))
       (sys::poke (elt _objy i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _signx
     (write-long (length _signx) s)
     (dotimes (i (length _signx))
       (sys::poke (elt _signx i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _signy
     (write-long (length _signy) s)
     (dotimes (i (length _signy))
       (sys::poke (elt _signy i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _objr
     (write-long (length _objr) s)
     (dotimes (i (length _objr))
       (sys::poke (elt _objr i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64[] _objx
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _objx (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _objx i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _objy
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _objy (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _objy i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _signx
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _signx (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _signx i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _signy
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _signy (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _signy i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _objr
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _objr (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _objr i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;;
   self)
  )

(setf (get planner_and_control::Perception :md5sum-) "bd15e37a0feb9c86e718db9ca65322b7")
(setf (get planner_and_control::Perception :datatype-) "planner_and_control/Perception")
(setf (get planner_and_control::Perception :definition-)
      "float64[] objx
float64[] objy
float64[] signx
float64[] signy
float64[] objr
")



(provide :planner_and_control/Perception "bd15e37a0feb9c86e718db9ca65322b7")


