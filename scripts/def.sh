#/bin/bash

WORD="$(copyq selection)"

script="$(readlink -f ${BASH_SOURCE[0]})"

base="$(dirname $script)"

wn "$WORD" -over | grep '1\.' > "$base/def_out"

espeak -f "$base/def_out"
