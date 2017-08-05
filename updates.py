#!/usr/bin/env python
'''Script to find canonical versions of own pkgbuilds in this repo'''
import os
import subprocess
import requests
import yaml
import pyaml
import hashlib

VERSIONS_FILE = os.path.join('versions.yml')

def get_github_release_info(owner, repo):
    '''Fetch latest github release on owner/repo'''
    url = 'https://api.github.com/repos/{}/{}/tags'.format(owner, repo)
    print('GET: {}'.format(url))
    resp = requests.get(url)
    latest = resp.json()[0]
    version = latest['name']
    # NB: latest['tarball_url'] is a similar alternative - but using canonical
    tar_url = 'https://github.com/{}/{}/archive/{}.tar.gz'.format(owner, repo, version)
    print('SHA256SUM: {}'.format(tar_url))
    tar_stream = requests.get(tar_url, stream=True)
    m = hashlib.sha256()
    for chunk in tar_stream.iter_content():
        m.update(chunk)
    return {
        'version': version,
        'shasum': m.hexdigest(),
        'url': tar_url
    }

def get_blackbox_release():
    '''Fetch latest github release of StackExchange/blackbox'''
    res = get_github_release_info('StackExchange', 'blackbox')
    res['version'] = res['version'][1:] # slice away leading v
    return res


def update_pkgbuild(pkg, info):
    '''Update pkgver and sha256sum line in PKGBUILD for a subdirectory'''
    cmd = "sed -i s/pkgver=.*/pkgver={}/ ./{}/PKGBUILD".format(info['version'], pkg)
    subprocess.Popen(cmd, shell=True)
    cmd = "sed -i s/sha256sums=.*/sha256sums=\(\\\'{}\\\'\)/ ./{}/PKGBUILD".format(info['shasum'], pkg)
    subprocess.Popen(cmd, shell=True)
    # NB: url is already static (with pkgver referenced) in PKGBUILD

if __name__ == '__main__':
    VERSIONS = None
    with open(VERSIONS_FILE, 'r') as file:
        VERSIONS = yaml.safe_load(file)
    print(VERSIONS)
    VERSIONS['blackbox'] = get_blackbox_release()

    # Write it down in a file for personal reference
    with open(VERSIONS_FILE, 'w') as file:
        pyaml.dump(VERSIONS, file, explicit_start=True)
        print("Updated {}".format(VERSIONS_FILE))

    # More importantly propagate versions to PKGBUILD files
    update_pkgbuild('blackbox-vcs', VERSIONS['blackbox'])
