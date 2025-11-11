# Backup degli originali (opzionale ma consigliato)
cp -r dispense dispense_backup

# Sostituisci tutti gli originali con i cleaned
for file in dispense/**/*.md.cleaned; do
    original="${file%.cleaned}"  # Rimuove .cleaned
    echo "Sostituendo: $original"
    mv "$file" "$original"
done

# Verifica
find dispense -name "*.md" -type f | head -5

