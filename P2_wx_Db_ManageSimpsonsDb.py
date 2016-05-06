import wx, db_program, os, sqlite3

class Frame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title, size=(800,600))
        panel=wx.Panel(self)

        menuBar = wx.MenuBar()
        
        fileMenu = wx.Menu()
        newItem = fileMenu.Append(wx.NewId(), "New", "Create a new file")
        self.Bind(wx.EVT_MENU, self.notImplemented, newItem)
        openItem = fileMenu.Append(wx.NewId(), "Open", "Open a file")
        self.Bind(wx.EVT_MENU, self.notImplemented, openItem)
        saveItem = fileMenu.Append(wx.NewId(), "Save", "Save this file")
        self.Bind(wx.EVT_MENU, self.notImplemented, saveItem)
        saveasItem = fileMenu.Append(wx.NewId(), "Save As", "Save this file with a new name")
        self.Bind(wx.EVT_MENU, self.notImplemented, saveasItem)
        closeItem = fileMenu.Append(wx.NewId(), "Close", "Close this file")
        self.Bind(wx.EVT_MENU, self.notImplemented, closeItem)
        fileMenu.AppendSeparator()
        exitItem = fileMenu.Append(wx.NewId(), "Exit", "Exit and close this frame")
        self.Bind(wx.EVT_MENU, self.exitProgram, exitItem)
        
        aboutMenu = wx.Menu()
        aboutItem = aboutMenu.Append(wx.ID_ABOUT, "About", "More information")
        self.Bind(wx.EVT_MENU, self.onAbout, aboutItem)

        menuBar.Append(fileMenu, "File")
        menuBar.Append(aboutMenu, "About")
        self.SetMenuBar(menuBar)

        self.CreateStatusBar()

        #*****Add New Character
        mybox = wx.StaticBox(panel, label="Add a new character", pos=(20,40), size=(280,240))
        wx.StaticText(mybox, label="Name:", pos=(30,40))
        wx.StaticText(mybox, label="Gender:", pos=(30,80))
        wx.StaticText(mybox, label="Age:", pos=(30,120))
        wx.StaticText(mybox, label="Occupation:", pos=(30,160))
        self.sName = wx.TextCtrl(mybox, size=(150,-1), pos=(130,40))
        self.sGen = wx.TextCtrl(mybox, size=(150,-1), pos=(130,80))
        self.sAge = wx.SpinCtrl(mybox, value="0", size=(70,25), pos=(130,120))
        self.sOcc = wx.TextCtrl(mybox, size=(150,-1), pos=(130,160))
        save = wx.Button(mybox, label="Add Character", pos=(100,200))
        save.Bind(wx.EVT_BUTTON, self.addCharacter)

        #*****Table
        self.listCtrl = wx.ListCtrl(panel, size=(400,400), pos=(350,40), style=wx.LC_REPORT |wx.BORDER_SUNKEN)
        self.listCtrl.InsertColumn(0, "ID")
        self.listCtrl.InsertColumn(1, "Name")
        self.listCtrl.InsertColumn(2, "Gender")
        self.listCtrl.InsertColumn(3, "Age")
        self.listCtrl.InsertColumn(4, "Occupation")

        #*****Delete
        deleteButton = wx.Button(panel, label="Delete", pos=(640, 450))
        self.listCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onSelect)
        deleteButton.Bind(wx.EVT_BUTTON, self.onDelete)

        self.fillListCtrl()
        self.Show()

    def exitProgram(self, event):
        self.Destroy()

    def notImplemented(self, event):
        dlg = wx.MessageDialog(self, "This item is not yet implemented.  So sorry.", "Unimplemented Item", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def onAbout(self, event):
        dlg = wx.MessageDialog(self, "This is a Python GUI-based program to interact with a simple database.  The GUI is powered by wxPython", "About", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def addCharacter(self, event):
        name = self.sName.GetValue()
        gen = self.sGen.GetValue()
        age = self.sAge.GetValue()
        occ = self.sOcc.GetValue()

        if (name == '') or (gen == '') or (age == '0') or (occ == ''):
            dlg = wx.MessageDialog(None, "Some character details are missing.  Enter values in each box.", "Missing Details", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return False
                               
        db_program.newCharacter(name, gen, age, occ)
        print db_program.viewAll()

        self.sName.Clear()
        self.sGen.Clear()
        self.sOcc.Clear()
        self.sAge.SetValue(0)

        self.fillListCtrl()

    def fillListCtrl(self):
        self.allData = db_program.viewAll()
        self.listCtrl.DeleteAllItems()
        for row in self.allData:
            print row
            self.listCtrl.Append(row)

    def onSelect(self, event):
        self.selectedId = event.GetText()

    def onDelete(self, event):
        db_program.deleteCharacter(self.selectedId)
        self.fillListCtrl()

app = wx.App()
frame = Frame("Python GUI")
app.MainLoop()
        
    
