from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import mysql.connector as con

import sys

from PyQt5.uic import loadUiType

ui, _ =loadUiType('Bookstore.ui')


mydb = con.connect(host='localhost' , port = '3306' , user = 'root' , password = 'root' , database = 'bookstore')
cursor = mydb.cursor()

class MainApp(QMainWindow, ui):

	mydb = con.connect(host='localhost' , port = '3306' , user = 'root' , password = 'root' , database = 'bookstore')
	cursor = mydb.cursor()

	def __init__(self):
		QMainWindow.__init__(self)
		self.setupUi(self)

		self.tabWidget.setCurrentIndex(0)
		self.tabWidget.tabBar().setVisible(False) 
		#self.menubar.setVisible(False) 	#to display top bar

		self.menu11.triggered.connect(self.registercust)
		self.b01.clicked.connect(self.registercust)

		self.menu21.triggered.connect(self.displaybook)
		self.b02.clicked.connect(self.displaybook)

		self.menu31.triggered.connect(self.bookborrow)
		self.b03.clicked.connect(self.bookborrow)

		self.menu41.triggered.connect(self.grandbill)
		self.b04.clicked.connect(self.grandbill)

		self.menu51.triggered.connect(self.exitt)

	def fill_customer_id(self):
		try:
			cid = 100
			cursor.execute("select * from customer")
			result = cursor.fetchall()
			if result:
				for Cust_id in result:
					cid += 1
			self.tb01.setText(str(cid+1))
		except con.error as e:
			print("guogb")
	
	
	
	def registercust(self):

		self.tabWidget.setCurrentIndex(0)
		self.fill_customer_id()
		try:
			id = self.tb01.text()
			name = self.tb02.text()
			pno = self.tb03.text()
			email = self.tb04.text()
			address = self.tb05.text() 

			query= "insert into Customer(Cust_id , Cust_Name , Phone , Email , Address) values(%s,%s,%s,%s,%s);"
			value = (id , name , pno , email , address)
			cursor.execute(query, value)
			mydb.commit()
			QMessageBox.information(self , "Bookstore Management System", "Registered Successfully")

			self.l11.setText("Registered Successfully ")

		except con.Error as e :
			self.l11.setText("Unsuccessfull Try Again")

		self.tb01.clear()
		self.tb02.clear()
		self.tb03.clear()
		self.tb04.clear()
		self.tb05.clear()

	def displaybook(self):
		self.tabWidget.setCurrentIndex(1)
		try:

			query = "select * from books"
			cursor.execute(query)
			result = cursor.fetchall()

			self.table01.setColumnWidth(0,100)
			self.table01.setColumnWidth(1,450)
			self.table01.setColumnWidth(2,190)
			self.table01.setColumnWidth(3,100)
			self.table01.setColumnWidth(4,100)

			self.table01.setRowCount(0)
			for row_number , row_data in enumerate(result):
				self.table01.insertRow(row_number)
				for column_number , data in enumerate(row_data):
					self.table01.setItem(row_number , column_number , QTableWidgetItem(str(data)))
			QMessageBox.information(self , "Bookstore Management System", "Displaying Books ")

		except con.Error as e:
			QMessageBox.information(self , "Bookstore Management System", "Unsuccessfull TryAgain ")


	def bookborrow(self):
		self.tabWidget.setCurrentIndex(2)
		try:

			custid = self.tb06.text()
			bookid= self.tb07.text()
			quantity = self.tb08.text() 

			args = (custid , bookid , quantity)
			cursor.callproc('generate_bill' , args)
			mydb.commit()

			self.ll31.setText("Book Bought ")

			QMessageBox.information(self, "Bookstore Management System", "Book Successfully Bought" )

		except con.Error as e:
			self.ll31.setText("Enter Data ")

		self.tb06.clear()
		self.tb07.clear()
		self.tb08.clear()

	def grandbill(self):
		self.tabWidget.setCurrentIndex(3)
		try:

			custtid = self.tb09.text()

			cursor.callproc('GRAND_BILL', [custtid])
			mydb.commit()

			self.table02.setColumnWidth(0,100)
			self.table02.setColumnWidth(1,200)
			self.table02.setColumnWidth(2,200)
			self.table02.setColumnWidth(3,200)
			self.table02.setColumnWidth(4,160)

			query = "select * from book_billing where Cust_id = %s;"
			cursor.execute(query , [custtid])
			result = cursor.fetchall()

			self.table02.setRowCount(0)
			for row_number , row_data in enumerate(result):
				self.table02.insertRow(row_number)
				for column_number , data in enumerate(row_data):
					self.table02.setItem(row_number , column_number , QTableWidgetItem(str(data)))


			self.ll41.setText("Successful ")
			QMessageBox.information(self, "Bookstore Management System", "Bill Successfully Generated" )

		except con.Error as e:
			self.ll41.setText("Enter Cust ID ")

		self.tb09.clear()

	def exitt(self):
		self.tabWidget.setCurrentIndex(4)




def main():
	app = QApplication(sys.argv)
	window = MainApp()
	window.show()
	app.exec_()

if __name__ == '__main__':
	main()
