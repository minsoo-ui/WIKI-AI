Set WshShell = CreateObject("WScript.Shell")

' 1. Start Backend FastAPI (Silently in background)
WshShell.CurrentDirectory = "D:\Google Antigravity\WIKI-AI\backend"
' Run cmd /c to execute and then exit the cmd wrapper, leaving python running hidden
WshShell.Run "cmd /c if exist venv\Scripts\activate (call venv\Scripts\activate) && python run.py", 0, False

' 2. Start Frontend React Vite (Silently in background)
WshShell.CurrentDirectory = "D:\Google Antigravity\WIKI-AI\frontend"
WshShell.Run "cmd /c npm run dev", 0, False

' 3. Wait 4 seconds for servers to start
WScript.Sleep 4000

' 4. Open the browser
WshShell.Run "http://localhost:5173"

Set WshShell = Nothing
