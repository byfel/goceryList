from re import S
from subprocess import DETACHED_PROCESS
from PyQt5 import uic, QtWidgets, QtCore, QtGui
import sys
from colorama import Cursor
import mysql.connector
#from mysql.connector
from reportlab.pdfgen import canvas
import pandas as pd


numero_id = 0


#conexão com o banco de dados Mysql

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="cadastro_produtos"
)
def editar():
    global numero_id

    linha = segunda_janela.tableWidget.currentRow()

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id=dados_lidos[linha][0]
    cursor.execute("SELECT * FROM produtos WHERE id="+ str(valor_id))
    produto = cursor.fetchall()

    JanelaEdit.show()

    

    JanelaEdit.lineEdit.setText(str(produto[0][0]))
    JanelaEdit.lineEdit_3.setText(str(produto[0][2]))
    JanelaEdit.lineEdit_4.setText(str(produto[0][3]))
    JanelaEdit.lineEdit_5.setText(str(produto[0][4]))
    JanelaEdit.lineEdit_6.setText(str(produto[0][5]))
    JanelaEdit.lineEdit_7.setText(str(produto[0][6]))
    numero_id = valor_id
    #print(produto[0][0])


def salvarEdit():
    #pega o numero do id
    global numero_id

    
    

    #valores digitados na janela de edição
    
    nome = JanelaEdit.lineEdit_3.text()
    #tipo = JanelaEdit.lineEdit_4.text()
    #marca =JanelaEdit.lineEdit_5.text()
    #medida = JanelaEdit.lineEdit_6.text()
    valor = JanelaEdit.lineEdit_7.text()

    #atualizar os dados no banco
    #cursor = banco.cursor()
    #cursor.execute("UPDATE produtos SET nome ='{}', tipo = '{}', marca = '{}', medida '{}', valor = '{}' WHERE id = {}".format(nome,tipo,marca,medida,valor,numero_id))
    cursor = banco.cursor()
    atualiza= """ UPDATE produtos SET valor =""" + str(valor)+ """ WHERE id = """ + str(numero_id)
    cursor.execute(atualiza)
    banco.commit()
    
    #atualizar janela

    JanelaEdit.close()
    segunda_janela.close()
    chamar_tela()

    


    
def deletar():
   linha = segunda_janela.tableWidget.currentRow()
   
   segunda_janela.tableWidget.removeRow(linha)

   cursor = banco.cursor()
   cursor.execute("SELECT id FROM produtos")
   dados_lidos = cursor.fetchall()
   valor_id=dados_lidos[linha][0]
   cursor.execute("DELETE FROM produtos WHERE id="+ str(valor_id))
  



def gera_pdf():
#função que imprime os dados no formato PDF.

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    y = 0
    pdf = canvas.Canvas("cadastro_produtos.pdf")
    pdf.setFont("Times-Bold", 20)
    pdf.drawString(200,800, "Produtos Cadastrado:")
    pdf.setFont("Times-Bold", 12)

    pdf.drawString(10,750, "ID")
    pdf.drawString(110,750, "CODIGO")
    pdf.drawString(210,750, "NOME")
    pdf.drawString(310,750, "TIPO")
    pdf.drawString(410,750, "MARCA")
    pdf.drawString(510,750, "MEDIDA")
    pdf.drawString(610,750, "VALOR")

    for i in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(10,750 -y, str(dados_lidos[i][0]))
        pdf.drawString(110,750 -y, str(dados_lidos[i][1]))
        pdf.drawString(210,750 -y, str(dados_lidos[i][2]))
        pdf.drawString(310,750 -y, str(dados_lidos[i][3]))
        pdf.drawString(410,750 -y, str(dados_lidos[i][4]))
        pdf.drawString(510,750 -y, str(dados_lidos[i][5]))
        pdf.drawString(610,750 -y, str(dados_lidos[i][6]))

    pdf.save()
    print("PDF FOI GERADO COM SUCESSO")




def funcao_principal():
    # Função que que pega od dados e inserem direto no banco de dados
    linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_2.text()
    linha3 = formulario.lineEdit_3.text()
    linha4 = formulario.lineEdit_4.text()
    linha5 = formulario.lineEdit_5.text()

    print("Nome:",linha1)
    print("Tipo:",linha2)
    print("Marca:",linha3)
    print("Medida:",linha4)
    print("Valor:",linha5)

    cursor = banco.cursor()
    comando_SQL = "INSERT INTO produtos (nome,tipo,marca,medida,valor) VALUES (%s,%s,%s,%s,%s)"
    dados = (str(linha1),str(linha2),str(linha3),str(linha4),str(linha5))
    cursor.execute(comando_SQL,dados)
    banco.commit()
    formulario.lineEdit.setText("")
    formulario.lineEdit_2.setText("")
    formulario.lineEdit_3.setText("")
    formulario.lineEdit_4.setText("")
    formulario.lineEdit_5.setText("")

def chamar_tela():

    #função para chamar a segunda a tela atravez do botão listar da primeira tela

    segunda_janela.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    segunda_janela.tableWidget.setRowCount(len(dados_lidos))
    segunda_janela.tableWidget.setColumnCount(7)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 7):
           segunda_janela.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))



def gera_csv():
    #gera um arquivo csv dos dados 

    import csv

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    # 1. cria o arquivo
    f = open('tabelaProdutos.csv', 'w', newline='', encoding='utf-8')

    # 2. cria o objeto de gravação
    w = csv.writer(f)

    # 3. grava as linhas
    #for i in range(len(dados_lidos)):
        #for j in range(0, 1):
    w.writerow(dados_lidos)

    # Recomendado: feche o arquivo
    #w.close() 


app=QtWidgets.QApplication([])
formulario=uic.loadUi("formulario.ui")
segunda_janela=uic.loadUi("Segunda_janela.ui")
JanelaEdit=uic.loadUi("JanelaEdit.ui")
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_3.clicked.connect(chamar_tela)
segunda_janela.pushButton_5.clicked.connect(gera_pdf)
segunda_janela.pushButton_4.clicked.connect(gera_csv)
segunda_janela.pushButton_3.clicked.connect(deletar)
segunda_janela.pushButton_2.clicked.connect(editar)
JanelaEdit.pushButton.clicked.connect(salvarEdit)



formulario.show()
app.exec()

