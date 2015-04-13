

# Version 0.2.7 #
Changelog:
  * Added options for tint2 tooltip support.

# Version 0.2.6 #
Changelog:
  * Added 'panel\_dock' option.
  * Split the 'Clock' tab into 2 tabs; one for format and one for other clock settings.
  * Added some formatting examples for the clock under one of the clock tabs.

# Version 0.2.5 #
Changelog:
  * Added 'systray\_sort' option.

# Version 0.2.4 #
Changelog:
  * Added support for 'taskbar\_active\_background\_id', 'task\_icon\_hsb' and 'task\_active\_icon\_hsb'.
  * Added mouse actions 'maximize\_restore', 'desktop\_left' and 'desktop\_right'.
  * Grouped all 'Task' related tabs under a new notebook.
  * User can disable 'taskbar\_active\_background\_id' option via checkbox

Bugfixes:
  * Fixed problem where colorbuttons were defaulting to Black rather than the colour set by fgColor in tintwizard.conf

# Version 0.2.3 #
Changelog:
  * Removed "single\_monitor" option from "taskbar\_mode"
  * Updated options available for "panel\_pos" to include "horizontal" / "vertical"
  * Changed default clock2 format from "%A %d %B" to "%a %d %b"
  * Replaced "task\_width" with "task\_maximum\_size"
  * The panel size label gets updated to either "Size (width, height)" or "Size (height, width)" depending on the orientation chosen.
  * Added link to http://code.google.com/p/tint2/ in README
  * Added the options "clock\_lclick\_command" and "clock\_rclick\_command"

# Version 0.2.2 #
Changelog:
  * Added "wm\_menu" option
  * Refactored some code
  * Added some documentation to code
  * After applying a config, the user is prompted if they'd like to use that as the default.

# Version 0.2.1 #
Changelog:
  * Re-wrote the README file

Bugfixes:
  * Fixed another problem with tintwizard.conf; as always - if you experience any difficulty with this, please submit a bug report.

# Version 0.2 #
Changelog:
  * Added statusbar which displays filename of config being edited, and alerts user when an unsaved change has been made.
  * Code refactored and documentation slightly improved.

Bugfixes:
  * Fixed errors reading from tintwizard.conf
  * Fixed problem validating typed hex values

# Version 0.1.3b #
Bugfix:
  * [Increased arbitrary clock format string limit to 50 characters.](http://code.google.com/p/tintwizard/issues/detail?id=27)

# Version 0.1.3 #
Changelog:
  * When generating configs, a default value is used if a text entry field is left empty
  * Added option to set maximum number of blinks (new in tint2.0.7-beta3)
  * Colors are fetched from the color-select button rather than accompanying text field - in case the user deletes the hex value

# Version 0.1.2 #
Bugfix:
  * Fixed problem where config was sometimes created in the wrong dir, depending on where the app was launched from.

# Version 0.1.1 #
Changelog:
  * Added option to allow user to open the default tint2 config
  * Changed the way in which the tint2 process id is found before restarting tint2 to apply new theme

# Version 0.1.0 #
I'm excited to announce that this project has reached a mini-milestone for me. My initial aim for this project was to create something which could create configs for tint2 and then apply them to tint2 with the click of a button. This version allows the user to do just that.

If anyone experiences any difficulties when using the "Apply Config" option, please let me know - as I've only had a chance to test this on my own computer.

My next aim is to make this as robust as possible. Currently, there is _very_ little error checking happening.

Changelog:
  * User can now set the default directory in which to open / save configs.
  * If user has not specified a default directory, the tint2 directory ($HOME/.config/tint2) is used.
  * Added option "Save As Default Config", to allow the user to save the current config as the default for tint2
  * Added option "Apply Config" to kill all instances of tint2 then start it again with the new config applied
  * The program will refuse to run if tint2 is not installed.
  * Appearance change: all labels are now left-justified.

Bugfixes:
  * Fixed problem with tintwizard.conf file being misplaced.
  * When a background style is removed, any properties currently using this will have their background id reset to 0
  * "Cancel" button on open dialog now acts accordingly
  * Fixed a couple of syntax errors
  * Fixed issue where tint2 process ids were being incorrectly parsed

# Version 0.04b #
I've decided not to add a panel preview to this project. As useful a feature as it would be, I just can't be bothered. If this ever gets popular enough and people _do_ want this feature then maybe I'll change my mind.

Bugfixes:
  * Fixed problem with config being placed in home directory rather than location of tintwizard.py

# Version 0.04 #
Changelog:
  * A configuration file can now be used to set default values for fonts and colors. The user cannot yet modify this through the program.
  * Added a "Change All Fonts" option which changes all font types at once.
  * Opening / Saving a file _should_ now remember what directory you were previously in

Bugfixes:
  * Pressing "Cancel" on open dialog now closes the dialog
  * Reset number of backgrounds for new configs
  * Background opacity now resets

# Version 0.03 #
Changelog:
  * Config files can be imported
  * Updated labels with some hints
  * Moved task spacing from 'Taskbar' to 'Tasks' tab

Bugfixes:
  * Program would still quit if you decided to "Cancel"
  * When parsing configs, fonts would not be updated

# Version 0.02 #
Changelog:
  * Added options for:
    1. Battery applet
    1. Systray
    1. Taskbar
  * Updated Panel and Task options to comply with the most recent version of tint2 (2.0.7-beta2)
  * Config file can now be saved
  * Added menu
  * Moved toolbar to top of interface.
  * Redesigned toolbar.
  * Added actions for New, Save, Save As, Refresh and Quit menu items
  * Added the About dialog
  * Selecting the Help menu item now uses the default web browser to open the Help wiki page
  * If the user quits before saving the file, the user is asked if they would like to save first
  * User can now add as many background styles as they like
  * Changed background ID selection to combo-box with all available styles

Bugfixes:
  * Color buttons were sometimes returning #RGB or #RRRRGGGGBBBB hex values and tint2 only works with #RRGGBB. Fixed this by manually converting (r, g, b) to #RRGGBB.

Added more development screenshots.

# Version 0.01 #
Project start date. An interface prototype has been produced with limited ability to generate configs.

Added screenshots to the gallery.