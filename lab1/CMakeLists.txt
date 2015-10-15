cmake_minimum_required(VERSION 3.2)
project(lab1)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES predicates.c main.cpp utils.cpp generate_points.cpp)
set(HEADER_FILES predicates.h utils.h generate_points.h)
add_executable(lab1 ${SOURCE_FILES})