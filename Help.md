

# Installation Requirements #
  * [Python 2.x](http://www.python.org/download/)
  * [PyGTK 2.x](http://www.pygtk.org/downloads.html)

# Installing tintwizard #
You do not have to "install" tintwizard. Just extract the files to _any_ directory, and run as instructed below.

## How do I run tintwizard? ##
  1. Place tintwizard.py and tintwizard.conf in any folder.
  1. Double-click on the tintiwzard.py file to run
  1. OR In a terminal, navigate to the folder where tintwizard.py is,
> > and type:
```
./tintwizard.py
```
> > or:
```
python tintwizard.py
```
  1. If neither of these steps work, please see "cannot run", below.
  1. If you have a newer version of tint2 installed, run `tint2conf`.

## How do I add tintwizard to Openbox menus? ##
  1. Run obmenu
  1. Choose the sub-menu where you wish to add tintwizard
  1. Click the 'New item' button
  1. In the 'Label' field, enter an appropriate name
  1. Click the '...' button next to the 'Execute' field and locate the tintwizard.py file
  1. Save your changes in obmenu


> The above steps can be adapted for other menu types, e.g. Gnome Menu.

## I cannot run tintwizard. ##
  1. Locate tintwizard.py in your file browser.
  1. Right-click on the file and select 'Properties'
  1. Select the 'Permissions' tab
  1. Be sure that the program has permission to be executed

  1. Alternatively, open a terminal in the same directory as tintwizard.py and type:
```
chmod +x tintwizard.py
```

# Using tintwizard #
## What does _option_ do? ##
Please read the [tint2 configuration guide](http://code.google.com/p/tint2/wiki/Configure) for in depth information on what everything does.

## How do I use my config? ##
```
tint2 -c PATH_TO_CONFIG_FILE
```

## How do I replace the default config? ##
Navigate to _$HOME/.config/tint2_ and replace the file _tint2rc_ with your config file.

## My config file does not work with tint2 ##
Are you using the most recent version of tint2?

## How do I suggest new features? ##
If you would like to suggest a new feature for tintwizard, please file a [feature request](http://code.google.com/p/tintwizard/issues/entry).

## How do I report bugs? ##
File bugs [here](http://code.google.com/p/tintwizard/issues/entry). Thank you for your support by reporting bugs.

# Configuring tintwizard #
## What does tintwizard.conf do? ##
This allows you to set default values for several options within tintwizard, such as background and font color. When a new tint2 config is created, these values will be used as default.

## Where is the config file located? ##
The config file is tintwizard.conf, in the _$HOME/.config/tint2_ directory.

## Font ##
The option _font_ is formatted like so:
```
font = name style size
```
For example:
```
font = Sans Bold 12
```
Alternatively, to not set a default font:
```
font = None
```

## Background Color ##
The option _bgColor_ is formatted like so:
```
bgColor = #rrggbb
```
For example:
```
bgColor = #ff0000
```
Alternatively, to not set a default background color:
```
bgColor = None
```

## Foreground Color ##
The option _fgColor_ is formatted like so:
```
fgColor = #rrggbb
```
For example:
```
fgColor = #ff0000
```
Alternatively, to not set a default foreground color:
```
fgColor = None
```

## Border Color ##
The option _borderColor_ is formatted like so:
```
borderColor = #rrggbb
```
For example:
```
borderColor = #ff0000
```
Alternatively, to not set a default foreground color:
```
borderColor = None
```

## Background Count ##
### What does this do? ###
This sets the default number of background styles to define.
### Format ###
The option _bgCount_ is formatted like so:
```
bgCount = number
```
For example:
```
bgCount = 3
```
Alternatively, to not set a default background count:
```
bgCount = None
```