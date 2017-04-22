# Notes to self

Should have pins for [voted packages](https://aur.archlinux.org/packages/?SB=w&SO=d&SO+=+a).

## Updating
### Pins

```sh
git submodule update --remote
git commit -am "bump pins"
```

### Personals

```sh
./update.py
```

Then propagate any diff in `versions.yml` to the packages, and run the `publish.sh` script with the folder name.
