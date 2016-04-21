#!/usr/bin/env python

# SM background processes
processes = ["tt", "ttB", "tB", "Bj", "jj", "test"]

# HT bins for the processes
HTbins = ["1500-3000","3000-5500","5500-8500","8500-100000"]

# QCUT for various processes
QCUT =  {
		"tt"	: 80.	,
		"ttB"	: 80.	,
		"tB"	: 60.	,
		"Bj"	: 40.	,
		"jj"	: 40.	,
		"test"	: 40.
		}

MGcmd  = 	{ 
"tt"	: 
"""define X = t t~
generate p p > X X @0
add process p p > X X j @1
add process p p > X X j j @2"""	,
			 
"ttB"	: 
"""define X = t t~
define V = w+ w- z a 
generate p p > X X V @0
add process p p > X X V j @1""" ,

"jj"	:
"""generate p p > j j @0
add process p p > j j j @1
add process p p > j j j j @2""" ,

"Bj"	:
"""define V = w+ w- z a
generate p p > V j @0
add process p p > V j j @1
add process p p > V j j j @2""" ,

"tB"	:
"""define X = t t~
define V = w+ w- z a
generate p p > X V j @0
add process p p > X V j j @2""" ,

"test"	:
"""generate p p > z z""" 
}
