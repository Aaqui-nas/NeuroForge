#include <pybind11/pybind11.h>

namespace py = pybind11;

PYBIND11_MODULE(_storage, m) {
    m.doc() = "NeuroForge storage C++ extension (not yet implemented)";
}
