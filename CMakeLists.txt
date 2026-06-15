cmake_minimum_required(VERSION 3.21)
project(neuroforge_cpp CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# --- pybind11 ---
include(FetchContent)
FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG        v2.12.0
)
FetchContent_MakeAvailable(pybind11)

# --- Google Test (pour les tests C++) ---
FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG        v1.14.0
)
FetchContent_MakeAvailable(googletest)

# --- Sous-modules C++ ---
add_subdirectory(src/cpp/storage)
add_subdirectory(src/cpp/metrics)

# --- Tests C++ ---
enable_testing()
add_subdirectory(tests/cpp)
