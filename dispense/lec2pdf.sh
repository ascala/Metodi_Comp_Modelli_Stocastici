#!/bin/bash

for f in Lec*.md; do
    pdf="PDFs/${f%.md}.pdf"
    if [ ! -f "$pdf" ] || [ "$f" -nt "$pdf" ]; then
        echo "Compilo $f → $pdf"
        pandoc "$f" -o "$pdf" \
            --pdf-engine=pdflatex \
            -H PdfLatexHeader.tex
    fi
done

