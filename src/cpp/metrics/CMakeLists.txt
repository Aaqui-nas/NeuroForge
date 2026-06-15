pybind11_add_module(_metrics
    bindings.cpp
    # src/ring_buffer.cpp  <- a ajouter lors de la phase 4
)

target_include_directories(_metrics PRIVATE include)
target_compile_options(_metrics PRIVATE -Wall -Wextra)

set_target_properties(_metrics PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/src/neuroforge/training"
)
