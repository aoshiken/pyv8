#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import PyV8

print "\nPyV8.JSEngine.version %s\n" % PyV8.JSEngine.version
print "PyV8.JSLocker.active %s\n" % PyV8.JSLocker.active
print "PyV8.JSLocker.locked %s\n" % PyV8.JSLocker.locked

with PyV8.JSLocker() as outter_locker:
    print "PyV8.JSLocker.active %s\n" % PyV8.JSLocker.active
    print "PyV8.JSLocker.locked %s\n" % PyV8.JSLocker.locked

class Global:
    result = []

    def add(self, value):
        with PyV8.JSUnlocker():
            time.sleep(0.1)

            self.result.append(value)

g = Global()

def run():
    print("Trying RUN before PyV8.JSContext...")
    with PyV8.JSContext(g) as ctxt:
        print("Inside RUN just before EVAL...")
        ctxt.eval("for (i=0; i<10; i++) add(i);")

threads = [threading.Thread(target=run)]#, threading.Thread(target=run)]

with PyV8.JSLocker():
    for t in threads: t.start()

for t in threads: t.join()

if len(g.result) != 10:
    print('ERROR!! Result must be 10 but is %s' % len(g.result))
else:
    print('SUCCESS!!')
