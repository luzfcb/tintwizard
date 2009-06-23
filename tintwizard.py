#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import os
import sys
import signal
import webbrowser
import math

# Project information
NAME = "tintwizard"
AUTHORS = ["Euan Freeman <euan04@gmail.com>"]
VERSION = "0.1.4"
COMMENTS = "tintwizard generates config files for the lightweight panel replacement tint2"
WEBSITE = "http://code.google.com/p/tintwizard/"

# Default values for text entry fields
BG_ROUNDING = "0"
BG_BORDER = "0"
PANEL_SIZE_X = "0"
PANEL_SIZE_Y = "40"
PANEL_MARGIN_X = "0"
PANEL_MARGIN_Y = "0"
PANEL_PADDING_X = "0"
PANEL_PADDING_Y = "0"
PANEL_MONITOR = "all"
TASKBAR_PADDING_X = "0"
TASKBAR_PADDING_Y = "0"
TASK_BLINKS = "7"
TASK_WIDTH = "200"
TASK_PADDING_X = "0"
TASK_PADDING_Y = "0"
TASK_SPACING = "0"
TRAY_PADDING_X = "0"
TRAY_PADDING_Y = "0"
TRAY_SPACING = "0"
CLOCK_FMT_1 = "%H:%M"
CLOCK_FMT_2 = "%A %d %B"
CLOCK_PADDING_X = "0"
CLOCK_PADDING_Y = "0"
BATTERY_LOW = "20"
BATTERY_ACTION = 'notify-send "battery low"'
BATTERY_PADDING_X = "0"
BATTERY_PADDING_Y = "0"

class TintWizardPrefGUI(gtk.Window):
	"""The dialog window which lets the user change the default preferences."""
	def __init__(self, tw):
		"""Create and shows the window."""
		self.tw = tw
		
		# Create top-level window
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		
		self.set_title("Preferences")
		self.connect("delete_event", self.quit)
		
		self.layout = gtk.Table(2, 2, False)
		
		self.table = gtk.Table(5, 2, False)
		self.table.set_row_spacings(5)
		self.table.set_col_spacings(5)
		
		temp = gtk.Label("Default Font")
		temp.set_alignment(0, 0.5)
		self.table.attach(temp, 0, 1, 0, 1)
		self.font = gtk.FontButton(self.tw.defaults["font"])
		self.font.set_alignment(0, 0.5)
		self.table.attach(self.font, 1, 2, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		temp = gtk.Label("Default Background Color")
		temp.set_alignment(0, 0.5)
		self.table.attach(temp, 0, 1, 1, 2)
		self.bgColor = gtk.ColorButton(gtk.gdk.color_parse(self.tw.defaults["bgColor"]))
		self.bgColor.set_alignment(0, 0.5)
		self.table.attach(self.bgColor, 1, 2, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		temp = gtk.Label("Default Foreground Color")
		temp.set_alignment(0, 0.5)
		self.table.attach(temp, 0, 1, 2, 3)
		self.fgColor = gtk.ColorButton(gtk.gdk.color_parse(self.tw.defaults["fgColor"]))
		self.fgColor.set_alignment(0, 0.5)
		self.table.attach(self.fgColor, 1, 2, 2, 3, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		temp = gtk.Label("Default Border Color")
		temp.set_alignment(0, 0.5)
		self.table.attach(temp, 0, 1, 3, 4)
		self.borderColor = gtk.ColorButton(gtk.gdk.color_parse(self.tw.defaults["borderColor"]))
		self.borderColor.set_alignment(0, 0.5)
		self.table.attach(self.borderColor, 1, 2, 3, 4, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		temp = gtk.Label("Number of Background Styles")
		temp.set_alignment(0, 0.5)
		self.table.attach(temp, 0, 1, 4, 5)
		self.bgCount = gtk.Entry(6)
		self.bgCount.set_width_chars(8)
		self.bgCount.set_text(str(self.tw.defaults["bgCount"]))
		self.table.attach(self.bgCount, 1, 2, 4, 5, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		temp = gtk.Label("Default directory")
		temp.set_alignment(0, 0.5)
		self.table.attach(temp, 0, 1, 5, 6)
		self.dir = gtk.Button(self.tw.defaults["dir"])
		self.dir.connect("clicked", self.chooseFolder)
		self.table.attach(self.dir, 1, 2, 5, 6, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		self.layout.attach(self.table, 0, 2, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND, xpadding=20, ypadding=5)
		
		temp = gtk.Button("Save", gtk.STOCK_SAVE)
		temp.set_name("save")
		temp.connect("clicked", self.save)
		self.layout.attach(temp, 0, 1, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND, ypadding=20)
		temp = gtk.Button("Cancel", gtk.STOCK_CANCEL)
		temp.set_name("cancel")
		temp.connect("clicked", self.quit)
		self.layout.attach(temp, 1, 2, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND, ypadding=20)
		
		self.add(self.layout)
		
		self.show_all()
	
	def chooseFolder(self, widget=None, direction=None):
		"""Called every time the folder button is clicked. Shows a file chooser."""
		chooser = gtk.FileChooserDialog("Choose Default Folder", self, gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		chooser.set_default_response(gtk.RESPONSE_OK)
		
		if self.tw.curDir != None:
			chooser.set_current_folder(self.tw.curDir)
		
		chooser.show()
		
		response = chooser.run()
		
		if response == gtk.RESPONSE_OK:
			self.dir.set_label(chooser.get_filename())
		else:
			chooser.destroy()
			return
		
		chooser.destroy()
	
	def quit(self, widget=None, event=None):
		"""Destroys the window."""
		self.destroy()
	
	def save(self, action=None):
		"""Called when the Save button is clicked."""
		if confirmDialog(self, "Overwrite configuration file?") == gtk.RESPONSE_YES:
			self.tw.defaults["font"] = self.font.get_font_name()
			self.tw.defaults["bgColor"] = rgbToHex(self.bgColor.get_color().red, self.bgColor.get_color().green, self.bgColor.get_color().blue)
			self.tw.defaults["fgColor"] = rgbToHex(self.fgColor.get_color().red, self.fgColor.get_color().green, self.fgColor.get_color().blue)
			self.tw.defaults["borderColor"] = rgbToHex(self.borderColor.get_color().red, self.borderColor.get_color().green, self.borderColor.get_color().blue)
			
			try:
				self.tw.defaults["bgCount"] = int(self.bgCount.get_text())
			except:
				errorDialog(self, "Invalid value for background count")
				return
			
			self.tw.defaults["dir"] = self.dir.get_label()
			self.curDir = self.tw.defaults["dir"]
			
			self.tw.writeConf()
			
			self.quit()

class TintWizardGUI(gtk.Window):
	"""The main window for the application."""
	def __init__(self):
		"""Create and show the window."""
		self.filename = None
		self.curDir = None
		self.toSave = False
		
		# Read conf file and set default values
		self.readConf()
		
		if self.defaults["bgColor"] in [None, "None"]:
			self.defaults["bgColor"] = "#000000"
			
		if self.defaults["fgColor"] in [None, "None"]:
			self.defaults["fgColor"] = "#ffffff"
		
		if self.defaults["borderColor"] in [None, "None"]:
			self.defaults["borderColor"] = "#ffffff"
			
		if self.defaults["dir"] in [None, "None"]:
			if os.path.exists(os.path.expandvars("${HOME}") + "/.config/tint2"):
				self.curDir = os.path.expandvars("${HOME}") + "/.config/tint2"
			else:
				self.curDir = None
		else:
			self.curDir = os.path.expandvars(self.defaults["dir"])
			
			if not os.path.exists(os.path.expandvars(self.curDir)):
				if os.path.exists(os.path.expandvars("${HOME}") + "/.config/tint2"):
					self.curDir = os.path.expandvars("${HOME}") + "/.config/tint2"
				else:
					self.curDir = None
		
		try:
			self.defaults["bgCount"] = int(self.defaults["bgCount"])
		except:
			self.defaults["bgCount"] = 2
			
		# Get the full location of the tint2 binary
		which = os.popen('which tint2')
		
		self.tint2Bin = which.readline().strip()
		
		which.close()
		
		if len(self.tint2Bin) == 0:
			errorDialog(self, "tint2 could not be found. Are you sure it is installed?")
			sys.exit(1)
		
		# Create top-level window
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		
		self.set_title("tintwizard")
		
		self.connect("delete_event", self.quit)
		
		# self.table is our main layout manager
		self.table = gtk.Table(4, 1, False)
		
		# Create menus and toolbar items
		ui = """
		<ui>
			<menubar name="MenuBar">
				<menu action="File">
					<menuitem action="New" />
					<menuitem action="Open" />
					<separator />
					<menuitem action="Save" />
					<menuitem action="Save As..." />
					<separator />
					<menuitem action="Quit" />
				</menu>
				<menu action="Tint2">
					<menuitem action="OpenDefault" />
					<menuitem action="SaveDefault" />
					<separator />
					<menuitem action="Apply" />
				</menu>
				<menu action="Tools">
					<menuitem action="FontChange" />
					<separator />
					<menuitem action="Defaults" />
				</menu>
				<menu action="HelpMenu">
					<menuitem action="Help" />
					<separator />
					<menuitem action="About" />
				</menu>
			</menubar>
			<toolbar name="ToolBar">
				<toolitem action="New" />
				<toolitem action="Open" />
				<toolitem action="Save" />
				<separator />
				<toolitem action="Apply" />
			</toolbar>
		</ui>
		"""
		
		# Set up UI manager
		self.uiManager = gtk.UIManager()
		
		accelGroup = self.uiManager.get_accel_group()
		self.add_accel_group(accelGroup)
		
		self.ag = gtk.ActionGroup("File")
		self.ag.add_actions([("File", None, "_File"),
						("New",gtk.STOCK_NEW, "_New", None, "Create a new config", self.new),
						("Open", gtk.STOCK_OPEN, "_Open", None, "Open an existing config", self.openFile),
						("Save", gtk.STOCK_SAVE, "_Save", None, "Save the current config", self.save),
						("Save As...", gtk.STOCK_SAVE_AS, "Save As", None, "Save the current config as...", self.saveAs),
						("SaveDefault", None, "Save As tint2 Default", None, "Save the current config as the tint2 default", self.saveAsDef),
						("OpenDefault", None, "Open tint2 Default", None, "Open the current tint2 default config", self.openDef),
						("Apply", gtk.STOCK_APPLY, "Apply Config", None, "Apply the current config to tint2", self.apply),
						("Quit", gtk.STOCK_QUIT, "_Quit", None, "Quit the program", self.quit),
						("Tools", None, "_Tools"),
						("Tint2", None, "Tint_2"),
						("HelpMenu", None, "_Help"),
						("FontChange",gtk.STOCK_SELECT_FONT, "Change All Fonts", None, "Change all fonts at once.", self.changeAllFonts),
						("Defaults",gtk.STOCK_PREFERENCES, "Change Defaults", None, "Change tintwizard defaults.", self.changeDefaults),
						("Help",gtk.STOCK_HELP, "_Help", None, "Get help with Tint Wizard", self.help),
						("About",gtk.STOCK_ABOUT, "_About Tint Wizard", None, "Find out more about Tint Wizard", self.about)])#,
						#("Refresh",gtk.STOCK_REFRESH, "_Refresh", None, "Refresh the panel preview", self.refreshClicked)])
		
		
		# Add main UI
		self.uiManager.insert_action_group(self.ag)
		self.uiManager.add_ui_from_string(ui)
		
		# Attach menubar and toolbar to main window
		self.table.attach(self.uiManager.get_widget("/MenuBar"), 0, 4, 0, 1)
		self.table.attach(self.uiManager.get_widget("/ToolBar"), 0, 4, 1, 2)
		
		# Create notebook
		self.notebook = gtk.Notebook()
		self.notebook.set_tab_pos(gtk.POS_TOP)
		
		# Create notebook pages
		# Background Options
		self.tableBgs = gtk.Table(rows=1, columns=1, homogeneous=False)
		self.tableBgs.set_row_spacings(5)
		self.tableBgs.set_col_spacings(5)
		
		self.bgNotebook = gtk.Notebook()
		self.bgNotebook.set_scrollable(True)
		
		self.tableBgs.attach(self.bgNotebook, 0, 2, 0, 1)
		
		self.bgs = []
		
		# Add buttons for adding/deleting background styles
		temp = gtk.Button("New Background", gtk.STOCK_NEW)
		temp.set_name("addBg")
		temp.connect("clicked", self.addBgClick)
		self.tableBgs.attach(temp, 0, 1, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		temp = gtk.Button("Delete Background", gtk.STOCK_DELETE)
		temp.set_name("delBg")
		temp.connect("clicked", self.delBgClick)
		self.tableBgs.attach(temp, 1, 2, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		# Panel Options
		self.tablePanel = gtk.Table(rows=9, columns=3, homogeneous=False)
		self.tablePanel.set_row_spacings(5)
		self.tablePanel.set_col_spacings(5)
		
		temp = gtk.Label("Position")
		temp.set_alignment(0, 0.5)
		self.tablePanel.attach(temp, 0, 1, 0, 1, xpadding=10)
		self.panelPosY = gtk.combo_box_new_text()
		self.panelPosY.append_text("bottom")
		self.panelPosY.append_text("top")
		self.panelPosY.set_active(0)
		self.panelPosY.connect("changed", self.changeOccurred)
		self.tablePanel.attach(self.panelPosY, 2, 3, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		self.panelPosX = gtk.combo_box_new_text()
		self.panelPosX.append_text("left")
		self.panelPosX.append_text("right")
		self.panelPosX.append_text("center")
		self.panelPosX.set_active(0)
		self.panelPosX.connect("changed", self.changeOccurred)
		self.tablePanel.attach(self.panelPosX, 1, 2, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		temp = gtk.Label("Size (x, y)")
		temp.set_alignment(0, 0.5)
		self.tablePanel.attach(temp, 0, 1, 1, 2, xpadding=10)
		self.panelSizeX = gtk.Entry(6)
		self.panelSizeX.set_width_chars(8)
		self.panelSizeX.set_text(PANEL_SIZE_X)
		self.panelSizeX.connect("changed", self.changeOccurred)
		self.tablePanel.attach(self.panelSizeX, 1, 2, 1, 2, xoptions=gtk.EXPAND)
		self.panelSizeY = gtk.Entry(6)
		self.panelSizeY.set_width_chars(8)
		self.panelSizeY.set_text(PANEL_SIZE_Y)
		self.panelSizeY.connect("changed", self.changeOccurred)
		self.tablePanel.attach(self.panelSizeY, 2, 3, 1, 2, xoptions=gtk.EXPAND)
		
		temp = gtk.Label("Margin (x, y)")
		temp.set_alignment(0, 0.5)
		self.tablePanel.attach(temp, 0, 1, 2, 3, xpadding=10)
		self.panelMarginX = gtk.Entry(6)
		self.panelMarginX.set_width_chars(8)
		self.panelMarginX.set_text(PANEL_MARGIN_X)
		self.panelMarginX.connect("changed", self.changeOccurred)
		self.tablePanel.attach(self.panelMarginX, 1, 2, 2, 3, xoptions=gtk.EXPAND)
		self.panelMarginY = gtk.Entry(6)
		self.panelMarginY.set_width_chars(8)
		self.panelMarginY.set_text(PANEL_MARGIN_Y)
		self.panelMarginY.connect("changed", self.changeOccurred)
		self.tablePanel.attach(self.panelMarginY, 2, 3, 2, 3, xoptions=gtk.EXPAND)
		
		temp = gtk.Label("Padding (x, y)")
		temp.set_alignment(0, 0.5)
		self.tablePanel.attach(temp, 0, 1, 3, 4, xpadding=10)
		self.panelPadX = gtk.Entry(6)
		self.panelPadX.set_width_chars(8)
		self.panelPadX.set_text(PANEL_PADDING_Y)
		self.panelPadX.connect("changed", self.changeOccurred)
		self.tablePanel.attach(self.panelPadX, 1, 2, 3, 4, xoptions=gtk.EXPAND)
		self.panelPadY = gtk.Entry(6)
		self.panelPadY.set_width_chars(8)
		self.panelPadY.set_text(PANEL_PADDING_Y)
		self.panelPadY.connect("changed", self.changeOccurred)
		self.tablePanel.attach(self.panelPadY, 2, 3, 3, 4, xoptions=gtk.EXPAND)
		
		temp = gtk.Label("Panel Background ID")
		temp.set_alignment(0, 0.5)
		self.tablePanel.attach(temp, 0, 1, 4, 5, xpadding=10)
		self.panelBg = gtk.combo_box_new_text()
		self.panelBg.append_text("0 (fully transparent)")
		for i in range(len(self.bgs)):
			self.panelBg.append_text(str(i+1))
		self.panelBg.set_active(0)
		self.panelBg.connect("changed", self.changeOccurred)
		self.tablePanel.attach(self.panelBg, 1, 2, 4, 5, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		temp = gtk.Label("Panel Monitor (all, 1, 2...)")
		temp.set_alignment(0, 0.5)
		self.tablePanel.attach(temp, 0, 1, 5, 6, xpadding=10)
		self.panelMonitor = gtk.Entry(6)
		self.panelMonitor.set_width_chars(8)
		self.panelMonitor.set_text(PANEL_MONITOR)
		self.panelMonitor.connect("changed", self.changeOccurred)
		self.tablePanel.attach(self.panelMonitor, 1, 2, 5, 6, xoptions=gtk.EXPAND)
		
		# Taskbar
		self.tableTaskbar = gtk.Table(rows=4, columns=3, homogeneous=False)
		self.tableTaskbar.set_row_spacings(5)
		self.tableTaskbar.set_col_spacings(5)
		
		temp = gtk.Label("Taskbar Mode")
		temp.set_alignment(0, 0.5)
		self.tableTaskbar.attach(temp, 0, 1, 0, 1, xpadding=10)
		self.taskbarMode = gtk.combo_box_new_text()
		self.taskbarMode.append_text("single_desktop")
		self.taskbarMode.append_text("multi_desktop")
		self.taskbarMode.append_text("single_monitor")
		self.taskbarMode.set_active(0)
		self.taskbarMode.connect("changed", self.changeOccurred)
		self.tableTaskbar.attach(self.taskbarMode, 1, 2, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		temp = gtk.Label("Padding (x, y)")
		temp.set_alignment(0, 0.5)
		self.tableTaskbar.attach(temp, 0, 1, 1, 2, xpadding=10)
		self.taskbarPadX = gtk.Entry(6)
		self.taskbarPadX.set_width_chars(8)
		self.taskbarPadX.set_text(TASKBAR_PADDING_X)
		self.taskbarPadX.connect("changed", self.changeOccurred)
		self.tableTaskbar.attach(self.taskbarPadX, 1, 2, 1, 2, xoptions=gtk.EXPAND)
		self.taskbarPadY = gtk.Entry(6)
		self.taskbarPadY.set_width_chars(8)
		self.taskbarPadY.set_text(TASKBAR_PADDING_Y)
		self.taskbarPadY.connect("changed", self.changeOccurred)
		self.tableTaskbar.attach(self.taskbarPadY, 2, 3, 1, 2, xoptions=gtk.EXPAND)
		
		temp = gtk.Label("Taskbar Background ID")
		temp.set_alignment(0, 0.5)
		self.tableTaskbar.attach(temp, 0, 1, 3, 4, xpadding=10)
		self.taskbarBg = gtk.combo_box_new_text()
		self.taskbarBg.append_text("0 (fully transparent)")
		for i in range(len(self.bgs)):
			self.taskbarBg.append_text(str(i+1))
		self.taskbarBg.set_active(0)
		self.taskbarBg.connect("changed", self.changeOccurred)
		self.tableTaskbar.attach(self.taskbarBg, 1, 2, 3, 4, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		# Task Options
		self.tableTask = gtk.Table(rows=12, columns=3, homogeneous=False)
		self.tableTask.set_row_spacings(5)
		self.tableTask.set_col_spacings(5)
		
		temp = gtk.Label("Number of 'Blinks' on Urgent Event")
		temp.set_alignment(0, 0.5)
		self.tableTask.attach(temp, 0, 1, 0, 1, xpadding=10)
		self.taskBlinks = gtk.Entry(6)
		self.taskBlinks.set_width_chars(8)
		self.taskBlinks.set_text(TASK_BLINKS)
		self.taskBlinks.connect("changed", self.changeOccurred)
		self.tableTask.attach(self.taskBlinks, 1, 2, 0, 1, xoptions=gtk.EXPAND)
		
		temp = gtk.Label("Show Text")
		temp.set_alignment(0, 0.5)
		self.tableTask.attach(temp, 0, 1, 1, 2, xpadding=10)
		self.taskTextCheckButton = gtk.CheckButton()
		self.taskTextCheckButton.set_active(True)
		self.taskTextCheckButton.connect("toggled", self.changeOccurred)
		self.tableTask.attach(self.taskTextCheckButton, 1, 2, 1, 2, xoptions=gtk.EXPAND)
		
		temp = gtk.Label("Centre Text")
		temp.set_alignment(0, 0.5)
		self.tableTask.attach(temp, 0, 1, 2, 3, xpadding=10)
		self.taskCentreCheckButton = gtk.CheckButton()
		self.taskCentreCheckButton.set_active(True)
		self.taskCentreCheckButton.connect("toggled", self.changeOccurred)
		self.tableTask.attach(self.taskCentreCheckButton, 1, 2, 2, 3, xoptions=gtk.EXPAND)
		
		temp = gtk.Label("Show Icon")
		temp.set_alignment(0, 0.5)
		self.tableTask.attach(temp, 0, 1, 3, 4, xpadding=10)
		self.taskIconCheckButton = gtk.CheckButton()
		self.taskIconCheckButton.set_active(True)
		self.taskIconCheckButton.connect("toggled", self.changeOccurred)
		self.tableTask.attach(self.taskIconCheckButton, 1, 2, 3, 4, xoptions=gtk.EXPAND)
		
		temp = gtk.Label("Width")
		temp.set_alignment(0, 0.5)
		self.tableTask.attach(temp, 0, 1, 4, 5, xpadding=10)
		self.taskWidth = gtk.Entry(6)
		self.taskWidth.set_width_chars(8)
		self.taskWidth.set_text(TASK_WIDTH)
		self.taskWidth.connect("changed", self.changeOccurred)
		self.tableTask.attach(self.taskWidth, 1, 2, 4, 5, xoptions=gtk.EXPAND)
		
		temp = gtk.Label("Padding (x, y)")
		temp.set_alignment(0, 0.5)
		self.tableTask.attach(temp, 0, 1, 5, 6, xpadding=10)
		self.taskPadX = gtk.Entry(6)
		self.taskPadX.set_width_chars(8)
		self.taskPadX.set_text(TASK_PADDING_X)
		self.taskPadX.connect("changed", self.changeOccurred)
		self.tableTask.attach(self.taskPadX, 1, 2, 5, 6, xoptions=gtk.EXPAND)
		self.taskPadY = gtk.Entry(6)
		self.taskPadY.set_width_chars(8)
		self.taskPadY.set_text(TASK_PADDING_Y)
		self.taskPadY.connect("changed", self.changeOccurred)
		self.tableTask.attach(self.taskPadY, 2, 3, 5, 6, xoptions=gtk.EXPAND)
		
		temp = gtk.Label("Horizontal Spacing")
		temp.set_alignment(0, 0.5)
		self.tableTask.attach(temp, 0, 1, 6, 7, xpadding=10)
		self.taskbarSpacing = gtk.Entry(6)
		self.taskbarSpacing.set_width_chars(8)
		self.taskbarSpacing.set_text(TASK_SPACING)
		self.taskbarSpacing.connect("changed", self.changeOccurred)
		self.tableTask.attach(self.taskbarSpacing, 1, 2, 6, 7, xoptions=gtk.EXPAND)
		
		temp = gtk.Label("Task Background ID")
		temp.set_alignment(0, 0.5)
		self.tableTask.attach(temp, 0, 1, 7, 8, xpadding=10)
		self.taskBg = gtk.combo_box_new_text()
		self.taskBg.append_text("0 (fully transparent)")
		for i in range(len(self.bgs)):
			self.taskBg.append_text(str(i+1))
		self.taskBg.set_active(0)
		self.taskBg.connect("changed", self.changeOccurred)
		self.tableTask.attach(self.taskBg, 1, 2, 7, 8, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		temp = gtk.Label("Task Active Background ID")
		temp.set_alignment(0, 0.5)
		self.tableTask.attach(temp, 0, 1, 8, 9, xpadding=10)
		self.taskActiveBg = gtk.combo_box_new_text()
		self.taskActiveBg.append_text("0 (fully transparent)")
		for i in range(len(self.bgs)):
			self.taskActiveBg.append_text(str(i+1))
		self.taskActiveBg.set_active(0)
		self.taskActiveBg.connect("changed", self.changeOccurred)
		self.tableTask.attach(self.taskActiveBg, 1, 2, 8, 9, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		# Font Options
		self.tableFont = gtk.Table(rows=3, columns=3, homogeneous=False)
		self.tableFont.set_row_spacings(5)
		self.tableFont.set_col_spacings(5)
		
		temp = gtk.Label("Font")
		temp.set_alignment(0, 0.5)
		self.tableFont.attach(temp, 0, 1, 0, 1, xpadding=10)
		self.fontButton = gtk.FontButton()
		
		if self.defaults["font"] in [None, "None"]:						# If there was no font specified in the config file
			self.defaults["font"] = self.fontButton.get_font_name()		# Use the gtk default
		
		self.fontButton.set_font_name(self.defaults["font"])
		self.fontButton.connect("font-set", self.changeOccurred)
		self.tableFont.attach(self.fontButton, 1, 2, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		temp = gtk.Label("Font Color")
		temp.set_alignment(0, 0.5)
		self.tableFont.attach(temp, 0, 1, 1, 2, xpadding=10)
		self.fontCol = gtk.Entry(7)
		self.fontCol.set_width_chars(9)
		self.fontCol.set_name("fontCol")
		self.fontCol.connect("activate", self.colorTyped)
		self.tableFont.attach(self.fontCol, 1, 2, 1, 2, xoptions=gtk.EXPAND)
		self.fontColButton = gtk.ColorButton(gtk.gdk.color_parse(self.defaults["fgColor"]))
		self.fontColButton.set_use_alpha(True)
		self.fontColButton.set_name("fontCol")
		self.fontColButton.connect("color-set", self.colorChange)
		self.tableFont.attach(self.fontColButton, 2, 3, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		self.fontCol.set_text(self.defaults["fgColor"])
		# Add this AFTER we set color to avoid "changed" event
		self.fontCol.connect("changed", self.changeOccurred)
		
		temp = gtk.Label("Active Font Color")
		temp.set_alignment(0, 0.5)
		self.tableFont.attach(temp, 0, 1, 2, 3, xpadding=10)
		self.fontActiveCol = gtk.Entry(7)
		self.fontActiveCol.set_width_chars(9)
		self.fontActiveCol.set_name("fontActiveCol")
		self.fontActiveCol.connect("activate", self.colorTyped)
		self.tableFont.attach(self.fontActiveCol, 1, 2, 2, 3, xoptions=gtk.EXPAND)
		self.fontActiveColButton = gtk.ColorButton(gtk.gdk.color_parse(self.defaults["fgColor"]))
		self.fontActiveColButton.set_use_alpha(True)
		self.fontActiveColButton.set_name("fontActiveCol")
		self.fontActiveColButton.connect("color-set", self.colorChange)
		self.tableFont.attach(self.fontActiveColButton, 2, 3, 2, 3, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		self.fontActiveCol.set_text(self.defaults["fgColor"])
		# Add this AFTER we set color to avoid "changed" event
		self.fontActiveCol.connect("changed", self.changeOccurred)
		
		temp = gtk.Label("Font Shadow")
		temp.set_alignment(0, 0.5)
		self.tableFont.attach(temp, 0, 1, 3, 4, xpadding=10)
		self.fontShadowCheckButton = gtk.CheckButton()
		self.fontShadowCheckButton.set_active(False)
		self.fontShadowCheckButton.connect("toggled", self.changeOccurred)
		self.tableFont.attach(self.fontShadowCheckButton, 1, 2, 3, 4, xoptions=gtk.EXPAND)
		
		# Systray Options
		self.tableTray = gtk.Table(rows=3, columns=3, homogeneous=False)
		self.tableTray.set_row_spacings(5)
		self.tableTray.set_col_spacings(5)
		
		temp = gtk.Label("Show Systray")
		temp.set_alignment(0, 0.5)
		self.tableTray.attach(temp, 0, 1, 0, 1, xpadding=10)
		self.trayCheckButton = gtk.CheckButton()
		self.trayCheckButton.set_active(True)
		self.trayCheckButton.connect("toggled", self.changeOccurred)
		self.tableTray.attach(self.trayCheckButton, 1, 2, 0, 1, xoptions=gtk.EXPAND)
		
		temp = gtk.Label("Padding (x, y)")
		temp.set_alignment(0, 0.5)
		self.tableTray.attach(temp, 0, 1, 1, 2, xpadding=10)
		self.trayPadX = gtk.Entry(6)
		self.trayPadX.set_width_chars(8)
		self.trayPadX.set_text(TRAY_PADDING_X)
		self.trayPadX.connect("changed", self.changeOccurred)
		self.tableTray.attach(self.trayPadX, 1, 2, 1, 2, xoptions=gtk.EXPAND)
		self.trayPadY = gtk.Entry(6)
		self.trayPadY.set_width_chars(8)
		self.trayPadY.set_text(TRAY_PADDING_Y)
		self.trayPadY.connect("changed", self.changeOccurred)
		self.tableTray.attach(self.trayPadY, 2, 3, 1, 2, xoptions=gtk.EXPAND)
		
		temp = gtk.Label("Horizontal Spacing")
		temp.set_alignment(0, 0.5)
		self.tableTray.attach(temp, 0, 1, 2, 3, xpadding=10)
		self.traySpacing = gtk.Entry(6)
		self.traySpacing.set_width_chars(8)
		self.traySpacing.set_text(TRAY_SPACING)
		self.traySpacing.connect("changed", self.changeOccurred)
		self.tableTray.attach(self.traySpacing, 1, 2, 2, 3, xoptions=gtk.EXPAND)
		
		temp = gtk.Label("Systray Background ID")
		temp.set_alignment(0, 0.5)
		self.tableTray.attach(temp, 0, 1, 3, 4, xpadding=10)
		self.trayBg = gtk.combo_box_new_text()
		self.trayBg.append_text("0 (fully transparent)")
		for i in range(len(self.bgs)):
			self.trayBg.append_text(str(i+1))
		self.trayBg.set_active(0)
		self.trayBg.connect("changed", self.changeOccurred)
		self.tableTray.attach(self.trayBg, 1, 2, 3, 4, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		# Clock Options
		self.tableClock = gtk.Table(rows=3, columns=3, homogeneous=False)
		self.tableClock.set_row_spacings(5)
		self.tableClock.set_col_spacings(5)
		
		temp = gtk.Label("Show Clock")
		temp.set_alignment(0, 0.5)
		self.tableClock.attach(temp, 0, 1, 0, 1, xpadding=10)
		self.clockCheckButton = gtk.CheckButton()
		self.clockCheckButton.set_active(True)
		self.clockCheckButton.connect("toggled", self.changeOccurred)
		self.tableClock.attach(self.clockCheckButton, 1, 2, 0, 1, xoptions=gtk.EXPAND)
		
		temp = gtk.Label("Time 1 Format")
		temp.set_alignment(0, 0.5)
		self.tableClock.attach(temp, 0, 1, 1, 2, xpadding=10)
		self.clock1Format = gtk.Entry(50)
		self.clock1Format.set_width_chars(20)
		self.clock1Format.set_text(CLOCK_FMT_1)
		self.clock1Format.connect("changed", self.changeOccurred)
		self.tableClock.attach(self.clock1Format, 1, 2, 1, 2, xoptions=gtk.EXPAND)
		self.clock1CheckButton = gtk.CheckButton("Show")
		self.clock1CheckButton.set_active(True)
		self.clock1CheckButton.connect("toggled", self.changeOccurred)
		self.tableClock.attach(self.clock1CheckButton, 2, 3, 1, 2, xoptions=gtk.EXPAND)
		
		temp = gtk.Label("Time 1 Font")
		temp.set_alignment(0, 0.5)
		self.tableClock.attach(temp, 0, 1, 2, 3, xpadding=10)
		self.clock1FontButton = gtk.FontButton()
		self.clock1FontButton.set_font_name(self.defaults["font"])
		self.clock1FontButton.connect("font-set", self.changeOccurred)
		self.tableClock.attach(self.clock1FontButton, 1, 2, 2, 3, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		temp = gtk.Label("Time 2 Format")
		temp.set_alignment(0, 0.5)
		self.tableClock.attach(temp, 0, 1, 3, 4, xpadding=10)
		self.clock2Format = gtk.Entry(50)
		self.clock2Format.set_width_chars(20)
		self.clock2Format.set_text(CLOCK_FMT_2)
		self.clock2Format.connect("changed", self.changeOccurred)
		self.tableClock.attach(self.clock2Format, 1, 2, 3, 4, xoptions=gtk.EXPAND)
		self.clock2CheckButton = gtk.CheckButton("Show")
		self.clock2CheckButton.set_active(True)
		self.clock2CheckButton.connect("toggled", self.changeOccurred)
		self.tableClock.attach(self.clock2CheckButton, 2, 3, 3, 4, xoptions=gtk.EXPAND)
		
		temp = gtk.Label("Time 2 Font")
		temp.set_alignment(0, 0.5)
		self.tableClock.attach(temp, 0, 1, 4, 5, xpadding=10)
		self.clock2FontButton = gtk.FontButton()
		self.clock2FontButton.set_font_name(self.defaults["font"])
		self.clock2FontButton.connect("font-set", self.changeOccurred)
		self.tableClock.attach(self.clock2FontButton, 1, 2, 4, 5, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		temp = gtk.Label("Clock Font Color")
		temp.set_alignment(0, 0.5)
		self.tableClock.attach(temp, 0, 1, 5, 6, xpadding=10)
		self.clockFontCol = gtk.Entry(7)
		self.clockFontCol.set_width_chars(9)
		self.clockFontCol.set_name("clockFontCol")
		self.clockFontCol.connect("activate", self.colorTyped)
		self.tableClock.attach(self.clockFontCol, 1, 2, 5, 6, xoptions=gtk.EXPAND)
		self.clockFontColButton = gtk.ColorButton(gtk.gdk.color_parse(self.defaults["fgColor"]))
		self.clockFontColButton.set_use_alpha(True)
		self.clockFontColButton.set_name("clockFontCol")
		self.clockFontColButton.connect("color-set", self.colorChange)
		self.tableClock.attach(self.clockFontColButton, 2, 3, 5, 6, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		self.clockFontCol.set_text(self.defaults["fgColor"])
		# Add this AFTER we set color to avoid "changed" event
		self.clockFontCol.connect("changed", self.changeOccurred)
		
		temp = gtk.Label("Padding (x, y)")
		temp.set_alignment(0, 0.5)
		self.tableClock.attach(temp, 0, 1, 6, 7, xpadding=10)
		self.clockPadX = gtk.Entry(6)
		self.clockPadX.set_width_chars(8)
		self.clockPadX.set_text(CLOCK_PADDING_X)
		self.clockPadX.connect("changed", self.changeOccurred)
		self.tableClock.attach(self.clockPadX, 1, 2, 6, 7, xoptions=gtk.EXPAND)
		self.clockPadY = gtk.Entry(6)
		self.clockPadY.set_width_chars(8)
		self.clockPadY.set_text(CLOCK_PADDING_Y)
		self.clockPadY.connect("changed", self.changeOccurred)
		self.tableClock.attach(self.clockPadY, 2, 3, 6, 7, xoptions=gtk.EXPAND)
		
		temp = gtk.Label("Clock Background ID")
		temp.set_alignment(0, 0.5)
		self.tableClock.attach(temp, 0, 1, 7, 8, xpadding=10)
		self.clockBg = gtk.combo_box_new_text()
		self.clockBg.append_text("0 (fully transparent)")
		for i in range(len(self.bgs)):
			self.clockBg.append_text(str(i+1))
		self.clockBg.set_active(0)
		self.clockBg.connect("changed", self.changeOccurred)
		self.tableClock.attach(self.clockBg, 1, 2, 7, 8, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		# Mouse Options
		self.tableMouse = gtk.Table(rows=4, columns=3, homogeneous=False)
		self.tableMouse.set_row_spacings(5)
		self.tableMouse.set_col_spacings(5)
		
		temp = gtk.Label("Middle Mouse Click Action")
		temp.set_alignment(0, 0.5)
		self.tableMouse.attach(temp, 0, 1, 0, 1, xpadding=10)
		self.mouseMiddle = gtk.combo_box_new_text()
		self.mouseMiddle.append_text("none")
		self.mouseMiddle.append_text("close")
		self.mouseMiddle.append_text("toggle")
		self.mouseMiddle.append_text("iconify")
		self.mouseMiddle.append_text("shade")
		self.mouseMiddle.append_text("toggle_iconify")
		self.mouseMiddle.set_active(0)
		self.mouseMiddle.connect("changed", self.changeOccurred)
		self.tableMouse.attach(self.mouseMiddle, 1, 2, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		temp = gtk.Label("Right Mouse Click Action")
		temp.set_alignment(0, 0.5)
		self.tableMouse.attach(temp, 0, 1, 1, 2, xpadding=10)
		self.mouseRight = gtk.combo_box_new_text()
		self.mouseRight.append_text("none")
		self.mouseRight.append_text("close")
		self.mouseRight.append_text("toggle")
		self.mouseRight.append_text("iconify")
		self.mouseRight.append_text("shade")
		self.mouseRight.append_text("toggle_iconify")
		self.mouseRight.set_active(0)
		self.mouseRight.connect("changed", self.changeOccurred)
		self.tableMouse.attach(self.mouseRight, 1, 2, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		temp = gtk.Label("Mouse Wheel Scroll Up Action")
		temp.set_alignment(0, 0.5)
		self.tableMouse.attach(temp, 0, 1, 2, 3, xpadding=10)
		self.mouseUp = gtk.combo_box_new_text()
		self.mouseUp.append_text("none")
		self.mouseUp.append_text("close")
		self.mouseUp.append_text("toggle")
		self.mouseUp.append_text("iconify")
		self.mouseUp.append_text("shade")
		self.mouseUp.append_text("toggle_iconify")
		self.mouseUp.set_active(0)
		self.mouseUp.connect("changed", self.changeOccurred)
		self.tableMouse.attach(self.mouseUp, 1, 2, 2, 3, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		temp = gtk.Label("Mouse Wheel Scroll Down Action")
		temp.set_alignment(0, 0.5)
		self.tableMouse.attach(temp, 0, 1, 3, 4, xpadding=10)
		self.mouseDown = gtk.combo_box_new_text()
		self.mouseDown.append_text("none")
		self.mouseDown.append_text("close")
		self.mouseDown.append_text("toggle")
		self.mouseDown.append_text("iconify")
		self.mouseDown.append_text("shade")
		self.mouseDown.append_text("toggle_iconify")
		self.mouseDown.set_active(0)
		self.mouseDown.connect("changed", self.changeOccurred)
		self.tableMouse.attach(self.mouseDown, 1, 2, 3, 4, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		# Battery Options
		self.tableBattery = gtk.Table(rows=8, columns=3, homogeneous=False)
		self.tableBattery.set_row_spacings(5)
		self.tableBattery.set_col_spacings(5)
		
		temp = gtk.Label("Show Battery Applet")
		temp.set_alignment(0, 0.5)
		self.tableBattery.attach(temp, 0, 1, 0, 1, xpadding=10)
		self.batteryCheckButton = gtk.CheckButton()
		self.batteryCheckButton.set_active(False)
		self.batteryCheckButton.connect("toggled", self.changeOccurred)
		self.tableBattery.attach(self.batteryCheckButton, 1, 2, 0, 1, xoptions=gtk.EXPAND)
		
		temp = gtk.Label("Battery Low Status (%)")
		temp.set_alignment(0, 0.5)
		self.tableBattery.attach(temp, 0, 1, 1, 2, xpadding=10)
		self.batteryLow = gtk.Entry(6)
		self.batteryLow.set_width_chars(8)
		self.batteryLow.set_text(BATTERY_LOW)
		self.batteryLow.connect("changed", self.changeOccurred)
		self.tableBattery.attach(self.batteryLow, 1, 2, 1, 2, xoptions=gtk.EXPAND)
		
		temp = gtk.Label("Battery Low Action")
		temp.set_alignment(0, 0.5)
		self.tableBattery.attach(temp, 0, 1, 2, 3, xpadding=10)
		self.batteryLowAction = gtk.Entry(150)
		self.batteryLowAction.set_width_chars(32)
		self.batteryLowAction.set_text(BATTERY_ACTION)
		self.batteryLowAction.connect("changed", self.changeOccurred)
		self.tableBattery.attach(self.batteryLowAction, 1, 3, 2, 3, xoptions=gtk.EXPAND)
		
		temp = gtk.Label("Battery 1 Font")
		temp.set_alignment(0, 0.5)
		self.tableBattery.attach(temp, 0, 1, 3, 4, xpadding=10)
		self.bat1FontButton = gtk.FontButton()
		self.bat1FontButton.set_font_name(self.defaults["font"])
		self.bat1FontButton.connect("font-set", self.changeOccurred)
		self.tableBattery.attach(self.bat1FontButton, 1, 2, 3, 4, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		temp = gtk.Label("Battery 2 Font")
		temp.set_alignment(0, 0.5)
		self.tableBattery.attach(temp, 0, 1, 4, 5, xpadding=10)
		self.bat2FontButton = gtk.FontButton()
		self.bat2FontButton.set_font_name(self.defaults["font"])
		self.bat2FontButton.connect("font-set", self.changeOccurred)
		self.tableBattery.attach(self.bat2FontButton, 1, 2, 4, 5, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		temp = gtk.Label("Battery Font Color")
		temp.set_alignment(0, 0.5)
		self.tableBattery.attach(temp, 0, 1, 5, 6, xpadding=10)
		self.batteryFontCol = gtk.Entry(7)
		self.batteryFontCol.set_width_chars(9)
		self.batteryFontCol.set_name("batteryFontCol")
		self.batteryFontCol.connect("activate", self.colorTyped)
		self.tableBattery.attach(self.batteryFontCol, 1, 2, 5, 6, xoptions=gtk.EXPAND)
		self.batteryFontColButton = gtk.ColorButton(gtk.gdk.color_parse(self.defaults["fgColor"]))
		self.batteryFontColButton.set_use_alpha(True)
		self.batteryFontColButton.set_name("batteryFontCol")
		self.batteryFontColButton.connect("color-set", self.colorChange)
		self.tableBattery.attach(self.batteryFontColButton, 2, 3, 5, 6, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		self.batteryFontCol.set_text(self.defaults["fgColor"])
		# Add this AFTER we set color to avoid "changed" event
		self.batteryFontCol.connect("changed", self.changeOccurred)
		
		temp = gtk.Label("Padding (x, y)")
		temp.set_alignment(0, 0.5)
		self.tableBattery.attach(temp, 0, 1, 6, 7, xpadding=10)
		self.batteryPadX = gtk.Entry(6)
		self.batteryPadX.set_width_chars(8)
		self.batteryPadX.set_text(BATTERY_PADDING_X)
		self.batteryPadX.connect("changed", self.changeOccurred)
		self.tableBattery.attach(self.batteryPadX, 1, 2, 6, 7, xoptions=gtk.EXPAND)
		self.batteryPadY = gtk.Entry(6)
		self.batteryPadY.set_width_chars(8)
		self.batteryPadY.set_text(BATTERY_PADDING_Y)
		self.batteryPadY.connect("changed", self.changeOccurred)
		self.tableBattery.attach(self.batteryPadY, 2, 3, 6, 7, xoptions=gtk.EXPAND)
		
		temp = gtk.Label("Battery Background ID")
		temp.set_alignment(0, 0.5)
		self.tableBattery.attach(temp, 0, 1, 7, 8, xpadding=10)
		self.batteryBg = gtk.combo_box_new_text()
		self.batteryBg.append_text("0 (fully transparent)")
		for i in range(len(self.bgs)):
			self.batteryBg.append_text(str(i+1))
		self.batteryBg.set_active(0)
		self.batteryBg.connect("changed", self.changeOccurred)
		self.tableBattery.attach(self.batteryBg, 1, 2, 7, 8, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		# View Config
		self.configArea = gtk.ScrolledWindow()
		self.configBuf = gtk.TextBuffer()
		self.configTextView = gtk.TextView(self.configBuf)
		self.configArea.add_with_viewport(self.configTextView)
		
		# Add backgrounds to notebooks
		for i in range(self.defaults["bgCount"]):
			self.addBgClick(None, init=True)
		
		self.bgNotebook.set_current_page(0)
		
		# Add pages to notebook
		self.notebook.append_page(self.tableBgs, gtk.Label("Backgrounds"))
		self.notebook.append_page(self.tablePanel, gtk.Label("Panel"))
		self.notebook.append_page(self.tableTaskbar, gtk.Label("Taskbar"))
		self.notebook.append_page(self.tableTask, gtk.Label("Tasks"))
		self.notebook.append_page(self.tableFont, gtk.Label("Task Fonts"))
		self.notebook.append_page(self.tableTray, gtk.Label("Systray"))
		self.notebook.append_page(self.tableClock, gtk.Label("Clock"))
		self.notebook.append_page(self.tableMouse, gtk.Label("Mouse"))
		self.notebook.append_page(self.tableBattery, gtk.Label("Battery"))
		self.notebook.append_page(self.configArea, gtk.Label("View Config"))
		
		self.notebook.connect("switch-page", self.switchPage)
		
		# Add notebook to window and show
		self.table.attach(self.notebook, 0, 4, 2, 3, xpadding=5, ypadding=5)
		
		# Create and add the status bar to the bottom of the main window
		self.statusBar = gtk.Statusbar()
		self.statusBar.set_has_resize_grip(True)
		self.updateStatusBar("New Config File [*]")
		self.table.attach(self.statusBar, 0, 4, 3, 4)
		
		self.add(self.table)
		
		self.show_all()
		
		# Create our property dictionary. This holds the widgets which correspond to each property
		self.propUI = {
			"panel_monitor": self.panelMonitor,
			"panel_position": (self.panelPosY, self.panelPosX),
			"panel_size": (self.panelSizeX, self.panelSizeY),
			"panel_margin": (self.panelMarginX, self.panelMarginY),
			"panel_padding": (self.panelPadX, self.panelPadY),
			"panel_background_id": self.panelBg,
			"taskbar_mode": self.taskbarMode,
			"taskbar_padding": (self.taskbarPadX, self.taskbarPadY, self.taskbarSpacing),
			"taskbar_background_id": self.taskbarBg,
			"task_icon": self.taskIconCheckButton,
			"task_text": self.taskTextCheckButton,
			"task_centered": self.taskCentreCheckButton,
			"task_width": self.taskWidth,
			"task_padding": (self.taskPadX, self.taskPadY),
			"task_background_id": self.taskBg,
			"task_active_background_id": self.taskActiveBg,
			"task_font": self.fontButton,
			"task_font_color": (self.fontCol, self.fontColButton),
			"task_active_font_color": (self.fontActiveCol, self.fontActiveColButton),
			"font_shadow": self.fontShadowCheckButton,
			"systray_padding": (self.trayPadX, self.trayPadY, self.traySpacing),
			"systray_background_id": self.trayBg,
			"time1_format": self.clock1Format,
			"time2_format": self.clock2Format,
			"time1_font": self.clock1FontButton,
			"time2_font": self.clock2FontButton,
			"clock_font_color": (self.clockFontCol, self.clockFontColButton),
			"clock_padding": (self.clockPadX, self.clockPadY),
			"clock_background_id": self.clockBg,
			"mouse_middle": self.mouseMiddle,
			"mouse_right": self.mouseRight,
			"mouse_scroll_up": self.mouseUp,
			"mouse_scroll_down": self.mouseDown,
			"battery": self.batteryCheckButton,
			"battery_low_status": self.batteryLow,
			"battery_low_cmd": self.batteryLowAction,
			"bat1_font": self.bat1FontButton,
			"bat2_font": self.bat2FontButton,
			"battery_font_color": (self.batteryFontCol, self.batteryFontColButton),
			"battery_padding": (self.batteryPadX, self.batteryPadY),
			"battery_background_id": self.batteryBg
		}
		
		self.generateConfig()
		
	def about(self, action=None):
		"""Displays the About dialog."""
		about = gtk.AboutDialog()
		about.set_program_name(NAME)
		about.set_version(VERSION)
		about.set_authors(AUTHORS)
		about.set_comments(COMMENTS)
		about.set_website(WEBSITE)
		about.run()
		about.destroy()
	
	def addBg(self):
		"""Adds a new background to the list of backgrounds."""
		self.bgs += [gtk.Table(4, 3, False)]
		
		temp = gtk.Label("Corner Rounding (px)")
		temp.set_alignment(0, 0.5)
		self.bgs[-1].attach(temp, 0, 1, 0, 1, xpadding=10)
		temp = gtk.Entry(7)
		temp.set_width_chars(9)
		temp.set_name("rounded")
		temp.set_text(BG_ROUNDING)
		temp.connect("changed", self.changeOccurred)
		self.bgs[-1].attach(temp, 1, 2, 0, 1, xoptions=gtk.EXPAND)
		
		temp = gtk.Label("Background Color")
		temp.set_alignment(0, 0.5)
		self.bgs[-1].attach(temp, 0, 1, 1, 2, xpadding=10)
		temp = gtk.Entry(7)
		temp.set_width_chars(9)
		temp.set_name("bgColEntry")
		temp.set_text(self.defaults["bgColor"])
		temp.connect("changed", self.changeOccurred)
		temp.connect("activate", self.colorTyped)
		self.bgs[-1].attach(temp, 1, 2, 1, 2, xoptions=gtk.EXPAND)
		temp = gtk.ColorButton(gtk.gdk.color_parse(self.defaults["bgColor"]))
		temp.set_use_alpha(True)
		temp.set_name("bgCol")
		temp.connect("color-set", self.colorChange)
		self.bgs[-1].attach(temp, 2, 3, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		temp = gtk.Label("Border Width (px)")
		temp.set_alignment(0, 0.5)
		self.bgs[-1].attach(temp, 0, 1, 2, 3, xpadding=10)
		temp = gtk.Entry(7)
		temp.set_width_chars(9)
		temp.set_name("border")
		temp.set_text(BG_BORDER)
		temp.connect("changed", self.changeOccurred)
		self.bgs[-1].attach(temp, 1, 2, 2, 3, xoptions=gtk.EXPAND)
		
		temp = gtk.Label("Border Color")
		temp.set_alignment(0, 0.5)
		self.bgs[-1].attach(temp, 0, 1, 3, 4, xpadding=10)
		temp = gtk.Entry(7)
		temp.set_width_chars(9)
		temp.set_name("borderColEntry")
		temp.connect("activate", self.colorTyped)
		temp.set_text(self.defaults["borderColor"])
		temp.connect("changed", self.changeOccurred)
		self.bgs[-1].attach(temp, 1, 2, 3, 4, xoptions=gtk.EXPAND)
		temp = gtk.ColorButton(gtk.gdk.color_parse(self.defaults["borderColor"]))
		temp.set_use_alpha(True)
		temp.set_name("borderCol")
		temp.connect("color-set", self.colorChange)
		self.bgs[-1].attach(temp, 2, 3, 3, 4, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
	
	# Note: Only set init to True when initialising background styles.
	# This prevents unwanted calls to changeOccurred()
	def addBgClick(self, widget=None, init=False):
		"""Creates a new background and adds a new tab to the notebook."""
		n = self.bgNotebook.get_n_pages()
		
		if n > (self.defaults["bgCount"] + 2):
			if confirmDialog(self, "You already have %d background styles. Are you sure you would like another?" % n) == gtk.RESPONSE_NO:
				return
		
		self.addBg()
		
		newId = len(self.bgs)
		
		self.bgNotebook.append_page(self.bgs[newId-1], gtk.Label("Background ID %d" % (newId)))
		
		self.bgNotebook.show_all()
		
		self.updateComboBoxes(n, "add")
		
		self.bgNotebook.set_current_page(n)
		
		if not init:
			self.changeOccurred()
	
	def apply(self, widget, event=None):
		"""Applies the current config to tint2."""
		if confirmDialog(self, "This will terminate all currently running instances of tint2 before applying config. Continue?") == gtk.RESPONSE_YES:
			if not self.save():
				return
			
			# Check if tint2 is running
			procs = os.popen('pidof "tint2"')				# Check list of active processes for tint2
			pids = []										# List of process ids for tint2
			
			for proc in procs.readlines():
				pids += [int(proc.strip().split(" ")[0])]
			
			procs.close()
			
			# If it is - kill it
			for pid in pids:
				os.kill(pid, signal.SIGTERM)
			
			# Lastly, start it
			os.spawnv(os.P_NOWAIT, self.tint2Bin, [self.tint2Bin, "-c" + self.filename])
	
	def changeAllFonts(self, widget):
		"""Changes all fonts at once."""
		dialog = gtk.FontSelectionDialog("Select Font")
		
		dialog.set_font_name(self.defaults["font"])
		
		if dialog.run() == gtk.RESPONSE_OK:
			newFont = dialog.get_font_name()
			
			self.clock1FontButton.set_font_name(newFont)
			self.clock2FontButton.set_font_name(newFont)
			self.bat1FontButton.set_font_name(newFont)
			self.bat2FontButton.set_font_name(newFont)
			self.fontButton.set_font_name(newFont)
		
		dialog.destroy()
		
		self.generateConfig()
		self.changeOccurred()
	
	def changeDefaults(self, widget=None):
		"""Shows the style preferences widget."""
		TintWizardPrefGUI(self)
	
	def changeOccurred(self, widget=None):
		"""Called when the user changes something, i.e. entry value"""
		self.toSave = True
		
		self.updateStatusBar(change=True)
	
	def colorButtonLookup(self, widget):
		"""Returns the color button associated with widget."""
		if widget.get_name() == "fontCol":
			return self.fontColButton
		elif widget.get_name() == "fontActiveCol":
			return self.fontActiveColButton
		elif widget.get_name() == "clockFontCol":
			return self.clockFontColButton
		elif widget.get_name() == "batteryFontCol":
			return self.batteryFontColButton
		elif widget.get_name() == "bgColEntry":
			bgID = self.bgNotebook.get_current_page()
			
			for child in self.bgs[bgID].get_children():
				if child.get_name() == "bgCol":
					
					return child
		elif widget.get_name() == "borderColEntry":
			bgID = self.bgNotebook.get_current_page()
			
			for child in self.bgs[bgID].get_children():
				if child.get_name() == "borderCol":
					
					return child
		
		return None
	
	def colorChange(self, widget):
		"""Update the text entry when a color button is updated."""
		r = widget.get_color().red
		g = widget.get_color().green
		b = widget.get_color().blue
		
		if widget.get_name() == "fontCol":
			self.fontCol.set_text(rgbToHex(r, g, b))
		elif widget.get_name() == "fontActiveCol":
			self.fontActiveCol.set_text(rgbToHex(r, g, b))
		elif widget.get_name() == "clockFontCol":
			self.clockFontCol.set_text(rgbToHex(r, g, b))
		elif widget.get_name() == "batteryFontCol":
			self.batteryFontCol.set_text(rgbToHex(r, g, b))
		elif widget.get_name() == "bgCol":
			bgID = self.bgNotebook.get_current_page()
			
			for child in self.bgs[bgID].get_children():
				if child.get_name() == "bgColEntry":
					
					child.set_text(rgbToHex(r, g, b))
					break
		elif widget.get_name() == "borderCol":
			bgID = self.bgNotebook.get_current_page()
			
			for child in self.bgs[bgID].get_children():
				if child.get_name() == "borderColEntry":
					
					child.set_text(rgbToHex(r, g, b))
					break
		
		self.changeOccurred()
	
	def colorTyped(self, widget):
		"""Update the color button when a valid value is typed into the entry."""
		s = widget.get_text()
		
		# The color button associated with this widget.
		colorButton = self.colorButtonLookup(widget)
		
		# Just a precautionary check - this situation should never arise.
		if not colorButton:
			print "Error in colorTyped() -- unrecognised entry widget."
			return
		
		# If the entered value is invalid, set textbox to the current
		# hex value of the associated color button.
		buttonHex = self.getHexFromWidget(colorButton)
		
		if len(s) != 7:
			errorDialog(self, "Invalid color specification!")
			#self.colorChange(widget) TODO - remove this when issue 29 is verified
			widget.set_text(buttonHex)
			return
		
		try:
			col = gtk.gdk.Color(s)
		except:
			errorDialog(self, "Invalid color specification!")
			#self.colorChange(widget) TODO - remove this when issue 29 is verified
			widget.set_text(buttonHex)
			return
		
		colorButton.set_color(col)
	
	# Note: only set init to True when removing backgrounds for a new config
	# This prevents unwanted calls to changeOccurred()
	def delBgClick(self, widget=None, prompt=True, init=False):
		"""Deletes the selected background after confirming with the user."""
		selected = self.bgNotebook.get_current_page()
		
		if selected == -1:			# Nothing to remove
			return
		
		if prompt:
			if confirmDialog(self, "Remove this background?") != gtk.RESPONSE_YES:
				return
			
		self.bgNotebook.remove_page(selected)
		self.bgs.pop(selected)
		
		for i in range(self.bgNotebook.get_n_pages()):
			self.bgNotebook.set_tab_label_text(self.bgNotebook.get_nth_page(i), "Background ID %d" % (i+1))
		
		self.bgNotebook.show_all()
		
		self.updateComboBoxes(len(self.bgs) + 1, "remove")
		
		if not init:
			self.changeOccurred()
	
	def generateConfig(self):
		"""Reads values from each widget and generates a config."""
		self.configBuf.delete(self.configBuf.get_start_iter(), self.configBuf.get_end_iter())
		self.configBuf.insert(self.configBuf.get_end_iter(), "# Tint2 config file\n")
		self.configBuf.insert(self.configBuf.get_end_iter(), "# Generated by tintwizard (http://code.google.com/p/tintwizard/)\n")
		self.configBuf.insert(self.configBuf.get_end_iter(), "\n# For information on manually configuring tint2 see http://code.google.com/p/tint2/wiki/Configure\n")
		self.configBuf.insert(self.configBuf.get_end_iter(), "\n# To use this as default tint2 config: save as $HOME/.config/tint2/tint2rc\n\n")
		
		self.configBuf.insert(self.configBuf.get_end_iter(), "# Background definitions\n")
		for i in range(len(self.bgs)):
			self.configBuf.insert(self.configBuf.get_end_iter(), "# ID %d\n" % (i + 1))
			
			for child in self.bgs[i].get_children():
				if child.get_name() == "rounded":
					rounded = child.get_text() if child.get_text() else BG_ROUNDING
				elif child.get_name() == "border":
					borderW = child.get_text() if child.get_text() else BG_BORDER
				elif child.get_name() == "bgCol":
					bgCol = self.getHexFromWidget(child)
					bgAlpha = int(child.get_alpha() / 65535.0 * 100)
				elif child.get_name() == "borderCol":
					borderCol = self.getHexFromWidget(child)
					borderAlpha = int(child.get_alpha() / 65535.0 * 100)
			
			self.configBuf.insert(self.configBuf.get_end_iter(), "rounded = %s\n" % (rounded))
			self.configBuf.insert(self.configBuf.get_end_iter(), "border_width = %s\n" % (borderW))
			self.configBuf.insert(self.configBuf.get_end_iter(), "background_color = %s %d\n" % (bgCol, bgAlpha))
			self.configBuf.insert(self.configBuf.get_end_iter(), "border_color = %s %d\n\n" % (borderCol, borderAlpha))
		
		self.configBuf.insert(self.configBuf.get_end_iter(), "# Panel\n")
		self.configBuf.insert(self.configBuf.get_end_iter(), "panel_monitor = %s\n" % (self.panelMonitor.get_text() if self.panelMonitor.get_text() else PANEL_MONITOR))
		self.configBuf.insert(self.configBuf.get_end_iter(), "panel_position = %s %s\n" % (self.panelPosY.get_active_text(), self.panelPosX.get_active_text()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "panel_size = %s %s\n" % (self.panelSizeX.get_text() if self.panelSizeX.get_text() else PANEL_SIZE_X,
															self.panelSizeY.get_text() if self.panelSizeY.get_text() else PANEL_SIZE_Y))
		self.configBuf.insert(self.configBuf.get_end_iter(), "panel_margin = %s %s\n" % (self.panelMarginX.get_text() if self.panelMarginX.get_text() else PANEL_MARGIN_X,
															self.panelMarginY.get_text() if self.panelMarginY.get_text() else PANEL_MARGIN_Y))
		self.configBuf.insert(self.configBuf.get_end_iter(), "panel_padding = %s %s\n" % (self.panelPadX.get_text() if self.panelPadX.get_text() else PANEL_PADDING_X,
															self.panelPadY.get_text() if self.panelPadY.get_text() else PANEL_PADDING_Y))
		self.configBuf.insert(self.configBuf.get_end_iter(), "panel_background_id = %s\n" % (self.panelBg.get_active()))
		
		self.configBuf.insert(self.configBuf.get_end_iter(), "\n# Taskbar\n")
		self.configBuf.insert(self.configBuf.get_end_iter(), "taskbar_mode = %s\n" % (self.taskbarMode.get_active_text()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "taskbar_padding = %s %s %s\n" % (self.taskbarPadX.get_text() if self.taskbarPadX.get_text() else TASKBAR_PADDING_X,
															self.taskbarPadY.get_text() if self.taskbarPadY.get_text() else TASKBAR_PADDING_X,
															self.taskbarSpacing.get_text() if self.taskbarSpacing.get_text() else TASK_SPACING))
		self.configBuf.insert(self.configBuf.get_end_iter(), "taskbar_background_id = %s\n" % (self.taskbarBg.get_active()))
		
		self.configBuf.insert(self.configBuf.get_end_iter(), "\n# Tasks\n")
		self.configBuf.insert(self.configBuf.get_end_iter(), "urgent_nb_of_blink = %s\n" % (self.taskBlinks.get_text() if self.taskBlinks.get_text() else TASK_BLINKS))
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_icon = %s\n" % int(self.taskIconCheckButton.get_active()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_text = %s\n" % int(self.taskTextCheckButton.get_active()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_centered = %s\n" % int(self.taskCentreCheckButton.get_active()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_width = %s\n" % (self.taskWidth.get_text() if self.taskWidth.get_text() else TASK_WIDTH))
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_padding = %s %s\n" % (self.taskPadX.get_text() if self.taskPadX.get_text() else TASK_PADDING_X,
															self.taskPadY.get_text() if self.taskPadY.get_text() else TASK_PADDING_Y))
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_background_id = %s\n" % (self.taskBg.get_active()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_active_background_id = %s\n" % (self.taskActiveBg.get_active()))
		
		self.configBuf.insert(self.configBuf.get_end_iter(), "\n# Fonts\n")
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_font = %s\n" % (self.fontButton.get_font_name()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_font_color = %s %s\n" % (self.getHexFromWidget(self.fontColButton),
															int(self.fontColButton.get_alpha() / 65535.0 * 100)))
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_active_font_color = %s %s\n" % (self.getHexFromWidget(self.fontActiveColButton),
															int(self.fontActiveColButton.get_alpha() / 65535.0 * 100)))
		self.configBuf.insert(self.configBuf.get_end_iter(), "font_shadow = %s\n" % int(self.fontShadowCheckButton.get_active()))
		
		self.configBuf.insert(self.configBuf.get_end_iter(), "\n# Systray")
		if not self.trayCheckButton.get_active():
			self.configBuf.insert(self.configBuf.get_end_iter(), " - DISABLED\n#")
		else:
			self.configBuf.insert(self.configBuf.get_end_iter(), "\n")
		self.configBuf.insert(self.configBuf.get_end_iter(), "systray_padding = %s %s %s\n" % (self.trayPadX.get_text() if self.trayPadX.get_text() else TRAY_PADDING_X,
															self.trayPadY.get_text() if self.trayPadY.get_text() else TRAY_PADDING_Y,
															self.traySpacing.get_text() if self.traySpacing.get_text() else TRAY_SPACING))
		self.configBuf.insert(self.configBuf.get_end_iter(), "systray_background_id = %s\n" % (self.trayBg.get_active()))
		
		if self.clockCheckButton.get_active():
			self.configBuf.insert(self.configBuf.get_end_iter(), "\n# Clock\n")
			if self.clock1CheckButton.get_active():
				self.configBuf.insert(self.configBuf.get_end_iter(), "time1_format = %s\n" % (self.clock1Format.get_text() if self.clock1Format.get_text() else CLOCK_FMT_1))
				self.configBuf.insert(self.configBuf.get_end_iter(), "time1_font = %s\n" % (self.clock1FontButton.get_font_name()))
			if self.clock2CheckButton.get_active():
				self.configBuf.insert(self.configBuf.get_end_iter(), "time2_format = %s\n" % (self.clock2Format.get_text() if self.clock2Format.get_text() else CLOCK_FMT_2))
				self.configBuf.insert(self.configBuf.get_end_iter(), "time2_font = %s\n" % (self.clock2FontButton.get_font_name()))
			self.configBuf.insert(self.configBuf.get_end_iter(), "clock_font_color = %s %s\n" % (self.getHexFromWidget(self.clockFontColButton),
															int(self.clockFontColButton.get_alpha() / 65535.0 * 100)))
			self.configBuf.insert(self.configBuf.get_end_iter(), "clock_padding = %s %s\n" % (self.clockPadX.get_text() if self.clockPadX.get_text() else CLOCK_PADDING_X,
															self.clockPadY.get_text() if self.clockPadY.get_text() else CLOCK_PADDING_Y))
			self.configBuf.insert(self.configBuf.get_end_iter(), "clock_background_id = %s\n" % (self.clockBg.get_active()))
		
		self.configBuf.insert(self.configBuf.get_end_iter(), "\n# Mouse\n")
		self.configBuf.insert(self.configBuf.get_end_iter(), "mouse_middle = %s\n" % (self.mouseMiddle.get_active_text()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "mouse_right = %s\n" % (self.mouseRight.get_active_text()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "mouse_scroll_up = %s\n" % (self.mouseUp.get_active_text()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "mouse_scroll_down = %s\n" % (self.mouseDown.get_active_text()))
		
		self.configBuf.insert(self.configBuf.get_end_iter(), "\n# Battery\n")
		self.configBuf.insert(self.configBuf.get_end_iter(), "battery = %s\n" % int(self.batteryCheckButton.get_active()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "battery_low_status = %s\n" % (self.batteryLow.get_text() if self.batteryLow.get_text() else BATTERY_LOW))
		self.configBuf.insert(self.configBuf.get_end_iter(), "battery_low_cmd = %s\n" % (self.batteryLowAction.get_text() if self.batteryLowAction.get_text() else BATTERY_ACTION))
		self.configBuf.insert(self.configBuf.get_end_iter(), "bat1_font = %s\n" % (self.bat1FontButton.get_font_name()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "bat2_font = %s\n" % (self.bat2FontButton.get_font_name()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "battery_font_color = %s %s\n" % (self.getHexFromWidget(self.batteryFontColButton),
															int(self.batteryFontColButton.get_alpha() / 65535.0 * 100)))
		self.configBuf.insert(self.configBuf.get_end_iter(), "battery_padding = %s %s\n" % (self.batteryPadX.get_text() if self.batteryPadX.get_text() else BATTERY_PADDING_Y,
															self.batteryPadY.get_text() if self.batteryPadY.get_text() else BATTERY_PADDING_Y))
		self.configBuf.insert(self.configBuf.get_end_iter(), "battery_background_id = %s\n" % (self.batteryBg.get_active()))
		
		self.configBuf.insert(self.configBuf.get_end_iter(), "\n# End of config")
	
	def getHexFromWidget(self, widget):
		"""Returns the #RRGGBB value of a widget."""
		r = widget.get_color().red
		g = widget.get_color().green
		b = widget.get_color().blue
		
		return rgbToHex(r, g, b)
	
	def help(self, action=None):
		"""Opens the Help wiki page in the default web browser."""
		try:
			webbrowser.open("http://code.google.com/p/tintwizard/wiki/Help")
		except:
			errorDialog(self, "Your default web-browser could not be opened.\nPlease visit http://code.google.com/p/tintwizard/wiki/Help")
	
	def main(self):
		"""Enters the main loop."""
		gtk.main()
	
	def new(self, action=None):
		"""Resets all the widgets to their default values."""
		if self.toSave:
			self.savePrompt()
		
		self.toSave = True
		self.filename = None
		
		# Backgrounds
		for i in range(len(self.bgs)):
			self.delBgClick(prompt=False, init=True)
			
		for i in range(self.defaults["bgCount"]):
			self.addBgClick(init=True)
		
		self.bgNotebook.set_current_page(0)
		
		# Panel
		self.panelPosY.set_active(0)
		self.panelPosX.set_active(0)
		self.panelSizeX.set_text(PANEL_SIZE_X)
		self.panelSizeY.set_text(PANEL_SIZE_Y)
		self.panelMarginX.set_text(PANEL_MARGIN_X)
		self.panelMarginY.set_text(PANEL_MARGIN_Y)
		self.panelPadX.set_text(PANEL_PADDING_Y)
		self.panelPadY.set_text(PANEL_PADDING_Y)
		self.panelBg.set_active(0)
		self.panelMonitor.set_text(PANEL_MONITOR)
		# Taskbar
		self.taskbarMode.set_active(0)
		self.taskbarPadX.set_text(TASKBAR_PADDING_X)
		self.taskbarPadY.set_text(TASKBAR_PADDING_Y)
		self.taskbarSpacing.set_text(TASK_SPACING)
		self.taskbarBg.set_active(0)
		# Tasks
		self.taskBlinks.set_text(TASK_BLINKS)
		self.taskCentreCheckButton.set_active(True)
		self.taskTextCheckButton.set_active(True)
		self.taskIconCheckButton.set_active(True)
		self.taskWidth.set_text(TASK_WIDTH)
		self.taskPadX.set_text(TASK_PADDING_X)
		self.taskPadY.set_text(TASK_PADDING_Y)
		self.taskBg.set_active(0)
		self.taskActiveBg.set_active(0)
		# Fonts
		self.fontButton.set_font_name(self.defaults["font"])
		self.fontColButton.set_alpha(65535)
		self.fontColButton.set_color(gtk.gdk.Color(0, 0, 0))
		self.fontCol.set_text(self.defaults["fgColor"])
		self.fontActiveColButton.set_alpha(65535)
		self.fontActiveColButton.set_color(gtk.gdk.Color(0, 0, 0))
		self.fontActiveCol.set_text(self.defaults["fgColor"])
		self.fontShadowCheckButton.set_active(False)
		# Systray
		self.trayCheckButton.set_active(True)
		self.trayPadX.set_text(TRAY_PADDING_X)
		self.trayPadY.set_text(TRAY_PADDING_X)
		self.traySpacing.set_text(TRAY_SPACING)
		self.trayBg.set_active(0)
		# Clock
		self.clockCheckButton.set_active(True)
		self.clock1Format.set_text(CLOCK_FMT_1)
		self.clock1CheckButton.set_active(True)
		self.clock1FontButton.set_font_name(self.defaults["font"])
		self.clock2Format.set_text(CLOCK_FMT_2)
		self.clock2CheckButton.set_active(True)
		self.clock2FontButton.set_font_name(self.defaults["font"])
		self.clockFontColButton.set_alpha(65535)
		self.clockFontColButton.set_color(gtk.gdk.Color(0, 0, 0))
		self.clockFontCol.set_text(self.defaults["fgColor"])
		self.clockPadX.set_text(CLOCK_PADDING_X)
		self.clockPadY.set_text(CLOCK_PADDING_Y)
		self.clockBg.set_active(0)
		# Mouse
		self.mouseMiddle.set_active(0)
		self.mouseRight.set_active(0)
		self.mouseUp.set_active(0)
		self.mouseDown.set_active(0)
		# Battery
		self.batteryCheckButton.set_active(False)
		self.batteryLow.set_text(BATTERY_LOW)
		self.batteryLowAction.set_text(BATTERY_ACTION)
		self.bat1FontButton.set_font_name(self.defaults["font"])
		self.bat2FontButton.set_font_name(self.defaults["font"])
		self.batteryFontColButton.set_alpha(65535)
		self.batteryFontColButton.set_color(gtk.gdk.Color(0, 0, 0))
		self.batteryFontCol.set_text(self.defaults["fgColor"])
		self.batteryPadX.set_text(BATTERY_PADDING_Y)
		self.batteryPadY.set_text(BATTERY_PADDING_Y)
		self.batteryBg.set_active(0)
		
		self.generateConfig()
		self.updateStatusBar("New Config File [*]")
	
	def openDef(self, widget=None):
		"""Opens the default tint2 config."""
		self.openFile(None, default=True)
	
	def openFile(self, widget=None, default=False):
		"""Reads from a config file."""
		self.new()
		
		if not default:
			chooser = gtk.FileChooserDialog("Open Config File", self, gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
			chooser.set_default_response(gtk.RESPONSE_OK)
			
			if self.curDir != None:
				chooser.set_current_folder(self.curDir)
			
			chooserFilter = gtk.FileFilter()
			chooserFilter.set_name("All files")
			chooserFilter.add_pattern("*")
			chooser.add_filter(chooserFilter)
			chooser.show()
			
			response = chooser.run()
			
			if response == gtk.RESPONSE_OK:
				self.filename = chooser.get_filename()
				self.curDir = os.path.dirname(self.filename)
			else:
				chooser.destroy()
				return
			
			chooser.destroy()
		else:
			self.filename = os.path.expandvars("$HOME/.config/tint2/tint2rc")
			self.curDir = os.path.expandvars("$HOME/.config/tint2")
		
		self.readFile()
		self.generateConfig()
		self.updateStatusBar()
	
	def parseBgs(self, string):
		"""Parses the background definitions from a string."""
		s = string.split("\n")
		
		bgDefs = []
		cur = -1
		
		for l in s:
			if "rounded" in l:
				bgDefs += [[l]]
				cur += 1
			elif "border_width" in l or "background_color" in l or "border_color" in l:
				bgDefs[cur] += [l]
		
		for d in bgDefs:
			self.addBg()
			
			for child in self.bgs[-1].get_children():
				if child.get_name() == "rounded":
					child.set_text(d[0].split("=")[1].strip())
				elif child.get_name() == "border":
					child.set_text(d[1].split("=")[1].strip())
				elif child.get_name() == "bgColEntry":
					child.set_text(d[2].split("=")[1].strip().split(" ")[0].strip())
					child.activate()
				elif child.get_name() == "borderColEntry":
					child.set_text(d[3].split("=")[1].strip().split(" ")[0].strip())
					child.activate()
				elif child.get_name() == "bgCol":
					child.set_alpha(int(int(d[2].split("=")[1].strip().split(" ")[1].strip()) * 65535 / 100.0))
				elif child.get_name() == "borderCol":
					child.set_alpha(int(int(d[3].split("=")[1].strip().split(" ")[1].strip()) * 65535 / 100.0))
			
			newId = len(self.bgs)
		
			self.bgNotebook.append_page(self.bgs[newId-1], gtk.Label("Background ID %d" % (newId)))
		
			self.bgNotebook.show_all()
		
			self.updateComboBoxes(newId-1, "add")
		
			self.bgNotebook.set_current_page(newId)
	
	def parseConfig(self, string):
		"""Parses the contents of a config file."""
		for line in string.split("\n"):
			s = line.split("=")
			
			e = s[0].strip()
			
			if e == "time1_format":
				self.parseProp(self.propUI[e], s[1], True, "time1")
			elif e == "time2_format":
				self.parseProp(self.propUI[e], s[1], True, "time2")
			elif e == "systray_padding":
				self.parseProp(self.propUI[e], s[1], True, "tray")
			else:
				if self.propUI.has_key(e):
					self.parseProp(self.propUI[e], s[1])
	
	def parseProp(self, prop, string, special=False, propType=""):
		"""Parses a variable definition from the conf file and updates the correct UI widget."""
		string = string.strip()
		eType = type(prop)
		
		if special:
			if propType == "time1":
				self.clockCheckButton.set_active(True)
				self.clock1CheckButton.set_active(True)
			elif propType == "time2":
				self.clockCheckButton.set_active(True)
				self.clock2CheckButton.set_active(True)
			elif propType == "tray":
				self.trayCheckButton.set_active(True)
		
		if eType == gtk.Entry:
			prop.set_text(string)
			prop.activate()
		elif eType == gtk.ComboBox:
			if string in ["bottom", "top", "left", "right", "center", "single_desktop", "multi_desktop", "single_monitor", "none", "close", "shade", "iconify", "toggle", "toggle_iconify"]:
				if string in ["bottom", "left", "single_desktop", "none"]:
					i = 0
				elif string in ["top", "right", "multi_desktop", "close"]:
					i = 1
				elif string in ["center", "single_monitor", "toggle"]:
					i = 2
				else:
					i = ["none", "close", "toggle", "iconify", "shade", "toggle_iconify"].index(string)
				
				prop.set_active(i)
			else:
				prop.set_active(int(string))
		elif eType == gtk.CheckButton:
			prop.set_active(bool(int(string)))
		elif eType == gtk.FontButton:
			prop.set_font_name(string)
		elif eType == gtk.ColorButton:
			prop.set_alpha(int(int(string) * 65535 / 100.0))
		elif eType == tuple:
			s = string.split(" ")
			for i in range(len(prop)):
				self.parseProp(prop[i], s[i])
	
	def quit(self, widget, event=None):
		"""Asks if user would like to save file before quitting, then quits the program."""
		if self.toSave:
			dialog = gtk.Dialog("Save config?", self, gtk.DIALOG_MODAL, (gtk.STOCK_YES, gtk.RESPONSE_YES, gtk.STOCK_NO, gtk.RESPONSE_NO, gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
			dialog.get_content_area().add(gtk.Label("Save config before quitting?"))
			dialog.get_content_area().set_size_request(300, 100)
			dialog.show_all()
			response = dialog.run()
			dialog.destroy()
			
			if response == gtk.RESPONSE_CANCEL:
				return True							# Return True to stop it quitting when we hit "Cancel"
			elif response == gtk.RESPONSE_NO:
				gtk.main_quit()
			elif response == gtk.RESPONSE_YES:
				self.save()
				gtk.main_quit()
		else:
			gtk.main_quit()
	
	def readConf(self):
		"""Reads the tintwizard configuration file - NOT tint2 config files."""
		self.defaults = {"font": None, "bgColor": None, "fgColor": None, "borderColor": None, "bgCount": None, "dir": None}
		
		if os.path.dirname(sys.argv[0]) == ".":
			pathName = "."
		else:
			pathName = os.path.dirname(sys.argv[0])
		
		if not os.path.exists(pathName + "/tintwizard.conf"):
			self.writeConf()
			return
		
		f = open(pathName + "/tintwizard.conf", "r")
		
		for line in f:
			if "=" in line:
				l = line.split("=")
				
				if self.defaults.has_key(l[0].strip()):
					self.defaults[l[0].strip()] = l[1].strip()
					
	def readFile(self):
		"""Reads in from a config file."""
		f = open(self.filename, "r")
		
		string = ""
		
		for line in f:
			if (line[0] != "#") and (len(line) > 2):
				string += line
		
		f.close()
		
		# Deselect the optional stuff, and we'll re-check them if the config has them enabled
		self.clockCheckButton.set_active(False)
		self.clock1CheckButton.set_active(False)
		self.clock2CheckButton.set_active(False)
		self.trayCheckButton.set_active(False)
		
		# Remove all background styles so we can create new ones as we read them
		for i in range(len(self.bgs)):
			self.delBgClick(None, False)
		
		self.parseBgs(string)
		
		self.parseConfig(string)
	
	def save(self, widget=None, event=None):
		"""Saves the generated config file."""
		
		# This function returns the boolean status of whether or not the
		# file saved, so that the apply() function knows if it should
		# kill the tint2 process and apply the new config.
		
		# If no file has been selected, force the user to "Save As..."
		if self.filename == None:
			return self.saveAs()
		else:
			self.generateConfig()
			self.writeFile()
			
			return True
	
	def saveAs(self, widget=None, event=None):
		"""Prompts the user to select a file and then saves the generated config file."""
		self.generateConfig()
		
		chooser = gtk.FileChooserDialog("Save Config File As...", self, gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
		chooser.set_default_response(gtk.RESPONSE_OK)
		
		if self.curDir != None:
			chooser.set_current_folder(self.curDir)
		
		chooserFilter = gtk.FileFilter()
		chooserFilter.set_name("All files")
		chooserFilter.add_pattern("*")
		chooser.add_filter(chooserFilter)
		chooser.show()
		
		response = chooser.run()
		
		if response == gtk.RESPONSE_OK:
			self.filename = chooser.get_filename()
			
			if os.path.exists(self.filename):
				overwrite = confirmDialog(self, "This file already exists. Overwrite this file?")
				
				if overwrite == gtk.RESPONSE_YES:
					self.writeFile()
					chooser.destroy()
					return True
				else:
					self.filename = None
					chooser.destroy()
					return False
			else:
				self.writeFile()
				chooser.destroy()
				return True
		else:
			self.filename = None
			chooser.destroy()
			return False
	
	def saveAsDef(self, widget=None, event=None):
		"""Saves the config as the default tint2 config."""
		if confirmDialog(self, "Overwrite current tint2 default config?") == gtk.RESPONSE_YES:
			self.filename = os.path.expandvars("${HOME}") + "/.config/tint2/tint2rc"
			self.curDir = os.path.expandvars("${HOME}") + "/.config/tint2"
			
			# If, for whatever reason, tint2 has no default config - create one.
			if not os.path.isfile(self.filename):
				f = open(self.filename, "w")
				f.write("# tint2rc")
				f.close()
				
			self.generateConfig()
			self.writeFile()
			
			return True
	
	def savePrompt(self):
		"""Prompt the user to save before creating a new file."""
		if confirmDialog(self, "Save current config?") == gtk.RESPONSE_YES:
			self.save(None)
	
	def switchPage(self, notebook, page, page_num):
		"""Handles notebook page switch events."""
		
		# If user selects the 'View Config' tab, update the textarea within this tab.
		if notebook.get_tab_label_text(notebook.get_nth_page(page_num)) == "View Config":
			self.generateConfig()
	
	def updateComboBoxes(self, i, action="add"):
		"""Updates the contents of a combo box when a background style has been added/removed."""
		cbs = [self.batteryBg, self.clockBg, self.taskbarBg, self.trayBg, self.taskActiveBg, self.taskBg, self.panelBg]
		
		if action == "add":
			for cb in cbs:
				cb.append_text(str(i+1))
		else:
			for cb in cbs:
				if cb.get_active() == i:		# If background is selected, set to a different value
					cb.set_active(0)
				
				cb.remove_text(i)
	
	def updateStatusBar(self, message="", change=False):
		"""Updates the message on the statusbar. A message can be provided,
		and if change is set to True (i.e. something has been modified) then
		an appropriate symbol [*] is shown beside filename."""
		contextID = self.statusBar.get_context_id("")
		
		self.statusBar.pop(contextID)
		
		if not message:
			message = "%s %s" % (self.filename or "New Config File", "[*]" if change else "")
		
		self.statusBar.push(contextID, message)
	
	def writeConf(self):
		"""Writes the tintwizard configuration file."""
		confStr = "#Start\n[defaults]\n"
		
		for key in self.defaults:
			confStr += "%s = %s\n" % (key, str(self.defaults[key]))
		
		confStr += "#End\n"
		
		pathName = "."
		
		if os.path.dirname(sys.argv[0]) != ".":
			pathName = os.path.dirname(sys.argv[0])
		
		f = open(pathName+"/tintwizard.conf", "w")
		
		f.write(confStr)
		
		f.close()
		
	def writeFile(self):
		"""Writes the contents of the config text buffer to file."""
		try:
			f = open(self.filename, "w")
			
			f.write(self.configBuf.get_text(self.configBuf.get_start_iter(), self.configBuf.get_end_iter()))
			
			f.close()
			
			self.toSave = False
			
			self.curDir = os.path.dirname(self.filename)
			
			self.updateStatusBar()
		except IOError:
			errorDialog(self, "Could not save file")

# General use functions
def confirmDialog(parent, message):
	"""Creates a confirmation dialog and returns the response."""
	dialog = gtk.MessageDialog(parent, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, message)
	dialog.show()
	response = dialog.run()
	dialog.destroy()
	return response

def errorDialog(parent=None, message="An error has occured!"):
	"""Creates an error dialog."""
	dialog = gtk.MessageDialog(parent, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message)
	dialog.show()
	dialog.run()
	dialog.destroy()

def numToHex(n):
	"""Convert integer n in range [0, 15] to hex."""
	try:
		return ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"][n]
	except:
		return -1

def rgbToHex(r, g, b):
	"""Constructs a 6 digit hex representation of color (r, g, b)."""
	r2 = trunc(r / 65535.0 * 255)
	g2 = trunc(g / 65535.0 * 255)
	b2 = trunc(b / 65535.0 * 255)
	
	return "#%s%s%s%s%s%s" % (numToHex(r2 / 16), numToHex(r2 % 16), numToHex(g2 / 16), numToHex(g2 % 16), numToHex(b2 / 16), numToHex(b2 % 16))

def trunc(n):
	"""Truncate a floating point number, rounding up or down appropriately."""
	c = math.fabs(math.ceil(n) - n)
	f = math.fabs(math.floor(n) - n)
	
	if c < f:
		return int(math.ceil(n))
	else:
		return int(math.floor(n))

# Direct execution of application
if __name__ == "__main__":
	tw = TintWizardGUI()
	tw.main()
