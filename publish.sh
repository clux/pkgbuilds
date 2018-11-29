#!/bin/bash
set -e

if [ ! -d "$1" ]; then
  echo "No such package $1"
  exit 1
fi

cd "$1"

makepkg --printsrcinfo > .SRCINFO
git add PKGBUILD .SRCINFO
git clux
git commit -m "bump blackbox pin"
# review, verify sha256sum got updated, try to build it, then push manually


# look over https://wiki.archlinux.org/index.php/Arch_User_Repository#Submitting_packages again
