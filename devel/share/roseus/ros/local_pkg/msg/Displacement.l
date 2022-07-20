;; Auto-generated. Do not edit!


(when (boundp 'local_pkg::Displacement)
  (if (not (find-package "LOCAL_PKG"))
    (make-package "LOCAL_PKG"))
  (shadow 'Displacement (find-package "LOCAL_PKG")))
(unless (find-package "LOCAL_PKG::DISPLACEMENT")
  (make-package "LOCAL_PKG::DISPLACEMENT"))

(in-package "ROS")
;;//! \htmlinclude Displacement.msg.html


(defclass local_pkg::Displacement
  :super ros::object
  :slots (_right ))

(defmethod local_pkg::Displacement
  (:init
   (&key
    ((:right __right) 0)
    )
   (send-super :init)
   (setq _right (round __right))
   self)
  (:right
   (&optional __right)
   (if __right (setq _right __right)) _right)
  (:serialization-length
   ()
   (+
    ;; int32 _right
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _right
       (write-long _right s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _right
     (setq _right (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get local_pkg::Displacement :md5sum-) "27e6ed38e0c67b7b02f5e993e0f9d6ef")
(setf (get local_pkg::Displacement :datatype-) "local_pkg/Displacement")
(setf (get local_pkg::Displacement :definition-)
      "int32 right
")



(provide :local_pkg/Displacement "27e6ed38e0c67b7b02f5e993e0f9d6ef")


