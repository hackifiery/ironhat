# Ironhat
Ironhat is a local AI coding agent. This means the model runs entirely on your computer and can run offline. Still quite buggy.
# Features
* Can edit or create files
    * (requests for your permission first, of course)
* Save/load conversations
* Automatic model pulling from Ollama
* Clean config file (`config.py`)
# Setup
Ironhat requires `ollama` and `rich`. To build, run
```sh
pip install .
```
and you can run
```sh
ironhat
```
# Todo
- [ ] Cleaner API
- [ ] Automatic conversation saving/loading
- [ ] Cleaner UI
- [ ] Better config features
