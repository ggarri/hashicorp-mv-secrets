#!/usr/bin/env python3

import hvac
import config as cfg

client = hvac.Client(url=cfg.url, token=cfg.token)
for secret in cfg.secrets:
    data = client.secrets.kv.v2.list_secrets(path=secret).get('data').get('keys')
    for addr in data:
        old_path = secret + '/' + addr
        new_path = secret + '/_' + addr
        
        if addr.startswith('0x'):
            val = client.secrets.kv.v2.read_secret_version(old_path)['data']['data']
            client.secrets.kv.v2.create_or_update_secret(path=new_path, secret=val)
            client.secrets.kv.v2.delete_secret_versions(path=old_path,versions=[1,2])
            client.secrets.kv.v2.delete_metadata_and_all_versions(path=old_path)
            print("Migrated to: " + new_path)
        else:
            print("Skipped " + old_path)
