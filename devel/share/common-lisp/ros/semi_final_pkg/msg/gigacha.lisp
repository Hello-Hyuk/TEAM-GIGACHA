; Auto-generated. Do not edit!


(cl:in-package semi_final_pkg-msg)


;//! \htmlinclude gigacha.msg.html

(cl:defclass <gigacha> (roslisp-msg-protocol:ros-message)
  ()
)

(cl:defclass gigacha (<gigacha>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <gigacha>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'gigacha)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name semi_final_pkg-msg:<gigacha> is deprecated: use semi_final_pkg-msg:gigacha instead.")))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <gigacha>) ostream)
  "Serializes a message object of type '<gigacha>"
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <gigacha>) istream)
  "Deserializes a message object of type '<gigacha>"
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<gigacha>)))
  "Returns string type for a message object of type '<gigacha>"
  "semi_final_pkg/gigacha")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'gigacha)))
  "Returns string type for a message object of type 'gigacha"
  "semi_final_pkg/gigacha")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<gigacha>)))
  "Returns md5sum for a message object of type '<gigacha>"
  "d41d8cd98f00b204e9800998ecf8427e")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'gigacha)))
  "Returns md5sum for a message object of type 'gigacha"
  "d41d8cd98f00b204e9800998ecf8427e")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<gigacha>)))
  "Returns full string definition for message of type '<gigacha>"
  (cl:format cl:nil "~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'gigacha)))
  "Returns full string definition for message of type 'gigacha"
  (cl:format cl:nil "~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <gigacha>))
  (cl:+ 0
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <gigacha>))
  "Converts a ROS message object to a list"
  (cl:list 'gigacha
))
