#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import Qt, QByteArray, QDataStream, QIODevice
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter, QColor
from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QMenu, QAction, \
    qApp, QFileDialog, QApplication, QDialog
from PyQt5.QtNetwork import QHostAddress, QTcpServer

class QImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tcpServer = None
        self.scaleFactor = 0.0

        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setVisible(False)

        self.setCentralWidget(self.scrollArea)

        self.createActions()
        self.createMenus()

        self.setWindowTitle("Image Viewer")
        self.resize(803,825)
        self.openImage()
        self.sessionOpened()

    def sessionOpened(self):
        self.tcpServer = QTcpServer(self)
        PORT = 8000
        address = QHostAddress('127.0.0.1')
        if not self.tcpServer.listen(address, PORT):
            print("cant listen!")
            self.close()
            return
        self.tcpServer.newConnection.connect(self.dealCommunication)

    def dealCommunication(self):
        # Get a QTcpSocket from the QTcpServer
        clientConnection = self.tcpServer.nextPendingConnection()
        # instantiate a QByteArray
        block = QByteArray()
        # QDataStream class provides serialization of binary data to a QIODevice
        out = QDataStream(block, QIODevice.ReadWrite)
        # We are using PyQt5 so set the QDataStream version accordingly.
        out.setVersion(QDataStream.Qt_5_0)
        out.writeUInt16(0)
        # this is the message we will send it could come from a widget.
        message = "ACK!"
        # get a byte array of the message encoded appropriately.
        message = bytes(message, encoding='ascii')
        # now use the QDataStream and write the byte array to it.
        out.writeString(message)
        out.device().seek(0)
        out.writeUInt16(block.size() - 2)
        # wait until the connection is ready to read
        while True:
            clientConnection.waitForReadyRead()
            # read incomming data
            instr = clientConnection.readAll()
            # in this case we print to the terminal could update text of a widget if we wanted.
            data = str(instr, encoding='ascii')
            print(data)
            if data.strip() == "END":
                break
            clientConnection.write(block)   
        clientConnection.disconnected.connect(clientConnection.deleteLater)
        clientConnection.disconnectFromHost()

    def openImage(self):
        filename = "/home/rsamanez/python/gui_programming/src/main/image/black.jpg"
        image = QImage(filename)
        #if image.isNull():
        #    QMessageBox.information(self, "Image Viewer", "Cannot load %s." % fileName)
        #    return
        w = 0
        for x in range(1, 800):
            for y in range(1,800):
                w = w + 1
                if w > 255:
                    w = 0
                image.setPixel(x,y,w)
        mypixmap = QPixmap.fromImage(image)
        #mypixmap = QPixmap(filename)
        self.imageLabel.setPixmap(mypixmap)
        self.scaleFactor = 1.0

        self.scrollArea.setVisible(True)
        self.fitToWindowAct.setEnabled(True)
        self.updateActions()

        if not self.fitToWindowAct.isChecked():
            self.imageLabel.adjustSize()
    def open(self):
        self.resize(100, 100)

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()



    def createActions(self):
        self.openAct = QAction("&Open...", self, shortcut="Ctrl+O", triggered=self.open)
        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        self.zoomInAct = QAction("Zoom &In (25%)", self, shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)
        self.zoomOutAct = QAction("Zoom &Out (25%)", self, shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)
        self.normalSizeAct = QAction("&Normal Size", self, shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)
        self.fitToWindowAct = QAction("&Fit to Window", self, enabled=False, checkable=True, shortcut="Ctrl+F",
                                      triggered=self.fitToWindow)


    def createMenus(self):
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)



        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    imageViewer = QImageViewer()
    imageViewer.show()
    sys.exit(app.exec_())
