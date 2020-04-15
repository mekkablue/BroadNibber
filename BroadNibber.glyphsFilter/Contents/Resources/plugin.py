# encoding: utf-8
from __future__ import division, print_function, unicode_literals

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
from Foundation import NSClassFromString

class BroadNibber(FilterWithDialog):
	# GUI elements:
	dialog = objc.IBOutlet()
	widthField = objc.IBOutlet()
	heightField = objc.IBOutlet()
	angleField = objc.IBOutlet()
	
	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': u'BroadNibber',
			'fr': u'Traceur',
			'de': u'Mit Breitfeder nachziehen',
			'es': u'Trazar con pluma chata',
			'zh': u'✒️扁头笔风格化',			
		})
		self.actionButtonLabel = Glyphs.localize({
			'en': u'Trace',
			'fr': u'Appliquer',
			'de': u'Nachziehen',
			'es': u'Aplicar',
			'zh': u'确定',
		})
		
		# Load dialog from .nib (without .extension)
		self.loadNib('IBdialog', __file__)
	
	# On dialog show
	@objc.python_method
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
	@objc.python_method
	def filter(self, thisLayer, inEditView, customParameters):
		
		# Called on font export, get value from customParameters
		if 'width' in customParameters:
			width = customParameters['width']
		if 'height' in customParameters:
			height = customParameters['height']
		if 'angle' in customParameters:
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
		self.offsetLayer( thisLayer, width*0.5, height*0.5, makeStroke=True, position=0.5, autoStroke=False )
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
	
	@objc.python_method
	def rotateLayer( self, thisLayer, angle ):
		"""Rotates all paths in the thisLayer."""
		rotation = NSAffineTransform.transform()
		rotation.rotateByDegrees_(angle)
		thisLayer.transform_checkForSelection_doComponents_(rotation,False,False)
	
	@objc.python_method
	def offsetLayer( self, thisLayer, offsetX, offsetY, makeStroke=False, position=0.5, autoStroke=False ):
		offsetFilter = NSClassFromString("GlyphsFilterOffsetCurve")
		try:
			# GLYPHS 3:	
			offsetFilter.offsetLayer_offsetX_offsetY_makeStroke_autoStroke_position_metrics_error_shadow_capStyleStart_capStyleEnd_keepCompatibleOutlines_(
				thisLayer,
				offsetX, offsetY, # horizontal and vertical offset
				makeStroke,     # if True, creates a stroke
				autoStroke,     # if True, distorts resulting shape to vertical metrics
				position,       # stroke distribution to the left and right, 0.5 = middle
				None, None, None, 0, 0, False )
		except:
			# GLYPHS 2:
			offsetFilter.offsetLayer_offsetX_offsetY_makeStroke_autoStroke_position_error_shadow_(
				thisLayer,
				offsetX, offsetY, # horizontal and vertical offset
				makeStroke,     # if True, creates a stroke
				autoStroke,     # if True, distorts resulting shape to vertical metrics
				position,       # stroke distribution to the left and right, 0.5 = middle
				None, None )
	
	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
	