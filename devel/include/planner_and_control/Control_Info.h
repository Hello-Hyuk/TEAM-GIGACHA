// Generated by gencpp from file planner_and_control/Control_Info.msg
// DO NOT EDIT!


#ifndef PLANNER_AND_CONTROL_MESSAGE_CONTROL_INFO_H
#define PLANNER_AND_CONTROL_MESSAGE_CONTROL_INFO_H


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
struct Control_Info_
{
  typedef Control_Info_<ContainerAllocator> Type;

  Control_Info_()
    : emergency_stop(0)
    , gear(0)
    , speed(0.0)
    , steer(0.0)
    , brake(0)  {
    }
  Control_Info_(const ContainerAllocator& _alloc)
    : emergency_stop(0)
    , gear(0)
    , speed(0.0)
    , steer(0.0)
    , brake(0)  {
  (void)_alloc;
    }



   typedef int16_t _emergency_stop_type;
  _emergency_stop_type emergency_stop;

   typedef int16_t _gear_type;
  _gear_type gear;

   typedef float _speed_type;
  _speed_type speed;

   typedef float _steer_type;
  _steer_type steer;

   typedef int16_t _brake_type;
  _brake_type brake;





  typedef boost::shared_ptr< ::planner_and_control::Control_Info_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::planner_and_control::Control_Info_<ContainerAllocator> const> ConstPtr;

}; // struct Control_Info_

typedef ::planner_and_control::Control_Info_<std::allocator<void> > Control_Info;

typedef boost::shared_ptr< ::planner_and_control::Control_Info > Control_InfoPtr;
typedef boost::shared_ptr< ::planner_and_control::Control_Info const> Control_InfoConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::planner_and_control::Control_Info_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::planner_and_control::Control_Info_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::planner_and_control::Control_Info_<ContainerAllocator1> & lhs, const ::planner_and_control::Control_Info_<ContainerAllocator2> & rhs)
{
  return lhs.emergency_stop == rhs.emergency_stop &&
    lhs.gear == rhs.gear &&
    lhs.speed == rhs.speed &&
    lhs.steer == rhs.steer &&
    lhs.brake == rhs.brake;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::planner_and_control::Control_Info_<ContainerAllocator1> & lhs, const ::planner_and_control::Control_Info_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace planner_and_control

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::planner_and_control::Control_Info_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::planner_and_control::Control_Info_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::planner_and_control::Control_Info_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::planner_and_control::Control_Info_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::planner_and_control::Control_Info_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::planner_and_control::Control_Info_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::planner_and_control::Control_Info_<ContainerAllocator> >
{
  static const char* value()
  {
    return "3dc9a678baa6090d119c5483385b8223";
  }

  static const char* value(const ::planner_and_control::Control_Info_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x3dc9a678baa6090dULL;
  static const uint64_t static_value2 = 0x119c5483385b8223ULL;
};

template<class ContainerAllocator>
struct DataType< ::planner_and_control::Control_Info_<ContainerAllocator> >
{
  static const char* value()
  {
    return "planner_and_control/Control_Info";
  }

  static const char* value(const ::planner_and_control::Control_Info_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::planner_and_control::Control_Info_<ContainerAllocator> >
{
  static const char* value()
  {
    return "int16 emergency_stop\n"
"int16 gear\n"
"float32 speed\n"
"float32 steer\n"
"int16 brake\n"
;
  }

  static const char* value(const ::planner_and_control::Control_Info_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::planner_and_control::Control_Info_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.emergency_stop);
      stream.next(m.gear);
      stream.next(m.speed);
      stream.next(m.steer);
      stream.next(m.brake);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct Control_Info_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::planner_and_control::Control_Info_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::planner_and_control::Control_Info_<ContainerAllocator>& v)
  {
    s << indent << "emergency_stop: ";
    Printer<int16_t>::stream(s, indent + "  ", v.emergency_stop);
    s << indent << "gear: ";
    Printer<int16_t>::stream(s, indent + "  ", v.gear);
    s << indent << "speed: ";
    Printer<float>::stream(s, indent + "  ", v.speed);
    s << indent << "steer: ";
    Printer<float>::stream(s, indent + "  ", v.steer);
    s << indent << "brake: ";
    Printer<int16_t>::stream(s, indent + "  ", v.brake);
  }
};

} // namespace message_operations
} // namespace ros

#endif // PLANNER_AND_CONTROL_MESSAGE_CONTROL_INFO_H