import os
def readFile(filePath: str) -> str:
    """Reads the contents of a local file safely and returns its text. Format: readFile(filePath: str) -> str"""
    try:
        with open(filePath, 'r') as file:
            return file.read()
    except Exception as e:
        return f"Error: {e}"

def listDirectory(dirPath: str = ".") -> list[str]:
    """Lists the files and folders in a specified directory. If no directory is specified, it defaults to the current working directory. If no directory is specified, it defaults to the current working directory. Format: listDirectory(dirPath: str = ".") -> list[str]"""
    try:
        return os.listdir(dirPath)
    except Exception as e:
        return [f"Error: {e}"]

def findInFile(filePath: str, keyword: str) -> list[str]:
    """Finds lines containing a specific keyword inside a file. All three arguments required. Format: findInFile(filePath: str, keyword: str) -> list[str]"""
    try:
        with open(filePath, 'r') as file:
            lines = file.readlines()
            return [line.strip() for line in lines if keyword in line]
    except Exception as e:
        return [f"Error: {e}"]

def replaceLineInFile(filePath: str, lineNumber: int, newLine: str) -> str:
    """Replaces lines in a file starting at targeted lineNumber. 
    If newLine contains multiple lines, it will overwrite the targeted line 
    AND the subsequent lines matching the incoming length, completely 
    stomping over them instead of pushing them down.
    Note that all three arguments are required. All three arguments are required. Use \\n for new lines. Lines are 1-indexed.
    Format: replaceLineInFile(filePath: str, lineNumber: int, newLine: str) -> str"""
    lineNumber -= 1 # Convert to 0-indexed
    try:
        with open(filePath, 'r') as file:
            lines = file.readlines()
        
        if 0 <= lineNumber < len(lines):
            new_lines_split = [line + '\n' for line in newLine.splitlines()]
            if not new_lines_split:
                new_lines_split = ['\n']
            num_lines_to_overwrite = len(new_lines_split)
            end_index = lineNumber + num_lines_to_overwrite
            lines[lineNumber : end_index] = new_lines_split
            
            with open(filePath, 'w') as file:
                file.writelines(lines)
            return "Success: Lines overwritten successfully."
        return "Error: Line number out of bounds."
    except Exception as e:
        return f"Error: {e}"

def insertLineInFile(filePath: str, lineNumber: int, newLine: str) -> str:
    """Inserts a line at a targeted line number inside a file. Note that if newLine contains new line characters, it will inserted as multiple lines (without replacing any lines). Note that all three arguments are required. Lines are 1-indexed.
    Use \\n for newlines. Format: insertLineInFile(filePath: str, lineNumber: int, newLine: str) -> str
    """
    lineNumber -= 1 # Convert to 0-indexed
    try:
        with open(filePath, 'r') as file:
            lines = file.readlines()
        
        if 0 <= lineNumber <= len(lines):
            lines.insert(lineNumber, newLine + '\n')
            with open(filePath, 'w') as file:
                file.writelines(lines)
            return "Success: Line inserted."
        return "Error: Line number out of bounds."
    except Exception as e:
        return f"Error: {e}"

def runPythonFile(filePath: str) -> str:
    """Executes a local Python file and returns its standard output as text. Format: runPythonFile(filePath: str) -> str"""
    import subprocess
    try:
        result = subprocess.run(['python', filePath], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"