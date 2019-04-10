# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 10:20:23 2019
@author: WellenWoo
界面语言设置窗口;
"""
import wx

class LangDialog(wx.Dialog):
    """设置语言的弹窗选择框;"""
    def __init__(self, *arg, **kw):
        # grab the config keyword and remove it from the dict
        self.lang_config = kw["config"]
        del kw['config']
        
        wx.Dialog.__init__(self, *arg, **kw)
                
        self.SetTitle("Language Setting")
        self.Bind(wx.EVT_CHOICE, self.OnChoice)
        self.__layout()
                
    def __layout(self):
        items = ["English","简体中文"]
        
        self.label = wx.StaticText(self, -1, "Language")
        self.choice = wx.Choice(self, choices = items)
        self.choice.SetSelection(0)
        
        self.btn_ok = wx.Button(self, wx.ID_OK, "")
        self.btn_cancel = wx.Button(self, wx.ID_CANCEL, "")
        
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1 = wx.FlexGridSizer(2, 5, 5)
        
        sizer1.Add(self.label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        sizer1.Add(self.choice, 0, wx.EXPAND, 4)
        sizer1.Add(self.btn_ok, 0, 0, 0)
        sizer1.Add(self.btn_cancel, 0, 0, 0)
        
        sizer0.Add(sizer1, 0, wx.ALL | wx.ALIGN_BOTTOM, 4)
        
        self.SetSizer(sizer0)
        sizer0.Fit(self)
        self.Layout()

    def OnChoice(self, evt):
        sel = self.choice.GetSelection()
        if sel == 0:            
            val = "LANGUAGE_ENGLISH"
        elif sel == 1:
            val = "LANGUAGE_CHINESE_SIMPLIFIED" #简体中文
        self.lang_config.Write('lang', val) 
