#!/usr/bin/env python
'''Script to find canonical versions of pkgbuilds in this repo'''
import os
import requests
import yaml
import pyaml
import hashlib
import semver
import json
import re

VERSIONS_FILE = os.path.join('versions.yml')

FORMULA = {
    'jenq': {
        'repo': 'clux/jenq',
        'executable': r'^jenq\.x86_64-unknown-linux-musl\.tar\.gz$',
        'shasum': r'^jenq\.sha256',
    },
}


def github_api_get(path, headers={}, **request_args):
    '''Make a GET request to the GitHub API'''
    url = f'https://api.github.com/{path}'
    #headers['Authorization'] = f'token {TOKEN}'
    print(f'GET: {url}')
    response = requests.get(url, headers=headers, **request_args)
    response.raise_for_status()
    return response


def get_latest_github_release(config):
    '''Get the latest GitHub release'''
    return github_api_get(f'repos/{config["repo"]}/releases/latest').json()


def find_asset(name, pattern, assets):
    '''Find the exectuable asset'''
    pattern = re.compile(pattern)
    for a in assets:
        if pattern.match(a['name']) is not None:
            return a
    print(assets)
    raise Exception(f'Unable to find asset for {name} matching {pattern}')


def download_asset(config, asset, **request_args):
    # https://developer.github.com/v3/repos/releases/#get-a-single-release-asset
    headers = { 'Accept': 'application/octet-stream' }
    return github_api_get(f'repos/{config["repo"]}/releases/assets/{asset["id"]}',
            headers=headers, **request_args)


def calculate_sha(config, asset):
    tar_stream = download_asset(config, asset, stream=True)
    m = hashlib.sha256()
    for chunk in tar_stream.iter_content():
        m.update(chunk)
    return m.hexdigest()


def get_sha(name, sha_asset, executable_asset):
    shas_content = download_asset(config, sha_asset).text
    lines = [x for x in shas_content.split('\n') if x != '']
    shas = dict([reversed(re.split(r'\s+', x, 1)) for x in shas_content.split('\n') if x != ''])
    if executable_asset['name'] not in shas:
        print(shas_content)
        raise Exception(f'No SHA checksum for {executable_asset["name"]} asset in {sha_asset["name"]}')
    return shas[executable_asset['name']]


def get_latest_version(name, config, original):
    '''Fetch latest github release on owner/repo'''
    release = get_latest_github_release(config)
    version = release['name']

    original_version = original['version'] if original is not None else None
    if original_version == version:
        print(f'{name}: Up to date ({version})')
        return original
    print(f'{name}: New version ({original_version} -> {version})')

    executable_asset = find_asset(name, config['executable'], release['assets'])

    if 'shasum' in config:
        sha_asset = find_asset(name, config['shasum'], release['assets'])
        shasum = get_sha(name, sha_asset, executable_asset)
    else:
        shasum = calculate_sha(config, executable_asset)

    print(f'{name}: Asset found {executable_asset["name"]} ({shasum})')

    return {
        'version': version,
        'shasum': shasum,
        'url': executable_asset['browser_download_url']
    }


def update_pkgbuild(pkg, info):
    '''Update tarball url and sha256 line in the Forumla'''
    path = f'./{pkg}/PKGBUILD'
    with open(path, 'r') as f:
        data = f.readlines()

    start_line = next(i for i, line in enumerate(data) if line.strip() == f'pkgname={pkg}')
    data[start_line + 1] = f"pkgver={info['version']}\n"
    data[start_line + 2] = f"sha256sums=('{info['shasum']}')\n"

    with open(path, 'w') as f:
        f.writelines(data)

if __name__ == '__main__':
    VERSIONS = None
    with open(VERSIONS_FILE, 'r') as file:
        VERSIONS = yaml.safe_load(file)

    for name, config in FORMULA.items():
        VERSIONS[name] = get_latest_version(name, config, VERSIONS.get(name, None))
        update_pkgbuild(name, VERSIONS[name])

    # Write it down in a file for personal reference
    with open(VERSIONS_FILE, 'w') as file:
        pyaml.dump(VERSIONS, file, explicit_start=True)
        print("Updated {}".format(VERSIONS_FILE))
