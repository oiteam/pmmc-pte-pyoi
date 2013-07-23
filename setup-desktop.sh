#!/bin/sh

action=${1:-install}

for name in pai sei
do

    # Install/Uninstall menu entries
    echo ">>> xdg-desktop-menu ${action} desktop/pmmc-oi-${name}.desktop"
    xdg-desktop-menu ${action} desktop/pmmc-oi-${name}.desktop

    # Install/Uninstall icons
    for size in 16 22 24 32 36 48 64 72 96 128 192 256
    do
        echo ">>> xdg-icon-resource ${action} --size ${size} icons/${name}/${name}-${size}.png pmmc-oi-${name}"
        xdg-icon-resource ${action} --size ${size} icons/${name}/${name}-${size}.png pmmc-oi-${name}
    done
done

echo ">>> xdg-desktop-menu ${action} desktop/pmmc-oi-socrates.desktop"
xdg-desktop-menu ${action} desktop/pmmc-oi-socrates.desktop