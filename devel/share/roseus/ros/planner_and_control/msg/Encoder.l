;; Auto-generated. Do not edit!


(when (boundp 'planner_and_control::Encoder)
  (if (not (find-package "PLANNER_AND_CONTROL"))
    (make-package "PLANNER_AND_CONTROL"))
  (shadow 'Encoder (find-package "PLANNER_AND_CONTROL")))
(unless (find-package "PLANNER_AND_CONTROL::ENCODER")
  (make-package "PLANNER_AND_CONTROL::ENCODER"))

(in-package "ROS")
;;//! \htmlinclude Encoder.msg.html


(defclass planner_and_control::Encoder
  :super ros::object
  :slots (_left _right ))

(defmethod planner_and_control::Encoder
  (:init
   (&key
    ((:left __left) 0)
    ((:right __right) 0)
    )
   (send-super :init)
   (setq _left (round __left))
   (setq _right (round __right))
   self)
  (:left
   (&optional __left)
   (if __left (setq _left __left)) _left)
  (:right
   (&optional __right)
   (if __right (setq _right __right)) _right)
  (:serialization-length
   ()
   (+
    ;; int32 _left
    4
    ;; int32 _right
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _left
       (write-long _left s)
     ;; int32 _right
       (write-long _right s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _left
     (setq _left (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _right
     (setq _right (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get planner_and_control::Encoder :md5sum-) "febc810ab9cc360ca3f47fcee4f2ba71")
(setf (get planner_and_control::Encoder :datatype-) "planner_and_control/Encoder")
(setf (get planner_and_control::Encoder :definition-)
      "int32 left
int32 right
")



(provide :planner_and_control/Encoder "febc810ab9cc360ca3f47fcee4f2ba71")


