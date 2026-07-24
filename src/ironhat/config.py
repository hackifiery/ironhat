from ironhat.toolset import *
from typing import Callable, Literal

MODEL:str = "gemma4:e2b"
TOOLS_ENABLED:bool = True
THINKING:bool | Literal['low', 'medium', 'high'] | None = "low"
TOOLS: list[Callable] = [readFile, findInFile, replaceLineInFile, insertLineInFile, runPythonFile, listFiles, writeToFile]
