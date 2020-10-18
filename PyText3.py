#!/usr/bin/env python3

"""
The main file for a basic code editor written
entirely with the python standard library

main.py
PyText3 Text Editor

Created by Kaleb Rosborough on 10/23/2018
Copyright © Shock9616 2018 All rights reserved
"""

#region Imports
from tkinter import *
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, END
from tkinter import ttk
import os
import sys
import prefs
import themes

try:
    # Try to import third party modules.
    import syntaxhighlighting
except ImportError:
    pass
#endregion

#region Global Variables
COL_BG = "grey"
COL_FG = "white"
CURRENT_FILE = "untitled"
#endregion

#region Custom Classes
class TextLineNumbers(tk.Canvas):
    """ Custom canvas class for creating line numbers """
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, fillcolor):
        """ redraw line numbers """
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, fill=fillcolor)
            i = self.textwidget.index("%s+1line" % i)

class CustomText(tk.Text):
    """ A custom text field class that can have line numbers attatched to it """
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        try:
            result = self.tk.call(cmd)
        except Exception:
            return None

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "replace", "delete") or
                args[0:3] == ("mark", "set", "insert") or
                args[0:2] == ("xview", "moveto") or
                args[0:2] == ("xview", "scroll") or
                args[0:2] == ("yview", "moveto") or
                args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result

    ##########################################
#endregion
#region Command Definitions

def onChange(event):
    fillColor = "#FFFFFF"
    linenumbers.redraw(fillcolor=fillColor)
    cursorPos = (textField.index(INSERT)).split(".")

    lineCount.config(text=("Line: " + cursorPos[0]))
    columnCount.config(text=("Column: " + str(int(cursorPos[1]) + 1)))

    # syntaxhighlighting.HighlightSyntax(textField, defaultTheme, language)

def closeWindow(event=None):
    if messagebox.askyesno("Quit", "Are you sure you want to exit?", icon="question"):
        if messagebox.askyesno("Save", "Would you like to save the current file?", icon="question"):
            saveFile()
        root.destroy()
        quit(1)

#region File Menu Commands
def newFile(event=None):
    # if len(textField.get("1.0", END + "-1c")) > 0: # If there is something in the file
    if messagebox.askyesno("Save", "Would you like to save the current file?", icon="question"):
        saveFile()
        textField.delete("1.0", tk.END)

    else:
        textField.delete("1.0", tk.END)

def openFile(event=None):
    file = filedialog.askopenfile(parent=root, mode="rb", title="Select a file to open")
    if messagebox.askyesno("Save", "Would you like to save the current file?", icon="question"):
        saveFile()
    if file is not None:
        contents = file.read()
        textField.delete("1.0", END)
        textField.insert("1.0", contents)
        CURRENT_FILE = file.name
        root.title(CURRENT_FILE)
        file.close()

#######################################################

def saveFileAs(event=None):
    selectedLanguage = language.get()
    if selectedLanguage == prefs.LANGUAGES[0]:
        file = filedialog.asksaveasfile(mode="w", defaultextension=".cpp", filetypes=(
            ("C++ File", "*.cpp"),
            ("HTML File", "*.html"),
            ("Java File", "*.java"),
            ("JavaScript File", "*.js"),
            ("Python File", "*.py"),
            ("Swift File", "*.swift"),
            ("Text File", "*.txt"),
            ("All Files", "*.*")
        ))
    elif selectedLanguage == prefs.LANGUAGES[1]:
        file = filedialog.asksaveasfile(mode="w", defaultextension=".html", filetypes=(
            ("HTML File", "*.html"),
            ("C++ File", "*.cpp"),
            ("Java File", "*.java"),
            ("JavaScript File", "*.js"),
            ("Python File", "*.py"),
            ("Swift File", "*.swift"),
            ("Text File", "*.txt"),
            ("All Files", "*.*")
        ))
    elif selectedLanguage == prefs.LANGUAGES[2]:
        file = filedialog.asksaveasfile(mode="w", defaultextension=".java", filetypes=(
            ("Java File", "*.java"),
            ("C++ File", "*.cpp"),
            ("HTML File", "*.html"),
            ("JavaScript File", "*.js"),
            ("Python File", "*.py"),
            ("Swift File", "*.swift"),
            ("Text File", "*.txt"),
            ("All Files", "*.*")
        ))
    elif selectedLanguage == prefs.LANGUAGES[3]:
        file = filedialog.asksaveasfile(mode="w", defaultextension=".js", filetypes=(
            ("JavaScript File", "*.js"),
            ("C++ File", "*.cpp"),
            ("HTML File", "*.html"),
            ("Java File", "*.java"),
            ("Python File", "*.py"),
            ("Swift File", "*.swift"),
            ("Text File", "*.txt"),
            ("All Files", "*.*")
        ))
    elif selectedLanguage == prefs.LANGUAGES[4]:
        file = filedialog.asksaveasfile(mode="w", defaultextension=".txt", filetypes=(
            ("Text File", "*.txt"),
            ("C++ File", "*.cpp"),
            ("HTML File", "*.html"),
            ("Java File", "*.java"),
            ("JavaScript File", "*.js"),
            ("Python File", "*.py"),
            ("Swift File", "*.swift"),
            ("All Files", "*.*")
        ))
    elif selectedLanguage == prefs.LANGUAGES[5]:
        file = filedialog.asksaveasfile(mode="w", defaultextension=".py", filetypes=(
            ("Python File", "*.py"),
            ("C++ File", "*.cpp"),
            ("HTML File", "*.html"),
            ("Java File", "*.java"),
            ("JavaScript File", "*.js"),
            ("Swift File", "*.swift"),
            ("Text File", "*.txt"),
            ("All Files", "*.*")
        ))
    elif selectedLanguage == prefs.LANGUAGES[6]:
        file = filedialog.asksaveasfile(mode="w", defaultextension=".swift", filetypes=(
            ("Swift File", "*.swift"),
            ("C++ File", "*.cpp"),
            ("HTML File", "*.html"),
            ("Java File", "*.java"),
            ("JavaScript File", "*.js"),
            ("Python File", "*.py"),
            ("Text File", "*.txt"),
            ("All Files", "*.*")
        ))
    else:
        file = filedialog.asksaveasfile(mode="w", defaultextension=".", filetypes=(
            ("All Files", "*.*"),
            ("Text File", "*.txt"),
            ("C++ File", "*.cpp"),
            ("HTML File", "*.html"),
            ("Java File", "*.java"),
            ("JavaScript File", "*.js"),
            ("Python File", "*.py"),
            ("Swift File", "*.swift")
        ))

    if file is None:
        return
    fileContent = textField.get(1.0, "end")
    file.write(fileContent)
    CURRENT_FILE = file.name
    root.title(CURRENT_FILE)
    file.close()

def saveFile(event=None):
    print("Saving file...")
    exists = os.path.isfile(str(CURRENT_FILE))
    if exists:
        with open(CURRENT_FILE, "w") as file:
            file.write(textField.get("1.0", "end"))
    else:
        saveFileAs()

#######################################################

#endregion
#region Edit Menu Commands
def undo(event=None):
    textField.event_generate("<<Undo>>")

def redo(event=None):
    textField.event_generate("<<Redo>>")

#######################################################
def copySelected(event=None):
    selectedText = textField.selection_get()
    root.clipboard_clear()
    root.clipboard_append(selectedText)

def cutSelected(event=None):
    textField.event_generate("<<Cut>>")

def paste(event=None):
    textField.event_generate("<<Paste>>")
    return "break"

def selectAll(event=None):
    textField.tag_add(SEL, "1.0", END)
    textField.mark_set(INSERT, "1.0")
    textField.see(INSERT)
    return "break"

#######################################################
def find(event=None):
    textField.tag_remove("found", "1.0", END)
    searchedText = simpledialog.askstring("Find", "Enter the text you want to find:")
    if searchedText == "":
        done = messagebox.showerror("Find", "Error: You did not enter any text")
    if searchedText:
        idx = "1.0"
        while 1:
            idx = textField.search(searchedText, idx, nocase=1, stopindex=END)
            if not idx:
                break
            lastidx = "%s+%dc" % (idx, len(searchedText))
            textField.tag_add("found", idx, lastidx)
            idx = lastidx
        done = messagebox.showinfo("Find", "Highlighting all instances of " + searchedText + ".")
        if done:
            textField.tag_remove("found", "1.0", END)

def replace(event=None):
    searchedText = simpledialog.askstring("Replace", "Enter the text you want to replace:")
    if searchedText:
        idx = "1.0"
        while 1:
            idx = textField.search(searchedText, idx, nocase=1, stopindex=END)
            if not idx:
                break
            lastidx = "%s+%dc" % (idx, len(searchedText))
            textField.tag_add("replace", idx, lastidx)
            idx = lastidx

    replaceText = simpledialog.askstring("Replace", "Enter the text you want to replace with:")
    if replaceText:
        idx = "1.0"
        while 1:
            idx = textField.search(searchedText, idx, nocase=1, stopindex=END)
            if not idx:
                break
            start = textField.index("replace.first")
            end = textField.index("replace.last")
            textField.insert(end, replaceText)
            textField.delete(start, end)
#endregion
#region Options Menu Commands
def openPreferences():
    def applySettings():
        newFont = font.get()
        fontSaveFile = open("font.sav", "w+")
        fontSaveFile.write(newFont)
        fontSaveFile.close()
        if sys.platform.startswith("darwin"):
            textField.configure(font=(newFont, 12))
        else:
            textField.configure(font=(newFont, 10))

        newTheme = theme.get()
        themeSaveFile = open("theme.sav", "w+")
        themeSaveFile.write(newTheme)
        themeSaveFile.close()
        themes.setTheme(textField, linenumbers, newTheme)

    def applyAndCloseSettings():
        applySettings()
        pw.destroy()

    def cancelSettings():
        pw.destroy()

    pw = Toplevel()
    pw.minsize(width=250, height=226)
    pw.title("Preferences")
    if sys.platform.startswith("darwin"):
        pw.iconbitmap("images/settingsicon.icns")
    else:
        pw.iconbitmap("images/settingsicon.ico")

    pw.wm_attributes("-topmost", 1)

    labelColumn = 0
    listColumn = 1

    fontRow = 0
    themeRow = 1

    # ***** Font Settings *****
    currentFont = open("font.sav", "r").readline()

    font = StringVar(pw)
    if currentFont in prefs.FONTS:
        font.set(currentFont)
    else:
        font.set(prefs.FONTS[2])  # Default font

    fontLabel = Label(pw, text="Font", padx=10)
    fontLabel.grid(row=0, column=0)

    fontList = OptionMenu(pw, font, *prefs.FONTS)
    fontList.config(width=15)
    fontList.grid(row=0, column=1)

    # ***** Theme Settings *****
    currentTheme = open("theme.sav", "r").readline()

    theme = StringVar(pw)
    if currentTheme in prefs.THEMES:
        theme.set(currentTheme)  # Default Theme
    else:
        theme.set(prefs.THEMES[26])

    themeLabel = Label(pw, text="Theme", padx=10)
    themeLabel.grid(row=1, column=0)

    themeList = OptionMenu(pw, theme, *prefs.THEMES)
    themeList.config(width=15)
    themeList.grid(row=1, column=1)

    # ***** Preview *****
    PREVEIW_TEXT = Text(pw, width=48, height=11)
    previewTextContent = prefs.PREVEIW_TEXT
    PREVEIW_TEXT.insert(END, previewTextContent)
    PREVEIW_TEXT.config(state="disabled")
    PREVEIW_TEXT.grid(row=0, column=3, rowspan=3, columnspan=15, padx=5, pady=5)

    # ***** Apply, Ok, and Cancel buttons *****
    okButton = Button(pw, text="Ok", command=applyAndCloseSettings)
    okButton.grid(row=5, column=13, padx=5, pady=5)

    applyButton = Button(pw, text="Apply", command=applySettings)
    applyButton.grid(row=5, column=14, padx=5, pady=5)

    cancelButton = Button(pw, text="Cancel", command=cancelSettings)
    cancelButton.grid(row=5, column=15, padx=5, pady=5)

    pw.mainloop()
#endregion
#region Help Menu Commands
def aboutPyText3(event=None):
    label = messagebox.showinfo("About PyText3", "Shock9616\nVersion: 1.0\n© 2018 Shock9616 All rights reserved",
                                icon="info")

def showCredits(event=None):
    cw = messagebox.showinfo("PyText3 Credits", prefs.CREDITS_TEXT, icon="info")
#endregion

#endregion

#region UI Setup
if __name__ == "__main__":
    print("Running PyText3 on " + sys.platform)

    root = tk.Tk()
    root.configure()
    root.minsize(width=650, height=450)
    root.title(CURRENT_FILE)
    if sys.platform.startswith("darwin"):
        root.iconbitmap("images/icon.icns")
    else:
        root.iconbitmap("images/icon.ico")
    root.protocol("WM_DELETE_WINDOW", closeWindow)

    textFont = open("font.sav", "r").readline()

    #region Set up basic UI elements

    defaultTheme = open("theme.sav", "r").readline()
    defaultFont = open("font.sav", "r").readline()

    toolBar = Frame(root, bd=1, relief="sunken")
    toolBar.pack(side="top", fill="x")

    textField = CustomText(root, wrap=NONE, undo=True, border=0)
    hsb = tk.Scrollbar(orient="horizontal", command=textField.xview)
    vsb = tk.Scrollbar(orient="vertical", command=textField.yview)
    textField.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set, font=(textFont, 10))
    textField.tag_configure("bigfont", font=("Helvetica", "10", "bold"))
    textField.tag_configure("found", background="gray")
    textField.tag_configure("replace", background="gray")
    if sys.platform.startswith("darwin"):
        textField.configure(font=(defaultFont, 12))
    else:
        textField.configure(font=(defaultFont, 10))
    linenumbers = TextLineNumbers(width=30, highlightthickness=1)
    linenumbers.attach(textField)

    statusBar = Frame(root, bd=1, height=50, relief="sunken")
    statusBar.pack(side="bottom", fill="x")

    hsb.pack(side="bottom", fill="x")
    vsb.pack(side="right", fill="y")
    linenumbers.pack(side="left", fill="y")
    textField.pack(side="right", fill="both", expand=True)

    textField.bind("<<Change>>", onChange)
    textField.bind("<Configure>", onChange)

    linenumbers.configure(highlightthickness=0)

    themes.setTheme(textField, linenumbers, defaultTheme)

    cursorPos = str(textField.index(INSERT)).split(".")
    #endregion
    #region Set up menu bar
    menuBar = Menu(root)
    root.config(menu=menuBar)

    #region Create Menu Bar Sub-Menus
    fileMenu = Menu(menuBar, tearoff=False)
    menuBar.add_cascade(label="File", menu=fileMenu)
    editMenu = Menu(menuBar, tearoff=False)
    menuBar.add_cascade(label="Edit", menu=editMenu)
    optionsMenu = Menu(menuBar, tearoff=False)
    menuBar.add_cascade(label="Options", menu=optionsMenu)
    #endregion
    #region Fill Sub-Menus for Windows and Linux
    if sys.platform.startswith("win32") or sys.platform.startswith("linux"):
        # ***** File Menu *****
        fileMenu.add_command(label="New File", command=newFile, accelerator="Ctrl+N")
        fileMenu.add_command(label="Open", command=openFile, accelerator="Ctrl+O")
        fileMenu.add_separator()
        fileMenu.add_command(label="Save", command=saveFile, accelerator="Ctrl+S")
        fileMenu.add_command(label="Save As", command=saveFileAs, accelerator="Ctrl+^+N")

        # ***** Edit Menu *****
        editMenu.add_command(label="Undo", command=undo, accelerator="Ctrl+Z")
        editMenu.add_command(label="Redo", command=redo, accelerator="Ctrl+^+Z")
        editMenu.add_separator()
        editMenu.add_command(label="Cut", command=cutSelected, accelerator="Ctrl+X")
        editMenu.add_command(label="Copy", command=copySelected, accelerator="Ctrl+C")
        editMenu.add_command(label="Paste", command=paste, accelerator="Ctrl+V")
        editMenu.add_command(label="Select All", command=selectAll, accelerator="Ctrl+A")
        editMenu.add_separator()
        editMenu.add_command(label="Find", command=find, accelerator="Ctrl+F")
        editMenu.add_command(label="Replace", command=replace, accelerator="Ctrl+H")

        # ***** Options Menu *****
        optionsMenu.add_command(label="Preferences", command=openPreferences)
    #endregion
    #region Fill Sub-Menus for Mac OS
    elif sys.platform.startswith("darwin"):
        # ***** File Menu *****
        fileMenu.add_command(label="New File", command=newFile, accelerator="Cmd+N")
        fileMenu.add_command(label="Open", command=openFile, accelerator="Cmd+O")
        fileMenu.add_separator()
        fileMenu.add_command(label="Save", command=saveFile, accelerator="Cmd+S")
        fileMenu.add_command(label="Save As", command=saveFileAs, accelerator="Cm^+S")

        # ***** Edit Menu *****
        editMenu.add_command(label="Undo", command=undo, accelerator="Cmd+Z")
        editMenu.add_command(label="Redo", command=redo, accelerator="Cmd+Shift+Z")
        editMenu.add_separator()
        editMenu.add_command(label="Cut", command=cutSelected, accelerator="Cmd+X")
        editMenu.add_command(label="Copy", command=copySelected, accelerator="Cmd+C")
        editMenu.add_command(label="Paste", command=paste, accelerator="Cmd+V")
        editMenu.add_command(label="Select All", command=selectAll, accelerator="CtCmd")
        editMenu.add_separator()
        editMenu.add_command(label="Find", command=find, accelerator="Cmd+F")
        editMenu.add_command(label="Replace", command=replace, accelerator="Cmd+H")

        # ***** Options Menu *****
        optionsMenu.add_command(label="Preferences", command=openPreferences, accelerator="Cmd+,")
    #endregion
    #region Help Menu
    helpMenu = Menu(menuBar, tearoff=False)
    menuBar.add_cascade(menu=helpMenu, label="Help")
    helpMenu.add_command(label="About", command=aboutPyText3)
    helpMenu.add_command(label="Credits", command=showCredits)
    #endregion
    #region Status Bar
    lineCount = Label(statusBar, text=("Line " + cursorPos[0]), bd=1)
    lineCount.pack(side="left")

    columnCount = Label(statusBar, text=("Column " + cursorPos[1]), bd=1)
    columnCount.pack(side="left")

    language = StringVar(root)
    language.set(prefs.LANGUAGES[4])

    languageSwitcher = OptionMenu(statusBar, language, *prefs.LANGUAGES)
    languageSwitcher.config(indicator=False, compound="none", relief="flat")
    languageSwitcher.pack(side="right", expand="no", fill="y")

    separator = ttk.Separator(statusBar, orient="vertical")
    separator.pack(side="right", fill="y")
    #endregion
    #endregion
    #region Set up key bindings
    #region Windows and Linux
    if sys.platform.startswith("win32") or sys.platform.startswith("linux"):
        textField.bind("<Control-n>", newFile)
        textField.bind("<Control-N>", newFile)
        textField.bind("<Control-o>", openFile)
        textField.bind("<Control-O>", openFile)
        textField.bind("<Control-s>", saveFile)
        textField.bind("<Control-S>", saveFile)
        textField.bind("<Control-Shift-s>", saveFileAs)
        textField.bind("<Control-Shift-S>", saveFileAs)
        textField.bind("<Control-n>", newFile)
        textField.bind("<Control-n>", newFile)
        textField.bind("<Control-q>", closeWindow)
        textField.bind("<Control-Q>", closeWindow)

        textField.bind("<Control-z>", undo)
        textField.bind("<Control-Z>", undo)
        textField.bind("<Control-Shift-z>", redo)
        textField.bind("<Control-Shift-Z>", redo)
        textField.bind("<Control-c>", copySelected)
        textField.bind("<Control-C>", copySelected)
        textField.bind("<Control-v>", paste)
        textField.bind("<Control-V>", paste)
        textField.bind("<Control-a>", selectAll)
        textField.bind("<Control-A>", selectAll)
        textField.bind("<Control-f>", find)
        textField.bind("<Control-F>", find)
        textField.bind("<Control-h>", replace)
        textField.bind("<Control-H>", replace)
    #endregion
    #region Mac OS
    elif sys.platform.startswith("darwin"):
        textField.bind("<Command-n>", newFile)
        textField.bind("<Command-N>", newFile)
        textField.bind("<Command-o>", openFile)
        textField.bind("<Command-O>", openFile)
        textField.bind("<Command-s>", saveFile)
        textField.bind("<Command-S>", saveFile)
        textField.bind("<Command-Shift-s>", saveFileAs)
        textField.bind("<Command-Shift-S>", saveFileAs)
        textField.bind("<Command-n>", newFile)
        textField.bind("<Command-n>", newFile)
        textField.bind("<Command-q>", closeWindow)
        textField.bind("<Command-Q>", closeWindow)

        textField.bind("<Command-z>", undo)
        textField.bind("<Command-Z>", undo)
        textField.bind("<Command-Shift-z>", redo)
        textField.bind("<Command-Shift-Z>", redo)
        textField.bind("<Command-x>", cutSelected)
        textField.bind("<Command-X>", cutSelected)
        textField.bind("<Command-c>", copySelected)
        textField.bind("<Command-C>", copySelected)
        textField.bind("<Command-v>", paste)
        textField.bind("<Command-V>", paste)
        textField.bind("<Command-a>", selectAll)
        textField.bind("<Command-A>", selectAll)
        textField.bind("<Command-f>", find)
        textField.bind("<Command-F>", find)
        textField.bind("<Command-h>", replace)
        textField.bind("<Command-H>", replace)
    #endregion
    #endregion

    root.mainloop()
#endregion
