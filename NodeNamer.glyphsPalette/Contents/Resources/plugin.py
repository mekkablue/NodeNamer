# encoding: utf-8

###########################################################################################################
#
#
#	Palette Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Palette
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *

class NodeNamer (PalettePlugin):
	
	dialog = objc.IBOutlet()
	nodeNameField = objc.IBOutlet()
	
	@objc.python_method
	def settings(self):
		self.name = Glyphs.localize({
			'en': u'Node Namer',
			'de': u'NodeNamer',
			'es': u'Nombrar los nodos',
			'fr': u'Nommer les nœuds',
			'zh': u'锚点名称',
		})
		
		# Load .nib dialog (without .extension)
		self.loadNib('IBdialog', __file__)
	
	@objc.python_method
	def start(self):
		# Adding a callback for the 'GSUpdateInterface' event
		Glyphs.addCallback(self.update, UPDATEINTERFACE)
	
	@objc.python_method
	def __del__(self):
		Glyphs.removeCallback(self.update)
	
	@objc.python_method
	def update( self, sender ):
		# only update if there is a window:
		if self.windowController():
			theseGlyphs = []
			font = self.windowController().document().font
			
			# We’re in the Edit View
			if font and font.currentTab and len(font.selectedLayers) == 1:
				selectedLayer = font.selectedLayers[0]
				selectedNodes = [item for item in selectedLayer.selection if type(item)==GSNode]
				nodeNames = [n.name for n in selectedNodes]
				uniqueNodeNames = set(nodeNames)
				numberOfUniqueNodeNames = len(uniqueNodeNames)
				numberOfSelectedNodes = len(selectedNodes)
				
				if numberOfSelectedNodes == 0:
					self.nodeNameField.setPlaceholderString_(Glyphs.localize({
						'en': u'No nodes selected',
						'de': u'Keine Punkte ausgewählt',
						'es': u'Ningún nodo seleccionado',
						'fr': u'Aucun nœud selectionné',
						'zh': u'未选中任何锚点',
					}))
					self.nodeNameField.setStringValue_("")
					
				elif numberOfUniqueNodeNames == 1:
					self.nodeNameField.setPlaceholderString_( Glyphs.localize({
						'en': u'Empty node name%s' % ("" if numberOfSelectedNodes==1 else "s"),
						'de': u'Kein%s Punktname%s gesetzt' % (
							"" if numberOfSelectedNodes==1 else "e",
							"" if numberOfSelectedNodes==1 else "n",
							),
						'es': u'Nota%s vacía%s.' % (
							"" if numberOfSelectedNodes==1 else "s",
							"" if numberOfSelectedNodes==1 else "s",
							),
						'fr': u'Nom%s vide%s' % (
							"" if numberOfSelectedNodes==1 else "s",
							"" if numberOfSelectedNodes==1 else "s",
							),
						'zh': u'未命名锚点',
					}))
					nodeName = tuple(uniqueNodeNames)[0]
					if not nodeName:
						nodeName = ""
					self.nodeNameField.setStringValue_(nodeName)
		
				else:
					self.nodeNameField.setPlaceholderString_(Glyphs.localize({
						'en': u'Multiple names',
						'de': u'Mehrere Namen',
						'es': u'Nombres múltiples',
						'fr': u'Multiples noms',
						'zh': u'多个名称',
					}))
					self.nodeNameField.setStringValue_("")
	
	@objc.IBAction
	def setNodeName_(self, sender):
		"""
		Sets the glyph note to whatever has been entered
		into the text field in the palette.
		"""
		
		if self.windowController():
			# Extract font from sender
			font = self.windowController().document().font

			# We’re in the Edit View
			if font and font.currentTab and len(font.selectedLayers) == 1:
				nodeName = self.nodeNameField.stringValue()
				if nodeName=="":
					nodeName=None
				selectedLayer = font.selectedLayers[0]
				selectedNodes = [item for item in selectedLayer.selection if type(item)==GSNode]
				for thisNode in selectedNodes:
					thisNode.name=self.nodeNameField.stringValue()
	

	
	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
	
	# Temporary Fix
	# Sort ID for compatibility with v919:
	_sortID = 0
	@objc.python_method
	def setSortID_(self, id):
		try:
			self._sortID = id
		except Exception as e:
			self.logToConsole( "NodeNamer setSortID_: %s" % str(e) )
	
	@objc.python_method
	def sortID(self):
		return self._sortID
	