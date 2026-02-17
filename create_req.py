# create_req.py
import os

content = """streamlit==1.28.0
pandas==2.0.3
numpy==1.24.3
plotly==5.17.0
"""

with open('requirements.txt', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ requirements.txt created!")
print(f"File size: {os.path.getsize('requirements.txt')} bytes")
print("\nFile contents:")
with open('requirements.txt', 'r') as f:
    print(f.read())
