import json
import os
import sys
import fb_sync
import logging

# open and read config file
f_path = os.path.join(os.path.dirname(sys.path[0]), 'sync', 'config.json')
try:
    f = open(f_path)
except FileNotFoundError:
    logging.error('Could not find configuration file.')
    exit()    
data = json.load(f)
f.close()

if 'master-fbs-path' not in data or \
    'dinasores' not in data:
    logging.error('Missing configuration attributes.')
    exit()

strategy = ''
if 'strategy' in data:
    strategy = data.get('strategy')

synchronizer = fb_sync.FBSync(data.get('master-fbs-path'), strategy)

dinasores = data.get('dinasores')
# loop over dinasores
print('Starting copying process')
for dinasore in dinasores:
    synchronizer.synchronize(dinasore)
print('Copying process concluded')
print('Synchronized {} DINASOREs'.format(len(dinasores)))


