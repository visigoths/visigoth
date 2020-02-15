#!/bin/bash

# run example in the current directory
python3 example.py

# take screenshot
google-chrome --headless --no-scrollbars --disable-gpu --window-size=2000,2000 --screenshot=screenshot.png example.svg >> /dev/null 2>&1

# produce thumbnail
convert -trim +repage -resize 256 screenshot.png thumbnail.png >> /dev/null 2>&1

# produce larger image
convert -trim +repage -resize 768 screenshot.png example.png >> /dev/null 2>&1

# cleanup
rm -f screenshot.png

