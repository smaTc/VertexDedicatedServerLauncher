import subprocess
import platform
import os
import traceback


from tkinter import ttk
from tkinter import *

cmd = ["",""]
args = []
proc = None


def runServer(cmd,arguments):
    orgPath = os.getcwd()
    os.chdir(cmd[0])
    comb = [cmd[1]] + arguments

    try:
        print("Executing command:")
        print(comb)
        proc = subprocess.Popen(comb,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    except:
        print("Exception occured")
        traceback.print_exc()

    os.chdir(orgPath)
    

"""
def killServer():
    if proc is not None:
        proc.kill()
    else:
        print("No server running!")
"""

def evalArgs(name,map,mode,port):
    mapMode = map + "?game=" + mode
    gameport = "-port=" + port
    servername = "-servername=\"" + name + "\""
    args = [mapMode,gameport,servername]
    return args

def fetchMapList():
    maps = []
    logPath = "MCS/Saved/Logs/MCS.log"
    if platform.system() != "Windows":
        logPath = "./" + logPath
    
    try:
        logFile = open(logPath)
        lines = logFile.readlines()

        startMapList = False

        for line in lines:
            if "ACTIVE MAP LIST" in line:
                startMapList = True
                continue
            if startMapList:
                if "========================" in line:
                    break 

               # m = line.split("[None] ")[1].split(" = ")[1]
                mPath = line.split(" = ")[1].split("/")
                m = mPath[len(mPath)-1].replace(" ","").replace("\n","")
                print(m)
                maps.append(m)

    except IOError:
        print("Log file not accessible. Does it exist?")
    finally:
        logFile.close()
    
    return maps
    
    

if platform.system() == "Windows":
    cmd[0] = "MCS/Binaries/Win64"
    cmd[1] = "MCSServer.exe"
else:
    cmd[0] = "MCS/Binaries/Linux"
    cmd[1] = "./MCSServer"



root = Tk()
root.title("Vertex Dedicated Server Launcher")

mainframe = ttk.Frame(root, padding="3 3 3 3")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

Label(mainframe,text="Servername").grid(row=0)
nameValue = StringVar()
nameValue.set("Vertex Dedicated Server")
nameInput = Entry(mainframe,textvariable=nameValue)
nameInput.grid(row=0,column=1)


Label(mainframe,text="Map").grid(row=1)
#mapList =["P_FFA_COMPLEX","P_CARGO_BAY","P_RIFT"]
mapList = fetchMapList()
mapComboBox = ttk.Combobox(mainframe,values=mapList)
mapComboBox.current(0)
mapComboBox.grid(row=1,column=1)


Label(mainframe,text="Mode").grid(row=2)
modeList =["OPEN","DUEL","TFFA"]
modeComboBox = ttk.Combobox(mainframe,values=modeList)
modeComboBox.current(0)
modeComboBox.grid(row=2,column=1)



Label(mainframe,text="Port").grid(row=3)
portValue = StringVar()
portValue.set("27070")
portInput = Entry(mainframe,textvariable=portValue)
portInput.grid(row=3,column=1)


Button(mainframe,text="Quit",command=root.quit).grid(sticky="SW",row=4,column=0,padx=5,pady=5)
Button(mainframe,text="Run Server",command=(lambda: runServer(cmd, evalArgs(nameValue.get(), mapComboBox.get(), modeComboBox.get(), portValue.get()) ))).grid(sticky="SE",row=4,column=2,padx=5,pady=5)
#Button(mainframe,text="Kill Server",command=(lambda: killServer())).grid(sticky="S",row=4,column=1,padx=5,pady=5)

root.mainloop()
