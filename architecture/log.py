import time

LOG = {'tmstamp':[]}

with open('log.csv','w') as f:
    f.write('tmstamp,mpu_6050,stc_3100,photo,antenna\n')

def log(dct):
    global LOG
    LOG['tmstamp'].append(time.time())
    for k, v in dct.items():
        if k not in LOG:
            LOG[k] = [v]
        else:
            LOG[k].append(v)
    if len(LOG.keys()) > 1:
        with open('log.csv','a') as f:
            string = ''
            for k,v in LOG.items():
                string += '"' + str(v[-1]) + '"' + ','
            string.lstrip(',')
            string += '\n'
            f.write(string)