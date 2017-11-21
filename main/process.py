import multiprocessing as mp
import random
import string
import requests
import time

random.seed(123)

# Define an output queue
output = mp.Queue()

# define a example function
def rand_string(length, output):
  proxies = { 'http': '83.149.70.159:13012', 'https': '83.149.70.159:13012'}
  r = requests.get('https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dbaby-products&field-keywords=B00MRZIGVG', proxies=proxies)
  output.put(r.status_code)

# Setup a list of processes that we want to run
processes = [mp.Process(target=rand_string, args=(5, output)) for x in range(4)]

s2 = time.time()
# Run processes
for p in processes:
    p.start()

# Exit the completed processes
for p in processes:
    p.join()

# Get process results from the output queue
results = [output.get() for p in processes]
s = time.time()
print s - s2
print(results)