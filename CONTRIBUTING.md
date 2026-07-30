# Contributing

Research contributions should label every statement as one of:

- `PROVED`
- `KNOWN` with a primary citation
- `COMPUTATIONAL`
- `CONJECTURE`
- `OPEN`

Before opening a pull request:

```bash
python -m unittest discover -s tests -v
python scripts/run_experiments.py
python scripts/generate_hasse.py
```

Do not call a result novel solely because a keyword search did not find it.
Include the closest theorem you found and explain the difference in models.

