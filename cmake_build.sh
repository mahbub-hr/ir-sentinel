#!/bin/bash
#
# @author mahbub
# 
# This script expect that it is inside the script directory under
# the root directory of the project

set -e 

PROJECT_ROOT=$(pwd)
BUILD_DIR="$PROJECT_ROOT/build"

if [[ ! -d "$BUILD_DIR" ]]; then
    mkdir -p $BUILD_DIR
fi

cd $BUILD_DIR

cmake .. -G Ninja \
    -DCMAKE_TOOLCHAIN_FILE=/work/vcpkg/scripts/buildsystems/vcpkg.cmake \
    -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_C_COMPILER="/opt/llvm-22/bin/clang" \
    -DCMAKE_CXX_COMPILER="/opt/llvm-22/bin/clang++" \
    -DLLVM_DIR=/opt/llvm-22/lib/cmake/llvm \
    -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

ninja