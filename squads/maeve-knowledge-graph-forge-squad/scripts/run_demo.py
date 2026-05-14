#!/usr/bin/env python3
import subprocess,sys
subprocess.check_call([sys.executable,'scripts/build_knowledge_graph.py','--input','examples/sample_knowledge_base','--output','output/demo_graph'])
print('Abra output/demo_graph/graph.html')
