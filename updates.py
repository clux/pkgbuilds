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

def get_sublime_build():
    '''Hacky parsing of sublime/3 page to get latest build'''
    resp = requests.get("http://www.sublimetext.com/3")
    match = re.search(r'Build (\d{4,5})', resp.text)
    return int(match.group(1))


def get_stable_rust_version():
    '''Hacky parsing of rust-lang download page to get latest stable version'''
    resp = requests.get("https://www.rust-lang.org/en-US/install.html")
    match = re.search(r'(\d+\.\d+\.\d+)', resp.text)
    return match.group(1)

if __name__ == '__main__':
    VERSIONS = None
    with open(VERSIONS_FILE, 'r') as file:
        VERSIONS = yaml.safe_load(file)
    print(VERSIONS)

    VERSIONS['subl_build'] = get_sublime_build()
    VERSIONS['rust_ver'] = get_stable_rust_version()
    VERSIONS['node'] = get_node_version()

    with open(VERSIONS_FILE, 'w') as file:
        pyaml.dump(VERSIONS, file, explicit_start=True)
        print("Updated {}".format(VERSIONS_FILE))
