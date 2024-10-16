import os, re
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from collections import deque
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from fpdf import FPDF

# Inicializando o estoque único e o preço total
estoque = deque()
preco_total = 0
vendas_diarias = {}
compras_diarias = {}
quantidades_diarias = {}
salario = 0
ficheiro = "funcionarios.txt"

#Armazem.....
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
                nome, area_trabalho, cargo, departamento, salario = line.strip().split(",")
                rowPosition = screen_RH.tableWidget.rowCount()
                screen_RH.tableWidget.insertRow(rowPosition)
                screen_RH.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(nome))
                screen_RH.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(area_trabalho))
                screen_RH.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(cargo))
                screen_RH.tableWidget.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(departamento))
                screen_RH.tableWidget.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(salario))

def salvar_dadosRH():
    """Salva os dados da tableWidget no ficheiro de texto."""
    with open(ficheiro, "w") as file:
        for row in range(screen_RH.tableWidget.rowCount()):
            nome = screen_RH.tableWidget.item(row, 0).text()
            area_trabalho = screen_RH.tableWidget.item(row, 1).text()
            cargo = screen_RH.tableWidget.item(row, 2).text()
            departamento = screen_RH.tableWidget.item(row, 3).text()
            salario = departamento = screen_RH.tableWidget.item(row, 4).text()
            file.write(f"{nome},{area_trabalho},{cargo},{departamento},{salario}\n")

def registrar_funcionario():
    """Adiciona um novo funcionário na tabela e no ficheiro."""
    nome = screen_RH.lineEdit_2.text()
    area_trabalho = screen_RH.lineEdit_5.text()
    cargo = screen_RH.lineEdit.text()
    departamento = screen_RH.lineEdit_3.text()
    salario = screen_RH.lineEdit_6.text()

    if nome and area_trabalho and cargo and departamento:
        rowPosition = screen_RH.tableWidget.rowCount()
        screen_RH.tableWidget.insertRow(rowPosition)

        screen_RH.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(nome))
        screen_RH.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(area_trabalho))
        screen_RH.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(cargo))
        screen_RH.tableWidget.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(departamento))
        screen_RH.tableWidget.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(salario))

        # Limpar campos de texto
        screen_RH.lineEdit_2.clear()
        screen_RH.lineEdit_5.clear()
        screen_RH.lineEdit.clear()
        screen_RH.lineEdit_3.clear()
        screen_RH.lineEdit_6.clear()

        # Salvar os dados no ficheiro
        salvar_dadosRH()

def alterar_funcionario():
    """Altera os dados do funcionário selecionado na tabela e atualiza o ficheiro."""
    selected_row = screen_RH.tableWidget.currentRow()

    if selected_row >= 0:  # Verifica se uma linha foi selecionada
        screen_RH.tableWidget.setItem(selected_row, 0, QtWidgets.QTableWidgetItem(screen_RH.lineEdit_2.text()))
        screen_RH.tableWidget.setItem(selected_row, 1, QtWidgets.QTableWidgetItem(screen_RH.lineEdit_5.text()))
        screen_RH.tableWidget.setItem(selected_row, 2, QtWidgets.QTableWidgetItem(screen_RH.lineEdit.text()))
        screen_RH.tableWidget.setItem(selected_row, 3, QtWidgets.QTableWidgetItem(screen_RH.lineEdit_3.text()))
        screen_RH.tableWidget.setItem(selected_row, 3, QtWidgets.QTableWidgetItem(screen_RH.lineEdit_4.text()))

        # Limpar campos de texto
        screen_RH.lineEdit_2.clear()
        screen_RH.lineEdit_5.clear()
        screen_RH.lineEdit.clear()
        screen_RH.lineEdit_3.clear()
        screen_RH.lineEdit_6.clear()

        # Atualizar o ficheiro com as alterações
        salvar_dadosRH()

def excluir_funcionario():
    """Remove o funcionário selecionado na tabela e atualiza o ficheiro."""
    selected_row = screen_RH.tableWidget.currentRow()

    if selected_row >= 0:  # Verifica se uma linha foi selecionada
        screen_RH.tableWidget.removeRow(selected_row)
        # Atualizar o ficheiro com as alterações
        salvar_dadosRH()

def gerar_relatorio_RH():
    """Gera um relatório em PDF com análise de salários, quantidade de trabalhadores e faixas salariais."""
    salarios = []

    # Coletar todos os salários da tabela
    for row in range(screen_RH.tableWidget.rowCount()):
        salario_item = screen_RH.tableWidget.item(row, 4)  # Assume que a coluna do salário é a 5ª
        if salario_item is not None:
            salarios.append(float(salario_item.text()))

    if not salarios:  # Verifica se não há salários registrados
        QMessageBox.information(screen_RH, "Relatório RH", "Não há funcionários cadastrados.")
        return

    quantidade_trabalhadores = len(salarios)
    salario_medio = sum(salarios) / quantidade_trabalhadores
    salario_minimo = min(salarios)
    salario_maximo = max(salarios)

    # Análise de Faixas Salariais
    faixa_baixa = len([salario for salario in salarios if salario < 20000])
    faixa_media = len([salario for salario in salarios if 20000 <= salario < 40000])
    faixa_alta = len([salario for salario in salarios if salario >= 40000])

    # Criar o PDF
    pdf = FPDF()
    pdf.add_page()
    
    # Adicionar título
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, 'Relatório de Recursos Humanos', 0, 1, 'C')

    # Adicionar conteúdo
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Quantidade de Trabalhadores: {quantidade_trabalhadores}", 0, 1)
    pdf.cell(0, 10, f"Salário Médio: {salario_medio:.2f} MT", 0, 1)
    pdf.cell(0, 10, f"Salário Mínimo: {salario_minimo:.2f} MT", 0, 1)
    pdf.cell(0, 10, f"Salário Máximo: {salario_maximo:.2f} MT", 0, 1)
    
    # Análise de Faixas Salariais
    pdf.cell(0, 10, 'Distribuição por Faixa Salarial:', 0, 1)
    pdf.cell(0, 10, f"Trabalhadores com salário abaixo de 20.000 MT: {faixa_baixa}", 0, 1)
    pdf.cell(0, 10, f"Trabalhadores com salário entre 20.000 e 40.000 MT: {faixa_media}", 0, 1)
    pdf.cell(0, 10, f"Trabalhadores com salário acima de 40.000 MT: {faixa_alta}", 0, 1)

    # Salvar o PDF
    pdf_output_path = "Relatório de RH.pdf"
    pdf.output(pdf_output_path)

    # Mensagem de confirmação
    QMessageBox.information(screen_RH, "Relatório RH", f"Relatório gerado com sucesso: {pdf_output_path}")

#Recurso Humanos...
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
def salvar_dadosArm():
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
    salvar_dadosArm()

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
    salvar_dadosArm()

# Função para limpar os campos de entrada
def limpar_campos():
    screen.lineEdit_2.clear()  # Limpa a linha de entrada para quantidade
    screen.lineEdit_3.clear()  # Limpa a linha de entrada para preço

# Função para exportar o relatório
def exportar_relatorio():
    """Gera um relatório em PDF com os valores totais, média por dia, quantidade atual e valor atual do estoque."""
    
    # Calcular os valores totais
    total_quantidade = sum(qtd for _, qtd, _ in estoque)
    total_valor = sum(qtd * preco for _, qtd, preco in estoque)
    
    # Calcular a média de valor por dia
    media_por_dia = total_valor / len(compras_diarias) if compras_diarias else 0
    
    # Criar o PDF
    pdf = FPDF()
    pdf.add_page()
    
    # Adicionar título
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, 'Relatório de Estoque', 0, 1, 'C')
    
    # Adicionar conteúdo
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Quantidade Total: {total_quantidade} itens", 0, 1)
    pdf.cell(0, 10, f"Valor Total: {total_valor:.2f} MT", 0, 1)
    pdf.cell(0, 10, f"Média de Valor por Dia: {media_por_dia:.2f} MT", 0, 1)
    
    # Adicionar detalhes das compras diárias
    pdf.cell(0, 10, 'Compras Diárias:', 0, 1)
    for data, valor in compras_diarias.items():
        pdf.cell(0, 10, f"{data}: {valor:.2f} MT", 0, 1)
    
    # Salvar o PDF
    pdf_output_path = "Relatório_de_Estoque.pdf"
    pdf.output(pdf_output_path)
    
    # Mensagem de confirmação
    QMessageBox.information(screen, "Relatório", f"Relatório exportado com sucesso: {pdf_output_path}")


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
    salvar_dadosRH

def voltarMainArm():
    main.show()
    screen.close()
    salvar_dadosArm()

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
screen_RH.actionRelatorio.triggered.connect(gerar_relatorio_RH)

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