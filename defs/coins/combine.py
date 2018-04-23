#!/usr/bin/env python3

import json
import glob
import re


def check_type(val, types, nullable=False, empty=False, regex=None):
    # check nullable
    if nullable and val is None:
        return True
    # check empty
    try:
        if not empty and len(val) == 0:
            return False
    except TypeError:
        pass
    # check regex
    if regex is not None:
        if types is not str:
            return False
        m = re.match(regex, val)
        if not m or m.string != val:
            return False
    # check type
    if isinstance(types, list):
        return True in [isinstance(val, t) for t in types]
    else:
        return isinstance(val, types)


def validate_coin(coin):
    assert check_type(coin['coin_name'], str)
    assert check_type(coin['coin_shortcut'], str)
    assert check_type(coin['coin_label'], str)
    assert check_type(coin['website'], str, empty=True)
    assert check_type(coin['github'], str, empty=True)
    assert check_type(coin['maintainer'], str)
    assert check_type(coin['curve_name'], str)
    assert check_type(coin['address_type'], int)
    assert check_type(coin['address_type_p2sh'], int)
    assert coin['address_type'] != coin['address_type_p2sh']
    assert check_type(coin['maxfee_kb'], int)
    assert check_type(coin['minfee_kb'], int)
    assert coin['maxfee_kb'] > coin['minfee_kb']
    assert check_type(coin['hash_genesis_block'], str, regex=r'[0-9a-f]{64}')
    assert check_type(coin['xprv_magic'], str, regex=r'[0-9a-f]{8}')
    assert check_type(coin['xpub_magic'], str, regex=r'[0-9a-f]{8}')
    assert check_type(coin['xpub_magic_segwit_p2sh'], str, regex=r'[0-9a-f]{8}', nullable=True)
    assert check_type(coin['slip44'], int)
    assert check_type(coin['segwit'], bool)
    assert check_type(coin['decred'], bool)
    assert check_type(coin['forkid'], int, nullable=True)
    assert check_type(coin['force_bip143'], bool, nullable=True)
    assert check_type(coin['default_fee_b'], dict)
    assert check_type(coin['dust_limit'], int)
    assert check_type(coin['blocktime_minutes'], [int, float])
    assert check_type(coin['signed_message_header'], str)
    assert check_type(coin['min_address_length'], int)
    assert check_type(coin['max_address_length'], int)
    assert check_type(coin['bitcore'], list, empty=True)
    assert check_type(coin['bech32_prefix'], str, nullable=True)
    assert check_type(coin['cashaddr_prefix'], str, nullable=True)


def process_json(fn):
    j = json.load(open(fn))
    validate_coin(j)
    return j


coins = {}
for fn in glob.glob('*.json'):
    c = process_json(fn)
    n = c['coin_name']
    coins[n] = c

json.dump(coins, open('../coins.json', 'w'), indent=4, sort_keys=True)

print('OK')