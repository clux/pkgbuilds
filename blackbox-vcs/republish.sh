#!/bin/bash
set -e

git clone ssh://aur@aur.archlinux.org/blackbox-vcs.git
cp PKGBUILD blackbox-vcs/
makepkg --printsrcinfo > blackbox-vcs/.SRCINFO
cd blackbox-vcs
git add PKGBUILD .SRCINFO
git clux
