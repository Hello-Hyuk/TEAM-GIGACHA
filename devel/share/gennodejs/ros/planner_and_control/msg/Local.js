// Auto-generated. Do not edit!

// (in-package planner_and_control.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let geometry_msgs = _finder('geometry_msgs');

//-----------------------------------------------------------

class Local {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.x = null;
      this.y = null;
      this.heading = null;
      this.dr_x = null;
      this.dr_y = null;
      this.dr_vel = null;
      this.orientation = null;
    }
    else {
      if (initObj.hasOwnProperty('x')) {
        this.x = initObj.x
      }
      else {
        this.x = 0.0;
      }
      if (initObj.hasOwnProperty('y')) {
        this.y = initObj.y
      }
      else {
        this.y = 0.0;
      }
      if (initObj.hasOwnProperty('heading')) {
        this.heading = initObj.heading
      }
      else {
        this.heading = 0.0;
      }
      if (initObj.hasOwnProperty('dr_x')) {
        this.dr_x = initObj.dr_x
      }
      else {
        this.dr_x = 0.0;
      }
      if (initObj.hasOwnProperty('dr_y')) {
        this.dr_y = initObj.dr_y
      }
      else {
        this.dr_y = 0.0;
      }
      if (initObj.hasOwnProperty('dr_vel')) {
        this.dr_vel = initObj.dr_vel
      }
      else {
        this.dr_vel = 0.0;
      }
      if (initObj.hasOwnProperty('orientation')) {
        this.orientation = initObj.orientation
      }
      else {
        this.orientation = new geometry_msgs.msg.Quaternion();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Local
    // Serialize message field [x]
    bufferOffset = _serializer.float64(obj.x, buffer, bufferOffset);
    // Serialize message field [y]
    bufferOffset = _serializer.float64(obj.y, buffer, bufferOffset);
    // Serialize message field [heading]
    bufferOffset = _serializer.float64(obj.heading, buffer, bufferOffset);
    // Serialize message field [dr_x]
    bufferOffset = _serializer.float64(obj.dr_x, buffer, bufferOffset);
    // Serialize message field [dr_y]
    bufferOffset = _serializer.float64(obj.dr_y, buffer, bufferOffset);
    // Serialize message field [dr_vel]
    bufferOffset = _serializer.float64(obj.dr_vel, buffer, bufferOffset);
    // Serialize message field [orientation]
    bufferOffset = geometry_msgs.msg.Quaternion.serialize(obj.orientation, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Local
    let len;
    let data = new Local(null);
    // Deserialize message field [x]
    data.x = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [y]
    data.y = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [heading]
    data.heading = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [dr_x]
    data.dr_x = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [dr_y]
    data.dr_y = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [dr_vel]
    data.dr_vel = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [orientation]
    data.orientation = geometry_msgs.msg.Quaternion.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 80;
  }

  static datatype() {
    // Returns string type for a message object
    return 'planner_and_control/Local';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '5482e65cb9b89e47309bd05fd67914ba';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64 x
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
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Local(null);
    if (msg.x !== undefined) {
      resolved.x = msg.x;
    }
    else {
      resolved.x = 0.0
    }

    if (msg.y !== undefined) {
      resolved.y = msg.y;
    }
    else {
      resolved.y = 0.0
    }

    if (msg.heading !== undefined) {
      resolved.heading = msg.heading;
    }
    else {
      resolved.heading = 0.0
    }

    if (msg.dr_x !== undefined) {
      resolved.dr_x = msg.dr_x;
    }
    else {
      resolved.dr_x = 0.0
    }

    if (msg.dr_y !== undefined) {
      resolved.dr_y = msg.dr_y;
    }
    else {
      resolved.dr_y = 0.0
    }

    if (msg.dr_vel !== undefined) {
      resolved.dr_vel = msg.dr_vel;
    }
    else {
      resolved.dr_vel = 0.0
    }

    if (msg.orientation !== undefined) {
      resolved.orientation = geometry_msgs.msg.Quaternion.Resolve(msg.orientation)
    }
    else {
      resolved.orientation = new geometry_msgs.msg.Quaternion()
    }

    return resolved;
    }
};

module.exports = Local;
