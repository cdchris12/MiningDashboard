#!/usr/bin/python
import re
import requests
import json
import pprint
import math
import os

try:
    os.stat("config.json")
except Exception:
    print "Config file missing!!!"
    return(1)
else:
    with open('config.json', 'rb') as infile:
        config = json.load(infile.read())
    # End with
# End try/except block

regex = re.compile("^[^{]*({[^}]*})")
pp = pprint.PrettyPrinter(indent=4)

data = {}

def parse(result=False):
    if not result: return()
    elif type(result) is not type([]): return()

    res_data = {}
    res_data['version'], res_data['main_coin'] = result.pop(0).split(' - ')

    res_data['runtime_mins'] = int(result.pop(0))

    res_data['main_speed'], res_data['main_valid'], res_data['main_rejected'] = result.pop(0).split(';')

    temp = {}
    for x,s in enumerate(result.pop(0).split(';')): temp[str(x)] = s
    res_data['main_hash_rate'] = temp

    res_data['alt_speed'], res_data['alt_valid'], res_data['alt_invalid'] = result.pop(0).split(';')

    temp = {}
    for x,s in enumerate(result.pop(0).split(';')): temp[str(x)] = s
    res_data['alt_hash_rate'] = temp

    temp = {}
    fans = result.pop(0).split(';')
    fan_list = []
    for i in range(int(math.floor(len(fans)/2))):
        temperature = fans.pop(0)
        speed = fans.pop(0)
        fan_list.append((temperature, speed))
    # End for
    for x,s in enumerate(fan_list): temp[str(x)] = {"temperature": s[0], "speed": s[1]}
    res_data['fan_speed'] = temp

    res_data['main_pool'], res_data['alt_pool'] = result.pop(0).split(';')

    res_data['main_invalid'], res_data['main_pool_switches'], res_data['alt_invalid'], res_data['alt_pool_switches'] = result.pop(0).split(';')

    temp = {}
    for x,s in enumerate(result.pop(0).split(';')): temp[str(x)] = s
    res_data['main_valid_per card'] = temp

    temp = {}
    for x,s in enumerate(result.pop(0).split(';')): temp[str(x)] = s
    res_data['main_rejected_per card'] = temp

    temp = {}
    for x,s in enumerate(result.pop(0).split(';')): temp[str(x)] = s
    res_data['main_invalid_per card'] = temp

    temp = {}
    for x,s in enumerate(result.pop(0).split(';')): temp[str(x)] = s
    res_data['alt_valid_per card'] = temp

    temp = {}
    for x,s in enumerate(result.pop(0).split(';')): temp[str(x)] = s
    res_data['alt_rejected_per card'] = temp

    temp = {}
    for x,s in enumerate(result.pop(0).split(';')): temp[str(x)] = s
    res_data['alt_invalid_per card'] = temp

    return res_data
# End def

def main():
    r = requests.session()
    for host in config['hosts']:
        try: res = r.get("%s:%s" % (host['url'], host['port']), timeout = 5)
        except requests.exceptions.ConnectTimeout:
            print "Miner %s is down!!" % host['name']
            continue
        else:
            raw = re.search(regex, res.content).groups()[0]
            try: parsed = json.loads(raw)
            except Exception: print "Miner %s failed to deliver valid data!!" % host['name']
            else:
                data[host['name']] = parse(parsed['result'])
            # End try/except/else block
        # End try/except/else block
    # End for

    pp.pprint(data)
# End def

if "__name__" == "__main__":
    main()
# End if
