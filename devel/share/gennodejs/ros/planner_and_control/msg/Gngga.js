// Auto-generated. Do not edit!

// (in-package planner_and_control.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class Gngga {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.latitude = null;
      this.longitude = null;
      this.quality_indicator = null;
      this.noise = null;
      this.satellite = null;
    }
    else {
      if (initObj.hasOwnProperty('latitude')) {
        this.latitude = initObj.latitude
      }
      else {
        this.latitude = 0.0;
      }
      if (initObj.hasOwnProperty('longitude')) {
        this.longitude = initObj.longitude
      }
      else {
        this.longitude = 0.0;
      }
      if (initObj.hasOwnProperty('quality_indicator')) {
        this.quality_indicator = initObj.quality_indicator
      }
      else {
        this.quality_indicator = 0.0;
      }
      if (initObj.hasOwnProperty('noise')) {
        this.noise = initObj.noise
      }
      else {
        this.noise = 0.0;
      }
      if (initObj.hasOwnProperty('satellite')) {
        this.satellite = initObj.satellite
      }
      else {
        this.satellite = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Gngga
    // Serialize message field [latitude]
    bufferOffset = _serializer.float64(obj.latitude, buffer, bufferOffset);
    // Serialize message field [longitude]
    bufferOffset = _serializer.float64(obj.longitude, buffer, bufferOffset);
    // Serialize message field [quality_indicator]
    bufferOffset = _serializer.float32(obj.quality_indicator, buffer, bufferOffset);
    // Serialize message field [noise]
    bufferOffset = _serializer.float32(obj.noise, buffer, bufferOffset);
    // Serialize message field [satellite]
    bufferOffset = _serializer.float32(obj.satellite, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Gngga
    let len;
    let data = new Gngga(null);
    // Deserialize message field [latitude]
    data.latitude = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [longitude]
    data.longitude = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [quality_indicator]
    data.quality_indicator = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [noise]
    data.noise = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [satellite]
    data.satellite = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 28;
  }

  static datatype() {
    // Returns string type for a message object
    return 'planner_and_control/Gngga';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '63e398a035d41ac999d8966a3c9d2faa';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64 latitude
    float64 longitude
    
    float32 quality_indicator # 0 - fix not available, 1 - GPS fix, 2 - Differential GPS fix
    float32 noise
    float32 satellite
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Gngga(null);
    if (msg.latitude !== undefined) {
      resolved.latitude = msg.latitude;
    }
    else {
      resolved.latitude = 0.0
    }

    if (msg.longitude !== undefined) {
      resolved.longitude = msg.longitude;
    }
    else {
      resolved.longitude = 0.0
    }

    if (msg.quality_indicator !== undefined) {
      resolved.quality_indicator = msg.quality_indicator;
    }
    else {
      resolved.quality_indicator = 0.0
    }

    if (msg.noise !== undefined) {
      resolved.noise = msg.noise;
    }
    else {
      resolved.noise = 0.0
    }

    if (msg.satellite !== undefined) {
      resolved.satellite = msg.satellite;
    }
    else {
      resolved.satellite = 0.0
    }

    return resolved;
    }
};

module.exports = Gngga;
