cmake_minimum_required(VERSION 3.16)
project(IR-Sentinel)

if (NOT "${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")
    message(FATAL_ERROR "Please use Clang to compile IslevSM. Detected: ${CMAKE_CXX_COMPILER_ID}")
endif()

set(C_STANDARD 11)
set(CMAKE_CXX_STANDARD 20)
set(ISLEVSM_PROJECT_ROOT ${CMAKE_CURRENT_LIST_DIR})

find_package(LLVM 22 REQUIRED CONFIG)
include_directories(${LLVM_INCLUDE_DIRS})
separate_arguments(LLVM_DEFINITIONS_LIST NATIVE_COMMAND ${LLVM_DEFINITIONS})
add_definitions(${LLVM_DEFINITIONS_LIST})

message(STATUS "LLVM VERSION: ${LLVM_PACKAGE_VERSION}")
message(STATUS "LLVM DIR: ${LLVM_DIR}")

llvm_map_components_to_libnames(llvm_libs 
    Support Core Passes
)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -frtti")


add_library(stats_collector SHARED
    cpp/stats_collector.cpp
)