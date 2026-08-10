import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.')
from drip_plan import get_plan

plan = get_plan('15-Days-of-Agentic-AI')
print(f'Total days in plan: {len(plan)}')
print(f'\nDay 3 (tomorrow) will push:')
msg, files = plan[2]
print(f'  Commit message: "{msg}"')
for f in files:
    print(f'  File: {f}')
print(f'\nRemaining schedule:')
for i in range(2, len(plan)):
    msg, files = plan[i]
    print(f'  Day {i+1}: {msg} ({len(files)} file(s))')
