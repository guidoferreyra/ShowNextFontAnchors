#!/usr/bin/env python
# encoding: utf-8
from __future__ import division, print_function, unicode_literals

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from math import radians, tan

class showNextFontAnchors(ReporterPlugin):
	
	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Next Font Anchors',
			'de': 'Anker der nächsten Schrift',
			'fr': 'les ancres de la police suivante',
			'es': 'anclas de la siguiente fuente',
			'pt': 'âncoras da próxima fonte',
			})
		
		self.missingAnchors=None

	@objc.python_method
	def background( self, Layer ):
		try:
			if len(Glyphs.fonts) > 1:
				NSColor.colorWithCalibratedRed_green_blue_alpha_( 0.0, 0.5, 0.3, 0.5 ).set()
				self.checkAnchors( Layer )
		except Exception as e:
			print(e)
			print()
			import traceback
			print(traceback.format_exc())
	
	@objc.python_method
	def checkAnchors ( self, Layer ):
		thisGlyph = Layer.parent
		thisFont = thisGlyph.parent
		thisMaster = Layer.master
		masters = thisFont.masters
		
		nextFont = Glyphs.fonts[1]
		nextFontMasters = nextFont.masters
		nextGlyph = nextFont.glyphs[thisGlyph.name]
		if not nextGlyph and "." in thisGlyph.name:
			dotOffset = thisGlyph.name.find(".")
			coreGlyphName = thisGlyph.name[:dotOffset]
			nextGlyph = nextFont.glyphs[coreGlyphName]
		
		if not nextGlyph:
			self.missingAnchors = None
		else:
			activeMasterIndex = masters.index(thisMaster)
		
			if len(masters) != len(nextFontMasters):
				nextLayer = nextGlyph.layers[0]
			else:
				nextLayer = nextGlyph.layers[activeMasterIndex]
		
			orange = NSColor.orangeColor().colorWithAlphaComponent_(0.67)
			grey = NSColor.grayColor().colorWithAlphaComponent_(0.9)
		
			#Hago sets de las listas
			nextFontAnchorsSet = set([a.name for a in nextLayer.anchors])
			thisFontAnchorsSet = set([a.name for a in Layer.anchors])

			#Hace sets con las difrencias
			missingInNextFont = thisFontAnchorsSet.difference(nextFontAnchorsSet)
			missingInThisFont = nextFontAnchorsSet.difference(thisFontAnchorsSet)

			anchorNamesMissingInThisFont = "\n".join(["+ %s "%name for name in missingInThisFont])
			self.drawTextAtPoint( anchorNamesMissingInThisFont, NSPoint(0,0), fontSize=10.0, fontColor=orange, align="bottomright" )
			
			anchorNamesMissingInNextFont = "\n".join(["− %s"%name for name in missingInNextFont])
			self.drawTextAtPoint( anchorNamesMissingInNextFont, NSPoint(0,0), fontSize=10.0, fontColor=grey, align="bottomleft" )
			
			self.missingAnchors = missingInThisFont
			
	
	@objc.python_method
	def conditionalContextMenus(self):
		# Execute only if layers are actually selected
		if not self.missingAnchors or len(Glyphs.font.selectedLayers)!=1:
			return []
		else:
			# Add context menu item
			contextMenus = [{
				'name': Glyphs.localize({
					'en': 'Add missing anchors from next font',
					'de': 'Fehlende Anker aus der nächsten Schrift hinzufügen',
					'fr': 'Ajouter les ancres manquantes de la police suivante',
					'es': 'Agregar anclas faltantes de la próxima fuente',
					'pt': 'Adicionar âncoras ausentes da próxima fuente',
					}), 
				'action': self.addMissingAnchors_
				}]

			# Return list of context menu items
			return contextMenus
	
	def addMissingAnchors_(self, sender=None):
		pass
		if self.missingAnchors:
			currentLayer = Glyphs.font.selectedLayers[0]
			if currentLayer:
				currentLayer.clearSelection()
				for i, anchorName in enumerate(self.missingAnchors):
					y = -10-i*20
					newAnchor = GSAnchor()
					newAnchor.name = anchorName
					newAnchor.position = NSPoint(0, y)
					currentLayer.anchors.append(newAnchor)
					currentLayer.selection.append(newAnchor)
	
	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
