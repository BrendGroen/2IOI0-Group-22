import pm4py
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

log = pm4py.read_xes('BPI_Challenge_2012.xes')
process_model = pm4py.discover_bpmn_inductive(log)
pm4py.view_bpmn(process_model)