#!/bin/python
"""
Hello World, but with more meat.
"""

import wx
import wx.lib.buttons as buttons
from conjureAnimals import ConjureAnimalsGenerator

class ConjureAnimalsGeneratorFrame(wx.Frame):

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(ConjureAnimalsGeneratorFrame, self).__init__(*args, **kw)
        # create a panel in the frame
        self.panel = wx.Panel(self)

        # and put some text with a larger bold font on it
        st = wx.StaticText(self.panel, label="Conjure Animals v1.0", pos=(7,7))
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)

        # create a menu bar
        self.makeMenuBar()

        conjureButton = buttons.GenButton(self.panel, -1, "Conjure!", pos=(25, 50))
        conjureButton.Bind(wx.EVT_BUTTON, self.onConjureButton)


    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """
        
        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        loadFileItem = fileMenu.Append(-1, "&Load File...\tCtrl-L", 
                "Choose a .json or .txt file to load as the animal set")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. on the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.onExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.onAbout, aboutItem)
        self.Bind(wx.EVT_MENU, self.onLoadFile, loadFileItem)




    def onExit(self, event):
        self.Close(True)

    def onLoadFile(self, event):
        openFileDialog = wx.FileDialog(self, "Open", "", "", 
                                      "JSON file (*.json)|*.json", 
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()

        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed their mind

        # Proceed loading the file chosen by the user
        pathname = openFileDialog.GetPath()
        try:
            self.animalGenerator = ConjureAnimalsGenerator(pathname)
        except IOError:
            wx.LogError("Cannot open file '%s'." % pathname)
        openFileDialog.Destroy()


    def onAbout(self, event):
        wx.MessageBox("This is a wxPython GUI for the Conjure Animals spell in D&D 5e." +
                      "\nSee Hobbs96 on github for more.", 
                      "About Conjure Animals",
                      wx.OK|wx.ICON_INFORMATION)

    def onConjureButton(self, event):
        pass



if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = ConjureAnimalsGeneratorFrame(None, title='Conjure Animals')
    frm.Show()
    app.MainLoop()