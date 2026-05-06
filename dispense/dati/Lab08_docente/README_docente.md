# Lab08 -- Materiale docente

Questa cartella contiene:

```text
Lab08_docente_completo/
|-- generate_synthetic_data.py
|-- data/
|   |-- poisson_interarrivals.csv
|   |-- jump_process.csv
|   |-- jump_process_metadata.csv
|   |-- ou_process.csv
|   |-- ou_metadata.csv
|   |-- sir_observed_stats.csv
|   |-- sir_metadata.csv
|   |-- sir_hidden_full_trajectory_teacher_only.csv
|   `-- soluzioni_parametri.csv
`-- README_docente.md
```

## Uso

Per rigenerare i dati:

```bash
python generate_synthetic_data.py
```

Lo script crea/aggiorna la cartella `data/`.

## Nota

`generate_synthetic_data.py`, `soluzioni_parametri.csv` e `sir_hidden_full_trajectory_teacher_only.csv`
non vanno distribuiti agli studenti se si vuole mantenere nascosti i parametri veri
e la traiettoria SIR completa.
