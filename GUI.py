# RTEMS Configuration GUI file
# Author: Shubham Somani

#!/usr/bin/python

from text import text_parser
import wx
import  wx.lib.scrolledpanel as scrolled
import os,sys
import random
import ConfigParser
import Generator
import re

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
                        # If not defined by default then leave empty
                        if("This is not defined by default" in parameters[section_index][parameter_index+3] or "This option is BSP specific." in parameters[section_index][parameter_index+3]):
                            input_text[section_index][parameter_index]=wx.TextCtrl(page[section_index],wx.ID_ANY,'')

                        # If the data type is of type RTEMS Attributes.
                        elif("RTEMS ATTRIBUTES" in (parameters[section_index][parameter_index+1].strip()).upper()):
                            task_attributes=['RTEMS_NO_FLOATING_POINT','RTEMS_FLOATING_POINT','RTEMS_LOCAL','RTEMS_GLOBAL','RTEMS_DEFAULT_ATTRIBUTES']
                            input_text[section_index][parameter_index]=wx.ComboBox(page[section_index],choices=task_attributes,style=wx.CB_DROPDOWN)
                            input_text[section_index][parameter_index].SetValue('RTEMS_DEFAULT_ATTRIBUTES')

                        # If the data type is of type RTEMS Modes.
                        elif("RTEMS MODE" in (parameters[section_index][parameter_index+1].strip()).upper()):
                            rtems_modes=['RTEMS_PREEMPT','RTEMS_NO_PREEMPT','RTEMS_NO_TIMESLICE','RTEMS_TIMESLICE','RTEMS_ASR','RTEMS_NO_ASR','RTEMS_INTERRUPT_LEVEL(0)','RTEMS_INTERRUPT_LEVEL(n)']
                            input_text[section_index][parameter_index]=wx.ComboBox(page[section_index],choices=rtems_modes,style=wx.CB_DROPDOWN)
                            input_text[section_index][parameter_index].SetValue('RTEMS_NO_PREEMPT')

                        # If default value is in the format- "The default value is xxx."
                        elif("The default value is " in parameters[section_index][parameter_index+3]):
                            temp=parameters[section_index][parameter_index+3].split("The default value is ")
                            temp2=temp[1]
                            if("." in temp2):
                                final=temp2.split(".")
                            #CONFIGURE_INIT_TASK_NAME is an exception as its default value has commas in it.
                            if("," in temp2 and label_text!="CONFIGURE_INIT_TASK_NAME"):
                                final=temp2.split(",")
                            input_text[section_index][parameter_index]=wx.TextCtrl(page[section_index],wx.ID_ANY,final[0])

                        #Else we dont know how to handle it! :(
                        else:
                            input_text[section_index][parameter_index]=wx.TextCtrl(page[section_index],wx.ID_ANY,'Enter Value')


                    # Tooltip showing default value

                    final_string=parameters[section_index][parameter_index+4]
                    if("@code{" in final_string):
                        final_string=final_string.replace("@code{","")
                        final_string=final_string.replace("}","")
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

            #Appending items to menu
            menubar.Append(file1, '&Header')
            self.SetMenuBar(menubar)

            #Items of file
            file1.Append(101, '&Save\tCtrl+S', 'Save the current configurations')
            file1.Append(102, '&Check\tCtrl+K', 'Checks the format of all values')
            file1.Append(103, '&Load\tCtrl+L', 'Load the saved state')
            file1.Append(104, '&Generate\tCtrl+G', 'Generate the header file')
            file1.AppendSeparator()
            file1.Append(105, '&Quit\tCtrl+Q', 'Quit the Application')

            #Event Handler
            self.Bind(wx.EVT_MENU,self.OnSave,id=101)
            self.Bind(wx.EVT_MENU,self.OnCheck,id=102)
            self.Bind(wx.EVT_MENU,self.OnLoad,id=103)
            self.Bind(wx.EVT_MENU,self.OnGenerate,id=104)
            self.Bind(wx.EVT_MENU,self.OnQuit,id=105)

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
            message="The following parameters are not given desired values "
            check_if_all_arguments_are_correct=0
            number_of_sections=len(parameters)
            for section_index in xrange(number_of_sections):
                for parameter_index in range(1,len(parameters[section_index]),6):
                    #print to see if correct parameters reach this function.
                    #label_text=parameters[section_index][parameter_index]
                    #print label_text+"   "+(str)(parameter_index)
                    #print input_text[section_index][parameter_index].GetValue()

                    if(parameters[section_index][parameter_index+1].strip()!="Boolean feature macro."):


                        if(input_text[section_index][parameter_index].GetValue()==""):
                            continue

                        #Validation stub if data type is RTEMS Name
                        if ("RTEMS NAME" in parameters[section_index][parameter_index+1].upper()):
                            value_entered=input_text[section_index][parameter_index].GetValue()
                            value_entered=value_entered.strip()
                            if re.match("^[0-9]+$", value_entered):
                                if (int)(value_entered)>= 0:
                                    continue
                            if "RTEMS_BUILD_NAME( 'U', 'I', '1', ' ' )" ==(value_entered.strip()).upper():
                                continue

                        #Validation stub if data type is function pointer
                        if("function pointer" in parameters[section_index][parameter_index+1] or "Function pointer" in parameters[section_index][parameter_index+1]):
                            value_entered=input_text[section_index][parameter_index].GetValue()
                            # Checking if the first character does not have a number.
                            if re.match("^[A-Za-z_]+$", value_entered[0]):
                                # Checking if the string has only characters -> (a-z, A-Z, 0-9, '_' )
                                if re.match("^[A-Za-z0-9_]+$", value_entered.strip()):
                                    continue

                        #Validation stub if data type is RTEMS Attributes or RTEMS Mode.
                        if("RTEMS ATTRIBUTES" in parameters[section_index][parameter_index+1].upper() or "RTEMS MODE" in parameters[section_index][parameter_index+1].upper()):
                            value_entered=input_text[section_index][parameter_index].GetValue()
                            if re.match("^[A-Za-z_0-9() ]+$", value_entered.strip()):
                                continue

                        #Validation stub if data type is an integer
                        if ("integer" in parameters[section_index][parameter_index+1] or "TASK ARGUMENT" in parameters[section_index][parameter_index+1].upper()):
                            value_entered=input_text[section_index][parameter_index].GetValue()
                            if re.match("^[A-Za-z0-9*+-/_ ]+$", value_entered.strip()):
                                continue

                        #Validation stub if data type is of type task priority.
                        if("TASK PRIORITY" in parameters[section_index][parameter_index+1].upper()):
                            value_entered=input_text[section_index][parameter_index].GetValue()
                            if (re.match("^[0-9]+$", value_entered)):
                                value_entered=(int)(value_entered.strip())
                                if(value_entered>=1 and value_entered<=255):
                                    continue

                        check_if_all_arguments_are_correct=1
                        message=message+"\n"+parameters[section_index][parameter_index]

            if check_if_all_arguments_are_correct == 1:
                dial = wx.MessageDialog(None,message, 'RTEMS Format Checker', wx.OK)
            else:
                dial = wx.MessageDialog(None,'All arguments are in correct format.'+'\n'+'Save Configurations and then generate header! :)', 'RTEMS Format Checker', wx.OK)
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

        def OnGenerate(self, event):
            Generator.create_header(parameters)
            dial = wx.MessageDialog(None,'Header file Generated', 'RTEMS', wx.OK)
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

