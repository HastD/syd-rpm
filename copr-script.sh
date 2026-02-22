#!/bin/sh -eux

# SPDX-FileCopyrightText: 2026 Daniel Hast
#
# SPDX-License-Identifier: MIT

git clone --depth=1 https://github.com/HastD/syd-rpm.git
cd syd-rpm
cargo vendor --versioned-dirs --locked vendor/
version=$(grep -oP '^Version:\s*\K\S+' rust-syd.spec)
tar -cJf "../syd-${version}-vendor.tar.xz" vendor/
mv rust-syd.spec ..
cd ..
rm -rf syd-rpm
