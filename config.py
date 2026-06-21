from toolset import *
from typing import Callable

MODEL:str = "gemma4:12b"
TOOLS: list[Callable] = [readFile, findInFile, replaceLineInFile, insertLineInFile, runPythonFile, listDirectory]