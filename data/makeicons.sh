#!/bin/bash
for bit in 16x16 22x22 32x32 48x48 64x64; do
    mkdir -p icons/$bit/apps/
    convert -resize $bit pyazan.png icons/$bit/apps/pyazan.png
done
