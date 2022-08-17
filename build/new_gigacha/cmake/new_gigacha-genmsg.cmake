# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "new_gigacha: 1 messages, 0 services")

set(MSG_I_FLAGS "-Inew_gigacha:/home/gigacha/TEAM-GIGACHA/src/new_gigacha/msg;-Istd_msgs:/opt/ros/melodic/share/std_msgs/cmake/../msg;-Igeometry_msgs:/opt/ros/melodic/share/geometry_msgs/cmake/../msg;-Inew_gigacha:/home/gigacha/TEAM-GIGACHA/src/new_gigacha/msg;-Ilocal_pkg:/home/gigacha/TEAM-GIGACHA/src/local_pkg/msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(new_gigacha_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/new_gigacha/msg/Perception.msg" NAME_WE)
add_custom_target(_new_gigacha_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "new_gigacha" "/home/gigacha/TEAM-GIGACHA/src/new_gigacha/msg/Perception.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(new_gigacha
  "/home/gigacha/TEAM-GIGACHA/src/new_gigacha/msg/Perception.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/new_gigacha
)

### Generating Services

### Generating Module File
_generate_module_cpp(new_gigacha
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/new_gigacha
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(new_gigacha_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(new_gigacha_generate_messages new_gigacha_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/new_gigacha/msg/Perception.msg" NAME_WE)
add_dependencies(new_gigacha_generate_messages_cpp _new_gigacha_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(new_gigacha_gencpp)
add_dependencies(new_gigacha_gencpp new_gigacha_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS new_gigacha_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(new_gigacha
  "/home/gigacha/TEAM-GIGACHA/src/new_gigacha/msg/Perception.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/new_gigacha
)

### Generating Services

### Generating Module File
_generate_module_eus(new_gigacha
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/new_gigacha
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(new_gigacha_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(new_gigacha_generate_messages new_gigacha_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/new_gigacha/msg/Perception.msg" NAME_WE)
add_dependencies(new_gigacha_generate_messages_eus _new_gigacha_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(new_gigacha_geneus)
add_dependencies(new_gigacha_geneus new_gigacha_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS new_gigacha_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(new_gigacha
  "/home/gigacha/TEAM-GIGACHA/src/new_gigacha/msg/Perception.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/new_gigacha
)

### Generating Services

### Generating Module File
_generate_module_lisp(new_gigacha
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/new_gigacha
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(new_gigacha_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(new_gigacha_generate_messages new_gigacha_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/new_gigacha/msg/Perception.msg" NAME_WE)
add_dependencies(new_gigacha_generate_messages_lisp _new_gigacha_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(new_gigacha_genlisp)
add_dependencies(new_gigacha_genlisp new_gigacha_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS new_gigacha_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(new_gigacha
  "/home/gigacha/TEAM-GIGACHA/src/new_gigacha/msg/Perception.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/new_gigacha
)

### Generating Services

### Generating Module File
_generate_module_nodejs(new_gigacha
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/new_gigacha
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(new_gigacha_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(new_gigacha_generate_messages new_gigacha_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/new_gigacha/msg/Perception.msg" NAME_WE)
add_dependencies(new_gigacha_generate_messages_nodejs _new_gigacha_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(new_gigacha_gennodejs)
add_dependencies(new_gigacha_gennodejs new_gigacha_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS new_gigacha_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(new_gigacha
  "/home/gigacha/TEAM-GIGACHA/src/new_gigacha/msg/Perception.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/new_gigacha
)

### Generating Services

### Generating Module File
_generate_module_py(new_gigacha
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/new_gigacha
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(new_gigacha_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(new_gigacha_generate_messages new_gigacha_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/gigacha/TEAM-GIGACHA/src/new_gigacha/msg/Perception.msg" NAME_WE)
add_dependencies(new_gigacha_generate_messages_py _new_gigacha_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(new_gigacha_genpy)
add_dependencies(new_gigacha_genpy new_gigacha_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS new_gigacha_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/new_gigacha)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/new_gigacha
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(new_gigacha_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()
if(TARGET geometry_msgs_generate_messages_cpp)
  add_dependencies(new_gigacha_generate_messages_cpp geometry_msgs_generate_messages_cpp)
endif()
if(TARGET new_gigacha_generate_messages_cpp)
  add_dependencies(new_gigacha_generate_messages_cpp new_gigacha_generate_messages_cpp)
endif()
if(TARGET local_pkg_generate_messages_cpp)
  add_dependencies(new_gigacha_generate_messages_cpp local_pkg_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/new_gigacha)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/new_gigacha
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(new_gigacha_generate_messages_eus std_msgs_generate_messages_eus)
endif()
if(TARGET geometry_msgs_generate_messages_eus)
  add_dependencies(new_gigacha_generate_messages_eus geometry_msgs_generate_messages_eus)
endif()
if(TARGET new_gigacha_generate_messages_eus)
  add_dependencies(new_gigacha_generate_messages_eus new_gigacha_generate_messages_eus)
endif()
if(TARGET local_pkg_generate_messages_eus)
  add_dependencies(new_gigacha_generate_messages_eus local_pkg_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/new_gigacha)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/new_gigacha
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(new_gigacha_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()
if(TARGET geometry_msgs_generate_messages_lisp)
  add_dependencies(new_gigacha_generate_messages_lisp geometry_msgs_generate_messages_lisp)
endif()
if(TARGET new_gigacha_generate_messages_lisp)
  add_dependencies(new_gigacha_generate_messages_lisp new_gigacha_generate_messages_lisp)
endif()
if(TARGET local_pkg_generate_messages_lisp)
  add_dependencies(new_gigacha_generate_messages_lisp local_pkg_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/new_gigacha)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/new_gigacha
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(new_gigacha_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()
if(TARGET geometry_msgs_generate_messages_nodejs)
  add_dependencies(new_gigacha_generate_messages_nodejs geometry_msgs_generate_messages_nodejs)
endif()
if(TARGET new_gigacha_generate_messages_nodejs)
  add_dependencies(new_gigacha_generate_messages_nodejs new_gigacha_generate_messages_nodejs)
endif()
if(TARGET local_pkg_generate_messages_nodejs)
  add_dependencies(new_gigacha_generate_messages_nodejs local_pkg_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/new_gigacha)
  install(CODE "execute_process(COMMAND \"/usr/bin/python2\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/new_gigacha\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/new_gigacha
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(new_gigacha_generate_messages_py std_msgs_generate_messages_py)
endif()
if(TARGET geometry_msgs_generate_messages_py)
  add_dependencies(new_gigacha_generate_messages_py geometry_msgs_generate_messages_py)
endif()
if(TARGET new_gigacha_generate_messages_py)
  add_dependencies(new_gigacha_generate_messages_py new_gigacha_generate_messages_py)
endif()
if(TARGET local_pkg_generate_messages_py)
  add_dependencies(new_gigacha_generate_messages_py local_pkg_generate_messages_py)
endif()
