# RTEMS Configuration GUI file
# Author: Shubham Somani

#!/usr/bin/python

from text import text_parser
import wx
import  wx.lib.scrolledpanel as scrolled
import os,sys
import random
import ConfigParser

# List of parameters to be read from file

parameters={}

def main():

    #This is the array of all fields in the GUI.It is declared globally so that other functions can access values entered in the fields.
    input_text=[[None for x in range(100)] for y in range(120)]

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
            inputsizer={}
            pagesizer={}
            page={}


            # Creation of sizer for panel and notebook
            topsizer=wx.BoxSizer(wx.VERTICAL)
            notebook=wx.Notebook(self.panel)


    #----------------------------Dynamic Creation of GUI starts-----------------------------------------


            # The first loop is for the creation of tabs in the GUI
            #print parameters
            number_of_sections=len(parameters)
            for section_index in xrange(number_of_sections):
                section_name=parameters[section_index][0]
                page[section_index]=Page(notebook)
                page[section_index].SetupScrolling()
                notebook.AddPage(page[section_index],section_name)
                pagesizer[section_index]=wx.BoxSizer(wx.VERTICAL)

                # The second loop is for information inside each page.
                # It is incremented by 6 every time as each set is of the form {parameter name, data type, range, default value, description, notes}

                for parameter_index in range(1,len(parameters[section_index]),6):

                    #Parameter name

                    label_text=parameters[section_index][parameter_index]
                    label[parameter_index]= wx.StaticText(page[section_index],wx.ID_ANY,label_text)

                    # Data Type and default value

                    if(parameters[section_index][parameter_index+1].strip()=="Boolean feature macro."):
                        input_text[section_index][parameter_index]=wx.CheckBox(page[section_index], wx.ID_ANY, '', (10, 10))
                    else:
                        if("The default value is " in parameters[section_index][parameter_index+3]):
                            temp=parameters[section_index][parameter_index+3].split("The default value is ")
                            temp2=temp[1]
                            if("." in temp2):
                                final=temp2.split(".")

                            #CONFIGURE_INIT_TASK_NAME is an exception as its default value has commas in it.
                            if("," in temp2 and label_text!="CONFIGURE_INIT_TASK_NAME"):
                                final=temp2.split(",")
                            input_text[section_index][parameter_index]=wx.TextCtrl(page[section_index],wx.ID_ANY,final[0])
                        else:
                            input_text[section_index][parameter_index]=wx.TextCtrl(page[section_index],wx.ID_ANY,'Enter Value')

                    # Tooltip showing default value

                    final_string=parameters[section_index][parameter_index+4]
                    if("@code{" in final_string):
                        temporary_string=final_string.split("@code{")
                        temporary_string_2=temporary_string[1].split("}")
                        final_string=temporary_string_2[0]+temporary_string_2[1]
                    label[parameter_index].SetToolTip(wx.ToolTip(final_string))

                    # Sizers

                    inputsizer[parameter_index]=wx.BoxSizer(wx.HORIZONTAL)
                    inputsizer[parameter_index].Add(label[parameter_index],0,wx.ALL,10)
                    inputsizer[parameter_index].Add(input_text[section_index][parameter_index],1,wx.ALL|wx.EXPAND,10)
                    pagesizer[section_index].Add(inputsizer[parameter_index],0,wx.ALL|wx.EXPAND,10)
                page[section_index].SetSizer(pagesizer[section_index])
            topsizer.Add(notebook,1,wx.EXPAND)
            self.panel.SetSizer(topsizer)
            #topsizer.Fit(self)

    #-----------------------------Dynamic Creation of GUI ends--------------------------------------------

            #menubar related details
            #Items of menu
            menubar = wx.MenuBar()
            file1=wx.Menu()
            edit=wx.Menu()
            help1=wx.Menu()

            #Appending items to menu
            menubar.Append(file1, '&File')
            menubar.Append(edit, '&Edit')
            menubar.Append(help1, '&Help')
            self.SetMenuBar(menubar)

            #Items of file
            file1.Append(101, '&Open', 'Open the existing configuration file')
            file1.Append(102, '&Save\tCtrl+S', 'Save the current configurations')
            file1.AppendSeparator()
            file1.Append(103, '&Check', 'Checks the format of all values')
            file1.Append(104, '&Load', 'Load the saved state')
            file1.Append(105, '&Quit\tCtrl+Q', 'Quit the Application')

            #Event Handler
            self.Bind(wx.EVT_MENU,self.OnOpen,id=101)
            self.Bind(wx.EVT_MENU,self.OnSave,id=102)
            self.Bind(wx.EVT_MENU,self.OnCheck,id=103)
            self.Bind(wx.EVT_MENU,self.OnLoad,id=104)
            self.Bind(wx.EVT_MENU,self.OnQuit,id=105)

        def OnOpen(self, event):
            dlg = wx.FileDialog(self,"Choose a file",os.getcwd(),"","*.*",wx.OPEN)
            if dlg.ShowModal() == wx.ID_OK:
                    path = dlg.GetPath()
                    mypath = os.path.basename(path)
                    self.SetStatusText("You selected: %s" %mypath)
            dlg.Destroy()

        def OnSave(self, event):

            index=0
            #using python's config parser
            config=ConfigParser.RawConfigParser()

            number_of_sections=len(parameters)
            section_name="start"
            config.add_section(section_name)

            for section_index in xrange(number_of_sections):
                for parameter_index in range(1,len(parameters[section_index]),6):
                    config.set(section_name,parameters[section_index][parameter_index],input_text[section_index][parameter_index].GetValue())
                    #index=index+1

            #writing into configuration.ini
            with open('configuration.ini','wb') as configfile:
                config.write(configfile)

            dial = wx.MessageDialog(None,'Values Saved', 'RTEMS', wx.OK)
            dial.ShowModal()


        def OnCheck(self, event):
            #INCOMPLETE
            message="The following parameters are not given desired values "
            number_of_sections=len(parameters)
            for section_index in xrange(number_of_sections):
                for parameter_index in range(1,len(parameters[section_index]),6):
                    #print to see if correct parameters reach this function.
                    #label_text=parameters[section_index][parameter_index]
                    #print label_text+"   "+(str)(parameter_index)
                    #print input_text[section_index][parameter_index].GetValue()
                    if(parameters[section_index][parameter_index+1].strip()!="Boolean feature macro."):

                        # Conditions not correct. Have to be changed according to ranges once they are updated.
                        if(input_text[section_index][parameter_index].GetValue()=="0" or input_text[section_index][parameter_index].GetValue()=="Enter Value"):
                            continue
                        else:
                            message=message+"\n"+parameters[section_index][parameter_index]
            dial = wx.MessageDialog(None,message, 'Not Compatible Data Types', wx.OK)
            dial.ShowModal()

        def OnLoad(self,event):
            #Method to read from configuration.ini

            config=ConfigParser.RawConfigParser()

            config.read('configuration.ini')
            section_name="start"
            number_of_sections=len(parameters)

            for section_index in xrange(number_of_sections):
                for parameter_index in range(1,len(parameters[section_index]),6):
                    temp=config.get("start",parameters[section_index][parameter_index])
                    if(parameters[section_index][parameter_index+1].strip()=="Boolean feature macro."):
                        if(temp=="True"):
                            input_text[section_index][parameter_index].SetValue(1)
                        else:
                            input_text[section_index][parameter_index].SetValue(0)
                        parameter_index=parameter_index+6
                        continue

                    input_text[section_index][parameter_index].SetValue(temp)

            dial = wx.MessageDialog(None,'Values Loaded', 'RTEMS', wx.OK)
            dial.ShowModal()

        def OnQuit(self,event):
            self.Close()

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

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   main()


# This function is called from the controller to set the parameter array and create the view
def set_parameters(data):
    global parameters
    parameters=data
    main()

