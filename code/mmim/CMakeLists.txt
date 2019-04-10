cmake_minimum_required(VERSION 3.0.0)
project(chuffed CXX C)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_executable(mingap 
    algorithms.cpp  computation.cpp  graph.cpp  
    greedy.cpp  main.cpp  print.cpp  simulation.cpp)
