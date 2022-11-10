# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "final_pkg: 1 messages, 0 services")

set(MSG_I_FLAGS "-Ifinal_pkg:/home/gigacha/TEAM-GIGACHA/src/final_pkg/msg;-Istd_msgs:/opt/ros/melodic/share/std_msgs/cmake/../msg;-Igeometry_msgs:/opt/ros/melodic/share/geometry_msgs/cmake/../msg;-Ifinal_pkg:/home/gigacha/TEAM-GIGACHA/src/final_pkg/msg;-Ilocal_pkg:/home/gigacha/TEAM-GIGACHA/src/local_pkg/msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(final_pkg_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/final_pkg/msg/Perception.msg" NAME_WE)
add_custom_target(_final_pkg_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "final_pkg" "/home/gigacha/TEAM-GIGACHA/src/final_pkg/msg/Perception.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(final_pkg
  "/home/gigacha/TEAM-GIGACHA/src/final_pkg/msg/Perception.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/final_pkg
)

### Generating Services

### Generating Module File
_generate_module_cpp(final_pkg
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/final_pkg
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(final_pkg_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(final_pkg_generate_messages final_pkg_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/final_pkg/msg/Perception.msg" NAME_WE)
add_dependencies(final_pkg_generate_messages_cpp _final_pkg_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(final_pkg_gencpp)
add_dependencies(final_pkg_gencpp final_pkg_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS final_pkg_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(final_pkg
  "/home/gigacha/TEAM-GIGACHA/src/final_pkg/msg/Perception.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/final_pkg
)

### Generating Services

### Generating Module File
_generate_module_eus(final_pkg
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/final_pkg
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(final_pkg_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(final_pkg_generate_messages final_pkg_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/final_pkg/msg/Perception.msg" NAME_WE)
add_dependencies(final_pkg_generate_messages_eus _final_pkg_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(final_pkg_geneus)
add_dependencies(final_pkg_geneus final_pkg_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS final_pkg_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(final_pkg
  "/home/gigacha/TEAM-GIGACHA/src/final_pkg/msg/Perception.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/final_pkg
)

### Generating Services

### Generating Module File
_generate_module_lisp(final_pkg
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/final_pkg
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(final_pkg_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(final_pkg_generate_messages final_pkg_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/final_pkg/msg/Perception.msg" NAME_WE)
add_dependencies(final_pkg_generate_messages_lisp _final_pkg_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(final_pkg_genlisp)
add_dependencies(final_pkg_genlisp final_pkg_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS final_pkg_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(final_pkg
  "/home/gigacha/TEAM-GIGACHA/src/final_pkg/msg/Perception.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/final_pkg
)

### Generating Services

### Generating Module File
_generate_module_nodejs(final_pkg
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/final_pkg
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(final_pkg_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(final_pkg_generate_messages final_pkg_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/final_pkg/msg/Perception.msg" NAME_WE)
add_dependencies(final_pkg_generate_messages_nodejs _final_pkg_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(final_pkg_gennodejs)
add_dependencies(final_pkg_gennodejs final_pkg_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS final_pkg_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(final_pkg
  "/home/gigacha/TEAM-GIGACHA/src/final_pkg/msg/Perception.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/final_pkg
)

### Generating Services

### Generating Module File
_generate_module_py(final_pkg
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/final_pkg
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(final_pkg_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(final_pkg_generate_messages final_pkg_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/final_pkg/msg/Perception.msg" NAME_WE)
add_dependencies(final_pkg_generate_messages_py _final_pkg_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(final_pkg_genpy)
add_dependencies(final_pkg_genpy final_pkg_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS final_pkg_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/final_pkg)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/final_pkg
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(final_pkg_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()
if(TARGET geometry_msgs_generate_messages_cpp)
  add_dependencies(final_pkg_generate_messages_cpp geometry_msgs_generate_messages_cpp)
endif()
if(TARGET final_pkg_generate_messages_cpp)
  add_dependencies(final_pkg_generate_messages_cpp final_pkg_generate_messages_cpp)
endif()
if(TARGET local_pkg_generate_messages_cpp)
  add_dependencies(final_pkg_generate_messages_cpp local_pkg_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/final_pkg)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/final_pkg
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(final_pkg_generate_messages_eus std_msgs_generate_messages_eus)
endif()
if(TARGET geometry_msgs_generate_messages_eus)
  add_dependencies(final_pkg_generate_messages_eus geometry_msgs_generate_messages_eus)
endif()
if(TARGET final_pkg_generate_messages_eus)
  add_dependencies(final_pkg_generate_messages_eus final_pkg_generate_messages_eus)
endif()
if(TARGET local_pkg_generate_messages_eus)
  add_dependencies(final_pkg_generate_messages_eus local_pkg_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/final_pkg)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/final_pkg
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(final_pkg_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()
if(TARGET geometry_msgs_generate_messages_lisp)
  add_dependencies(final_pkg_generate_messages_lisp geometry_msgs_generate_messages_lisp)
endif()
if(TARGET final_pkg_generate_messages_lisp)
  add_dependencies(final_pkg_generate_messages_lisp final_pkg_generate_messages_lisp)
endif()
if(TARGET local_pkg_generate_messages_lisp)
  add_dependencies(final_pkg_generate_messages_lisp local_pkg_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/final_pkg)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/final_pkg
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(final_pkg_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()
if(TARGET geometry_msgs_generate_messages_nodejs)
  add_dependencies(final_pkg_generate_messages_nodejs geometry_msgs_generate_messages_nodejs)
endif()
if(TARGET final_pkg_generate_messages_nodejs)
  add_dependencies(final_pkg_generate_messages_nodejs final_pkg_generate_messages_nodejs)
endif()
if(TARGET local_pkg_generate_messages_nodejs)
  add_dependencies(final_pkg_generate_messages_nodejs local_pkg_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/final_pkg)
  install(CODE "execute_process(COMMAND \"/usr/bin/python2\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/final_pkg\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/final_pkg
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(final_pkg_generate_messages_py std_msgs_generate_messages_py)
endif()
if(TARGET geometry_msgs_generate_messages_py)
  add_dependencies(final_pkg_generate_messages_py geometry_msgs_generate_messages_py)
endif()
if(TARGET final_pkg_generate_messages_py)
  add_dependencies(final_pkg_generate_messages_py final_pkg_generate_messages_py)
endif()
if(TARGET local_pkg_generate_messages_py)
  add_dependencies(final_pkg_generate_messages_py local_pkg_generate_messages_py)
endif()
