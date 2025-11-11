#!/usr/bin/env python3

import os
import re
import sys
from pathlib import Path

def clean_math_blocks(content):
    """Pulisce i blocchi matematici $$ ... $$"""
    
    # Pattern per trovare blocchi matematici
    # Gestisce sia blocchi singola linea che multi-linea
    math_pattern = r'(\s*)\$\$(\s*)(.*?)(\s*)\$\$(\s*)'
    
    def replacer(match):
        before_space, open_space, content, close_space, after_space = match.groups()
        # Rimuove spazi extra ma mantiene il contenuto
        return f'{before_space}$${content}$${after_space}'
    
    # Applica la sostituzione
    cleaned = re.sub(math_pattern, replacer, content, flags=re.DOTALL)
    return cleaned

def clean_markdown_file(file_path, output_suffix='.cleaned'):
    """Pulisce un file markdown"""
    
    print(f"Processing: {file_path}")
    
    try:
        # Leggi il file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Applica le pulizie
        cleaned_content = clean_math_blocks(content)
        
        # Scrivi il file cleaned
        output_path = file_path + output_suffix
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        print(f"✓ Created: {output_path}")
        
        # Mostra differenze
        original_lines = content.split('\n')
        cleaned_lines = cleaned_content.split('\n')
        
        print("Changes found:")
        for i, (orig, clean) in enumerate(zip(original_lines, cleaned_lines)):
            if orig != clean:
                print(f"Line {i+1}:")
                print(f"  Original: '{orig}'")
                print(f"  Cleaned:  '{clean}'")
                print()
        
        return True
        
    except Exception as e:
        print(f"✗ Error processing {file_path}: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 md_cleaner.py <directory_or_file>")
        sys.exit(1)
    
    target = sys.argv[1]
    
    if os.path.isfile(target) and target.endswith('.md'):
        # Singolo file
        clean_markdown_file(target)
    elif os.path.isdir(target):
        # Tutti i file nella directory
        md_files = list(Path(target).glob('**/*.md'))
        print(f"Found {len(md_files)} markdown files")
        
        for md_file in md_files:
            clean_markdown_file(str(md_file))
    else:
        print(f"Error: {target} is not a valid file or directory")
        sys.exit(1)

if __name__ == '__main__':
    main()