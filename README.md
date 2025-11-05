# vibe-1

Prototype implementation of the "AI Comfort App" concept. The repository now includes a
command-line experience that mirrors the chat, relaxation, story, and daily boost modes
from the design document.

## Getting started

Create a virtual environment (optional but recommended) and install the only runtime
dependency, which is the Python standard library.

```bash
python -m venv .venv
source .venv/bin/activate
```

Run the interactive console experience:

```bash
python -m app.cli
```

You can teach the assistant facts, start guided relaxation, explore story prompts, or
receive a daily uplifting message.

## Tests

Execute the automated tests with:

```bash
pytest
```
