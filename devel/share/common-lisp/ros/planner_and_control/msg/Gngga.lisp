; Auto-generated. Do not edit!


(cl:in-package planner_and_control-msg)


;//! \htmlinclude Gngga.msg.html

(cl:defclass <Gngga> (roslisp-msg-protocol:ros-message)
  ((latitude
    :reader latitude
    :initarg :latitude
    :type cl:float
    :initform 0.0)
   (longitude
    :reader longitude
    :initarg :longitude
    :type cl:float
    :initform 0.0)
   (quality_indicator
    :reader quality_indicator
    :initarg :quality_indicator
    :type cl:float
    :initform 0.0)
   (noise
    :reader noise
    :initarg :noise
    :type cl:float
    :initform 0.0)
   (satellite
    :reader satellite
    :initarg :satellite
    :type cl:float
    :initform 0.0))
)

(cl:defclass Gngga (<Gngga>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Gngga>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Gngga)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name planner_and_control-msg:<Gngga> is deprecated: use planner_and_control-msg:Gngga instead.")))

(cl:ensure-generic-function 'latitude-val :lambda-list '(m))
(cl:defmethod latitude-val ((m <Gngga>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader planner_and_control-msg:latitude-val is deprecated.  Use planner_and_control-msg:latitude instead.")
  (latitude m))

(cl:ensure-generic-function 'longitude-val :lambda-list '(m))
(cl:defmethod longitude-val ((m <Gngga>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader planner_and_control-msg:longitude-val is deprecated.  Use planner_and_control-msg:longitude instead.")
  (longitude m))

(cl:ensure-generic-function 'quality_indicator-val :lambda-list '(m))
(cl:defmethod quality_indicator-val ((m <Gngga>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader planner_and_control-msg:quality_indicator-val is deprecated.  Use planner_and_control-msg:quality_indicator instead.")
  (quality_indicator m))

(cl:ensure-generic-function 'noise-val :lambda-list '(m))
(cl:defmethod noise-val ((m <Gngga>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader planner_and_control-msg:noise-val is deprecated.  Use planner_and_control-msg:noise instead.")
  (noise m))

(cl:ensure-generic-function 'satellite-val :lambda-list '(m))
(cl:defmethod satellite-val ((m <Gngga>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader planner_and_control-msg:satellite-val is deprecated.  Use planner_and_control-msg:satellite instead.")
  (satellite m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Gngga>) ostream)
  "Serializes a message object of type '<Gngga>"
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'latitude))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'longitude))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'quality_indicator))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'noise))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'satellite))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Gngga>) istream)
  "Deserializes a message object of type '<Gngga>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'latitude) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'longitude) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'quality_indicator) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'noise) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'satellite) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Gngga>)))
  "Returns string type for a message object of type '<Gngga>"
  "planner_and_control/Gngga")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Gngga)))
  "Returns string type for a message object of type 'Gngga"
  "planner_and_control/Gngga")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Gngga>)))
  "Returns md5sum for a message object of type '<Gngga>"
  "63e398a035d41ac999d8966a3c9d2faa")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Gngga)))
  "Returns md5sum for a message object of type 'Gngga"
  "63e398a035d41ac999d8966a3c9d2faa")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Gngga>)))
  "Returns full string definition for message of type '<Gngga>"
  (cl:format cl:nil "float64 latitude~%float64 longitude~%~%float32 quality_indicator # 0 - fix not available, 1 - GPS fix, 2 - Differential GPS fix~%float32 noise~%float32 satellite~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Gngga)))
  "Returns full string definition for message of type 'Gngga"
  (cl:format cl:nil "float64 latitude~%float64 longitude~%~%float32 quality_indicator # 0 - fix not available, 1 - GPS fix, 2 - Differential GPS fix~%float32 noise~%float32 satellite~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Gngga>))
  (cl:+ 0
     8
     8
     4
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Gngga>))
  "Converts a ROS message object to a list"
  (cl:list 'Gngga
    (cl:cons ':latitude (latitude msg))
    (cl:cons ':longitude (longitude msg))
    (cl:cons ':quality_indicator (quality_indicator msg))
    (cl:cons ':noise (noise msg))
    (cl:cons ':satellite (satellite msg))
))
