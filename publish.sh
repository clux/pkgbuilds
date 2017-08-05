#!/bin/bash
set -e

if [ ! -d "$1" ]; then
  echo "No such package $1"
  exit 1
fi

cd "$1"

git clone "ssh://aur@aur.archlinux.org/$1.git"
cp PKGBUILD "$1/"
makepkg --printsrcinfo > "$1/.SRCINFO"
cd "$1"
git add PKGBUILD .SRCINFO
git clux
# review, verify sha256sum got updated, try to build it, then push


# look over https://wiki.archlinux.org/index.php/Arch_User_Repository#Submitting_packages again
