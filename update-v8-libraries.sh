#!/bin/bash

V8_SRC_FOLDER="$(sed -n 's/^V8_HOME[ \t]*=[ \t"]*\([^"]*\)["]*/\1/p' ./settings.py | head -1)"

if [[ "${V8_SRC_FOLDER}" == "" ]] || [[ ! -d "${V8_SRC_FOLDER}" ]]; then
    echo
    echo "ERROR!! Nonexistant source folder \"${V8_SRC_FOLDER}\""
    echo
    exit 1
fi

grep -P '^PYV8_DEBUG\s?=\s?True' ./settings.py > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "Copying V8 libraries for DEBUG..."
    cp -v /usr/local/src/v8-compiling-folder/v8/out/x64.debug/obj.target/src/lib*.a              /usr/local/lib/
    cp -v /usr/local/src/v8-compiling-folder/v8/out/x64.debug/obj.target/third_party/icu/lib*.a  /usr/local/lib/
    cp -v /usr/local/src/v8-compiling-folder/v8/out/x64.debug/lib.target/lib*.so                 /usr/local/lib/
    cp -v /usr/local/src/v8-compiling-folder/v8/out/x64.debug/*_blob.bin                         /usr/local/lib/
    cp -v /usr/local/src/v8-compiling-folder/v8/out/x64.debug/icudtl.dat                         /usr/local/lib/
else
    echo "Copying V8 libraries for RELEASE..."
    cp -v /usr/local/src/v8-compiling-folder/v8/out/x64.release/obj.target/src/lib*.a              /usr/local/lib/
    cp -v /usr/local/src/v8-compiling-folder/v8/out/x64.release/obj.target/third_party/icu/lib*.a  /usr/local/lib/
    cp -v /usr/local/src/v8-compiling-folder/v8/out/x64.release/lib.target/lib*.so                 /usr/local/lib/
    cp -v /usr/local/src/v8-compiling-folder/v8/out/x64.release/*_blob.bin                         /usr/local/lib/
    cp -v /usr/local/src/v8-compiling-folder/v8/out/x64.release/icudtl.dat                         /usr/local/lib/
fi

