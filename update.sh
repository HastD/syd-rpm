#!/bin/bash

set -euo pipefail

version=$(cargo info -q syd | grep -oP '^version: \K[0-9]+(?:\.[0-9]+)?(?:\.[0-9]+)?$')

sed -Ei --sandbox -e "s/^Version:([[:blank:]]*).*/Version:\1${version}/" rust-syd.spec

curl -fLsS -o Cargo.toml "https://gitlab.exherbo.org/sydbox/sydbox/-/raw/v${version}/Cargo.toml" \
    -o Cargo.lock "https://gitlab.exherbo.org/sydbox/sydbox/-/raw/v${version}/Cargo.lock"
