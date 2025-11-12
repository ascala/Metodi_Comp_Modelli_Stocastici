#!/bin/bash

# Backup degli originali (se non esiste)
if [ ! -d "dispense_backup" ]; then
    echo "Creo backup in dispense_backup..."
    cp -r dispense dispense_backup
fi

# Processa i file e sovrascrivi gli originali in dispense
find dispense -name "*.md" -print0 | while IFS= read -r -d '' file; do
    echo "Processing: $file"
    
    # Esegui lo script
    python3 md_cleaner.py "$file" # >> dispense_backup/cleaning.log 2>&1
    
    # Sostituisci l'originale con il cleaned
    if [ -f "$file.cleaned" ]; then
        mv "$file.cleaned" "$file"
        echo "✓ Updated: $file"
    else
        echo "✗ Error processing: $file"
    fi
done

echo "Completato! File in 'dispense' sono stati aggiornati, backup in 'dispense_backup'"
