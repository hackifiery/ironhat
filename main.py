import ollama
from ollama import Message, ResponseError

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
#from rich.panel import Panel
#from rich.syntax import Syntax

from toolset import *

con = Console()

MODEL = "qwen3.5:9b"

tools = {
    "readFile": readFile,
    "findInFile": findInFile,
    "replaceLineInFile": replaceLineInFile,
    "insertLineInFile": insertLineInFile,
    "runPythonFile": runPythonFile,
    "listDirectory": listDirectory
}
while True:
    q = con.input("> ").strip()
    if not q: continue
    if q.lower() in {"/exit", "/quit"}: break
    messages: list[dict[str, str] | Message] = [
        {"role": "user", "content": q}
    ]

    stream = ollama.chat(
        model=MODEL,
        messages=messages,
        stream=True,
        tools=[readFile, findInFile, replaceLineInFile, insertLineInFile, runPythonFile, listDirectory]
    )

    toolCalls = []
    calledTool = True # whether the most recent AI message contains tool calls
    while calledTool:
        calledTool = False
        aiMsg = None
        t = ""
        with Live(Markdown(f"{MODEL}: "), console=con, refresh_per_second=20) as live:
            try:
                for chunk in stream:
                    if chunk.message.content:
                        t += chunk.message.content
                        # Re-render the entire accumulated text as markdown
                        live.update(Markdown(f"{MODEL}: {t}"))
                        
                    if chunk.message.tool_calls:
                        aiMsg = chunk.message  
                        for tool_call in chunk.message.tool_calls:
                            calledTool = True
                            toolCalls.append(tool_call)
            except ResponseError as e:
                con.print(f"\n[bold red][Ollama Parsing Error]:[/bold red] {e}")
                messages.append({
                    "role": "user", 
                    "content": "Your last tool call formatting failed the XML parser. If you are trying to write multi-line blocks, try using shorter code segments, avoid complex nested quotes within arguments, or use the writeFile tool."
                })
                calledTool = True  # retry response

        if toolCalls:
            assert aiMsg is not None # will never happen, just for type checking
            messages.append(aiMsg)
            for call in toolCalls:
                toolName = call.function.name
                toolArgs = call.function.arguments
                
                con.print(f"invoke function: {toolName}{toolArgs}")
                
                # human safeguard before executing tool calls
                choice = con.input("[yellow]Allow execution? (y/N): [/yellow]").strip().lower()
                
                if choice == 'y':
                    func = tools.get(toolName)
                    if func:
                        try:
                            result = func(**toolArgs)
                        except Exception as e:
                            result = f"Error during tool execution: {e}"
                        calledTool = True
                        # print(f"[System Output]: {result}")
                        messages.append({"role": "tool", "name": toolName, "content": str(result)})
                    else:
                        raise Exception("[Error]: Tool mapping failed.")
                else:
                    con.print("[System]: Blocked by user approval.")
                    messages.append({"role": "tool", "name": toolName, "content": "Error: User actively denied permission to execute this tool."})
            toolCalls.clear()
            if calledTool:
                stream = ollama.chat(
                    model=MODEL,
                    messages=messages,
                    stream=True,
                    tools=[readFile, findInFile, replaceLineInFile, insertLineInFile, runPythonFile, listDirectory]
                )

        con.print()