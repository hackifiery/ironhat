import ollama
from ollama import Message, ResponseError

from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
#from rich.panel import Panel
#from rich.syntax import Syntax
import config
from typing import Callable
import src.utils as utils
import os

from src.toolset import *
def main()->None:
    #print(os.getcwd())
    con = Console()

    model = config.MODEL

    toolsDict:dict[str, Callable] = dict(zip([i.__name__ for i in config.TOOLS], config.TOOLS)) # tool name to tool callable
    tools: list[Callable] = config.TOOLS
    messages: list[dict[str, str] | Message] = []

    utils.pullModelIfNotExists(model)

    while True:
        q = con.input("> ").strip()
        if not q: continue
        if q[0] == "/":
            if q.lower() in ["/exit", "/quit", "/q"]: break
            elif q.split()[0].lower() in ["/save", "/s"]:
                if len(q.split()) < 2: con.print("[red]Error: Please provide a filename to save the conversation.[/red]"); continue
                utils.saveConversation(messages, q.split()[1])
            elif q.split()[0].lower() in ["/load", "/l"]:
                if len(q.split()) < 2: con.print("[red]Error: Please provide a filename to load the conversation from.[/red]"); continue
                messages = utils.loadConversation(q.split()[1])
            continue

        """if q.lower().split()[0] == "/model":
            if len(q.split()) < 2:
                con.print(model)
                continue
            model = q.split()[1]
            ollama.pull(model)

            con.print(f"[green]Switched to model: {model}[/green]")
            continue
        """
        messages.append({"role": "user", "content": q})

        stream = ollama.chat(
            model=model,
            messages=messages,
            stream=True,
            tools=tools
        )

        toolCalls = []
        calledTool = True # whether the most recent AI message contains tool calls
        while calledTool:
            calledTool = False
            aiMsg = None
            t = ""
            with Live(Markdown(f"{model}: "), console=con, refresh_per_second=20) as live:
                try:
                    for chunk in stream:
                        if chunk.message.content:
                            t += chunk.message.content
                            # Re-render the entire accumulated text as markdown
                            live.update(Markdown(f"{model}: {t}"))
                            
                        if chunk.message.tool_calls:
                            # 1 or more tools called
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
                assert aiMsg is not None # will never happen, just for type checking :\
                messages.append(aiMsg)
                for call in toolCalls:
                    toolName = call.function.name
                    toolArgs = call.function.arguments
                    
                    con.print(f"invoke function: {toolName}{toolArgs}")
                    
                    # human safeguard before executing tool calls
                    choice = con.input("[yellow]Allow execution? (y/N): [/yellow]").strip().lower()
                    
                    if choice == 'y':
                        func = toolsDict.get(toolName)
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
                        model=model,
                        messages=messages,
                        stream=True,
                        tools=tools
                    )

            con.print()

if __name__ == "__main__":
    main()