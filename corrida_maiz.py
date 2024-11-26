from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

import sys
import mysql.connector

def create_db_connection():
    return mysql.connector.connect(
        host="localhost",   # Cambia esto si tu base de datos está en un servidor diferente
        user="root",  # Reemplaza con tu usuario de MySQL
        password="root",  # Reemplaza con tu contraseña de MySQL
        database="Molino",  #Base de datos correspondiente.
    )


# Ventana principal con título y botón para continuar
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Corrida de Maíz MOLINO")
        self.setGeometry(600, 100, 600, 500)
       # Estilo para imagen de fondo de la ventana principal
        self.setStyleSheet("""
            QMainWindow {
                background-image: url('TORTILLA.jpg');
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }
        """)


        # Título
        self.label = QLabel("Corrida de Maíz MOLINO", self)
        self.label.setGeometry(120, 50, 350, 30)
        font = QFont("Arial", 20)  # Cambia "Arial" por el nombre de la fuente deseada y 16 por el tamaño
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        # Botón para pasar a la siguiente interfaz
        self.pushButton = QPushButton("Siguiente", self)
        self.pushButton.setGeometry(250, 200, 100, 40)
        self.pushButton.clicked.connect(self.openNextWindow)

         # Botón para salir de la aplicación
        self.exitButton = QPushButton("Salir", self)
        self.exitButton.setGeometry(250, 250, 100, 40)
        self.exitButton.clicked.connect(self.close)  # Cierra la ventana principal y termina el programa

     # Función para abrir la segunda ventana
    def openNextWindow(self):
        self.secondWindow = SecondWindow()
        self.secondWindow.show()
        self.close()


# Segunda ventana con seis botones
class SecondWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MENU MOLINO")
        self.setGeometry(600, 100, 600, 500)

        # Botón para regresar a la ventana principal
        self.backButton = QPushButton("Volver a INICIO", self)
        self.backButton.setGeometry(400, 400, 160, 50)
                                   #IZQ-DER,ARRIBA-ABAJO,ANCHO,LARGO
        self.backButton.clicked.connect(self.goBackToMain)
          # Estilo para imagen de fondo de la ventana de opciones
        self.setStyleSheet("""
            QMainWindow {
                background-image: url('CAMPO.jpg');
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }
        """)
        

        # Botón 1
        self.pushButton1 = QPushButton("TORTILLERIAS REGISTRADAS", self)
        self.pushButton1.setGeometry(40, 150, 200, 40)
        self.pushButton1.clicked.connect(lambda: self.openOptionWindow("I1 TORTILLERIAS REGISTRADAS", ["Id_Tortilleria", "Nombre", "Nombre_Dueño", " Dirección", "Telefono", "Contraseña"]))

        # Botón 2
        self.pushButton2 = QPushButton("Almacen", self)
        self.pushButton2.setGeometry(250, 150, 100, 40)
        self.pushButton2.clicked.connect(lambda: self.openOptionWindow("I2 Almacen", ["Id_Almacen", "Id_Producto", "Cantidad_Stock", " Nivel_Minimo"]))

        # Botón 3
        self.pushButton3 = QPushButton("Ordenes de Tortillerias", self)
        self.pushButton3.setGeometry(400, 150, 150, 40)
        self.pushButton3.clicked.connect(lambda: self.openOptionWindow("I3 Ordenes de Tortillerias", ["Id_Orden ", "Id_Proveedor", "Fecha_Orden", "Estado"]))

        # Botón 4
        self.pushButton4 = QPushButton("Pedidos", self)
        self.pushButton4.setGeometry(40, 300, 100, 40)
        self.pushButton4.clicked.connect(lambda: self.openOptionWindow("I4 Pedido", ["Id_Pedido", "Id_Tortilleria", "Cantidad_Masa", "Fecha_Pedido", "Hora_Pedido", "Estado"]))

        # Botón 5
        self.pushButton5 = QPushButton("Factura", self)
        self.pushButton5.setGeometry(250, 300, 100, 40)
        self.pushButton5.clicked.connect(lambda: self.openOptionWindow("I5 Factura", ["ID", "Id_Factura ", " Id_Tortilleria", "Fecha_Factura", "Monto_Total", "Estado_Pago"]))

        # Botón 6
        self.pushButton6 = QPushButton("Pagos", self)
        self.pushButton6.setGeometry(400, 300, 100, 40)
        self.pushButton6.clicked.connect(lambda: self.openOptionWindow("I6 Pagos", ["Id_Pago", " Id_Factura", "Monto_Pagado", "Fecha_Pago", "Estado_Pago"]))

          # Función para abrir una ventana de opción específica con títulos de columnas personalizados
    def openOptionWindow(self, title, column_names):
        self.optionWindow = OptionWindow(title, column_names, self)
        self.optionWindow.show()
        self.close()

    # Función para volver a la ventana principal
    def goBackToMain(self):
        self.mainWindow = MainWindow()
        self.mainWindow.show()
        self.close()


# Clase genérica para cada interfaz con tabla para ingresar datos, botón de regreso y nombres de columnas personalizados
class OptionWindow(QMainWindow):
    def __init__(self, title, column_names, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle(title)
        self.setGeometry(200, 200, 500, 400)

        # Layout principal
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Etiqueta con el título de la interfaz
        self.label = QLabel(title, self)
        self.layout.addWidget(self.label)

        # Tabla con nombres de columnas personalizados
        self.table = QTableWidget(self)
        self.table.setColumnCount(len(column_names))
        self.table.setHorizontalHeaderLabels(column_names)
        self.layout.addWidget(self.table)

        # Botón para cargar datos de MySQL 
        if title == "I1 TORTILLERIAS REGISTRADAS":
            self.loadDataButton = QPushButton("Cargar datos de 'Tortilleria'", self)
            self.loadDataButton.clicked.connect(self.loadDataFromDatabase)
            self.layout.addWidget(self.loadDataButton)

        elif title == "I2 Almacen":
            self.loadDataButton = QPushButton("Cargar datos de 'Almacen'", self)
            self.loadDataButton.clicked.connect(self.loadDataFromAlmacen)
            self.layout.addWidget(self.loadDataButton)

        elif title == "I3 Ordenes de Tortillerias":
            self.loadDataButton = QPushButton("Cargar datos de 'Orden_Proveedor'", self)
            self.loadDataButton.clicked.connect(self.loadDataFromOrdenProveedor)
            self.layout.addWidget(self.loadDataButton)    

        elif title == "I4 Pedido":
            self.loadDataButton = QPushButton("Cargar datos de 'Pedido'", self)
            self.loadDataButton.clicked.connect(self.loadDataFromPedido)
            self.layout.addWidget(self.loadDataButton)
#----------------------------------------------------------------------------------------------------
        # Botón para agregar una fila (opcional, si deseas agregar manualmente)
        #self.addRowButton = QPushButton("Agregar Fila", self)
        #self.addRowButton.clicked.connect(self.addRow)
        #self.layout.addWidget(self.addRowButton)

        # Botón para guardar en MySQL (opcional)
        #self.saveButton = QPushButton("Guardar en MySQL", self)
        #self.saveButton.clicked.connect(self.saveToDatabase)
        #self.layout.addWidget(self.saveButton)
#-----------------------------------------------------------------------------------------------------
        # Botón para regresar al menú de opciones
        self.backButton = QPushButton("Volver a Opciones", self)
        self.backButton.clicked.connect(self.goBackToOptions)
        self.layout.addWidget(self.backButton)

    # Función para cargar datos de la tabla 'Tortilleria' y mostrarlos en la tabla de la interfaz 1
    def loadDataFromDatabase(self):
        connection = create_db_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM Tortilleria"
        cursor.execute(query)
        results = cursor.fetchall()
        self.table.setRowCount(len(results))

        for row_index, row_data in enumerate(results):
            for column_index, data in enumerate(row_data):
                self.table.setItem(row_index, column_index, QTableWidgetItem(str(data)))

        cursor.close()
        connection.close()
        print("Datos cargados desde la tabla 'Tortilleria'")
#------------------------------------------------------------------------------------------------    
    # Función para cargar datos de la tabla 'Almacen' en Interfaz 2
    def loadDataFromAlmacen(self):
        connection = create_db_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM Almacen"
        cursor.execute(query)
        results = cursor.fetchall()
        self.table.setRowCount(len(results))

        for row_index, row_data in enumerate(results):
            for column_index, data in enumerate(row_data):
                self.table.setItem(row_index, column_index, QTableWidgetItem(str(data)))

        cursor.close()
        connection.close()
        print("Datos cargados desde la tabla 'Almacen'")

#-------------------------------------------------------------------------------------------
    # Función para cargar datos de la tabla 'Orden_Proveedor' en Interfaz 3
    def loadDataFromOrdenProveedor(self):
        connection = create_db_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM Orden_Proveedor"
        cursor.execute(query)
        results = cursor.fetchall()
        self.table.setRowCount(len(results))

        for row_index, row_data in enumerate(results):
            for column_index, data in enumerate(row_data):
                self.table.setItem(row_index, column_index, QTableWidgetItem(str(data)))

        cursor.close()
        connection.close()
        print("Datos cargados desde la tabla 'Orden_Proveedor'")    
#-------------------------------------------------------------------------------------------------
    # Función para cargar datos de la tabla 'Pedido' en Interfaz 4
    def loadDataFromPedido(self):
        connection = create_db_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM Pedido"
        cursor.execute(query)
        results = cursor.fetchall()
        self.table.setRowCount(len(results))

        for row_index, row_data in enumerate(results):
            for column_index, data in enumerate(row_data):
                self.table.setItem(row_index, column_index, QTableWidgetItem(str(data)))

        cursor.close()
        connection.close()
        print("Datos cargados desde la tabla 'Pedido'")

#---------------------------------------------------------------------------------------------------
    # Función para agregar una fila a la tabla
    def addRow(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

    # Función para guardar los datos en la base de datos MySQL
    def saveToDatabase(self):
        connection = create_db_connection()
        cursor = connection.cursor()

        for row in range(self.table.rowCount()):
            data = []
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                data.append(item.text() if item else None)

            placeholders = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO datos_interfaz ({', '.join(self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount()))}) VALUES ({placeholders})"
            cursor.execute(query, data)

        connection.commit()
        cursor.close()
        connection.close()
        print("Datos guardados en la base de datos")

    # Función para volver a la ventana de opciones
    def goBackToOptions(self):
        self.parent_window.show()
        self.close()

# Configuración e inicio de la aplicación (parte principal)
def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()