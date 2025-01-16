cmake_minimum_required(VERSION 3.21)

# Set the version
project(QuadratureRules VERSION "{{VERSION}}" LANGUAGES CXX)
include(GNUInstallDirs)

if (WIN32)
    # Windows requires all symbols to be manually exported.
    # This flag exports all symbols automatically, as in Unix.
    set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS TRUE)
endif()

# Source files
add_library(quadraturerules)

# Set the C++ standard
target_compile_features(quadraturerules PUBLIC cxx_std_20)

target_include_directories(quadraturerules PRIVATE ${CMAKE_CURRENT_BINARY_DIR})

set(HEADERS_quadraturerules
  ${CMAKE_CURRENT_SOURCE_DIR}/quadraturerules/quadraturerules.h
  {{for Q in rules}}
  ${CMAKE_CURRENT_SOURCE_DIR}/quadraturerules/{{Q.snake_case_name}}.h
  {{end for}}
)
target_sources(quadraturerules PRIVATE
  ${CMAKE_CURRENT_SOURCE_DIR}/quadraturerules/quadraturerules.cpp
  {{for Q in rules}}
  ${CMAKE_CURRENT_SOURCE_DIR}/quadraturerules/{{Q.snake_case_name}}.cpp
  {{end for}}
)
# Configure the library
set_target_properties(quadraturerules PROPERTIES PUBLIC_HEADER quadraturerules/quadraturerules.h)
set_target_properties(quadraturerules PROPERTIES PRIVATE_HEADER "${HEADERS_quadraturerules}")
target_include_directories(quadraturerules PUBLIC
  $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
  "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR};${CMAKE_CURRENT_SOURCE_DIR}>")

if (UNIX)
    list(APPEND QUADRATURERULES_DEVELOPER_FLAGS -O2;-g;-pipe)
    list(APPEND QUADRATURERULES_COMPILER_FLAGS -Wall;-Werror;-Wextra;-Wno-comment;-pedantic;)
    target_compile_options(quadraturerules PRIVATE "$<$<OR:$<CONFIG:Debug>,$<CONFIG:Developer>>:${QUADRATURERULES_COMPILER_FLAGS}>")
    target_compile_options(quadraturerules PRIVATE $<$<CONFIG:Developer>:${QUADRATURERULES_DEVELOPER_FLAGS}>)
endif()

install(TARGETS quadraturerules
  EXPORT QuadratureRulesTargets
  RUNTIME_DEPENDENCY_SET dependencies
  PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
  PRIVATE_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/quadraturerules
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR} COMPONENT RuntimeExecutables
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR} COMPONENT RuntimeLibraries
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR} COMPONENT Development
)
if (INSTALL_RUNTIME_DEPENDENCIES AND WIN32)
  # https://discourse.cmake.org/t/migration-experiences-comparison-runtime-dependency-set-vs-fixup-bundle-bundleutilities
  install(RUNTIME_DEPENDENCY_SET dependencies DESTINATION ${CMAKE_INSTALL_BINDIR} PRE_EXCLUDE_REGEXES [[api-ms-win-.*]] [[ext-ms-.*]] POST_EXCLUDE_REGEXES [[.*(\\|/)system32(\\|/).*\.dll]])
endif()

# Configure CMake helpers
include(CMakePackageConfigHelpers)
write_basic_package_version_file(QuadratureRulesConfigVersion.cmake VERSION ${PACKAGE_VERSION}
  COMPATIBILITY AnyNewerVersion)
configure_package_config_file(QuadratureRulesConfig.cmake.in ${CMAKE_CURRENT_BINARY_DIR}/QuadratureRulesConfig.cmake
  INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/quadraturerules)

# Install CMake files
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/QuadratureRulesConfig.cmake ${CMAKE_CURRENT_BINARY_DIR}/QuadratureRulesConfigVersion.cmake
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/quadraturerules COMPONENT Development)
install(EXPORT QuadratureRulesTargets FILE QuadratureRulesTargets.cmake NAMESPACE QuadratureRules::
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/quadraturerules)
