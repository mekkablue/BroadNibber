# BroadNibber.glyphsFilter

This is a plugin for the [Glyphs font editor](http://glyphsapp.com/) by Georg Seifert.
It turns monolines of all selected glyphs into broad-nib strokes. After installation, it will add the menu item *Filter > BroadNibber*. You can set a keyboard shortcut in System Preferences.

![Broad-nibbing a monoline.](BroadNibber.png "BroadNibber")

### Installation

1. Download the complete ZIP file and unpack it, or clone the repository.
2. Double click the .glyphsFilter file. Confirm the dialog that appears in Glyphs.
3. Restart Glyphs

### Usage Instructions

1. Open a glyph in Edit View, or select any number of glyphs in Font or Edit View.
2. Use *Filter > BroadNibber* to add broad-nib strokes to your lines. Experiment with the values.

Alternatively, you can also use it as a custom parameter:

	Property: Filter
	Value: BroadNibber; width:<width>; height:<height>; angle:<angle>

... where `<width>` is the width of the pen, `<height>` its thickness, and `<angle>` the nib angle. The order does not matter, e.g.:
	
	Property: Filter
	Value: BroadNibber; height:30; angle:10; width:40

At the end of the parameter value, you can hang `exclude:` or `include:`, followed by a comma-separated list of glyph names. This will apply the filter only to the included glyphs, or the glyphs not excluded, respectively.

### Requirements

The plugin needs Glyphs 2.4 or higher. I assume it will not work in earlier versions.

### License

Copyright 2014 Rainer Erich Scheichelbauer (@mekkablue).
Based on sample code by Georg Seifert (@schriftgestalt).

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

See the License file included in this repository for further details.
