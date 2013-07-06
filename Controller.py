import wx
import os
import GUI
from text import text_parser

class Frame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title, pos=(150,150), size=(400,350))

        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

        m_text = wx.StaticText(panel, -1, "Welcome to RTEMS Configuration Tool!")
        m_text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        m_text.SetSize(m_text.GetBestSize())

        but=wx.Button(panel, 1, 'Open')
        but.SetToolTip(wx.ToolTip("Please select conf.t from RTEMS"))
        self.Bind(wx.EVT_BUTTON, self.OnOpen, id=1)

        self.Centre()

        box.AddSpacer((150,75))
        box.Add(m_text, 1, wx.CENTER)
        box.Add(but,0, wx.CENTER)
        box.AddSpacer((75,75))
        
        panel.SetSizer(box)
        #panel.Layout()

    def OnOpen(self,e):
        """ Open a file"""
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            data = open(os.path.join(self.dirname, self.filename), 'r')
            contents=data.readlines()
            parameters=text_parser.return_parameters(contents)
            GUI.set_parameters(parameters)
            
            data.close()
        dlg.Destroy()
    

app = wx.App(redirect=True)
top = Frame("RTEMS")
top.Show()
app.MainLoop()
