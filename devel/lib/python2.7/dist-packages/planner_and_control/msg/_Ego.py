# This Python file uses the following encoding: utf-8
"""autogenerated by genpy from planner_and_control/Ego.msg. Do not edit."""
import codecs
import sys
python3 = True if sys.hexversion > 0x03000000 else False
import genpy
import struct


class Ego(genpy.Message):
  _md5sum = "3d75df4892b9e15b8e081e6cd21cb013"
  _type = "planner_and_control/Ego"
  _has_header = False  # flag to mark the presence of a Header object
  _full_text = """float64 x
float64 y
float64 heading
int32 index
float32 speed
float32 steer
int32 brake
int16 gear
int16 auto_manual"""
  __slots__ = ['x','y','heading','index','speed','steer','brake','gear','auto_manual']
  _slot_types = ['float64','float64','float64','int32','float32','float32','int32','int16','int16']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       x,y,heading,index,speed,steer,brake,gear,auto_manual

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      super(Ego, self).__init__(*args, **kwds)
      # message fields cannot be None, assign default values for those that are
      if self.x is None:
        self.x = 0.
      if self.y is None:
        self.y = 0.
      if self.heading is None:
        self.heading = 0.
      if self.index is None:
        self.index = 0
      if self.speed is None:
        self.speed = 0.
      if self.steer is None:
        self.steer = 0.
      if self.brake is None:
        self.brake = 0
      if self.gear is None:
        self.gear = 0
      if self.auto_manual is None:
        self.auto_manual = 0
    else:
      self.x = 0.
      self.y = 0.
      self.heading = 0.
      self.index = 0
      self.speed = 0.
      self.steer = 0.
      self.brake = 0
      self.gear = 0
      self.auto_manual = 0

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types

  def serialize(self, buff):
    """
    serialize message into buffer
    :param buff: buffer, ``StringIO``
    """
    try:
      _x = self
      buff.write(_get_struct_3di2fi2h().pack(_x.x, _x.y, _x.heading, _x.index, _x.speed, _x.steer, _x.brake, _x.gear, _x.auto_manual))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize(self, str):
    """
    unpack serialized message in str into this message instance
    :param str: byte array of serialized message, ``str``
    """
    if python3:
      codecs.lookup_error("rosmsg").msg_type = self._type
    try:
      end = 0
      _x = self
      start = end
      end += 44
      (_x.x, _x.y, _x.heading, _x.index, _x.speed, _x.steer, _x.brake, _x.gear, _x.auto_manual,) = _get_struct_3di2fi2h().unpack(str[start:end])
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e)  # most likely buffer underfill


  def serialize_numpy(self, buff, numpy):
    """
    serialize message with numpy array types into buffer
    :param buff: buffer, ``StringIO``
    :param numpy: numpy python module
    """
    try:
      _x = self
      buff.write(_get_struct_3di2fi2h().pack(_x.x, _x.y, _x.heading, _x.index, _x.speed, _x.steer, _x.brake, _x.gear, _x.auto_manual))
    except struct.error as se: self._check_types(struct.error("%s: '%s' when writing '%s'" % (type(se), str(se), str(locals().get('_x', self)))))
    except TypeError as te: self._check_types(ValueError("%s: '%s' when writing '%s'" % (type(te), str(te), str(locals().get('_x', self)))))

  def deserialize_numpy(self, str, numpy):
    """
    unpack serialized message in str into this message instance using numpy for array types
    :param str: byte array of serialized message, ``str``
    :param numpy: numpy python module
    """
    if python3:
      codecs.lookup_error("rosmsg").msg_type = self._type
    try:
      end = 0
      _x = self
      start = end
      end += 44
      (_x.x, _x.y, _x.heading, _x.index, _x.speed, _x.steer, _x.brake, _x.gear, _x.auto_manual,) = _get_struct_3di2fi2h().unpack(str[start:end])
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e)  # most likely buffer underfill

_struct_I = genpy.struct_I
def _get_struct_I():
    global _struct_I
    return _struct_I
_struct_3di2fi2h = None
def _get_struct_3di2fi2h():
    global _struct_3di2fi2h
    if _struct_3di2fi2h is None:
        _struct_3di2fi2h = struct.Struct("<3di2fi2h")
    return _struct_3di2fi2h
