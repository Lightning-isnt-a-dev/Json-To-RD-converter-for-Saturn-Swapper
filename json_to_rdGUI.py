import yaml
import os, sys
import tkinter, customtkinter
import subprocess as sp
import easygui
import threading as mp
import shutil
import requests
import pickle
import atexit
from pathlib import Path
from zipfile import ZipFile
from PIL import Image

#installed with pip: easygui, customtkinter, pyyaml, pillowm requests



#listoftests BrilliantBomber.json default_axe_to_stellar_axe.json Selene_To_The_Rogue_LAROI_ELECTRIFIED.json Sludgehammer_To_Candy_Axe.json BoogieDownToGetGriddy.json


#def masterskeletalnull(replacestring):
    #if "Base" in os.path.dirname(replacestring) and ("Skeleton" in os.path.basename(replacestring) or "Fortnite_M_Avg_Player" in os.path.basename(replacestring)):
        #return True

def multiprocess(func, arg):
    if arg == None:
        proc = mp.Thread(target=func)
    else:
        proc = mp.Thread(target=func, args=(arg,))
    proc.start()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def defcolortheme(choice):
    if choice == "Blue":
        customtkinter.set_default_color_theme("blue")
        prefs["theme"] = "blue"
    elif choice == "Green":
        customtkinter.set_default_color_theme("green")
        prefs["theme"] = "green"
    elif choice == "Dark Blue":
        customtkinter.set_default_color_theme("dark-blue")
        prefs["theme"] = "dark-blue"
    returntomain.destroy()
    dropdownframe.destroy()
    settingspage()

def selectall():
    autodowncompiler.select()
    autocompile.select()
    autodelrd.select()
    autodeljson.select()

def deselectall():
    autodowncompiler.deselect()
    autocompile.deselect()
    autodelrd.deselect()
    autodeljson.deselect()

def toggleall():
    if automateall.get() == 1:
        selectall()
    elif automateall.get() == 0:
        deselectall()

def pack():
    autodowncompiler.pack(side="bottom", pady="10")
    autocompile.pack(side="bottom", pady="10")
    autodelrd.pack(side="bottom", pady="10")
    autodeljson.pack(side="bottom", pady="10")

def forget():
    autocompile.forget()
    autodowncompiler.forget()
    autodelrd.forget()
    autodeljson.forget()

def showoptions():
    if options.cget("image") == plus:
        options.configure(image=minus)
        pack()

        if automateall.get() == 1:
            selectall()
        elif automateall.get() == 0:
            deselectall
        
        app.geometry("550x450")

    elif options.cget("image") == minus:
        options.configure(image=plus)
        checkboxframe2.configure(height=10)
        forget()

        app.geometry("550x290")

def downloadables(x, wfile, json):
    wfile.write("\n\n")

    LocalPluginsPath = os.getenv("LOCALAPPDATA") + "/JsonToRD/UEFN-resources/" + os.path.basename(json).split(".")[0]
    LocalPluginsPath = LocalPluginsPath.replace("\\", "/")

    IsZip = False

    for k, v in list(x["Downloadables"][0].items()):
        if k == "zip":
            IsZip = True
            get = requests.get(v)
            with open("plugin.zip", "wb") as writing:
                writing.write(get.content)
            break
        else:
            get = requests.get(v)
            with open("plugin." + k, "wb") as writing:
                writing.write(get.content)
            wfile.write(f'system.Download("file://{LocalPluginsPath}/plugin.{k}", "{k}");\n')
            try:
                os.remove(LocalPluginsPath + "/plugin." + k)
                shutil.move("plugin." + k, LocalPluginsPath)
            except FileNotFoundError:
                shutil.move("plugin." + k, LocalPluginsPath)
        
    
    if not os.path.exists(os.getenv("LOCALAPPDATA") + "/JsonToRD/UEFN-resources/"):
        os.makedirs(os.getenv("LOCALAPPDATA") + "/JsonToRD/UEFN-resources/")

    try:
        os.makedirs(LocalPluginsPath)
    except FileExistsError:
        pass
    
    if IsZip:
        with ZipFile("plugin.zip") as zipped:
            for fil in [filename for filename in zipped.infolist() if not filename.is_dir() and os.path.splitext(filename.filename)[1] in [".pak", ".sig", ".utoc", ".ucas"]]:
                with zipped.open(fil) as contents:
                    with open(LocalPluginsPath+f"/{os.path.basename(fil.filename)}", 'wb') as output:
                        output.write(contents.read())

        os.remove("plugin.zip")

        for fil in os.listdir(LocalPluginsPath):
            wfile.write(f'system.Download("file://{LocalPluginsPath}/{fil}", "{fil.split(".")[1]}");')
            wfile.write("\n")

    wfile.write("\n")

def seekwrite(pathtoexists, wfile, seekin, writein, downloads, skin, inpjson):
    if seekin == "CustomCharacterFaceData" or " " in writein:
        return
    #elif "Game" not in os.path.dirname(writein) and "BRCosmetics" not in os.path.dirname(writein) and downloads == False:
        #writeout = "/"
    else:
        writeout = os.path.dirname(writein) + "/" + os.path.basename(writein)

    seekout = os.path.dirname(seekin) + "/" + os.path.basename(seekin)

    tSkinPaths = {
        "Same as plugin" : "/Game/Characters/Player/Female/Medium/Bodies/F_MED_Ramirez_Fallback/Meshes/F_MED_Ramirez_Fallback.F_MED_Ramirez_Fallback",
        "Jennifer Walters" : "/Game/Characters/Player/Female/Medium/Bodies/F_MED_HighTower_Honeydew_Swole/Meshes/F_MED_HighTower_Honeydew_Swole.F_MED_HighTower_Honeydew_Swole",
        "Twyn" : "/Game/Characters/Player/Female/Medium/Bodies/F_MED_Candor_Tech/Meshes/F_MED_Candor_Tech.F_MED_Candor_Tech",
        "Lexa" : "/Game/Characters/Player/Female/Medium/Bodies/F_MED_Lexa_Armored/Meshes/F_MED_Lexa_Armored.F_MED_Lexa_Armored"
    }

    listofgamepaths = ["Game", "BRCosmetics", "VehicleCosmetics", "MeshCosmetics"]

    if downloads and "Meshes" in seekout and "AnimBP" not in seekout and skin == False:
        seekout = tSkinPaths[tSkin.get()]

    if downloads and Path(writeout).parts[1] not in listofgamepaths:
        pak = open(os.getenv("LOCALAPPDATA") + "/JsonToRD/UEFN-resources/" + os.path.splitext(os.path.basename(inpjson))[0]+"/plugin.pak" , 'r', encoding="ascii", errors="ignore").readlines()[1:37]
        line = [x for x in pak if ".up" in x][0]
        pluginUID = os.path.basename(line[line.index("../"): line.index(".up")])
        if "Feature" in pluginUID:
            pluginUID = pluginUID.split("Feature")[1]
        if Path(writeout).parts[1] != pluginUID:
            writeout = "/" + pluginUID + writeout
    

    if pathtoexists:
        wfile.write("search = to.CreateSoftObjectProperty(\"" + seekout + "\")" + ";" + "\n")
        wfile.write("replace = to.CreateSoftObjectProperty(\"" + writeout + "\")" + ";" + "\n")
        wfile.write("to.SwapSoftObjectProperty(search, replace);\n\n")

    elif not pathtoexists:
        wfile.write("search = from.CreateSoftObjectProperty(\"" + seekout + "\")" + ";" + "\n")
        wfile.write("replace = from.CreateSoftObjectProperty(\"" + writeout + "\")" + ";" + "\n")
        wfile.write("from.SwapSoftObjectProperty(search, replace);\n\n")

        

def json_to_rd(jsonpath):
    if not os.path.exists(pathfielddata.get()):
        return
    
    if not os.path.exists(jsonpath):
        header.configure("Invalid JSON path.", text_color="red")
        return
    #using yaml cause json doesnt like the extra comma in some plugins
    #if there are tabs, remove them because yaml doesnt like them

        #try decrypting
    try:
        yamlread = open(jsonpath, encoding='utf-8').read()
        yamlread = yamlread.replace("\t", "    ")
        x = yaml.safe_load(yamlread)
        x["Name"]
    except:
        try:
            x["default_name"]
        except TypeError:
            yamlread = sp.run("%s %s" % (resource_path('resources\\deob\\galaxy_deobfuscator.exe'), jsonpath), capture_output=True, text=True)
            yamlread = yamlread.stdout.replace("\t", "    ")
            x = yaml.safe_load(yamlread)
            print(x)


    #check for the type of json
    try:
        x["Name"]
        x["Swapicon"]
        signs = [("Name","Name"), ("Swapicon","Icon"), ("Message", "Author")]
        difjson = False
    except KeyError:
        try:
            x["default_name"]
            signs = [("default_name","Name"), ("swapped_icon","Icon"), ("messages", "Author")]
            difjson = True
        except KeyError:
            signs = [("Name","Name"), ("Icon","Icon"), ("Message", "Author")]
            difjson = False

    try:
        x["AssetPathTo"]
        AssetPathInSigns = True
    except KeyError:
        AssetPathInSigns = False
        pass



    #check if it wants to download files
    try:
        x["Downloadables"]
        downloads=True
    except:
        downloads=False

    header.configure("Writing signs...", text_color="white")

    #open a file and write the signs
    rdpath = os.path.basename(jsonpath).split(".")[0] + ".rd"
    wfile = open(rdpath, "w", encoding="utf-8")
    for sign, sign_name in signs:
        signing = ('sign: "%s", "%s"\n' % (sign_name, x[sign]))
        wfile.write(signing)
    wfile.write('sign: "Description", "Converted from galaxy swapper, by Lightning."\n')
    header.configure("Wrote signs!", text_color="white")

    #download the files
    if downloads == True:
        downloadables(x, wfile, jsonpath)

    #creation
    wfile.write('\narchive from;\n')
    wfile.write('archive to;\n')
    wfile.write('SoftObjectProperty search;\n')
    wfile.write('SoftObjectProperty replace;\n\n')

    #swaps
    header.configure("Writing imports and swaps...", text_color="white")

    try:
        assets = x["swaps"]
    except KeyError:
        try:
            assets = x["Swaps"]
        except KeyError:
            assets = x["Assets"]

    if AssetPathInSigns:
        AssetPath = x["AssetPathTo"]
        assets = x["AssetPathTo"]
        assets = [assets]
        pathtoexists = False

    for asset in assets:
        if not AssetPathInSigns:
            pathtoexists = True
            AssetPath = asset["AssetPath"]
            try:
                AssetPathTo = asset["AssetPathTo"]
            except KeyError:
                pathtoexists = False

        notskin = False
        if "/WID" in AssetPath or "/Emotes" in AssetPath or "/MusicPacks" in AssetPath:
            notskin = True

        tSkinImport = {
            "Jennifer Walters" : {
                "Head" : ("fortnitegame/Content/Characters/CharacterParts/Female/Medium/Heads/CP_Head_F_HightowerHoneydew_Swole.uasset", "/Game/Characters/Player/Female/Medium/Heads/F_MED_HighTower_Honeydew_Head_01/Meshes/F_MED_HighTower_Honeydew_Head_01.F_MED_HighTower_Honeydew_Head_01"),
                "FaceAcc" : ("fortnitegame/Content/Characters/CharacterParts/FaceAccessories/CP_F_MED_HightowerHoneydew_Swole.uasset", "/Game/Characters/Player/Female/Medium/Bodies/F_MED_HighTower_Honeydew_Swole/Meshes/Parts/F_MED_HighTower_Honeydew_Swole_FaceAcc.F_MED_HighTower_Honeydew_Swole_FaceAcc"),
                "Body" : "FortniteGame/Content/Athena/Heroes/Meshes/Bodies/CP_Body_Commando_F_HightowerHoneydew_Swole.uasset"
            },

            "Twyn" : {
                "Head" : ("", ""),
                "FaceAcc" : ("", ""),
                "Body" : "FortniteGame/Content/Athena/Heroes/Meshes/Bodies/CP_Athena_Body_F_CandorTech.uasset"
            },

            "Lexa" : {
                "Head" : ("fortnitegame/Content/Characters/CharacterParts/Female/Medium/Heads/CP_Head_F_Lexa_Armored.uasset", "/Game/Characters/CharacterParts/Female/Medium/Heads/CP_Head_F_Lexa_Armored.CP_Head_F_Lexa_Armored"),
                "FaceAcc" : ("fortnitegame/Content/Characters/CharacterParts/FaceAccessories/CP_F_MED_LexaArmored_FaceAcc.uasset", "/Game/Characters/Player/Female/Medium/Bodies/F_MED_Lexa_Armored/Meshes/Parts/F_MED_Lexa_Armored.F_MED_Lexa_Armored"),
                "Body" : "fortnitegame/Content/Athena/Heroes/Meshes/Bodies/CP_Body_Commando_F_LexaArmored.uasset"
            }
        }
        if tSkin.get() != "Same as plugin" and downloads == True and notskin == False:
            for cp, paths in tSkinImport[tSkin.get()].items():
                #if the characterpart is the body, just set the assetpath to be the import 
                if cp == "Body":
                    AssetPath = paths
                    break

                #uasset is the asset and mesh is the mesh path
                uasset, mesh = paths
                wfile.write(f'from = import "{uasset}";\n')
                wfile.write(f'search = from.CreateSoftObjectProperty("{mesh}");\n')
                #invalidate the unneeded mesh
                wfile.write('replace = from.CreateSoftObjectProperty("/Game/invalid.invalid");\n')
                wfile.write('from.SwapSoftObjectProperty(search, replace);\n')
                wfile.write('from.Save();\n\n\n')

            
        if pathtoexists == True:
            fromar = "\nfrom = import \"" + AssetPath + "\"" + ";\n"
            wfile.write(fromar)
            toar = "to = import \"" + AssetPathTo + "\"" + ";" + "\n\n"
            wfile.write(toar)
        elif pathtoexists == False:
            fromar = "\nfrom = import \"" + AssetPath + "\"" + ";" + "\n\n"
            wfile.write(fromar)

        if AssetPathInSigns:
            swaps = x["Swaps"]
        if AssetPathInSigns and notskin == False and tSkin.get() == "Same as plugin":
            wfile.write('from.Invalidate(); \n')
            wfile.write("from.Save(); \n\n\n")
            wfile.write('from = import "FortniteGame/Content/Athena/Heroes/Meshes/Bodies/CP_Athena_Body_F_Fallback.uasset";\n\n')

        if not AssetPathInSigns:
            try:
                swaps = asset["Swaps"]
            except KeyError:
                try:
                    swaps = asset["swaps"]
                except KeyError:
                    swaps = None

        if swaps is None:
            wfile.write("\nfrom.Swap(to);\n")
            wfile.write("from.Save();\n")    
            continue

        swap_items = []
        if difjson == True:
            swap_items = swaps.items()
        elif difjson == False:
            swap_items = [(swap["search"], swap["replace"]) for swap in swaps]
        
        swaps_sorted = sorted(swap_items, key=lambda d: len(d[1]), reverse=True)


        for searchstring, replacestring in swaps_sorted:
            #if not masterskeletalnull(replacestring):

            seekwrite(pathtoexists, wfile, searchstring, replacestring, downloads, notskin, jsonpath)
        if pathtoexists is True:
            wfile.write("\n\nfrom.Swap(to);\n")
            wfile.write("from.Save();\n")
        elif pathtoexists is False:
            wfile.write("from.Save();\n\n")

    if automateall.get() == 1:
        multiprocess(rd_to_csp, os.path.basename(pathfielddata.get()).split(".")[0] + ".rd")
        os.path.basename(pathfielddata.get()).split(".")[0] + ".json"
        os.path.basename(pathfielddata.get()).split(".")[0] + ".rd"
    else:
        pass

    if autocompile.get() == 0:
        converttocsp.pack(padx=5, pady=5, side='right')
    
    elif autocompile.get() == 1:
        multiprocess(rd_to_csp, os.path.basename(pathfielddata.get()).split(".")[0] + ".rd")

    if autodeljson.get() == 1:
        os.remove(os.path.basename(pathfielddata.get()).split(".")[0] + ".json")

    header.configure(text="Done converting to RD!", text_color="white")
    wfile.close()


def rd_to_csp(rd):
    if os.path.exists(rd):
        header.configure("Compiling...", text_color="white")
        if os.path.exists("Radon.Repl.exe"):
            shutil.move("Radon.Repl.exe", os.getenv("LOCALAPPDATA")+"/JsonToRD")
        if os.path.exists(os.getenv("LOCALAPPDATA")+"/JsonToRD/Radon.Repl.exe"):
            sp.run(os.getenv("LOCALAPPDATA")+"/JsonToRD/Radon.repl.exe", input=rd.encode())
            try:
                os.remove(os.getenv("LOCALAPPDATA") + "/saturn/plugins/" + rd + ".csp")
            except FileNotFoundError:
                pass
            shutil.move(os.getcwd() + "\\" + rd + ".csp", "%s\saturn\plugins" % (os.getenv("LOCALAPPDATA")))

            if autodelrd.get() == 1:
                os.remove(os.path.basename(pathfielddata.get()).split(".")[0] + ".rd")
            header.configure(text="Done compiling!", text_color="white")

        elif not os.path.exists(os.getenv("LOCALAPPDATA")+"/JsonToRD/Radon.Repl.exe"):
            if autodowncompiler.get() == 0:
                header.configure(text="Compiler not found!", text_color="red")
                global downloadcompiler
                downloadcompiler = customtkinter.CTkButton(compile_frame, text="Download Compiler", command=lambda: multiprocess(downcompiler, None))
                downloadcompiler.pack(padx=5, pady=5, side="left")
            else:
                multiprocess(downcompiler, None)    
    else:
        header.configure(text="Please convert your json first.", text_color="red")


def downcompiler():
    header.configure(text="Downloading complier...", text_color="white")
    get = requests.get(f"https://cdn.discordapp.com/attachments/1158794948670406746/1183848587805851708/Radon.zip")
    with open("Radon.Repl.zip", "wb") as writing:
        writing.write(get.content)
    shutil.unpack_archive("Radon.Repl.zip", os.getcwd())
    os.remove("Radon.Repl.zip")
    shutil.move("Radon.Repl.exe", os.getenv("LOCALAPPDATA")+"/JsonToRD")
    header.configure(text="Compiler downloaded!", text_color="white")
    try:
        downloadcompiler.forget()
    except NameError:
        pass
    if autodowncompiler.get() == 1:
        multiprocess(rd_to_csp, os.path.basename(pathfielddata.get()).split(".")[0] + ".rd")


def settingspage():
    try:
        settings.destroy()
        info_frame.destroy()
        convert_frame.destroy()
        compile_frame.destroy()
        checkboxframe1.destroy()
        checkboxframe2.destroy()
        tFrame.destroy()
    except:
        pass

    app.geometry("550x120")

    global returntomain, returnicon
    returnicon=customtkinter.CTkImage(Image.open(resource_path("resources\\icons\\return.png")), size=(20, 20))
    returntomain = customtkinter.CTkButton(app, image=returnicon, text="", fg_color="transparent", width=20, height=20, command=mainpage)
    returntomain.pack(padx=5, pady=5, anchor="nw")

    global dropdownframe
    dropdownframe = customtkinter.CTkFrame(app, fg_color="transparent")
    dropdownframe.pack()

    global appearance
    appearancevar = tkinter.StringVar()
    appearance = customtkinter.CTkOptionMenu(dropdownframe, values=["System", "Dark", "Light"], variable=appearancevar, command=lambda appearancevar : customtkinter.set_appearance_mode(appearancevar))
    appearancevar.set("Choose Appearance Color")
    appearance.pack(padx=5, pady=20, side="left")
    
    global theme, themevar
    themevar = tkinter.StringVar()
    theme = customtkinter.CTkOptionMenu(dropdownframe, values=["Blue", "Dark Blue", "Green"], variable=themevar, command=lambda themevar : defcolortheme(themevar))
    themevar.set("Choose Color Theme")
    theme.pack(padx=5, pady=20, side="right")


def mainpage():
    try:
        returntomain.destroy()
        dropdownframe.destroy()
    except:
        pass

    app.geometry("550x285")

    global settings
    settingscog=customtkinter.CTkImage(Image.open(resource_path("resources\\icons\\settings.png")), size=(20, 20))
    settings = customtkinter.CTkButton(app, image=settingscog, text="", fg_color="transparent", width=20, height=20, command=lambda: settingspage())
    settings.pack(padx=5, pady=5, anchor="ne")

    global tFrame
    tFrame = customtkinter.CTkFrame(app, fg_color="transparent")
    tFrame.pack()

    global tInfo
    tInfo = customtkinter.CTkLabel(tFrame, text="UEFN plugin skin to swap from (will get saved)", font=("Arial", 15))
    tInfo.pack(padx=5, pady=5, side="top")

    global tSkin
    tSkinInp = tkinter.StringVar()
    tSkin = customtkinter.CTkOptionMenu(tFrame, values=["Same as plugin", "Jennifer Walters", "Twyn (NOT WORKING RN)", "Lexa"], variable=tSkinInp)
    tSkin.set(prefs["tSkin"])
    tSkin.pack(padx=5, pady=5, side="bottom")

    global info_frame
    info_frame = customtkinter.CTkFrame(app, fg_color="transparent")
    info_frame.pack()

    global header
    header = customtkinter.CTkLabel(info_frame, text="Input the path to your json:", font=("Arial", 20))
    header.pack(padx=6, pady=9)

    jsonpathbuttonpic=customtkinter.CTkImage(Image.open(resource_path("resources\\icons\\upload.png")), size=(27, 27))
    jsonpathbutton = customtkinter.CTkButton(info_frame, height=27, width=27, image=jsonpathbuttonpic, fg_color="transparent", text="", command=lambda : pathfielddata.set(easygui.fileopenbox()))
    jsonpathbutton.pack(padx=5, side='right', anchor="n")

    global pathfielddata
    pathfielddata = tkinter.StringVar()
    pathfield = customtkinter.CTkEntry(info_frame, width=350, height=35, textvariable=pathfielddata)
    pathfield.pack()
    pathfielddata.set("Input Path Here")

    global checkboxframe1
    checkboxframe1 = customtkinter.CTkFrame(app, fg_color="transparent", height=10)
    checkboxframe1.pack()

    global checkboxframe2
    checkboxframe2 = customtkinter.CTkFrame(app, fg_color="transparent", height=10)
    checkboxframe2.pack()

    global automateall
    automateall = customtkinter.CTkCheckBox(checkboxframe1, text="Automate everything", command=toggleall)
    automateall.pack(side="left", padx=15, pady=5)
    if prefs["autoall"] == 1:
        automateall.select()
    
    global plus, minus, options
    plus = customtkinter.CTkImage(Image.open(resource_path("resources\\icons\\plus.png")), size=(12, 12))
    minus = customtkinter.CTkImage(Image.open(resource_path("resources\\icons\\minus.png")), size=(12, 12))
    options = customtkinter.CTkButton(checkboxframe1, text="", fg_color="transparent", image=plus, command=showoptions, width=12, height=12)
    options.pack(side="right")

    global autodowncompiler
    autodowncompiler = customtkinter.CTkCheckBox(checkboxframe2, text = "Auto download compiler if not found", command=lambda : automateall.deselect())
    if prefs["download"] == 1:
        autodowncompiler.select()

    global autocompile
    autocompile = customtkinter.CTkCheckBox(checkboxframe2, text = "Auto compile after converting the plugin", command=lambda : automateall.deselect())
    if prefs["compile"] == 1:
        autocompile.select()

    global autodelrd
    autodelrd = customtkinter.CTkCheckBox(checkboxframe2, text = "Auto delete the RD file after compiling", command=lambda : automateall.deselect())
    if prefs["delrd"] == 1:
        autodelrd.select()

    global autodeljson
    autodeljson = customtkinter.CTkCheckBox(checkboxframe2,text = "Auto delete the JSON file after compiling", command=lambda : automateall.deselect())
    if prefs["deljson"] == 1:
        autodeljson.select()

    global convert_frame
    convert_frame = customtkinter.CTkFrame(app, fg_color="transparent")
    convert_frame.pack()

    global compile_frame
    compile_frame = customtkinter.CTkFrame(app, fg_color="transparent")
    compile_frame.pack()

    converttord = customtkinter.CTkButton(convert_frame, text="Convert to RD", command=lambda : json_to_rd(pathfielddata.get()))
    converttord.pack(padx=5, pady=5, side='left')

    global converttocsp
    converttocsp = customtkinter.CTkButton(convert_frame, text="Compile", command=lambda : multiprocess(rd_to_csp, os.path.basename(pathfielddata.get()).split(".")[0] + ".rd"))


    app.mainloop()



def onexit():
    prefs["appearance"] = customtkinter.get_appearance_mode()
    prefs["deljson"] = autodeljson.get()
    prefs["delrd"] = autodelrd.get()
    prefs["compile"] = autocompile.get()
    prefs["download"] = autodowncompiler.get()
    prefs["autoall"] = automateall.get()
    prefs["tSkin"] = tSkin.get()

    with open(os.getenv("LOCALAPPDATA")+"/JsonToRD/prefs", "wb") as savefile:
        savefile.write(pickle.dumps(prefs))


if __name__ == "__main__":
    global prefs
    prefs = {"appearance": "dark", "theme": "dark-blue", "deljson": "1", "delrd": "1", "compile": "1", "download": "1", "autoall": "1", "tSkin": "Same as plugin"}

    if os.path.exists(os.getenv("LOCALAPPDATA")+"/JsonToRD/prefs"):
        with open(os.getenv("LOCALAPPDATA")+"/JsonToRD/prefs", "rb") as file:
            tempprefs = pickle.loads(file.read())
        for key in tempprefs:
            prefs[key] = tempprefs[key]
    
    customtkinter.set_appearance_mode(prefs["appearance"])
    customtkinter.set_default_color_theme(prefs["theme"])

    app = customtkinter.CTk()
    app.geometry("550x275")
    app.title("Json to RD converter")

    
    mainpage()

atexit.register(onexit)
