// Generated by gencpp from file planner_and_control/Ego.msg
// DO NOT EDIT!


#ifndef PLANNER_AND_CONTROL_MESSAGE_EGO_H
#define PLANNER_AND_CONTROL_MESSAGE_EGO_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace planner_and_control
{
template <class ContainerAllocator>
struct Ego_
{
  typedef Ego_<ContainerAllocator> Type;

  Ego_()
    : x(0.0)
    , y(0.0)
    , heading(0.0)
    , index(0)
    , target_speed(0.0)
    , target_brake(0.0)
    , target_gear(0.0)
    , speed(0.0)
    , steer(0.0)
    , brake(0)
    , gear(0)
    , auto_manual(0)  {
    }
  Ego_(const ContainerAllocator& _alloc)
    : x(0.0)
    , y(0.0)
    , heading(0.0)
    , index(0)
    , target_speed(0.0)
    , target_brake(0.0)
    , target_gear(0.0)
    , speed(0.0)
    , steer(0.0)
    , brake(0)
    , gear(0)
    , auto_manual(0)  {
  (void)_alloc;
    }



   typedef double _x_type;
  _x_type x;

   typedef double _y_type;
  _y_type y;

   typedef double _heading_type;
  _heading_type heading;

   typedef int32_t _index_type;
  _index_type index;

   typedef float _target_speed_type;
  _target_speed_type target_speed;

   typedef float _target_brake_type;
  _target_brake_type target_brake;

   typedef float _target_gear_type;
  _target_gear_type target_gear;

   typedef float _speed_type;
  _speed_type speed;

   typedef float _steer_type;
  _steer_type steer;

   typedef int32_t _brake_type;
  _brake_type brake;

   typedef int16_t _gear_type;
  _gear_type gear;

   typedef int16_t _auto_manual_type;
  _auto_manual_type auto_manual;





  typedef boost::shared_ptr< ::planner_and_control::Ego_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::planner_and_control::Ego_<ContainerAllocator> const> ConstPtr;

}; // struct Ego_

typedef ::planner_and_control::Ego_<std::allocator<void> > Ego;

typedef boost::shared_ptr< ::planner_and_control::Ego > EgoPtr;
typedef boost::shared_ptr< ::planner_and_control::Ego const> EgoConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::planner_and_control::Ego_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::planner_and_control::Ego_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::planner_and_control::Ego_<ContainerAllocator1> & lhs, const ::planner_and_control::Ego_<ContainerAllocator2> & rhs)
{
  return lhs.x == rhs.x &&
    lhs.y == rhs.y &&
    lhs.heading == rhs.heading &&
    lhs.index == rhs.index &&
    lhs.target_speed == rhs.target_speed &&
    lhs.target_brake == rhs.target_brake &&
    lhs.target_gear == rhs.target_gear &&
    lhs.speed == rhs.speed &&
    lhs.steer == rhs.steer &&
    lhs.brake == rhs.brake &&
    lhs.gear == rhs.gear &&
    lhs.auto_manual == rhs.auto_manual;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::planner_and_control::Ego_<ContainerAllocator1> & lhs, const ::planner_and_control::Ego_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace planner_and_control

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::planner_and_control::Ego_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::planner_and_control::Ego_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::planner_and_control::Ego_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::planner_and_control::Ego_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::planner_and_control::Ego_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::planner_and_control::Ego_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::planner_and_control::Ego_<ContainerAllocator> >
{
  static const char* value()
  {
    return "0869400e66da0a77dc77cb9c63aed1a9";
  }

  static const char* value(const ::planner_and_control::Ego_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x0869400e66da0a77ULL;
  static const uint64_t static_value2 = 0xdc77cb9c63aed1a9ULL;
};

template<class ContainerAllocator>
struct DataType< ::planner_and_control::Ego_<ContainerAllocator> >
{
  static const char* value()
  {
    return "planner_and_control/Ego";
  }

  static const char* value(const ::planner_and_control::Ego_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::planner_and_control::Ego_<ContainerAllocator> >
{
  static const char* value()
  {
    return "float64 x\n"
"float64 y\n"
"float64 heading\n"
"int32 index\n"
"float32 target_speed\n"
"float32 target_brake\n"
"float32 target_gear\n"
"float32 speed\n"
"float32 steer\n"
"int32 brake\n"
"int16 gear\n"
"int16 auto_manual\n"
;
  }

  static const char* value(const ::planner_and_control::Ego_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::planner_and_control::Ego_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.x);
      stream.next(m.y);
      stream.next(m.heading);
      stream.next(m.index);
      stream.next(m.target_speed);
      stream.next(m.target_brake);
      stream.next(m.target_gear);
      stream.next(m.speed);
      stream.next(m.steer);
      stream.next(m.brake);
      stream.next(m.gear);
      stream.next(m.auto_manual);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct Ego_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::planner_and_control::Ego_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::planner_and_control::Ego_<ContainerAllocator>& v)
  {
    s << indent << "x: ";
    Printer<double>::stream(s, indent + "  ", v.x);
    s << indent << "y: ";
    Printer<double>::stream(s, indent + "  ", v.y);
    s << indent << "heading: ";
    Printer<double>::stream(s, indent + "  ", v.heading);
    s << indent << "index: ";
    Printer<int32_t>::stream(s, indent + "  ", v.index);
    s << indent << "target_speed: ";
    Printer<float>::stream(s, indent + "  ", v.target_speed);
    s << indent << "target_brake: ";
    Printer<float>::stream(s, indent + "  ", v.target_brake);
    s << indent << "target_gear: ";
    Printer<float>::stream(s, indent + "  ", v.target_gear);
    s << indent << "speed: ";
    Printer<float>::stream(s, indent + "  ", v.speed);
    s << indent << "steer: ";
    Printer<float>::stream(s, indent + "  ", v.steer);
    s << indent << "brake: ";
    Printer<int32_t>::stream(s, indent + "  ", v.brake);
    s << indent << "gear: ";
    Printer<int16_t>::stream(s, indent + "  ", v.gear);
    s << indent << "auto_manual: ";
    Printer<int16_t>::stream(s, indent + "  ", v.auto_manual);
  }
};

} // namespace message_operations
} // namespace ros

#endif // PLANNER_AND_CONTROL_MESSAGE_EGO_H
