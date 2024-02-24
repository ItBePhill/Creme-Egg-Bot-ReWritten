import os

files = os.listdir()

for i in files:
    if os.path.splitext(i)[1] == ".webm" or os.path.splitext(i)[1] == ".webp":
        os.remove(i)
        print(f"removed: {i}")
    


