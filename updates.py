#!/usr/bin/env python
'''Script to find canonical versions of own pkgbuilds in this repo'''
import os
import subprocess
import requests
import yaml
import pyaml

VERSIONS_FILE = os.path.join('versions.yml')

def get_node_version():
    '''Find latest nodejs LTS version'''
    resp = requests.get("https://nodejs.org/download/release/index.json")
    last_lts = [v for v in resp.json() if v['lts']][0]

    return last_lts['version'][1:] # remove leading 'v'

def get_blackbox_release():
    '''Fetch latest github release of StackExchange/blackbox'''
    resp = requests.get("https://api.github.com/repos/StackExchange/blackbox/tags")
    latest = resp.json()[0]
    # NB: could use git, instead maybe, that way we have a sha (it's in the resp)
    return latest['name'][1:] # slice away leading v

def bump_pkgver(pkg, ver):
    '''Update pkgver line in PKGBUILD for a subdirectory'''
    cmd = "sed -i s/pkgver=.*/pkgver={}/ ./{}/PKGBUILD".format(ver, pkg)
    subprocess.Popen(cmd, shell=True)

if __name__ == '__main__':
    VERSIONS = None
    with open(VERSIONS_FILE, 'r') as file:
        VERSIONS = yaml.safe_load(file)
    print(VERSIONS)
    VERSIONS['blackbox'] = get_blackbox_release()
    VERSIONS['node'] = get_node_version()

    # Write it down in a file for personal reference
    with open(VERSIONS_FILE, 'w') as file:
        pyaml.dump(VERSIONS, file, explicit_start=True)
        print("Updated {}".format(VERSIONS_FILE))

    # More importantly propagate versions to PKGBUILD files
    bump_pkgver('nodejs-lts', VERSIONS['node'])
    bump_pkgver('blackbox-vcs', VERSIONS['blackbox'])
