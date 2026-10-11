# BioScavenger

A screen-free, offline nature quest engine. Listen, go outside, explore, and earn Nature Credits.

Built for Hacktoberfest ("Touch the Grass" theme).

---

## Overview

BioScavenger delivers a short scavenger quest as an audio briefing. You put your device away, explore the outdoors to find items such as leaves, bark, or flowers, then return and upload a photo as proof.

Everything runs locally on your machine. No internet connection, accounts, or tracking.

---

## Features

- **Fully offline.** Runs on a local AI model with no cloud services or costs.
- **Audio quests.** Calm, hands-free voice narration.
- **Photo proof.** Upload a picture to earn Nature Credits.
- **Private by design.** No telemetry, no location tracking, no remote data.

---

## Tech Stack

| Component | Technology |
|---|---|
| Language model | Qwen2.5-3B via [Ollama](https://ollama.com) |
| Speech synthesis | [Piper TTS](https://github.com/rhasspy/piper) |
| Interface | Streamlit (Python) |
| Data format | JSON, parsed into game tasks |

---

## Getting Started

### Requirements

- Python 3.10 or higher
- [Ollama](https://ollama.com)

### 1. Clone the repository

```bash
git clone https://github.com/Richs03/BioScavenger.git
cd BioScavenger
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the language model

In a separate terminal:

```bash
ollama run qwen2.5:3b
```

### 4. Set up Piper TTS (Windows)

1. Download the Windows release of [Piper TTS](https://github.com/rhasspy/piper).
2. Download the voice model `en_US-lessac-medium.onnx` and its `.json` config file.
3. Place `piper.exe` and the voice files in the project root folder.

### 5. Launch the app

```bash
python -m streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## How to Play

1. Click **Generate Quest**.
2. Listen to the audio briefing.
3. Put your device away and head outside.
4. Find the items described in the quest.
5. Upload a photo as proof.
6. Earn Nature Credits.

---

## Project Structure

```
BioScavenger/
  app.py              Main application
  requirements.txt    Python dependencies
  piper.exe           Piper TTS binary (download separately)
  *.onnx, *.json      Voice model files (download separately)
```

---

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a pull request

Suggested areas: new quest themes, additional voice models, and Linux/macOS setup instructions.
