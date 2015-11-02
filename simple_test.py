import ecflow

# define suite
defs = ecflow.Defs()
suite = defs.add_suite('test')
# update ECF_HOME and ECF_INCLUDE variables for entire suite
suite.add_variable('ECF_HOME', '/home/eclark/ecflow_demo')
suite.add_variable('ECF_INCLUDE','/home/eclark/ecflow_demo/include')
# add task t1
suite.add_task('t1')
# save definition file
defs.save_as_defs('test.def')
