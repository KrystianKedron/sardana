#!/usr/bin/env python

#############################################################################
##
## This file is part of Taurus, a Tango User Interface Library
## 
## http://www.tango-controls.org/static/taurus/latest/doc/html/index.html
##
## Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
## 
## Taurus is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## Taurus is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
## 
## You should have received a copy of the GNU Lesser General Public License
## along with Taurus.  If not, see <http://www.gnu.org/licenses/>.
##
#############################################################################

"""This module contains the graphics view widget for jdraw files"""

__all__ = ["TaurusJDrawSynopticsView"]

__docformat__ = 'restructuredtext'

import os
import traceback
import subprocess
from taurus.qt import Qt
from taurus.core import DeviceNameValidator,AttributeNameValidator
from taurus.qt.qtgui.graphic.taurusgraphic import parseTangoUri
from taurus.qt.qtcore.mimetypes import TAURUS_ATTR_MIME_TYPE, TAURUS_DEV_MIME_TYPE, TAURUS_MODEL_MIME_TYPE
from taurus.qt.qtgui.base import TaurusBaseWidget
import jdraw_parser

class TaurusJDrawSynopticsView(Qt.QGraphicsView, TaurusBaseWidget):
    '''
    TaurusJDrawSynopticsView and TaurusGraphicsScene signals/slots
    
    External events::
    
     Slot selectGraphicItem(const QString &) displays a selection
     mark around the TaurusGraphicsItem that matches the argument passed.
    
    Mouse Left-button events::
    
     Signal graphicItemSelected(QString) is triggered, passing the
     selected TaurusGraphicsItem.name() as argument.
    
    Mouse Right-button events::
    
     TaurusGraphicItem.setContextMenu([(ActionName,ActionMethod(device_name))]
     allows to configure custom context menus for graphic items using a list
     of tuples. Empty tuples will insert separators in the menu.
    '''    
    __pyqtSignals__ = ("itemsChanged","modelsChanged","graphicItemSelected(QString)","graphicSceneClicked(QPoint)")

    def __init__(self, parent = None, designMode = False, updateMode=None, alias = None, resizable = True):
        name = self.__class__.__name__
        self.call__init__wo_kw(Qt.QGraphicsView, parent)
        self.call__init__(TaurusBaseWidget, name, designMode=designMode)
        self._currF = self.modelName
        self.path = ''
        self.w_scene = None
        self.h_scene = None
        self._fileName ="Root"
        self._mousePos = (0,0)
        self.setResizable(resizable)
        self.setInteractive(True)
        self.setAlias(alias)
        self.setDragEnabled(True)
        
        # By default the items will update the view when necessary.
        # This default value is much more efficient then the QQraphicsView default
        # value, so if you decide to change then expect a lot of processor to be
        # used by your application.
        if updateMode is None:
            self.setViewportUpdateMode(Qt.QGraphicsView.NoViewportUpdate)
        else:
            self.setViewportUpdateMode(updateMode)

    def defineStyle(self):
        self.updateStyle()

    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
    # TaurusBaseWidget over writing
    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-

    def isReadOnly(self):
        return True

    def update(self):
        #self.emit_signal()
        self.emitColors()

    def openJDraw(self):
        ifile = unicode(Qt.QFileDialog.getOpenFileName( self, 'Load JDraw File', '', 'JDraw File (*.jdw)'))
        if not ifile: return
        fileName = ifile.split("/")
        self._fileName = fileName[-1]
        self.setModel(ifile)
        return fileName[-1]
        
    def setAlias(self,alias):
        """ Assigning a dictionary like {'Tag':'Value'} with tags to be replaced in object names while parsing. """
        if (isinstance(alias,dict) or hasattr(alias,'items')) and alias:
            self.alias = alias
        else:
            self.alias = None
        return

    def get_item_list(self):
        return [item._name for item in self.scene().items() if hasattr(item,'_name') and item._name]
    
    def get_device_list(self):
        items = [(item,parseTangoUri(item)) for item in self.get_item_list()]
        return list(set(v['devicename'] for k,v in items if v)) 
    
    def get_item_colors(self,emit = False):
        item_colors = {}
        try:
            for item in self.scene().items():
                if not getattr(item,'_name','') or not getattr(item,'_currBgBrush',None):
                    continue
                item_colors[item._name] = item._currBgBrush.color().name()
            if emit: self.emit(Qt.SIGNAL("itemsChanged"),self.modelName.split('/')[-1].split('.')[0],item_colors)
        except:
            self.warning('Unable to emitColors: %s'%traceback.format_exc())
        return item_colors
        
    #@Qt.pyqtSignature("selectGraphicItem(QString)")
    @Qt.pyqtSignature("selectGraphicItem(const QString &)")
    def selectGraphicItem(self,item_name):
        self.scene().selectGraphicItem(item_name)
        return False
    
    @Qt.pyqtSignature("graphicItemSelected(QString)")
    def graphicItemSelected(self,item_name):
        self.emit(Qt.SIGNAL("graphicItemSelected(QString)"),item_name)
        
    @Qt.pyqtSignature("graphicSceneClicked(QPoint)")
    def graphicSceneClicked(self,point):
        self.debug('In TaurusJDrawSynopticsView.graphicSceneClicked(%s,%s)'%(point.x(),point.y()))
        self.emit(Qt.SIGNAL("graphicSceneClicked(QPoint)"),point)        
        
    def modelsChanged(self):
        items = self.get_item_list()
        self.info('modelsChanged(%s)'%len(items))
        self.emit(Qt.SIGNAL("modelsChanged"),items)
    
    def emitColors(self): 
        '''emit signal which is used to refresh the tree and colors of icons depend of the current status in jdrawSynoptic'''
        self.get_item_colors(True)

    def get_sizes(self):
        srect = self.scene().sceneRect()
        sizes = [x for s in (self.size(),self.sizeHint(),srect.size()) for x in (s.width(),s.height())]
        try:
            s = self.parent().size()
            sizes.extend([s.width(),s.height()])
        except: sizes.extend([0,0])
        return tuple(sizes)
    
    def fitting(self,ADJUST_FRAME = False):
        """
        Parent size is the size of the bigger panel (desn't keep ratio)
        Rect size never changes (fixed by the graphics objects)
        Size and SizeHint move one around the other
        
        the method works well until an object is clicked, 
        then the whole reference changes and doesn't work again.
        """
        
        srect = self.scene().sceneRect()
        w,h = (srect.width(),srect.height())
        offset = self.mapToGlobal(Qt.QPoint(srect.x(),srect.y()))
        x0,y0 = (offset.x(),offset.y())

        self.debug('\n\nIn TauJDrawSynopticsView.fitting()')
        self.debug(self.get_sizes())
        self.debug('\tAdjusting SizeHint: size(%s,%s),hint(%s,%s),srect(%s,%s),parent(%s,%s)'%self.get_sizes())
        self.debug('\toffset = %s,%s ; size = %s,%s'%(x0,y0,w,h))
        self.fitInView(x0,y0,w,h,Qt.Qt.KeepAspectRatio)
        
        if ADJUST_FRAME: #This additional resizing adjust the "white" frame around the synoptic
            self.debug('\tResizing: size(%s,%s),hint(%s,%s),srect(%s,%s),parent(%s,%s)'%self.get_sizes())
            self.resize(self.sizeHint()+Qt.QSize(5,5)) 
            
        #THIS LINE MUST BE ALWAYS EXECUTED, It prevents the UP/DOWN resize BUG!!!
        #apparently Qt needs this 2 fitInView calls to be aware of it, maybe first offset was not good
        self.debug('\tFitting:: size(%s,%s),hint(%s,%s),srect(%s,%s),parent(%s,%s)'%self.get_sizes())
        self.fitInView(x0,y0,w,h,Qt.Qt.KeepAspectRatio)
        
        self.debug('Done: size(%s,%s),hint(%s,%s),srect(%s,%s),parent(%s,%s)\n\n'%self.get_sizes())
        
    def resizeEvent(self, event):
        """ It has been needed to reimplent size policies """
        if not self.resizable() or not self.scene() or isinstance(self.parent(),Qt.QScrollArea) or not self.isVisible():
            self.debug('In TaurusJDrawSynopticsView('+self._fileName+').resizeEvent(): Disabled')
            return
        try:
            self.debug('In TaurusJDrawSynopticsView('+self._fileName+').resizeEvent()')
            if self.size() == self.sizeHint():
                self.debug('\tSize already fits: %s'%self.size())
                return
            self.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)
            self.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOff)
            self.fitting()
            self.emitColors()
        except Exception,e:
            self.warning('Exception in JDrawView('+self._fileName+').resizeEvent: %s' % traceback.format_exc())
            pass

    def refreshModel(self):
        self.setModel(self.getModelName())

    def updateStyle(self):
        self.repaint()
        
    def repaint(self):
        Qt.QGraphicsView.repaint(self)
        #self.fitting()        
        
    def getGraphicsFactory(self,delayed=False):
        import jdraw
        return jdraw.TaurusJDrawGraphicsFactory(self,alias=(self.alias or None),delayed=delayed) #self.parent())

    ###########################################################################
    
    def getFramed(self):
        try: parent = self.parent()
        except: parent = None
        frame = Qt.QFrame(parent)
        self.setFrameStyle(self.StyledPanel|self.Raised)
        self.setLineWidth(2)        
        self.setParent(frame)
        return frame      
        
    def setResizable(self,resizable):
        self._resizable = resizable
        
    def resizable(self):
        return self._resizable
        
    def mousePressEvent(self,event):
        """ Records last event position to use it for DragEvents """
        try: 
            self.mousePos = event.scenePos().x(),event.scenePos().y()
        except:
            self.mousePos = event.x(), event.y()
            self.debug('MouseEvent received is not a GraphicsScene event, using raw position %s'%str(self.mousePos))
        TaurusBaseWidget.mousePressEvent(self,event)
        
    def getModelMimeData(self):
        """ Used for drag events """
        model,mimeData = '',None
        try:
            #model = getattr(self.scene().itemAt(*self.mousePos),'_name','')
            model = getattr(self.scene()._selectedItems[0],'_name','')
            self.debug('getModelMimeData(%s)'%model)
            mimeData = Qt.QMimeData()
            if model:
                if DeviceNameValidator().getParams(model): 
                    self.debug('getMimeData(): DeviceModel at %s: %s',self.mousePos,model)
                    mimeData.setData(TAURUS_DEV_MIME_TYPE,model)
                elif AttributeNameValidator().getParams(model):
                    self.debug('getMimeData(): AttributeModel at %s: %s',self.mousePos,model)
                    mimeData.setData(TAURUS_ATTR_MIME_TYPE,model)
                else:
                    self.debug('getMimeData(): UnknownModel at %s: %s',self.mousePos,model)
                    mimeData.setData(TAURUS_MODEL_MIME_TYPE, model)
        except:
            self.warning('jdrawView.getModelMimeData(%s): unable to get MimeData'%model)
            self.warning(traceback.format_exc())
        return mimeData
        

    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
    # QT properties 
    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-

    @Qt.pyqtSignature("setModel(QString)")
    def setModel(self, model, alias = None, delayed = False):
        self.modelName = str(model)
        self._currF = str(model)
        if alias is not None: self.setAlias(alias)
        self.info('setModel(%s)'%model)
        if self._currF:
            #filename = str(self._currFile.absoluteFilePath())
            filename = self._currF
            filename = os.path.realpath(filename)
            if os.path.isfile(filename):            
                self.debug("Starting to parse %s" % filename)
                self.path = os.path.dirname(filename)
                factory = self.getGraphicsFactory(delayed=delayed)
                scene = jdraw_parser.parse(filename, factory)
                self.debug("Obtained %s(%s)", type(scene).__name__,filename)
                if not scene:
                    self.warning("TaurusJDrawSynopticsView.setModel(%s): Unable to parse %s!!!"%(model,filename))
                elif self.w_scene is None and scene.sceneRect():
                    self.w_scene = scene.sceneRect().width()
                    self.h_scene = scene.sceneRect().height()
                else: self.debug('JDrawView.sceneRect() is NONE!!!')
                self.setScene(scene)
                Qt.QObject.connect(self.scene(), Qt.SIGNAL("graphicItemSelected(QString)"), self, Qt.SLOT("graphicItemSelected(QString)"))
                Qt.QObject.connect(self.scene(), Qt.SIGNAL("graphicSceneClicked(QPoint)"), self, Qt.SLOT("graphicSceneClicked(QPoint)"))
                Qt.QObject.connect(Qt.QApplication.instance(), Qt.SIGNAL("lastWindowClosed()"), self.scene().panel_launcher.kill )
                self.modelsChanged()
                self.setWindowTitle(self.modelName)
                #The emitted signal contains the filename and a dictionary with the name of items and its color
                self.emitColors()#get_item_colors(emit=True)
                self.fitting(True)
            else:
                self.setScene(None)
            
    #def destroy(destroyWindow=True,destroySubWindows=True):
    def closeEvent(self,event):
        try: self.scene().panel_launcher.kill()
        except: print(traceback.format_exc())
        Qt.QGraphicsView.closeEvent(self,event)
        #Qt.QGraphicsView.destroy(self,destroyWindow,destroySubWindows)

    def setModels(self):
        """ This method triggers item.setModel(item._name) in all internal items. """
        for item in self.scene().items():
            if item._name and isinstance(item, taurus.qt.qtgui.graphic.TaurusGraphicsItem):
                self.debug('TaurusJDrawGraphicsFactory.setModels(): calling item.setModel(%s)'%(item._name))
                item.setModel(item._name)

    def getModel(self):
        return self._currF

    @classmethod
    def getQtDesignerPluginInfo(cls):
        ret = TaurusBaseWidget.getQtDesignerPluginInfo()
        ret['group'] = 'Taurus Display'
        ret['module'] = 'taurus.qt.qtgui.graphic'
        ret['icon'] = ":/designer/graphicsview.png"
        return ret
    
    model = Qt.pyqtProperty("QString", getModel, setModel)
    
    
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def jdraw_view_main():
    import sys
    import taurus.qt.qtgui.graphic
    taurus.setLogLevel(taurus.Info)
    app = Qt.QApplication(sys.argv)
    
    #form = Qt.QDialog()
    #ly=Qt.QVBoxLayout(form)
    #container=Qt.QWidget()
    #ly.addWidget(container)   
    #for m in sys.argv[1:]:
        #tv=TaurusJDrawSynopticsView(container, designMode=False)
        #tv.setModel(m)
        
    form = taurus.qt.qtgui.graphic.TaurusJDrawSynopticsView(designMode=False)
    form.show()
    form.setModel(sys.argv[1])
    form.setWindowTitle(sys.argv[1].rsplit('.',1)[0])
    #def kk(*args):print("\tgraphicItemSelected(%s)"%str(args))
    #form.connect(form,Qt.SIGNAL("graphicItemSelected(QString)"), kk)
    form.fitting()
    sys.exit(app.exec_())

if __name__ == "__main__":
    jdraw_view_main()