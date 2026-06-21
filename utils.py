import ollama
import json
import os

def pullModelIfNotExists(s:str)->None:
    if s not in [i.model for i in ollama.list().models]:
        print(f"{s} not found locally. Pulling from registry...")
        for progress in ollama.pull(s, stream=True):
            status = progress.get('status', '') or 0
            completed = progress.get('completed', 0) or 0
            total = progress.get('total', 0) or 0
            if total > 0:
                percent = (completed / total) * 100
                print(f"\rStatus: {status} ({percent:.1f}%)", end="", flush=True)
            else:
                print(f"\ndone", end="", flush=True)

def saveConversation(msgs: list[dict[str, str] | ollama.Message], fname: str) -> None:
    with open(fname, 'w') as f:
        for i in msgs:
            if isinstance(i, dict):
                f.write(json.dumps(i) + "\n")
            elif isinstance(i, ollama.Message):
                f.write(json.dumps({"role": i.role, "content": i.content}) + "\n")

def loadConversation(fname: str) -> list[dict[str, str] | ollama.Message]:
    l:list[dict[str, str] | ollama.Message] = []
    with open(fname, 'r') as f:
        for line in f:
            l.append(json.loads(line))
    return l
