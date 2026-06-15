pybind11_add_module(_storage
    bindings.cpp
    # src/object_store.cpp  <- a ajouter lors de la phase 3
)

target_include_directories(_storage PRIVATE include)
target_compile_options(_storage PRIVATE -Wall -Wextra)

# Placer le .so dans le package Python storage
set_target_properties(_storage PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/src/neuroforge/storage"
)
