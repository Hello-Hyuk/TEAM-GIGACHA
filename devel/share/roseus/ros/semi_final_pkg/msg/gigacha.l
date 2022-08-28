;; Auto-generated. Do not edit!


(when (boundp 'semi_final_pkg::gigacha)
  (if (not (find-package "SEMI_FINAL_PKG"))
    (make-package "SEMI_FINAL_PKG"))
  (shadow 'gigacha (find-package "SEMI_FINAL_PKG")))
(unless (find-package "SEMI_FINAL_PKG::GIGACHA")
  (make-package "SEMI_FINAL_PKG::GIGACHA"))

(in-package "ROS")
;;//! \htmlinclude gigacha.msg.html


(defclass semi_final_pkg::gigacha
  :super ros::object
  :slots ())

(defmethod semi_final_pkg::gigacha
  (:init
   (&key
    )
   (send-super :init)
   self)
  (:serialization-length
   ()
   (+
    0
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;;
   self)
  )

(setf (get semi_final_pkg::gigacha :md5sum-) "d41d8cd98f00b204e9800998ecf8427e")
(setf (get semi_final_pkg::gigacha :datatype-) "semi_final_pkg/gigacha")
(setf (get semi_final_pkg::gigacha :definition-)
      "
")



(provide :semi_final_pkg/gigacha "d41d8cd98f00b204e9800998ecf8427e")


