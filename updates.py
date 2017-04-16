#!/usr/bin/env python
import re
import os
import requests
import yaml
import pyaml
import subprocess

VERSIONS_FILE = os.path.join('versions.yml')

def get_node_version():
    '''Find latest nodejs LTS version'''
    resp = requests.get("https://nodejs.org/download/release/index.json")
    last_lts = [v for v in resp.json() if v['lts']][0]

    return last_lts['version']

def get_stable_rust_version():
    '''Hacky parsing of rust-lang download page to get latest stable version'''
    resp = requests.get("https://www.rust-lang.org/en-US/install.html")
    match = re.search(r'(\d+\.\d+\.\d+)', resp.text)
    return match.group(1)

def get_blackbox_release():
    '''Fetch latest github release of StackExchange/blackbox'''
    resp = requests.get("https://api.github.com/repos/StackExchange/blackbox/tags")
    latest = resp.json()[0]
    # NB: could use git, instead maybe, that way we have a sha (it's in the resp)
    return latest['name'][1:] # slice away leading v

if __name__ == '__main__':
    VERSIONS = None
    with open(VERSIONS_FILE, 'r') as file:
        VERSIONS = yaml.safe_load(file)
    print(VERSIONS)
    VERSIONS['blackbox_version'] = get_blackbox_release()
    VERSIONS['rust_ver'] = get_stable_rust_version()
    VERSIONS['node'] = get_node_version()

    with open(VERSIONS_FILE, 'w') as file:
        pyaml.dump(VERSIONS, file, explicit_start=True)
        print("Updated {}".format(VERSIONS_FILE))