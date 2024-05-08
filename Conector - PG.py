################################################################################################################
############################### Consultas Socios e CNPJ na Receita Postgres  ###################################
################################################################################################################

import tkinter as tk
from tkinter import scrolledtext, messagebox
import psycopg2
from psycopg2 import Error

def pesquisar_por_nome_e_nome_usuario(cursor, nome, cpf):
    resultados_totais = []
    for i in range(10):
        tabela = f"Socios{i}"
        query = f"SELECT * FROM \"Receita\".\"{tabela}\" WHERE \"Socios\" LIKE '%{nome}%' AND \"Socios\" LIKE '%{cpf}%'"
        cursor.execute(query)
        resultados = cursor.fetchall()
        if resultados:
            resultados_totais.extend(resultados)
    return resultados_totais

def pesquisar_cnpj_raiz_socios(cursor, cnpj_raiz_lista):
    resultados_totais = []
    for i in range(10):
        tabela_socios = f"Socios{i}"
        for cnpj_raiz in cnpj_raiz_lista:
            query_socios = f"SELECT * FROM \"Receita\".\"{tabela_socios}\" WHERE \"CNPJ Raiz\" = '{cnpj_raiz}'"
            cursor.execute(query_socios)
            resultados_socios = cursor.fetchall()
            if resultados_socios:
                resultados_com_origem_socios = [(resultado, tabela_socios) for resultado in resultados_socios]
                resultados_totais.extend(resultados_com_origem_socios)
    return resultados_totais

def pesquisar_cnpj_raiz_empresas(cursor, cnpj_raiz_lista):
    resultados_totais = []
    for i in range(10):
        tabela_empresas = f"Empresas{i}"
        for cnpj_raiz in cnpj_raiz_lista:
            query_empresas = f"SELECT * FROM \"Receita\".\"{tabela_empresas}\" WHERE \"CNPJ Raiz\" = '{cnpj_raiz}'"
            cursor.execute(query_empresas)
            resultados_empresas = cursor.fetchall()
            if resultados_empresas:
                resultados_com_origem_empresas = [(resultado, tabela_empresas) for resultado in resultados_empresas]
                resultados_totais.extend(resultados_com_origem_empresas) 
    return resultados_totais

def pesquisar_cnpj_raiz_estabelecimentos(cursor, cnpj_raiz_lista):
    resultados_totais = []
    for i in range(10):
        tabela_estabelecimentos = f"Estabelecimentos{i}"
        for cnpj_raiz in cnpj_raiz_lista:
            query_estabelecimentos = f"SELECT * FROM \"Receita\".\"{tabela_estabelecimentos}\" WHERE \"CNPJ Raiz\" = '{cnpj_raiz}'"
            cursor.execute(query_estabelecimentos)
            resultados_estabelecimentos = cursor.fetchall()
            if resultados_estabelecimentos:
                resultados_com_origem_estabelecimentos = [(resultado, tabela_estabelecimentos) for resultado in resultados_estabelecimentos]
                resultados_totais.extend(resultados_com_origem_estabelecimentos)                              
    return resultados_totais

def formatar_cpf(cpf):
    cpf = cpf.replace(".", "").replace("-", "").replace("/", "")
    if len(cpf) != 11:
        raise ValueError("CPF deve conter 11 dígitos")
    cpf_formatado = "***" + cpf[3:9] + "**"
    return cpf_formatado

def consultar_nome():
    resultados_text.delete(1.0, tk.END)
    resultados_text.insert(tk.END, "Realizando Pesquisas...\n")
    resultados_text.update()

    conn = psycopg2.connect(
        user="postgres",
        password="sandro01",
        host="localhost",
        port="5432",
        database="postgres"
    )

    nome = nome_entry.get().upper()
    cpf = cpf_entry.get()

    try:
        cpf_formatado = formatar_cpf(cpf)
    except ValueError as e:
        messagebox.showerror("Erro", str(e))
        return

    cursor = conn.cursor()
    resultados_socios = pesquisar_por_nome_e_nome_usuario(cursor, nome, cpf_formatado)
    cnpj_raiz_lista = [resultado[0] for resultado in resultados_socios]
    resultados_socios_cnpj_raiz = pesquisar_cnpj_raiz_socios(cursor, cnpj_raiz_lista)
    cursor.close()

    cursor = conn.cursor()
    resultados_empresas_cnpj_raiz = pesquisar_cnpj_raiz_empresas(cursor, cnpj_raiz_lista)
    cursor.close()

    cursor = conn.cursor()
    resultados_estabelecimentos_cnpj_raiz = pesquisar_cnpj_raiz_estabelecimentos(cursor, cnpj_raiz_lista)
    cursor.close()

    resultados_combinados = resultados_empresas_cnpj_raiz + resultados_estabelecimentos_cnpj_raiz + resultados_socios_cnpj_raiz
    resultados_combinados.sort(key=lambda x: str(x[0][0]))

    for resultado, origem_tabela in resultados_combinados:
        if "empresas" in origem_tabela.lower():
            exibir_resultado_empresas(resultado, origem_tabela)
        elif "socios" in origem_tabela.lower():
            exibir_resultado_socios(resultado, origem_tabela)
        elif "estabelecimentos" in origem_tabela.lower():
            exibir_resultado_estabelecimentos(resultado, origem_tabela)

    if not (resultados_socios_cnpj_raiz or resultados_empresas_cnpj_raiz or resultados_estabelecimentos_cnpj_raiz):
        resultados_text.insert(tk.END, "Nenhum resultado encontrado")

    conn.close()

def exibir_resultado_estabelecimentos(resultado, origem_tabela):
    mensagem = ""
    cnpj_raiz, matriz_filial, nome_fantasia, situacao_cadastral, data_situacao_cadastral, motivo_situacao_cadastral, nome_cidade_exterior, pais, data_inicio_atividade, cnae_principal, cnae_secundario, correio_eletronico, situacao_especial, data_situacao_especial, cnpj, endereco, telefones = resultado
    mensagem += f"Cnpj: {cnpj}\n"
    mensagem += f"Matriz/Filial: {matriz_filial}\n"
    mensagem += f"Nome Fantasia: {nome_fantasia}\n"
    mensagem += f"Situação Cadastral: {situacao_cadastral} - Data Situação Cadastral: {data_situacao_cadastral}\n"
    mensagem += f"Constituição: {data_inicio_atividade}\n"
    mensagem += f"Motivo Situação Cadastral: {motivo_situacao_cadastral}\n"
    mensagem += f"Cnae Principal: {cnae_principal}\n"
    mensagem += f"Cnae Secundário: {cnae_secundario}\n"
    mensagem += f"Telefones: {telefones}\n"
    mensagem += f"Correio Eletrônico: {correio_eletronico}\n"
    mensagem += f"Endereço: {endereco}\n"
    mensagem += f"Situação Especial: {situacao_especial}\n"
    mensagem += f"Data Situação Especial: {data_situacao_especial}\n"
    mensagem += f"País (Offshore): {pais}\n"
    mensagem += f"Nome da Cidade no Exterior: {nome_cidade_exterior}\n"
    mensagem += "********* QSA: ************\n"
    resultados_text.insert(tk.END, mensagem)

def exibir_resultado_empresas(resultado, origem_tabela):
    mensagem = ""
    cnpj_raiz, Nome_da_Empresa, Capital_Social, Ente_Federativo, Qualificacao_do_responsavel, Natureza_Juridica, Porte_da_Empresa = resultado
    mensagem += f"Nome da Empresa: {Nome_da_Empresa}\n"
    mensagem += f"Capital Social: {Capital_Social}\n"
    mensagem += f"Natureza Jurídica: {Natureza_Juridica}\n"
    mensagem += f"Porte da Empresa: {Porte_da_Empresa}\n"
    mensagem += f"Ente Federativo: {Ente_Federativo}\n"
    mensagem += f"Qualificação do responsável: {Qualificacao_do_responsavel}\n"
    mensagem += f"CNPJ Raiz: {cnpj_raiz}\n"
    resultados_text.insert(tk.END, mensagem)

def exibir_resultado_socios(resultado, origem_tabela):
    mensagem = ""
    cnpj_raiz, pais, representante_legal, nome_representante, qualificacao_representante, socios = resultado
    mensagem += f" - {socios} - "
    mensagem += f"País : {pais} - "  
    mensagem += f"Nome do Representante: {nome_representante} - "  
    mensagem += f"Doc Representante Legal: {representante_legal} - "    
    mensagem += f"Qualificação do Representante Legal: {qualificacao_representante}\n"
    mensagem += "\n"
    resultados_text.insert(tk.END, mensagem)


def limpar_cnpj(cnpj):
    return ''.join(filter(str.isdigit, cnpj))

def consultar_db(cnpj_r, cnpj):
    resultados_text.delete(1.0, tk.END)
    conexao = psycopg2.connect(
        user="postgres",
        password="sandro01",
        host="localhost",
        port="5432",
        database="postgres"
    )

    cursor = conexao.cursor()

    resultados_estabelecimentos_cnpj = []
    resultados_estabelecimentos_cnpj_raiz = []
    resultados_empresas = []
    resultados_socios = []

    for i in range(10):
        tabela = f"Estabelecimentos{i}"
        cursor.execute(f"SELECT * FROM \"Receita\".\"{tabela}\" WHERE \"Cnpj\" = '{cnpj}'")
        resultados = cursor.fetchall()
        for resultado in resultados:
            resultados_estabelecimentos_cnpj.append((resultado, tabela))

    for i in range(10):
        tabela = f"Estabelecimentos{i}"
        cursor.execute(f"SELECT * FROM \"Receita\".\"{tabela}\" WHERE \"CNPJ Raiz\" = '{cnpj_r}'")
        resultados = cursor.fetchall()
        for resultado in resultados:
            resultados_estabelecimentos_cnpj_raiz.append((resultado, tabela))

    for i in range(10):
        tabela = f"Empresas{i}"
        cursor.execute(f"SELECT * FROM \"Receita\".\"{tabela}\" WHERE \"CNPJ Raiz\" = '{cnpj_r}'")
        resultados = cursor.fetchall()
        for resultado in resultados:
            resultados_empresas.append((resultado, tabela))

    for i in range(10):
        tabela = f"Socios{i}"
        cursor.execute(f"SELECT * FROM \"Receita\".\"{tabela}\" WHERE \"CNPJ Raiz\" = '{cnpj_r}'")
        resultados = cursor.fetchall()
        for resultado in resultados:
            resultados_socios.append((resultado, tabela))

    cursor.close()
    conexao.close()

    return resultados_estabelecimentos_cnpj, resultados_estabelecimentos_cnpj_raiz, resultados_empresas, resultados_socios

def pesquisar():
    cnpj_input = entry_cnpj.get()
    cnpj_limpo = limpar_cnpj(cnpj_input)
    cnpj_r = cnpj_limpo[:8]
    cnpj = cnpj_limpo

    resultados_estabelecimentos_cnpj, resultados_estabelecimentos_cnpj_raiz, resultados_empresas, resultados_socios = consultar_db(cnpj_r, cnpj)

    resultados_combinados = resultados_empresas + resultados_estabelecimentos_cnpj + resultados_socios + resultados_estabelecimentos_cnpj_raiz

    num_resultados_socios = len(resultados_socios)
    for i, (resultado, origem_tabela) in enumerate(resultados_combinados):
        if "empresas" in origem_tabela.lower():
            exibir_resultado_empresas(resultado, origem_tabela)
        elif "socios" in origem_tabela.lower():
            exibir_resultado_socios(resultado, origem_tabela)
        elif "estabelecimentos" in origem_tabela.lower() and i < num_resultados_socios:
            exibir_resultado_estabelecimentos(resultado, origem_tabela)

    if not (resultados_estabelecimentos_cnpj or resultados_estabelecimentos_cnpj_raiz or resultados_empresas or resultados_socios):
        resultados_text.insert(tk.END, "Nenhum resultado encontrado")

root = tk.Tk()
root.title("Consulta CNPJ")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Campo de Nome
label_nome = tk.Label(frame, text="Nome")
label_nome.grid(row=0, column=0, sticky="w")
nome_entry = tk.Entry(frame, width=50)  # Aumentando a largura do campo de entrada
nome_entry.grid(row=0, column=0)        # Movendo o campo para a coluna 1

# Campo de CPF
label_cpf = tk.Label(frame, text="CPF")
label_cpf.grid(row=1, column=0, sticky="w")
cpf_entry = tk.Entry(frame, width=50)   # Aumentando a largura do campo de entrada
cpf_entry.grid(row=1, column=0)         # Movendo o campo para a coluna 1

# Botão de pesquisa por nome
botao_pesquisar_nome = tk.Button(frame, text="Pesquisar por Nome", command=consultar_nome)
botao_pesquisar_nome.grid(row=2, column=0, columnspan=2, pady=(5,5))

# Campo de CNPJ
label_cnpj = tk.Label(frame, text="CNPJ")
label_cnpj.grid(row=3, column=0, sticky="w")
entry_cnpj = tk.Entry(frame, width=50)  # Aumentando a largura do campo de entrada
entry_cnpj.grid(row=3, column=0)        # Movendo o campo para a coluna 1

# Botão de pesquisa por CNPJ
botao_pesquisar_cnpj = tk.Button(frame, text="Pesquisar por CNPJ", command=pesquisar)
botao_pesquisar_cnpj.grid(row=4, column=0, columnspan=2, pady=(5,0))

# Área de resultados
resultados_text = scrolledtext.ScrolledText(frame, width=150, height=50, wrap=tk.WORD)
resultados_text.grid(row=5, column=0, columnspan=2, pady=(10,0))

root.mainloop()