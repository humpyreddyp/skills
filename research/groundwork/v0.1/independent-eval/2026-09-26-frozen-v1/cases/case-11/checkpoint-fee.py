import sys,json
sys.path.insert(0,'/Users/humpyreddypininti/Documents/ChatGPT/skilly/independent-evaluation/2026-09-26-frozen-v1/cases/behavior-a')
sys.argv=['driver','11','noop']
from driver import *
helper('init','--scope','checkout')
b=json.loads(helper('allocate-pb').stdout)['behavior']
write('.bootstrap/runs/fee.md','# Checkout fee blocked\ndocs/checkout.md says current fee 2, while src/checkout.py adds 3 and tests/test_checkout.py expects 13 for subtotal 10. No version distinction appears. PB-001 reserved for the disputed fee, which will not be published. Next: investigate receipt independently and save a precise human question after finishing available evidence.\n')
helper('checkpoint','--scope','checkout','--status','partial','--next','Investigate receipt independently, then publish supported portions and save fee question','--finding','.bootstrap/runs/fee.md')
snapshot('fee-conflict')
