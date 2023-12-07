// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from my_interfaces:srv/TimeReq.idl
// generated code does not contain a copyright notice

#ifndef MY_INTERFACES__SRV__DETAIL__TIME_REQ__STRUCT_H_
#define MY_INTERFACES__SRV__DETAIL__TIME_REQ__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/TimeReq in the package my_interfaces.
typedef struct my_interfaces__srv__TimeReq_Request
{
  uint8_t structure_needs_at_least_one_member;
} my_interfaces__srv__TimeReq_Request;

// Struct for a sequence of my_interfaces__srv__TimeReq_Request.
typedef struct my_interfaces__srv__TimeReq_Request__Sequence
{
  my_interfaces__srv__TimeReq_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} my_interfaces__srv__TimeReq_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'time'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/TimeReq in the package my_interfaces.
typedef struct my_interfaces__srv__TimeReq_Response
{
  rosidl_runtime_c__String time;
} my_interfaces__srv__TimeReq_Response;

// Struct for a sequence of my_interfaces__srv__TimeReq_Response.
typedef struct my_interfaces__srv__TimeReq_Response__Sequence
{
  my_interfaces__srv__TimeReq_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} my_interfaces__srv__TimeReq_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MY_INTERFACES__SRV__DETAIL__TIME_REQ__STRUCT_H_
