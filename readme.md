# Sublime Upload to [JustPaste.me](http://justpaste.me) Plugin

- A Sublime Text 2 plugin that uploads code snippets to [JustPaste.me](http://justpaste.me). Once uploaded, the link is immediately copied to your clipboard, ready to share with your friends!

## Installation

1. Via [**Package Control**](http://wbond.net/sublime_packages/package_control): Press <kbd>ctrl</kbd> + <kbd>shift</kbd> + <kbd>p</kbd> and Search for the package `Just Paste`.

1. [Download the plugin](https://github.com/downloads/Apathetic012/JustPaste/JustPaste%20v1.0.zip) and extract it to your **Packages** Directory

## Usage

- Highlight a code or go to the file you want to upload its code

- Either `right click > Upload to JustPaste` or use the plugin-default keyboard shortcut `F1` to upload:
   - a snippet of highlighted code
   - the current file

![](http://i.imgur.com/womux.png)

- Link will be automatically copied to your clipboard

![](http://i.imgur.com/SUonN.png)

### Change keyboard shortcut

Go to `Preferences > Key Bindings - User` and add the following line:

    { "keys": ["ctrl+shift+j"], "command": "justpaste" }

Change `ctrl+shift+j` with the key combination you want to bind the plugin with.

