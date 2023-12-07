// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from my_interfaces:srv/TimeReq.idl
// generated code does not contain a copyright notice

#ifndef MY_INTERFACES__SRV__DETAIL__TIME_REQ__BUILDER_HPP_
#define MY_INTERFACES__SRV__DETAIL__TIME_REQ__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "my_interfaces/srv/detail/time_req__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace my_interfaces
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_interfaces::srv::TimeReq_Request>()
{
  return ::my_interfaces::srv::TimeReq_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace my_interfaces


namespace my_interfaces
{

namespace srv
{

namespace builder
{

class Init_TimeReq_Response_time
{
public:
  Init_TimeReq_Response_time()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::my_interfaces::srv::TimeReq_Response time(::my_interfaces::srv::TimeReq_Response::_time_type arg)
  {
    msg_.time = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_interfaces::srv::TimeReq_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_interfaces::srv::TimeReq_Response>()
{
  return my_interfaces::srv::builder::Init_TimeReq_Response_time();
}

}  // namespace my_interfaces

#endif  // MY_INTERFACES__SRV__DETAIL__TIME_REQ__BUILDER_HPP_
