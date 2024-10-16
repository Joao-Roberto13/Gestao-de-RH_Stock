import os, re
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from collections import deque
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from fpdf import FPDF

#Armazem.....
# Ficheiro para salvar os dados
ficheiro = "funcionarios.txt"

def filtro(text, table_widget):
    text = re.sub(r'[\W_]+', "", text).lower()
    for row in range(table_widget.rowCount()):
        hide_row = True
        for col in range(table_widget.columnCount()):
            item = table_widget.item(row, col)
            if item and text in item.text().lower():
                hide_row = False
                break
        table_widget.setRowHidden(row, hide_row)

def carregar_dadosRH():
    """Carrega os dados do ficheiro de texto para a tableWidget."""
    if os.path.exists(ficheiro):
        with open(ficheiro, "r") as file:
            for line in file:
                nome, area_trabalho, cargo, departamento = line.strip().split(",")
                rowPosition = screen_RH.tableWidget.rowCount()
                screen_RH.tableWidget.insertRow(rowPosition)
                screen_RH.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(nome))
                screen_RH.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(area_trabalho))
                screen_RH.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(cargo))
                screen_RH.tableWidget.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(departamento))

def salvar_dados():
    """Salva os dados da tableWidget no ficheiro de texto."""
    with open(screen_RH.ficheiro, "w") as file:
        for row in range(screen_RH.tableWidget.rowCount()):
            nome = screen_RH.tableWidget.item(row, 0).text()
            area_trabalho = screen_RH.tableWidget.item(row, 1).text()
            cargo = screen_RH.tableWidget.item(row, 2).text()
            departamento = screen_RH.tableWidget.item(row, 3).text()
            file.write(f"{nome},{area_trabalho},{cargo},{departamento}\n")

def registrar_funcionario():
    """Adiciona um novo funcionário na tabela e no ficheiro."""
    nome = screen_RH.lineEdit_2.text()
    area_trabalho = screen_RH.lineEdit_5.text()
    cargo = screen_RH.lineEdit.text()
    departamento = screen_RH.lineEdit_3.text()

    if nome and area_trabalho and cargo and departamento:
        rowPosition = screen_RH.tableWidget.rowCount()
        screen_RH.tableWidget.insertRow(rowPosition)

        screen_RH.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(nome))
        screen_RH.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(area_trabalho))
        screen_RH.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(cargo))
        screen_RH.tableWidget.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(departamento))

        # Limpar campos de texto
        screen_RH.lineEdit_2.clear()
        screen_RH.lineEdit_5.clear()
        screen_RH.lineEdit.clear()
        screen_RH.lineEdit_3.clear()

        # Salvar os dados no ficheiro
        screen_RH.salvar_dados()

def alterar_funcionario():
    """Altera os dados do funcionário selecionado na tabela e atualiza o ficheiro."""
    selected_row = screen_RH.tableWidget.currentRow()

    if selected_row >= 0:  # Verifica se uma linha foi selecionada
        screen_RH.tableWidget.setItem(selected_row, 0, QtWidgets.QTableWidgetItem(screen_RH.lineEdit_2.text()))
        screen_RH.tableWidget.setItem(selected_row, 1, QtWidgets.QTableWidgetItem(screen_RH.lineEdit_5.text()))
        screen_RH.tableWidget.setItem(selected_row, 2, QtWidgets.QTableWidgetItem(screen_RH.lineEdit.text()))
        screen_RH.tableWidget.setItem(selected_row, 3, QtWidgets.QTableWidgetItem(screen_RH.lineEdit_3.text()))

        # Limpar campos de texto
        screen_RH.lineEdit_2.clear()
        screen_RH.lineEdit_5.clear()
        screen_RH.lineEdit.clear()
        screen_RH.lineEdit_3.clear()

        # Atualizar o ficheiro com as alterações
        screen_RH.salvar_dados()

def excluir_funcionario():
    """Remove o funcionário selecionado na tabela e atualiza o ficheiro."""
    selected_row = screen_RH.tableWidget.currentRow()

    if selected_row >= 0:  # Verifica se uma linha foi selecionada
        screen_RH.tableWidget.removeRow(selected_row)
        # Atualizar o ficheiro com as alterações
        screen_RH.salvar_dados()

#Recurso Humanos...
# Inicializando o estoque único e o preço total
estoque = deque()
preco_total = 0
vendas_diarias = {}
compras_diarias = {}
quantidades_diarias = {}

# Função para carregar dados do arquivo de texto
def carregar_dadosArmazem():
    global preco_total, estoque, vendas_diarias, compras_diarias, quantidades_diarias

    try:
        with open("dados_estoque.txt", "r") as file:
            for line in file:
                data, quantidade, preco = line.strip().split(",")
                quantidade = int(quantidade)
                preco = float(preco)
                aprovisionar(data, quantidade, preco)  # Chama a função para aprovisionar produtos
    except FileNotFoundError:
        # Arquivo não encontrado, iniciar com estoque vazio
        pass
    except Exception as e:
        QMessageBox.warning(screen, "Erro ao carregar dados", str(e))

# Função para salvar dados no arquivo de texto
def salvar_dados():
    with open("dados_estoque.txt", "w") as file:
        
        # Itera sobre os itens no estoque e grava no arquivo
        for data, quantidade, preco in estoque:
            file.write(f"{data},{quantidade},{preco}\n")

# Função para aprovisionar os produtos no estoque
def aprovisionar(data, quantidade, preco):
    global preco_total
    # Atualiza o preço total com base na quantidade e no preço
    preco_total += quantidade * preco

    # Atualiza as compras diárias
    if data in compras_diarias:
        compras_diarias[data] += quantidade * preco
    else:
        compras_diarias[data] = quantidade * preco
    
    # Atualiza as quantidades diárias
    if data in quantidades_diarias:
        quantidades_diarias[data] += quantidade
    else:
        quantidades_diarias[data] = quantidade

    # O estoque agora deve ser uma estrutura que aceita a data, a quantidade e o preço
    estoque.append((data, quantidade, preco))

    # Atualiza a interface da tableWidget
    adicionar_linha_tabela(data, quantidade, preco)
    atualizar_preco_total()
    atualizar_quantidade_total()

# Função para adicionar uma linha na tableWidget
def adicionar_linha_tabela(data, quantidade, preco):
    # Calcular o total
    total = quantidade * preco

    # Contar as linhas existentes e adicionar uma nova
    row_position = screen.tableWidget.rowCount()
    screen.tableWidget.insertRow(row_position)

    # Preencher as colunas da nova linha
    screen.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(data))
    screen.tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(str(quantidade)))
    screen.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(f"{preco:.2f} MT"))
    screen.tableWidget.setItem(row_position, 3, QtWidgets.QTableWidgetItem(f"{total:.2f} MT"))  # Adiciona o valor total

# Função para atualizar a tableWidget após venda (limpar e repopular)
def atualizar_tabela_apos_venda():
    screen.tableWidget.setRowCount(0)  # Limpa todas as linhas da tabela
    for data, quantidade, preco in estoque:
        adicionar_linha_tabela(data, quantidade, preco)

# Função para atualizar o preço total exibido
def atualizar_preco_total():
    screen.label_6.setText(f"Preço Total: {preco_total:.2f} MT")

# Função para atualizar a quantidade total exibida
def atualizar_quantidade_total():
    total_quantidade = sum(qtd for _, qtd, _ in estoque)
    screen.label_7.setText(f"Quantidade Total: {total_quantidade}")

# Função para adicionar produto
def adicionar_produto():
    data = screen.dateEdit.date().toString("dd-MM-yy")

    # Captura os dados do produto
    try:
        quantidade = int(screen.lineEdit_2.text())  # Quantidade
        preco = float(screen.lineEdit_3.text())  # Preço
    except ValueError:
        QMessageBox.warning(screen, "Erro", "Por favor, insira uma quantidade e um preço válidos.")
        return

    if quantidade <= 0 or preco < 0:
        QMessageBox.warning(screen, "Erro", "A quantidade deve ser maior que zero e o preço não pode ser negativo.")
        return

    # Verifica o método de aprovisionamento selecionado
    if screen.radioButton.isChecked():
        aprovisionar(data, quantidade, preco)
    elif screen.radioButton_2.isChecked():
        aprovisionar(data, quantidade, preco)  # Você pode adaptar isso para LIFO

    # Limpar os campos após adicionar
    limpar_campos()
    # Salvar dados no arquivo ao adicionar um novo produto
    salvar_dados()

# Função para vender produtos (FIFO)
def vender_fifo(quantidade):
    global preco_total
    vendidos = 0
    valor_vendido = 0  # Total arrecadado na venda
    data_atual = datetime.date.today().strftime("%Y-%m-%d")  # Formato da data para o dicionário

    while vendidos < quantidade and estoque:
        data, qtd_estoque, preco = estoque.popleft()  # Remove o primeiro item do estoque

        if qtd_estoque > (quantidade - vendidos):
            # Retorna o restante para o estoque
            estoque.appendleft((data, qtd_estoque - (quantidade - vendidos), preco))  
            valor_vendido += (quantidade - vendidos) * preco
            vendidos = quantidade
        else:
            valor_vendido += qtd_estoque * preco
            vendidos += qtd_estoque

    preco_total -= valor_vendido

    # Atualiza as vendas diárias
    if data_atual in vendas_diarias:
        vendas_diarias[data_atual] += valor_vendido
    else:
        vendas_diarias[data_atual] = valor_vendido

    mensagem = f"Total Vendido: {vendidos} unidades\nValor Total: {valor_vendido:.2f} MT"
    QMessageBox.information(screen, "Venda (FIFO)", mensagem)
    atualizar_tabela_apos_venda()
    atualizar_preco_total()
    atualizar_quantidade_total()
    screen.spinBox.setValue(1)

# Função para vender produtos (LIFO)
def vender_lifo(quantidade):
    global preco_total
    vendidos = 0
    valor_vendido = 0  # Total arrecadado na venda
    data_atual = datetime.date.today().strftime("%Y-%m-%d")  # Formato da data para o dicionário

    while vendidos < quantidade and estoque:
        data, qtd_estoque, preco = estoque.pop()  # Remove o último item do estoque

        if qtd_estoque > (quantidade - vendidos):
            # Retorna o restante para o estoque
            estoque.append((data, qtd_estoque - (quantidade - vendidos), preco))
            valor_vendido += (quantidade - vendidos) * preco
            vendidos = quantidade
        else:
            valor_vendido += qtd_estoque * preco
            vendidos += qtd_estoque

    preco_total -= valor_vendido

    # Atualiza as vendas diárias
    if data_atual in vendas_diarias:
        vendas_diarias[data_atual] += valor_vendido
    else:
        vendas_diarias[data_atual] = valor_vendido

    mensagem = f"Total Vendido: {vendidos} unidades\nValor Total: {valor_vendido:.2f} MT"
    QMessageBox.information(screen, "Venda (LIFO)", mensagem)
    atualizar_tabela_apos_venda()
    atualizar_preco_total()
    atualizar_quantidade_total()
    screen.spinBox.setValue(1)

# Função para remover produto
def remover_produto():
    quantidade = screen.spinBox.value()  # Obter a quantidade a ser vendida do QSpinBox

    if quantidade <= 0:
        QMessageBox.warning(screen, "Erro", "Selecione uma quantidade válida para remover.")
        return

    # Verifica o método de venda selecionado
    if screen.radioButton.isChecked():  # Se FIFO estiver selecionado
        vender_fifo(quantidade)
    elif screen.radioButton_2.isChecked():  # Se LIFO estiver selecionado
        vender_lifo(quantidade)
    else:
        QMessageBox.warning(screen, "Erro", "Selecione um método de venda (FIFO ou LIFO).")

    # Limpar os campos após remover
    screen.spinBox.setValue(1)
    salvar_dados()

# Função para limpar os campos de entrada
def limpar_campos():
    screen.lineEdit_2.clear()  # Limpa a linha de entrada para quantidade
    screen.lineEdit_3.clear()  # Limpa a linha de entrada para preço

# Função para exportar o relatório
def exportar_relatorio():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Relatório de Estoque", ln=True, align='C')

    # Total e médias diárias
    total_vendas = sum(vendas_diarias.values())
    media_diarias = total_vendas / len(vendas_diarias) if vendas_diarias else 0

    pdf.cell(200, 10, f"Total Vendas: {total_vendas:.2f} MT", ln=True)
    pdf.cell(200, 10, f"Média Diária: {media_diarias:.2f} MT", ln=True)

    pdf.output("relatorio_estoque.pdf")

    QMessageBox.warning(screen, "Concluido", "Relátorio Exportado com Sucesso!")

def exibir_graficos():
    # Configurar a figura e o canvas
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))

    # Gráfico da quantidade que entrou no estoque por dia
    datas_compra = list(compras_diarias.keys())
    quantidades_compra = [quantidade for quantidade in compras_diarias.values()]
    axs[0].bar(datas_compra, quantidades_compra, color='blue')
    axs[0].set_title('Quantidade Comprada por Dia')
    axs[0].set_xlabel('Data')
    axs[0].set_ylabel('Quantidade')
    axs[0].tick_params(axis='x', rotation=45)

    # Gráfico do valor das vendas feitas por dia
    datas_venda = list(vendas_diarias.keys())
    valores_venda = [valor for valor in vendas_diarias.values()]
    axs[1].bar(datas_venda, valores_venda, color='green')
    axs[1].set_title('Valor das Vendas por Dia')
    axs[1].set_xlabel('Data')
    axs[1].set_ylabel('Valor (MT)')
    axs[1].tick_params(axis='x', rotation=45)

    # Gráfico do valor que entrou no estoque por dia
    datas_quantidade = list(quantidades_diarias.keys())
    quantidades_total = [quantidade for quantidade in quantidades_diarias.values()]
    axs[2].bar(datas_quantidade, quantidades_total, color='orange')
    axs[2].set_title('Valor Total Entrado no Estoque por Dia')
    axs[2].set_xlabel('Data')
    axs[2].set_ylabel('Valor (MT)')
    axs[2].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()

def abrirRH():
    carregar_dadosRH()
    main.close()
    screen_RH.show()

def abrirArmazem():
    carregar_dadosArmazem()
    main.close()
    screen.show()

def voltarMainRH():
    main.show()
    screen_RH.close()

def voltarMainArm():
    main.show()
    screen.close()

app = QtWidgets.QApplication([])
# Carrega a interface do arquivo .ui
screen_RH = uic.loadUi("Gestão_RH.ui")
screen = uic.loadUi("Gestão_Armazém.ui")
main = uic.loadUi("Gestão_Main.ui")

# Conectar os widgets aos métodos
screen_RH.pushButton.clicked.connect(registrar_funcionario)  # Botão Registrar
screen_RH.pushButton_2.clicked.connect(alterar_funcionario)  # Botão Alterar
screen_RH.pushButton_3.clicked.connect(excluir_funcionario)  # Botão Excluir        
screen_RH.lineEdit_4.textChanged.connect(lambda: filtro(screen_RH.lineEdit_4.text(), screen_RH.tableWidget))
screen_RH.actionSair.triggered.connect(voltarMainRH)

# Conectar botões às funções
screen.pushButton.clicked.connect(adicionar_produto)
screen.pushButton_2.clicked.connect(remover_produto)
screen.actionExportar.triggered.connect(exportar_relatorio)
screen.actionDashBoard_2.triggered.connect(exibir_graficos)
screen.actionSair_2.triggered.connect(voltarMainArm)

main.pushButton.clicked.connect(abrirRH)
main.pushButton_2.clicked.connect(abrirArmazem)
main.pushButton_3.clicked.connect(lambda: app.closeAllWindows())

main.show()
app.exec_()