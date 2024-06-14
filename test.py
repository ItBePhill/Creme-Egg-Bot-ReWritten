import random, pprint, time, datetime
pp = pprint.PrettyPrinter()
logs.info(f"Shuffle command was called! by: {interaction.user}")
await interaction.response.send_message(f"Shuffling...")
t1 = time.time()
shufflequeue = self.queue.copy()
newqueue=[]
for i in range(len(shufflequeue) -1):
    newqueue.append(0)
first = shufflequeue.pop(0)
for num in range(len(shufflequeue)):
    newqueue[num] = shufflequeue.pop(random.randint(0, len(shufflequeue) - 1))
newqueue.insert(0, first)
for i in range(0, len(newqueue)):
    newqueue[i]["id"] = i
t2 = time.time()
print(f"Shuffle took: {datetime.timedelta(seconds=t2-t1)}")