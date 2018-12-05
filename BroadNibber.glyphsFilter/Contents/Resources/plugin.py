# encoding: utf-8

###########################################################################################################
#
#
#	Filter with dialog Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Filter%20with%20Dialog
#
#	For help on the use of Interface Builder:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates
#
#
###########################################################################################################

import objc, math
from GlyphsApp import *
from GlyphsApp.plugins import *

class BroadNibber(FilterWithDialog):
	# GUI elements:
	dialog = objc.IBOutlet()
	widthField = objc.IBOutlet()
	heightField = objc.IBOutlet()
	angleField = objc.IBOutlet()
	
	# offset curve filter: 
	offsetCurveFilter = NSClassFromString("GlyphsFilterOffsetCurve")
	
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': u'BroadNibber',
			'fr': u'Traceur',
			'de': u'Mit Breitfeder nachziehen',
			'es': u'Trazar con pluma chata',
			'zh': u'扁头笔风格化',			
		})
		self.actionButtonLabel = Glyphs.localize({
			'en': u'Trace',
			'fr': u'Appliquer',
			'de': u'Nachziehen',
			'es': u'Aplicar',
			'zh': u'应用',
		})
		
		# Load dialog from .nib (without .extension)
		self.loadNib('IBdialog', __file__)
	
	# On dialog show
	def start(self):
		# Default settings:
		NSUserDefaults.standardUserDefaults().registerDefaults_({
			"com.mekkablue.BroadNibber.width": "50",
			"com.mekkablue.BroadNibber.height": "10",
			"com.mekkablue.BroadNibber.angle": "30",
		})
		
		# Populate entry fields
		self.widthField.setStringValue_(Glyphs.defaults['com.mekkablue.BroadNibber.width'])
		self.heightField.setStringValue_(Glyphs.defaults['com.mekkablue.BroadNibber.height'])
		self.angleField.setStringValue_(Glyphs.defaults['com.mekkablue.BroadNibber.angle'])
		
		# Set focus to text field
		self.widthField.becomeFirstResponder()
		
	# Actions triggered by UI input:
	@objc.IBAction
	def setWidth_( self, sender ):
		# Store value coming in from dialog
		Glyphs.defaults['com.mekkablue.BroadNibber.width'] = sender.floatValue()
		# Trigger redraw
		self.update()
	
	@objc.IBAction
	def setHeight_( self, sender ):
		# Store value coming in from dialog
		Glyphs.defaults['com.mekkablue.BroadNibber.height'] = sender.floatValue()
		# Trigger redraw
		self.update()
	
	@objc.IBAction
	def setAngle_( self, sender ):
		# Store value coming in from dialog
		Glyphs.defaults['com.mekkablue.BroadNibber.angle'] = sender.floatValue()
		# Trigger redraw
		self.update()
	
	# Actual filter
	def filter(self, thisLayer, inEditView, customParameters):
		
		# Called on font export, get value from customParameters
		if customParameters.has_key('width'):
			width = customParameters['width']
		if customParameters.has_key('height'):
			height = customParameters['height']
		if customParameters.has_key('angle'):
			angle = customParameters['angle']
		
		# Called through UI, use stored value
		else:
			width = float(Glyphs.defaults['com.mekkablue.BroadNibber.width'])
			height = float(Glyphs.defaults['com.mekkablue.BroadNibber.height'])
			angle = float(Glyphs.defaults['com.mekkablue.BroadNibber.angle'])
		
		# insert points at extrema and in inflections (better offset results):
		thisLayer.addExtremePoints()
		thisLayer.addInflectionPoints()
		# rotate and expand:
		self.rotateLayer( thisLayer, -angle )
		self.offsetCurveFilter.offsetLayer_offsetX_offsetY_makeStroke_autoStroke_position_error_shadow_( 
			thisLayer, # Layer
			width*0.5, # offsetX
			height*0.5, # offsetY
			True, # makeStroke
			False, # autoStroke
			0.5, # position
			None, # error
			None # shadow
			)
		# rotate back and tidy up paths:
		self.rotateLayer( thisLayer, angle )
		thisLayer.cleanUpPaths()
	
	def generateCustomParameter( self ):
		return "%s; width:%s; height:%s; angle:%s;" % (
			self.__class__.__name__, 
			Glyphs.defaults['com.mekkablue.BroadNibber.width'],
			Glyphs.defaults['com.mekkablue.BroadNibber.height'],
			Glyphs.defaults['com.mekkablue.BroadNibber.angle'],
			)
	
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__

	def rotateLayer( self, thisLayer, angle ):
		"""Rotates all paths in the thisLayer."""
		rotation = NSAffineTransform.transform()
		rotation.rotateByDegrees_(angle)
		thisLayer.transform_checkForSelection_doComponents_(rotation,False,False)
	
