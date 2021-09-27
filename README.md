# pkgbuilds
Personal experiments, AUR pins, and the occasional original AUR package.

## Updating
Update pins and verify sanity of updated `PKGBUILD` files.

```sh
git submodule update --recursive --remote
./updates.py # github source tarballs
./update.py # github releases assets
```

## Submitted to AUR
- [blackbox-vcs](https://aur.archlinux.org/packages/blackbox-vcs/)
- [jenq](https://aur.archlinux.org/packages/jenq/)

## Everything else
Please ignore.

## Manual
A couple of things we don't pin, they can be installed manually with `yay`:

- hadolint-bin
- shellcheck-bin
