# -*- coding:utf-8 -*-

import wx
import os
from wx.lib.wordwrap import wordwrap
import  wx.lib.dialogs
from Wins import LangDialog

__author__ = 'WellenWoo'

_ = wx.GetTranslation

Keys = 'abcdefghijklmnopqrstuvwxyz0123456789'
Values = ['.-','-...','-.-.','-..','.','..-.','--.','....',
          '..','.---','-.-','.-..','--','-.','---','.--.',
          '--.-','.-.','...','-', '..-','...-','.--','-..-',
          '-.--','--..','-----','.----','..---','...--',
          '....-','.....','-....','--...','---..','----.']
CODE = dict(zip(Keys.upper(), Values))

class MainWindow(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(800,400))

        self.lang_config = wx.Config()
        self.__lang_init()
        
        self.contents = wx.TextCtrl (self,style=wx.TE_MULTILINE |wx.TE_BESTWRAP)
        self.contents.SetBackgroundColour((80,180,30))
        self.coder = wx.TextCtrl (self,style=wx.TE_MULTILINE | wx.TE_BESTWRAP )
        self.coder.SetBackgroundColour((20,200,100))

        self.msgFont = self.contents.GetFont()
        self.msgColour = wx.BLACK
        font = wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.contents.SetFont(font)
        self.coderFont = self.coder.GetFont()
        self.coderColour = wx.BLACK
        self.coder.SetFont(font)

        self.findData = wx.FindReplaceData()

        """创建状态栏"""
        self.CreateStatusBar()   
        
        """file菜单布局"""
        filemenu = wx.Menu()
        self.menuNew = filemenu.Append(wx.ID_NEW  ,"&New\tCtrl+N","New a file 新建")
        self.menuOpen = filemenu.Append(wx.ID_OPEN ,"&Open\tCtrl+O","Open a file 打开")
        self.menuSave = filemenu.Append(wx.ID_SAVE  ,"&Save\tCtrl+S","Save the file 保存")

        """菜单分隔线"""
        filemenu.AppendSeparator()   
        self.menuPageSetup = filemenu.Append(wx.ID_ANY   ,"&PageSetup","Setup the page 页面设置")
        self.menuPrint = filemenu.Append(wx.ID_PRINT   ,"&Print\tCtrl+P","Print the file 打印")
        filemenu.AppendSeparator()
        self.menuExit = filemenu.Append(wx.ID_EXIT   ,"E&xit\tCtrl+Q","Tenminate the program 退出")

        """edit菜单布局"""
        editmenu = wx.Menu ()
        self.menuFind = editmenu.Append(wx.ID_FIND ,"&Find\tCtrl+F","Find the choosen contents 查找")
        self.menuReplace = editmenu.Append(wx.ID_REPLACE  ,"&Replace\tCtrl+R","Replace the choosen contents 替代")
        editmenu.AppendSeparator()
        self.menuSelectAll = editmenu.Append(wx.ID_SELECTALL ,"Select&All","Select all 全选")

        """格式菜单布局"""
        formatmenu = wx.Menu ()
        self.menuMsgFont = formatmenu.Append(wx.ID_ANY ,"&msg Font","Set the message font 设置输入字体")
        self.menuCoderFont = formatmenu.Append(wx.ID_ANY ,"&coder Font","Set the coder font 设置输出字体")
        self.menulang = formatmenu.Append(wx.ID_ANY, _("Language"), _("set GUI language"))

        """帮助菜单布局"""
        helpmenu = wx.Menu ()
        self.menuhelpdoc = helpmenu.Append(wx.ID_ANY ,"usage\tF1","usage 使用说明")
        self.menuAbout = helpmenu.Append(wx.ID_ABOUT ,"&About","Information about this program 关于本软件")
             
        """菜单栏布局"""
        menuBar = wx.MenuBar ()
        menuBar.Append(filemenu,_("&File"))
        menuBar.Append(editmenu,_("&Edit"))
        menuBar.Append(formatmenu,_("&Format"))
        menuBar.Append(helpmenu,_("&Help"))
        self.SetMenuBar(menuBar)

        self.__DoLayout()
        self.__Binds()
        
    def __DoLayout(self):
        """创建按钮"""
        self.MsgFontButton = wx.Button (self,label = _('Message Font'))
        self.CoderFontButton = wx.Button(self,label = _("Coder Font"))
        
        self.encoderButton = wx.Button (self,label = _('Encode'))
        self.decoderButton = wx.Button (self,label = _('Decode'))

        """布局"""
        self.sizer0 = wx.BoxSizer (wx.HORIZONTAL )
        
        self.sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer1.Add(self.MsgFontButton, 1, wx.EXPAND)
        self.sizer1.Add(self.CoderFontButton, 1, wx.EXPAND)
        
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer2.Add(self.encoderButton, 1, wx.EXPAND)
        self.sizer2.Add(self.decoderButton, 1, wx.EXPAND)
            
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.sizer0, 0, wx.EXPAND)
        self.sizer.Add(self.sizer1, 0, wx.EXPAND)
        self.sizer.Add(self.contents, 1, wx.EXPAND)
        self.sizer.Add(self.coder, 1, wx.EXPAND)
        self.sizer.Add(self.sizer2, 0, wx.EXPAND)

        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)

        """显示布局"""
        self.Show(True)
        
    def __Binds(self):     
        """函数绑定"""
        self.Bind(wx.EVT_MENU,self.OnAbout,self.menuAbout)
        self.Bind(wx.EVT_MENU,self.OnExit,self.menuExit)
        self.Bind(wx.EVT_MENU,self.OnOpen,self.menuOpen)
        self.Bind(wx.EVT_MENU,self.OnSave,self.menuSave)
        self.Bind(wx.EVT_MENU,self.OnPrint,self.menuPrint)
        self.Bind(wx.EVT_MENU,self.OnNew,self.menuNew)
        self.Bind(wx.EVT_MENU,self.OnPageSetup,self.menuPageSetup)

        self.Bind(wx.EVT_MENU,self.OnShowFind,self.menuFind)
        self.Bind(wx.EVT_MENU,self.OnShowFindReplace,self.menuReplace)
        
        self.Bind(wx.EVT_MENU,self.OnSelectFont,self.menuMsgFont)
        self.Bind(wx.EVT_MENU,self.OnSelectCoderFont,self.menuCoderFont)
        self.Bind(wx.EVT_MENU, self.set_lang, self.menulang)

        self.Bind(wx.EVT_MENU,self.Onhelpdoc,self.menuhelpdoc)
        
        self.Bind(wx.EVT_BUTTON,self.OnSelectFont,self.MsgFontButton)
        self.Bind(wx.EVT_BUTTON,self.OnSelectCoderFont,self.CoderFontButton)
        
        self.Bind(wx.EVT_BUTTON,self.Encode,self.encoderButton)
        self.Bind(wx.EVT_BUTTON,self.Decode,self.decoderButton)        

    def __lang_init(self):
        """语言设置初始化;"""
        language = self.lang_config.Read('lang', 'LANGUAGE_DEFAULT')

        # Setup the Locale
        self.locale = wx.Locale(getattr(wx, language))

        path = os.path.abspath("./locale") + os.path.sep
        self.locale.AddCatalogLookupPathPrefix(path)
#        self.locale.AddCatalog(self.GetAppName())
        self.locale.AddCatalog("Detector")

    def set_lang(self, evt):
        """设置语言;"""
        self.ch_lang = LangDialog(self, -1, config = self.lang_config)
        self.ch_lang.Show(True)
        
    def OnAbout(self, evt):
        """About 函数"""
        info = wx.AboutDialogInfo()
        info.Name = "Morse Encoder"
        info.Version = "6.1"
        info.Copyright = "(C) 2019 All Right Reserved"
        info.Description = wordwrap('''
Morse code is a method of transmitting text
information as a series of on-off tones, lights,
or clicks that can be directly understood by
a skilled listener or observer without special equipment.\n''',
        350,wx.ClientDC(self.coder))
        info.WebSite = ("https://github.com/WellenWoo/morse", "feedback")
        info.Developers = [ "Wellen Woo\n wellenwoo@163.com" ]        
        wx.AboutBox(info)
        
    def OnPageSetup(self, evt):
        """PageSetup函数"""
        data = wx.PageSetupDialogData()
        data.SetMarginTopLeft( (15, 15) )
        data.SetMarginBottomRight( (15, 15) )
        data.SetPaperId(wx.PAPER_A4)
        dlg = wx.PageSetupDialog(self, data)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetPageSetupData()
            tl = data.GetMarginTopLeft()
            br = data.GetMarginBottomRight()
        dlg.Destroy()

    def OnExit(self,event):
        self.Close(True)
        
    def OnOpen(self,event):
        """Open 函数"""
        self.dirname=''
        dlg = wx.FileDialog(self,_("choose a file"),self.dirname,"","*.*",wx.OPEN )
        if dlg.ShowModal()==wx.ID_OK :
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname,self.filename),'r')
            self.contents.SetValue(f.read())
            f.close()
        dlg.Destroy()
        
    def OnSave(self,event):
        """Save 函数"""
        s1 = self.contents.GetValue()
        s2 = self.coder.GetValue()
        s3 = s1+'\n=============\n'+s2
        
        self.dirname=''
        dlg = wx.FileDialog(self,_("save the file"),self.dirname,"","*.txt",wx.SAVE )
        if dlg.ShowModal()==wx.ID_OK :
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f1 = os.path.join(self.dirname,self.filename)
            with open(f1,'a') as f:
                f.write(s3.encode('utf8'))
                f.close()                         
        dlg.Destroy()
    
    def OnNew(self,event):
        """New 函数"""
        app = wx.App(False)
        frame = MainWindow(None, _('Moser'))
        app.MainLoop()
    
    def OnPrint(self,event):
        """Print 函数 """
        data = wx.PrintDialogData()
        data.EnableSelection(True)
        data.EnablePrintToFile(True)
        data.EnablePageNumbers(True)
        data.SetMinPage(1)
        data.SetMaxPage(5)
        data.SetAllPages(True)
        dlg = wx.PrintDialog(self, data)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetPrintDialogData()
        dlg.Destroy()
       
    def Onhelpdoc(self, evt):
        """操作说明函数"""
        f0 = "README.md"
        with open(f0,"r") as f:
            helpdoc = f.read()        
        dlg = wx.lib.dialogs.ScrolledMessageDialog(self, helpdoc, "helpdoc使用说明")
        dlg.ShowModal()
        
    def BindFindEvents(self, win):
        """查找及替换函数"""
        win.Bind(wx.EVT_FIND, self.OnFind)
        win.Bind(wx.EVT_FIND_NEXT, self.OnFind)
        win.Bind(wx.EVT_FIND_REPLACE, self.OnFind)
        win.Bind(wx.EVT_FIND_REPLACE_ALL, self.OnFind)

    def OnShowFind(self, evt):       
        dlg = wx.FindReplaceDialog(self, self.findData, "Find")
        self.BindFindEvents(dlg)
        dlg.Show(True)

    def OnShowFindReplace(self, evt):
        dlg = wx.FindReplaceDialog(self, self.findData, _("Find & Replace"), wx.FR_REPLACEDIALOG)
        self.BindFindEvents(dlg)
        dlg.Show(True)

    def OnFind(self, evt):
        print repr(evt.GetFindString()), repr(self.findData.GetFindString())
        map = {
            wx.wxEVT_COMMAND_FIND : "FIND",
            wx.wxEVT_COMMAND_FIND_NEXT : "FIND_NEXT",
            wx.wxEVT_COMMAND_FIND_REPLACE : "REPLACE",
            wx.wxEVT_COMMAND_FIND_REPLACE_ALL : "REPLACE_ALL",
            }

        et = evt.GetEventType()
        
        if et in map:
            evtType = map[et]
        else:
            evtType = "**Unknown Event Type**"

        if et in [wx.wxEVT_COMMAND_FIND_REPLACE, wx.wxEVT_COMMAND_FIND_REPLACE_ALL]:
            replaceTxt = "Replace text: %s" % evt.GetReplaceString()
        else:
            replaceTxt = ""

    
    def Encode(self,event):
        """编码函数"""       
        msg = self.contents.GetValue()
        self.coder.Clear()
        for char in msg:
                if char == ' ':
                    self.coder.GetValue()

                    print
                else:
                    text = CODE[char.upper()] + '   '
                    self.coder.GetValue()
                    self.coder.write("%s " %  (text))
                    
    def Decode(self,event):
        """解码函数""" 
        Decode_value = CODE.keys()
        Decode_key = CODE.values()
        Decode_dict = dict(zip(Decode_key,Decode_value))
        
        msg = self.contents.GetValue()
        self.coder.Clear()
        msg1 = msg.split()
        text = []
        for str in msg1:
            if str in Decode_dict.keys():
                text.append(Decode_dict[str])
        self.coder.write("%s " % (text))
   
    def OnSelectFont(self, evt):
        """设置contents字体 """
        msg = self.contents.GetValue()
        data = wx.FontData()
        data.EnableEffects(True)
        data.SetColour(self.msgColour)         # set colour
        data.SetInitialFont(self.msgFont)

        dlg = wx.FontDialog(self, data)
        
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetFontData()
            font = data.GetChosenFont()
            colour = data.GetColour()

            self.msgFont = font
            self.msgColour = colour
            self.contents.SetFont(self.msgFont)
            self.contents.SetForegroundColour(self.msgColour)
        dlg.Destroy()
  
    def OnSelectCoderFont(self, evt):
        """设置coder字体"""
        coder = self.coder.GetValue()
        data = wx.FontData()
        data.EnableEffects(True)
        data.SetColour(self.coderColour)         # set colour
        data.SetInitialFont(self.coderFont)

        dlg = wx.FontDialog(self, data)
        
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetFontData()
            font = data.GetChosenFont()
            colour = data.GetColour()

            self.coderFont = font
            self.coderColour = colour
            self.coder.SetFont(self.coderFont)
            self.coder.SetForegroundColour(self.coderColour)
        dlg.Destroy()

if __name__=='__main__':
    app = wx.App(False)
    frame = MainWindow(None, 'Morse')
    app.MainLoop()
