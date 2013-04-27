# RTEMS Configuration GUI file
# Author: Shubham Somani

#!/usr/bin/python
import config_parser

import wx
import  wx.lib.scrolledpanel as scrolled
import os,sys
import random

parameters={}

#creating a configuration file
config_parser.write()

#reading from the configuration file
parameters=config_parser.read()

class Page(scrolled.ScrolledPanel):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent,style = wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)

class MyApp(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title, wx.DefaultPosition, wx.Size(1366, 768))
        
        # Creation of panel
        
        self.panel = wx.Panel(self, wx.ID_ANY)

        
        # Declaration of variables
        
        label={}
        input_text={}
        inputsizer={}
        pagesizer={}
        page={}
        id_number=0


        # Creation of sizer for panel and notebook
        
        topsizer=wx.BoxSizer(wx.VERTICAL)
        notebook=wx.Notebook(self.panel)


#----------------------------Dynamic Creation of GUI starts-----------------------------------------

        
        # The first loop is for the creation of tabs in the GUI

        number_of_sections=len(parameters)
        for section_index in xrange(number_of_sections):
            section_name=parameters[section_index][0]
            page[section_index]=Page(notebook)
            notebook.AddPage(page[section_index],section_name)
            pagesizer[section_index]=wx.BoxSizer(wx.VERTICAL)

            # The second loop is for information inside each page.
            # It is incremented by 3 every time as each set is of the form {parameter name,data type,default value}

            for parameter_index in range(1,len(parameters[section_index]),3):

                #Parameter name

                label_text=parameters[section_index][parameter_index]
                label[id_number]= wx.StaticText(page[section_index],wx.ID_ANY,label_text)

                # Data Type

                if(parameters[section_index][parameter_index+1].strip()=="Boolean feature macro."):
                    input_text[id_number]=wx.CheckBox(page[section_index], wx.ID_ANY, '', (10, 10))
                else:
                    if("The default for this field is " in parameters[section_index][parameter_index+2]):
                        temp=parameters[section_index][parameter_index+2].split("The default for this field is ")
                        temp2=temp[1]
                        final=temp2.split(".")
                        input_text[id_number]=wx.TextCtrl(page[section_index],wx.ID_ANY,final[0])
                    else:
                        input_text[id_number]=wx.TextCtrl(page[section_index],wx.ID_ANY,'Enter Value')

                # Tooltip showing default value

                label[id_number].SetToolTip(wx.ToolTip(parameters[section_index][parameter_index+2]))

                # Sizers

                inputsizer[id_number]=wx.BoxSizer(wx.HORIZONTAL)
                inputsizer[id_number].Add(label[id_number],0,wx.ALL,10)
                inputsizer[id_number].Add(input_text[id_number],1,wx.ALL|wx.EXPAND,10)
                pagesizer[section_index].Add(inputsizer[id_number],0,wx.ALL|wx.EXPAND,10)
            page[section_index].SetSizer(pagesizer[section_index])
        topsizer.Add(notebook,1,wx.EXPAND)
        self.panel.SetSizer(topsizer)
        topsizer.Fit(self)
        
#-----------------------------Dynamic Creation of GUI ends--------------------------------------------

        #menubar related details
        #Items of menu
        menubar = wx.MenuBar()
        file1=wx.Menu()
        edit=wx.Menu()
        help1=wx.Menu()

        #Items of file
        file1.Append(101, '&Open', 'Open the existing configuration file')
        file1.Append(102, '&Save\tCtrl+S', 'Save the current configurations')
        file1.AppendSeparator()
        file1.Append(103, '&Quit\tCtrl+Q', 'Quit the Application')

        #Appending items to menu
        menubar.Append(file1, '&File')  
        menubar.Append(edit, '&Edit') 
        menubar.Append(help1, '&Help')
        self.SetMenuBar(menubar)

        #Event Handler
        self.Bind(wx.EVT_MENU,self.OnQuit,id=103)
        self.Bind(wx.EVT_MENU,self.OnOpen,id=101)        
        
    def OnQuit(self,event):
        self.Close()

    def OnOpen(self, event):
        dlg = wx.FileDialog(self,"Choose a file",os.getcwd(),"","*.*",wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                mypath = os.path.basename(path)
                self.SetStatusText("You selected: %s" %mypath)
        dlg.Destroy()

#Main Class
class RTEMS_Configuration_GUI(wx.App):
    def OnInit(self):
        #Call to Application class
        frame=MyApp(None,-1,'RTEMS')
        frame.SetToolTip(wx.ToolTip('Configuration GUI'))
        frame.CreateStatusBar()
        frame.Show(True)
        return True

app= RTEMS_Configuration_GUI(0)
app.MainLoop()
