import pm4py
import pandas as pd

log = pm4py.read_xes('BPI_Challenge_2012.xes')
process_model = pm4py.discover_bpmn_inductive(log)
pm4py.view_bpmn(process_model)
df = pm4py.convert_to_dataframe(log)
