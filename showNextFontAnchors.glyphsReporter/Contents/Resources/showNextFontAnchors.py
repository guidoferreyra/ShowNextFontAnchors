#!/usr/bin/env python
# encoding: utf-8




import objc
from Foundation import *
from AppKit import *
import sys, os, re
import math

MainBundle = NSBundle.mainBundle()
path = MainBundle.bundlePath() + "/Contents/Scripts"
if not path in sys.path:
	sys.path.append( path )

from GlyphsApp import *

GlyphsReporterProtocol = objc.protocolNamed( "GlyphsReporter" )

class showNextFontAnchors ( NSObject, GlyphsReporterProtocol ):
	
	def init( self ):
		try:
			#Bundle = NSBundle.bundleForClass_( NSClassFromString( self.className() ));
			return self
		except Exception as e:
			self.logToConsole( "init: %s" % str(e) )
	
	def interfaceVersion( self ):
		try:
			return 1
		except Exception as e:
			self.logToConsole( "interfaceVersion: %s" % str(e) )
	
	def title( self ):
		try:
			return "Next Font Anchors"
		except Exception as e:
			self.logToConsole( "title: %s" % str(e) )
	
	def keyEquivalent( self ):
		try:
			return None
		except Exception as e:
			self.logToConsole( "keyEquivalent: %s" % str(e) )
	
	def modifierMask( self ):
		try:
			return 0
		except Exception as e:
			self.logToConsole( "modifierMask: %s" % str(e) )
	
	def drawForegroundForLayer_( self, Layer ):
		try:
			pass
		except Exception as e:
			self.logToConsole( "drawForegroundForLayer_: %s" % str(e) )
	
	
	def checkAnchors ( self, Layer ):

		thisGlyph = Layer.parent
		thisFont = thisGlyph.parent
		thisMaster = thisFont.selectedFontMaster
		masters = thisFont.masters
		split = str(thisGlyph).split('"')
		nextFont = Glyphs.fonts[1]
		nextFontMasters = nextFont.masters
		nextGlyph = nextFont.glyphs[split[1]]

		xHeight = thisFont.selectedFontMaster.xHeight
		angle = thisFont.selectedFontMaster.italicAngle
		offset = math.tan(math.radians(angle)) * xHeight/2
		
		lista1 = []
		lista2 = []

		initPos = 5
		fontColor1 = NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.91, 0.32, 0.06, 0.45 )
		fontColor2 = NSColor.colorWithCalibratedRed_green_blue_alpha_( 0, 0, 0, 0.45 )
		fontColor3 = NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.0, 0.5, 0.3, 0.8 )

		try:
			# Glyphs 2 (Python 2.7)
			activeMasterIndex = masters.index(thisMaster)
		except:
			# Glyphs 1 (Python 2.6)
			for i, k in enumerate(masters):
				if thisMaster == masters[i]:
					activeMasterIndex = i

		
		if len(masters) != len(nextFontMasters):
			nextLayer = nextGlyph.layers[0]
		else:
			nextLayer = nextGlyph.layers[activeMasterIndex]

		
		for nextLayerAnchor in nextLayer.anchors:
			lista1.append(nextLayerAnchor.name)
			step = + 20
			self.drawTextAtPoint( u"· %s" % nextLayerAnchor.name, (10 - offset, initPos), 14.0, fontColor1 )
			initPos = initPos + step
		for thisLayerAnchor in Layer.anchors:
			lista2.append(thisLayerAnchor.name)
			self.drawTextAtPoint( u"· %s" % thisLayerAnchor.name, (10 - offset, initPos), 14.0, fontColor2 )
			initPos = initPos + step


		#Hago sets de las listas
		font1Set = set(lista1)
		font2Set = set(lista2)
		
		#Hace sets con las difrencias
		diff1 = font1Set.difference(font2Set)
		diff2 = font2Set.difference(font1Set)

		ok = "ok"
		if not diff1 and not diff2:
			self.drawTextAtPoint( u"OK", (10 - offset, initPos), 14.0, fontColor3 )


	
	def drawBackgroundForLayer_( self, Layer ):
		try:
			NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.0, 0.5, 0.3, 0.5 ).set()
			self.checkAnchors ( Layer )
		except Exception as e:
			self.logToConsole( "drawBackgroundForLayer_: %s" % str(e) )
	
	def drawBackgroundForInactiveLayer_( self, Layer ):
		try:
			#pass
			NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.0, 0.5, 0.3, 0.5 ).set()
			self.checkAnchors ( Layer )	
		except Exception as e:
			self.logToConsole( "drawBackgroundForInactiveLayer_: %s" % str(e) )
	
	def needsExtraMainOutlineDrawingForInactiveLayer_( self, Layer ):
		return True
	
	def drawTextAtPoint( self, text, textPosition, fontSize, fontColor):
		try:
			glyphEditView = self.controller.graphicView()
			currentZoom = self.getScale()
			fontAttributes = { 
				NSFontAttributeName: NSFont.labelFontOfSize_( fontSize/currentZoom ),
				NSForegroundColorAttributeName: fontColor }
			displayText = NSAttributedString.alloc().initWithString_attributes_( text, fontAttributes )
			textAlignment = 0 # top left: 6, top center: 7, top right: 8, center left: 3, center center: 4, center right: 5, bottom left: 0, bottom center: 1, bottom right: 2
			glyphEditView.drawText_atPoint_alignment_( displayText, textPosition, textAlignment )
		except Exception as e:
			self.logToConsole( "drawTextAtPoint: %s" % str(e) )
	
	def getHandleSize( self ):
		try:
			Selected = NSUserDefaults.standardUserDefaults().integerForKey_( "GSHandleSize" )
			if Selected == 0:
				return 5.0
			elif Selected == 2:
				return 10.0
			else:
				return 7.0 # Regular
		except Exception as e:
			self.logToConsole( "getHandleSize: HandleSize defaulting to 7.0. %s" % str(e) )
			return 7.0

	def getScale( self ):
		try:
			return self.controller.graphicView().scale()
		except:
			self.logToConsole( "Scale defaulting to 1.0" )
			return 1.0
	
	def setController_( self, Controller ):
		try:
			self.controller = Controller
		except Exception as e:
			self.logToConsole( "Could not set controller" )
	
	def logToConsole( self, message ):
		myLog = "Show %s plugin:\n%s" % ( self.title(), message )
		NSLog( myLog )
