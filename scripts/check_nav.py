import sys
import os

# Ensure project root is on sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app import app

with app.test_client() as c:
    resp = c.get('/login')
    text = resp.data.decode('utf-8', errors='replace')
    print('STATUS', resp.status_code)
    start = text.find('<nav')
    end = text.find('</nav>', start)
    print('NAV_FOUND', start != -1)
    if start != -1:
        print(text[start:end+6])
    else:
        print(text[:800])
    print('\nINDEX of "Trek Management System":', text.find('Trek Management System'))
