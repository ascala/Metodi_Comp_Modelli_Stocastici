#!/bin/bash

for f in Slides*.md; do
    pdf="PDFs/${f%.md}.pdf"
    if [ ! -f "$pdf" ] || [ "$f" -nt "$pdf" ]; then
        echo "Compilo slide $f → $pdf"
        pandoc "$f" -o "$pdf" \
            --pdf-engine=pdflatex \
            -H BeamerHeader.tex \
            -t beamer --slide-level=2
    fi
done
