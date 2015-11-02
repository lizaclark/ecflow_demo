#!/usr/bin/env python2.7
import os
import ecflow

def create_family_f1():
    f1 = ecflow.Family("f1" )
    f1.add_task("t1")
    f1.add_task("t2")
    return f1

print "Creating suite definition"
defs = ecflow.Defs()
suite = defs.add_suite("test")
suite.add_variable("ECF_INCLUDE", "/home/eclark/ecflow_demo/include") 
suite.add_variable("ECF_HOME", "/home/eclark/ecflow_demo")

suite.add_family( create_family_f1() )
print defs

print "Checking job creation: .ecf -> .job0"
print defs.check_job_creation()

print "Saving definition to file 'test.def'"
defs.save_as_defs("test.def")
