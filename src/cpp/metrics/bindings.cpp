#include <pybind11/pybind11.h>

namespace py = pybind11;

PYBIND11_MODULE(_metrics, m) {
    m.doc() = "NeuroForge metrics C++ extension (not yet implemented)";
}
