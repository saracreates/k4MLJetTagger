#[[
Copyright (c) 2020-2024 Key4hep-Project.

This file is part of Key4hep.
See https://key4hep.github.io/key4hep-doc/ for further info.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
]]
CMAKE_MINIMUM_REQUIRED(VERSION 3.12)


project(k4MLJetTagger)

# please keep this layout for version setting, used by the automatic tagging script
set(PACKAGE_VERSION_MAJOR 1)
set(PACKAGE_VERSION_MINOR 2)
set(PACKAGE_VERSION_PATCH 3)

set(PACKAGE_VERSION "${PACKAGE_VERSION_MAJOR}.${PACKAGE_VERSION_MINOR}.${PACKAGE_VERSION_PATCH}")

# dependencies are declared like this

# For some reason, the find_package with DD4hep must be the first one
find_package(DD4hep REQUIRED COMPONENTS DDRec DDG4 DDParsers)
# dd4hep_set_compiler_flags() expects DD4hep_SET_RPATH to be set to ON
# otherwise it will not set the rpath when installing
set(DD4HEP_SET_RPATH ON)

find_package(ROOT COMPONENTS RIO Tree)
find_package(EDM4HEP)
find_package(k4FWCore)
find_package(Gaudi)

# make sure the onnx find script is found:
set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)
find_package(onnxruntime REQUIRED)
if(onnxruntime_FOUND)
  message("ONNX Runtime inference library found.")
else()
  message("ONNX Runtime not found!")
endif()

#---------------------------------------------------------------

include(cmake/Key4hepConfig.cmake)

include(GNUInstallDirs)

include(CTest)

add_subdirectory(k4MLJetTagger)
add_subdirectory(tests)

include(cmake/CreateProjectConfig.cmake)


