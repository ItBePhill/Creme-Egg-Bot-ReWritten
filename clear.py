import os

files = os.listdir(f"{os.path.dirname(__file__)}//Songs")

for file in files:
    if os.path.splitext(file)[1] == ".webm":
        os.remove(f"{os.path.dirname(__file__)}//Songs//{file}.webm")

files = os.listdir(f"{os.path.dirname(__file__)}//Songs//Images//Videos")

for file in files:
    if os.path.splitext(file)[1] == ".webp":
        os.remove(f"{os.path.dirname(__file__)}//Songs//Images//Videos//{file}")
if os.path.exists(f"{os.path.dirname(__file__)}//songs.db"):
    os.remove(f"{os.path.dirname(__file__)}//songs.db")