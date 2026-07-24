import os
import sys
import subprocess

def readFile(filePath: str) -> str:
    """Reads the contents of a local file safely and returns its text. 
    Format: readFile(filePath: str) -> str"""
    try:
        with open(filePath, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error: {e}"

def listFiles(dirPath: str = ".") -> list[str]:
    """Lists the files and folders in a specified directory. Defaults to current directory.
    Format: listFiles(dirPath: str = ".") -> list[str]"""
    try:
        return os.listdir(dirPath)
    except Exception as e:
        return [f"Error: {e}"]

def findInFile(filePath: str, keyword: str) -> list[str]:
    """Finds lines containing a specific keyword inside a file.
    Format: findInFile(filePath: str, keyword: str) -> list[str]"""
    try:
        with open(filePath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            return [line.strip() for line in lines if keyword in line]
    except Exception as e:
        return [f"Error: {e}"]

def replaceLineInFile(filePath: str, lineNumber: int, newLine: str) -> str:
    """Replaces lines in a file starting at targeted lineNumber. 
    If newLine contains multiple lines, it will overwrite the targeted line 
    AND subsequent lines matching the incoming length.
    Lines are 1-indexed. Use \\n for newlines.
    Format: replaceLineInFile(filePath: str, lineNumber: int, newLine: str) -> str"""
    idx = lineNumber - 1  # Convert to 0-indexed
    try:
        with open(filePath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        if 0 <= idx < len(lines):
            # Split lines while preserving individual newline tokens
            incoming_lines = [line + '\n' for line in newLine.split('\n')]
            # If the last element was a trailing newline split, pop the empty trailing string
            if incoming_lines and incoming_lines[-1] == '\n' and newLine.endswith('\n'):
                incoming_lines.pop()

            num_to_overwrite = len(incoming_lines)
            lines[idx : idx + num_to_overwrite] = incoming_lines
            
            with open(filePath, 'w', encoding='utf-8') as file:
                file.writelines(lines)
            return "Success: Lines overwritten successfully."
        return "Error: Line number out of bounds."
    except Exception as e:
        return f"Error: {e}"

def insertLineInFile(filePath: str, lineNumber: int, newLine: str) -> str:
    """Inserts text at targeted line number without replacing existing content.
    Lines are 1-indexed. Use \\n for newlines.
    Format: insertLineInFile(filePath: str, lineNumber: int, newLine: str) -> str"""
    idx = lineNumber - 1  # Convert to 0-indexed
    try:
        with open(filePath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        if 0 <= idx <= len(lines):
            incoming_lines = [line + '\n' for line in newLine.split('\n')]
            if incoming_lines and incoming_lines[-1] == '\n' and newLine.endswith('\n'):
                incoming_lines.pop()

            lines[idx:idx] = incoming_lines
            
            with open(filePath, 'w', encoding='utf-8') as file:
                file.writelines(lines)
            return "Success: Line inserted successfully."
        return "Error: Line number out of bounds."
    except Exception as e:
        return f"Error: {e}"

def writeToFile(filePath: str, text: str) -> str:
    """Writes text to a file at filePath, completely overwriting its content.
    Format: writeToFile(filePath: str, text: str) -> str"""
    try:
        with open(filePath, "w", encoding='utf-8') as file:
            file.write(text)
        return f"Success: Written to {filePath} successfully."
    except Exception as e:
        return f"Error: {e}"

def runPythonFile(filePath: str) -> str:
    """Executes a local Python file using the active runtime and returns stdout/stderr.
    Format: runPythonFile(filePath: str) -> str"""
    try:
        result = subprocess.run(
            [sys.executable, filePath], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout if result.stdout else "Success: Executed with no output."
    except subprocess.CalledProcessError as e:
        return f"Error (Exit Code {e.returncode}):\n{e.stderr}"
    except Exception as e:
        return f"Error: {e}"