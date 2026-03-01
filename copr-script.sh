#!/bin/sh -eux

# SPDX-FileCopyrightText: 2026 Daniel Hast
#
# SPDX-License-Identifier: GPL-3.0-only

git clone --depth 1 https://github.com/HastD/syd-rpm.git
cd syd-rpm
cp syd.spec ..
version=$(grep -oP '^Version:\s*\K\S+' syd.spec)
tar -cJf "../syd-selinux-${version}.tar.xz" selinux
cd ..

git clone --depth 1 --branch "v${version}" https://gitlab.exherbo.org/sydbox/sydbox.git "syd-${version}"
tar -cJf "syd-${version}.tar.xz" "syd-${version}"
cd "syd-${version}"
cargo vendor --versioned-dirs --locked vendor
tar -cJf "../syd-${version}-vendor.tar.xz" vendor
cd ..

rm -rf syd-rpm "syd-${version}"
