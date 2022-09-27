#!/usr/bin/env bash


set -eo pipefail

LINK="${1:-https://karpathy.ai/lexicap/0321-small.html}"

wget --quiet -O transcript.html "$LINK"

python3 ./summarize.py
