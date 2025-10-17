# ARTW StyleKit

Academic writing style analyzer and generator for Turkish art history journals.

## Quick Start
```bash
# 1. Setup
python -m venv .venv
.venv\Scripts\activate
pip install click pymupdf python-dotenv rich loguru jsonlines

# 2. Ingest corpus (test with 10 files)
python -m artw.cli ingest --src C:\Korpus --out data/corpus.jsonl --sample 10

# 3. Build profile
python -m artw.cli profile --corpus data/corpus.jsonl --out data/style_profile.json

# 4. Inspect profile
python -m artw.cli inspect --profile data/style_profile.json
```

## Project Structure
```
artw_stylekit/
├── artw/
│   ├── ingest/          # PDF parsing, parallel processing
│   ├── analysis/        # Style profiling, citation checking
│   ├── cli/             # Command-line interface
│   ├── config.py        # Configuration
│   └── logger.py        # Logging setup
├── data/                # Corpus data (gitignored)
├── out/                 # Generated outputs (gitignored)
└── tests/               # Tests (TODO)
```

## Commands

- `ingest` - Extract text from PDF corpus
- `profile` - Analyze writing style
- `inspect` - View profile statistics

## Requirements

- Python 3.10+
- Windows 10/11
- PDF corpus in `C:\Korpus`

## Next Steps

- [ ] Prompt generation (LLM integration)
- [ ] DOCX export
- [ ] Citation validation
- [ ] Template matching

## License

MIT
