#!/bin/bash

for f in Slides*.md; do
    pdf="${f%.md}.pdf"
    if [ ! -f "$pdf" ]; then
        echo "Compilo slide $f → $pdf"
        pandoc "$f" -o "$pdf" \
            --pdf-engine=pdflatex \
            -t beamer
    fi
done
