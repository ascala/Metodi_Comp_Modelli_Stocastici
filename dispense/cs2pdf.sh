#!/bin/bash

for f in casestudy/CS*/CaseStudy*.md; do
    dir=$(dirname "$f")
    base=$(basename "${f%.md}")
    pdf="PDFs/${base}.pdf"

    if [ ! -f "$pdf" ] || [ "$f" -nt "$pdf" ]; then
        echo "Compilo $f -> $pdf"
        pandoc "$f" -o "$pdf" \
            --pdf-engine=xelatex \
            --resource-path="$dir:." \
            -H header.tex
    fi
done
