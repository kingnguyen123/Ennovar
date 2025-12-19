import sys
import os
os.chdir(r'c:\Users\kingd\Ennovar')
sys.path.insert(0, r'c:\Users\kingd\Ennovar')

from backend.utils.database import get_category_sales

result = get_category_sales("Feminine", '2023-01-01', '2023-12-31')
print(result)