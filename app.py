import sys
import time
import serial
import serial.tools.list_ports
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, QRegExp
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QRegExpValidator
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow

#HILO DE RECEPCION
class ReceiveThread(QThread):
    messageReceive = pyqtSignal(str)

    def __init__(self, ser):
        super(ReceiveThread, self).__init__()
        self.ser = ser

    def run(self):
        global connectionStatus
        self.runningState = True
        print("Corriendo papa")
        while self.runningState:
                try:
                    mensaje = self.ser.readline().decode().rstrip()
                    self.messageReceive.emit(mensaje)
                except serial.SerialException as e:
                    print(f"{str(e)}")
                    connectionStatus = False 
                    self.runningState = False
                except UnicodeDecodeError as e:
                    print(f"Error de decodificación Unicode: {str(e)}")   


    def stop(self):
        self.runningState = False

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("main.ui", self)
        self.ser = None
        self.receiveThread = None

        self.peso = 0

        #self.inicioStatus = False

        self.ui_components()

        timer = QTimer(self)
        timer.timeout.connect(self.connect_port)
        timer.start(1500)

        self.alertaBtn.clicked.connect(self.alerta_btn_call)
        self.iniciarBtn.clicked.connect(self.iniciar_btn_call)
        self.detenerBtn.clicked.connect(self.detener_btn_call)
        self.taraBtn.clicked.connect(self.tara_btn_call)


    def ui_components(self):
       pixmap = QPixmap("fondo.jpg")
       self.fondo.setPixmap(pixmap)

       pixmap = QPixmap("usb_off.png")
       self.statusIcon.setPixmap(pixmap)

       regex = QRegExp("[0-9]+")
       validator = QRegExpValidator(regex)
       self.selPesoLE.setValidator(validator)
       
       self.alertaFrame.hide()
       self.detenerBtn.setEnabled(True)

    def alerta_btn_call(self):
        self.alertaFrame.hide()

    def tara_btn_call(self):
        if self.ser:
               message = 't'
               self.ser.write(message.encode())
               self.alertaFrame.show()
               self.alertaBtn.hide()
               self.alertaLbl.setText('Seteando tara...')
    
    def iniciar_btn_call(self):
        #self.inicioStatus = True
        if self.ser:
            txt = self.selPesoLE.text()
            if(txt == ""):
                return
            self.peso = int(txt)
            if(self.peso > 0 and self.peso <= 125):
                self.iniciarBtn.setEnabled(False)
                self.taraBtn.setEnabled(False)
                self.detenerBtn.setEnabled(True)
                self.progressBar.setValue(0)
                self.progressBar.setMaximum(self.peso)

                message = 'in' + chr(self.peso)
                self.ser.write(message.encode())
            else:
                self.alertaFrame.show()
                self.alertaLbl.setText('Seleccione un peso de\n 1 a 125g.')   
        
    def detener_btn_call(self):
        if self.ser:
            self.iniciarBtn.setEnabled(True)
            self.taraBtn.setEnabled(True)
            self.detenerBtn.setEnabled(False)
            message = 'd'
            self.ser.write(message.encode())
            self.progressBar.setValue(0)                    

    def connect_port(self):
        global connectionStatus
        if not connectionStatus:
            puertos_disponibles = serial.tools.list_ports.comports()
            puertos = []
            for puerto in puertos_disponibles:
                puertos.append(puerto.device)  
            if puertos != []:
                if not self.receiveThread or not self.receiveThread.isRunning():
                    try: 
                        self.ser = serial.Serial(puerto[0], velocidad)
                        print(f'Conexión establecida en el puerto {puerto}')
                        self.receiveThread = ReceiveThread(self.ser)
                        self.receiveThread.messageReceive.connect(self.handleResults)
                        self.receiveThread.start()
                        connectionStatus = True  
                        pixmap = QPixmap("usb.png")
                        self.statusIcon.setPixmap(pixmap)
                    except serial.SerialException as e:
                        print(f"No se pudo conectar al puerto {puertos[0]}: {str(e)}")
                        connectionStatus = False
            else:
                pixmap = QPixmap("usb_off.png")
                self.statusIcon.setPixmap(pixmap)  
                self.ser = None
                             
    def handleResults(self, new_result):
        try:
            if(new_result[0] == 'p'):
                percent = int(float(new_result[1:]))
                self.progressBar.setValue(percent)
            elif(new_result[0] == 'T'):
                self.alertaFrame.show()
                self.alertaBtn.show()
                self.alertaLbl.setText('Tara completa')
            elif(new_result[0] == 'c'):
                self.alertaFrame.show()
                self.alertaLbl.setText('Completado')
                self.iniciarBtn.setEnabled(True)
                self.taraBtn.setEnabled(True)
                self.detenerBtn.setEnabled(False)        
        except:
            pass        

    def open_info(self):
        self.info_open_anim.start()

    def close_info(self):
        self.info_close_anim.start()           
    
if __name__ == '__main__':            

    connectionStatus = False
    velocidad = 9600        
    app = QApplication(sys.argv)
    form = MainWindow()
    widget = QtWidgets.QStackedWidget()
    widget.setFixedHeight(457)
    widget.setFixedWidth(751)
    widget.addWidget(form)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Saliendo")   