#!/bin/bash

for f in Lec*.md; do
    pdf="${f%.md}.pdf"
    if [ ! -f "$pdf" ]; then
        echo "Compilo $f → $pdf"
        pandoc "$f" -o "$pdf" \
            --pdf-engine=pdflatex \
            -H header.tex
    fi
done

