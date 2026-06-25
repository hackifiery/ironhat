from ironhat.toolset import *
from typing import Callable

MODEL:str = "gemma3:270m"
TOOLS: list[Callable] = []#[readFile, findInFile, replaceLineInFile, insertLineInFile, runPythonFile, listDirectory]
