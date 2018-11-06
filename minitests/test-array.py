#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import PyV8

with PyV8.JSContext() as ctxt:
    array = ctxt.eval("""
                var array = new Array();

                for (i=0; i<10; i++)
                {
                    array[i] = 10-i;
                }

                array;
                """)
    array[5] = 0

    del array[5]

    array[1:3] = [9, 9, 9]

    array[5:8] = [8, 8]

    print("Array5 = [%s]" % array)

    if [10, 9, 9, 9, 7, 8, 8, 3, 2, 1] != list(array):
        print('ERROR!! [10, 9, 9, 9, 7, 8, 8, 3, 2, 1] != %s' % list(array))
        sys.exit(1)

    del array[1:4]

    if [10, 7, 8, 8, 3, 2, 1] != list(array):
        print('ERROR22!')
        sys.exit(1)

    ctxt.locals.array1 = PyV8.JSArray(5)
    ctxt.locals.array2 = PyV8.JSArray([1, 2, 3, 4, 5])

    for i in range(len(ctxt.locals.array2)):
        ctxt.locals.array1[i] = ctxt.locals.array2[i] * 10

    ctxt.eval("""
        var sum = 0;

        for (i=0; i<array1.length; i++)
            sum += array1[i]

        for (i=0; i<array2.length; i++)
            sum += array2[i]
        """)

    if 165 != ctxt.locals.sum:
        print('ERROR33!!')
        sys.exit(1)
    ctxt.locals.array3 = [1, 2, 3, 4, 5]

    if ctxt.eval('array3[1] === 2') is not True:
        print('ERROR44')
        sys.exit(1)

    if ctxt.eval('array3[9] === undefined') is not True:
        print('ERROR55')
        sys.exit(1)

    args = [
        ["a = Array(7); for(i=0; i<a.length; i++) a[i] = i; a[3] = undefined; a[a.length-1]; a", "0,1,2,,4,5,6", [0, 1, 2, None, 4, 5, 6]],
        ["a = Array(7); for(i=0; i<a.length - 1; i++) a[i] = i; a[a.length-1]; a", "0,1,2,3,4,5,", [0, 1, 2, 3, 4, 5, None]],
        ["a = Array(7); for(i=1; i<a.length; i++) a[i] = i; a[a.length-1]; a", ",1,2,3,4,5,6", [None, 1, 2, 3, 4, 5, 6]]
    ]

    for arg in args:
        array = ctxt.eval(arg[0])

        if arg[1] != str(array):
            print('ERROR66')
            sys.exit(1)

        if arg[2] != [array[i] for i in range(len(array))]:
            print('ERROR77')
            sys.exit(1)
