#!/bin/bash

# Directory containing HTML templates
TEMPLATES_DIR="templates"

# Favicon link to be inserted
FAVICON_LINK='<link rel="icon" type="image/x-icon" href="{{ url_for('static', filename='icons/favicon.ico') }}">'

# Find all HTML files in the templates directory and its subdirectories
find "$TEMPLATES_DIR" -type f -name "*.html" | while read -r file; do
    # Check if the favicon link is already present, if not, insert it
    if ! grep -q "$FAVICON_LINK" "$file"; then
        # Insert the favicon link after the <head> tag
        sed -i "/<head>/a \ \ \ \ $FAVICON_LINK" "$file"
        echo "Favicon added to: $file"
    else
        echo "Favicon already present in: $file"
    fi
done