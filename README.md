## DISCLAIMER
The following instructions have been tested on Debian Stretch x64 **ONLY**, YMMV.

The PyV8 library has been built with the following assumptions:
- The Google "depot tools" used for setup V8 will be cloned under the folder `/usr/local/src/depot_tools`
- The Google V8 repository will be cloned under the folder `/usr/local/src/v8-compiling-folder/v8`
- This PyV8 repository will be cloned into `/usr/local/src/pyv8`
- PyV8 will be built with Python2


### APT PACKAGES
```
# apt-get install python-dev git g++ gcc libboost-dev libboost-system-dev libboost-python-dev libboost-filesystem-dev libboost-log-dev libboost-regex-dev libboost-thread-dev libboost-timer-dev libboost-serialization-dev libboost-iostreams-dev libboost-atomic-dev libboost-chrono-dev
```


### HOW TO BUILD THE V8 LIBRARIES

Clone the "depot tools" repository and add it to the path:
```
root@dev-x64:/usr/local/src# git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
root@dev-x64:/usr/local/src#
root@dev-x64:/usr/local/src# export PATH=$PATH:/usr/local/src/depot_tools
```

Create the V8 compiling folder and clone the V8 repository using the `depot_tools`:
```
root@dev-x64:/usr/local/src# mkdir v8-compiling-folder
root@dev-x64:/usr/local/src# cd v8-compiling-folder/
root@dev-x64:/usr/local/src/v8-compiling-folder# fetch v8
Running: gclient root
[...]
Running hooks: 100% (32/32), done.
Running: git submodule foreach 'git config -f $toplevel/.git/config submodule.$name.ignore all'
Running: git config --add remote.origin.fetch '+refs/tags/*:refs/tags/*'
Running: git config diff.ignoreSubmodules all
```

Now that we have the V8 repository cloned we'll use the 5.8.110 revision (according to the PyV8 `settings.py` file that was the latest version tested):
```
root@dev-x64:/usr/local/src/v8-compiling-folder# cd v8/
root@dev-x64:/usr/local/src/v8-compiling-folder/v8# git checkout 5.8.110
Previous HEAD position was 63ca293dcf... Remove PersistentContainerCallbackType::kWeak
HEAD is now at 5dd3abff9a... Version 5.8.110
```

We'll update the V8 dependencies according to our choosed version
```
root@dev-x64:/usr/local/src/v8-compiling-folder/v8# gclient sync
Running depot tools as root is sad.
Syncing projects: 100% (21/21), done.
[...]
GYP is now disabled by default in runhooks.

If you really want to run this, either run
`python gypfiles/gyp_v8` explicitly by hand
or set the environment variable GYP_CHROMIUM_NO_ACTION=0.
Running hooks: 100% (22/22), done.
root@dev-x64:/usr/local/src/v8-compiling-folder/v8#
root@dev-x64:/usr/local/src/v8-compiling-folder/v8# python gypfiles/gyp_v8
Updating projects from gyp files...
```

We can finally compile V8 as Release for platform x64:
```
root@dev-x64:/usr/local/src/v8-compiling-folder/v8# make x64.release -j4 werror=no
[...]
  LINK(target) /usr/local/src/v8-compiling-folder/v8/out/x64.release/unittests
  TOUCH /usr/local/src/v8-compiling-folder/v8/out/x64.release/obj.target/gypfiles/All.stamp
make[1]: Leaving directory '/usr/local/src/v8-compiling-folder/v8/out'
root@dev-x64:/usr/local/src/v8-compiling-folder/v8#
```

V8 provides some binaries for testing, a minimal test follows:
```
root@dev-x64:/usr/local/src/v8-compiling-folder/v8# out/x64.release/v8_shell
V8 version 5.8.110 [sample shell]
> i=50
50
> i+1
51
>
```

Arrived here our V8 v5.8.110 engine has been correctly built and tested but we need it as a shared library for being used from PyV8.
Let's compile it:
```
root@dev-x64:/usr/local/src/v8-compiling-folder/v8# make x64.release -j4 library=shared werror=no
[...]
  LINK(target) /usr/local/src/v8-compiling-folder/v8/out/x64.release/unittests
  TOUCH /usr/local/src/v8-compiling-folder/v8/out/x64.release/obj.target/gypfiles/All.stamp
make[1]: Leaving directory '/usr/local/src/v8-compiling-folder/v8/out'
root@dev-x64:/usr/local/src/v8-compiling-folder/v8#
root@dev-x64:/usr/local/src/v8-compiling-folder/v8# out/x64.release/v8_shell
V8 version 5.8.110 [sample shell]
> i=50
50
> i+1
51
>
root@dev-x64:/usr/local/src/v8-compiling-folder/v8#
root@dev-x64:/usr/local/src/v8-compiling-folder/v8# ls -l out/x64.release/lib.target/
-rwxr-xr-x 2 root root  3392288 Oct 17 17:14 libicui18n.so
-rwxr-xr-x 2 root root  2056568 Oct 17 17:14 libicuuc.so
-rwxr-xr-x 2 root root   118376 Oct 17 17:14 libv8_libbase.so
-rwxr-xr-x 2 root root    90560 Oct 17 17:14 libv8_libplatform.so
-rwxr-xr-x 2 root root 19107152 Oct 17 17:23 libv8.so
```

Copy the header files needed for compilation of external programs/libraries (like PyV8):
```
root@dev-x64:/usr/local/src/v8-compiling-folder/v8# cp -vR include/* /usr/include/
```

...the libraries...
```
root@dev-x64:/usr/local/src/v8-compiling-folder/v8# cp -v out/x64.release/lib.target/lib*.so /usr/local/lib/
root@dev-x64:/usr/local/src/v8-compiling-folder/v8# cp -v out/x64.release/obj.target/src/lib*.a /usr/local/lib/
root@dev-x64:/usr/local/src/v8-compiling-folder/v8# cp -v out/x64.release/obj.target/third_party/icu/lib*.a /usr/local/lib/
root@dev-x64:/usr/local/src/v8-compiling-folder/v8# ldconfig -v
```

...and the JS natives...
```
root@dev-x64:/usr/local/src/v8-compiling-folder/v8# cp -v out/x64.release/natives_blob.bin /usr/local/lib
root@dev-x64:/usr/local/src/v8-compiling-folder/v8# cp -v out/x64.release/snapshot_blob.bin /usr/local/lib
root@dev-x64:/usr/local/src/v8-compiling-folder/v8# cp -v out/x64.release/icudtl.dat /usr/local/lib
```

### BUILD AND INSTALL PYV8

The usual way...
```
root@dev-x64:/usr/local/src/pyv8# python setup.py clean && python setup.py build && python setup.py install
```

Minimal test1:
```
root@dev-x64:/usr/local/src/pyv8# cd /tmp ; python /usr/local/src/pyv8/demos/helloworld.py ; cd -
Hello World
/usr/local/src/pyv8
```

Minimal test2:
```
root@dev-x64:/usr/local/src/pyv8# cd ..
root@dev-x64:/usr/local/src# python
Python 2.7.13 (default, Nov 24 2017, 17:33:09)
[GCC 6.3.0 20170516] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import PyV8
>>> with PyV8.JSContext() as ctxt:
...     with PyV8.JSEngine() as engine:
...         s = engine.compile("1+2")
...         s.run()
...
3
```
