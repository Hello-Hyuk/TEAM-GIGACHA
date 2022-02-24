// Auto-generated. Do not edit!

// (in-package planner_and_control.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let Path = require('./Path.js');

//-----------------------------------------------------------

class Ego {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.x = null;
      this.y = null;
      this.heading = null;
      this.index = null;
      this.speed = null;
      this.steer = null;
      this.brake = null;
      this.gear = null;
      this.target_speed = null;
      this.global_path = null;
      this.auto_manual = null;
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
      if (initObj.hasOwnProperty('index')) {
        this.index = initObj.index
      }
      else {
        this.index = 0;
      }
      if (initObj.hasOwnProperty('speed')) {
        this.speed = initObj.speed
      }
      else {
        this.speed = 0.0;
      }
      if (initObj.hasOwnProperty('steer')) {
        this.steer = initObj.steer
      }
      else {
        this.steer = 0.0;
      }
      if (initObj.hasOwnProperty('brake')) {
        this.brake = initObj.brake
      }
      else {
        this.brake = 0;
      }
      if (initObj.hasOwnProperty('gear')) {
        this.gear = initObj.gear
      }
      else {
        this.gear = 0;
      }
      if (initObj.hasOwnProperty('target_speed')) {
        this.target_speed = initObj.target_speed
      }
      else {
        this.target_speed = 0.0;
      }
      if (initObj.hasOwnProperty('global_path')) {
        this.global_path = initObj.global_path
      }
      else {
        this.global_path = [];
      }
      if (initObj.hasOwnProperty('auto_manual')) {
        this.auto_manual = initObj.auto_manual
      }
      else {
        this.auto_manual = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Ego
    // Serialize message field [x]
    bufferOffset = _serializer.float64(obj.x, buffer, bufferOffset);
    // Serialize message field [y]
    bufferOffset = _serializer.float64(obj.y, buffer, bufferOffset);
    // Serialize message field [heading]
    bufferOffset = _serializer.float64(obj.heading, buffer, bufferOffset);
    // Serialize message field [index]
    bufferOffset = _serializer.int32(obj.index, buffer, bufferOffset);
    // Serialize message field [speed]
    bufferOffset = _serializer.float32(obj.speed, buffer, bufferOffset);
    // Serialize message field [steer]
    bufferOffset = _serializer.float32(obj.steer, buffer, bufferOffset);
    // Serialize message field [brake]
    bufferOffset = _serializer.int32(obj.brake, buffer, bufferOffset);
    // Serialize message field [gear]
    bufferOffset = _serializer.int16(obj.gear, buffer, bufferOffset);
    // Serialize message field [target_speed]
    bufferOffset = _serializer.float32(obj.target_speed, buffer, bufferOffset);
    // Serialize message field [global_path]
    // Serialize the length for message field [global_path]
    bufferOffset = _serializer.uint32(obj.global_path.length, buffer, bufferOffset);
    obj.global_path.forEach((val) => {
      bufferOffset = Path.serialize(val, buffer, bufferOffset);
    });
    // Serialize message field [auto_manual]
    bufferOffset = _serializer.int16(obj.auto_manual, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Ego
    let len;
    let data = new Ego(null);
    // Deserialize message field [x]
    data.x = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [y]
    data.y = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [heading]
    data.heading = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [index]
    data.index = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [speed]
    data.speed = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [steer]
    data.steer = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [brake]
    data.brake = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [gear]
    data.gear = _deserializer.int16(buffer, bufferOffset);
    // Deserialize message field [target_speed]
    data.target_speed = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [global_path]
    // Deserialize array length for message field [global_path]
    len = _deserializer.uint32(buffer, bufferOffset);
    data.global_path = new Array(len);
    for (let i = 0; i < len; ++i) {
      data.global_path[i] = Path.deserialize(buffer, bufferOffset)
    }
    // Deserialize message field [auto_manual]
    data.auto_manual = _deserializer.int16(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    object.global_path.forEach((val) => {
      length += Path.getMessageSize(val);
    });
    return length + 52;
  }

  static datatype() {
    // Returns string type for a message object
    return 'planner_and_control/Ego';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '258a1134fe7ea402fb7a013bfa91a320';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64 x
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
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Ego(null);
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

    if (msg.index !== undefined) {
      resolved.index = msg.index;
    }
    else {
      resolved.index = 0
    }

    if (msg.speed !== undefined) {
      resolved.speed = msg.speed;
    }
    else {
      resolved.speed = 0.0
    }

    if (msg.steer !== undefined) {
      resolved.steer = msg.steer;
    }
    else {
      resolved.steer = 0.0
    }

    if (msg.brake !== undefined) {
      resolved.brake = msg.brake;
    }
    else {
      resolved.brake = 0
    }

    if (msg.gear !== undefined) {
      resolved.gear = msg.gear;
    }
    else {
      resolved.gear = 0
    }

    if (msg.target_speed !== undefined) {
      resolved.target_speed = msg.target_speed;
    }
    else {
      resolved.target_speed = 0.0
    }

    if (msg.global_path !== undefined) {
      resolved.global_path = new Array(msg.global_path.length);
      for (let i = 0; i < resolved.global_path.length; ++i) {
        resolved.global_path[i] = Path.Resolve(msg.global_path[i]);
      }
    }
    else {
      resolved.global_path = []
    }

    if (msg.auto_manual !== undefined) {
      resolved.auto_manual = msg.auto_manual;
    }
    else {
      resolved.auto_manual = 0
    }

    return resolved;
    }
};

module.exports = Ego;
