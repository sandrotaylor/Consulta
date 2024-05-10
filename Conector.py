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
        query = f"SELECT * FROM \"public\".\"{tabela}\" WHERE \"Socios\" LIKE '%{nome}%' AND \"Socios\" LIKE '%{cpf}%'"
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
            query_socios = f"SELECT * FROM \"public\".\"{tabela_socios}\" WHERE \"Cnpj Raiz\" = '{cnpj_raiz}'"
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
            query_empresas = f"SELECT * FROM \"public\".\"{tabela_empresas}\" WHERE \"Cnpj Raiz\" = '{cnpj_raiz}'"
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
            query_estabelecimentos = f"SELECT * FROM \"public\".\"{tabela_estabelecimentos}\" WHERE \"Cnpj Raiz\" = '{cnpj_raiz}'"
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
        user="Sandro",
        password="sandro01",
        host="postgresql-171633-0.cloudclusters.net",
        port="18857",
        database="Banco_Receita"
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
            exibir_resultado_empresas(resultado, origem_tabela, resultados_text)  # Passar o argumento widget_text
        elif "socios" in origem_tabela.lower():
            exibir_resultado_socios(resultado, origem_tabela, resultados_text)  # Passar o argumento widget_text
        elif "estabelecimentos" in origem_tabela.lower():
            exibir_resultado_estabelecimentos(resultado, origem_tabela, resultados_text)  # Passar o argumento widget_text

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
        user="Sandro",
        password="sandro01",
        host="postgresql-171633-0.cloudclusters.net",
        port="18857",
        database="Banco_Receita"
    )

    cursor = conexao.cursor()

    resultados_estabelecimentos_cnpj = []
    resultados_estabelecimentos_cnpj_raiz = []
    resultados_empresas = []
    resultados_socios = []

    for i in range(10):
        tabela = f"Estabelecimentos{i}"
        cursor.execute(f"SELECT * FROM \"public\".\"{tabela}\" WHERE \"Cnpj\" = '{cnpj}'")
        resultados = cursor.fetchall()
        for resultado in resultados:
            resultados_estabelecimentos_cnpj.append((resultado, tabela))

    for i in range(10):
        tabela = f"Estabelecimentos{i}"
        cursor.execute(f"SELECT * FROM \"public\".\"{tabela}\" WHERE \"Cnpj Raiz\" = '{cnpj_r}'")
        resultados = cursor.fetchall()
        for resultado in resultados:
            resultados_estabelecimentos_cnpj_raiz.append((resultado, tabela))

    for i in range(10):
        tabela = f"Empresas{i}"
        cursor.execute(f"SELECT * FROM \"public\".\"{tabela}\" WHERE \"Cnpj Raiz\" = '{cnpj_r}'")
        resultados = cursor.fetchall()
        for resultado in resultados:
            resultados_empresas.append((resultado, tabela))

    for i in range(10):
        tabela = f"Socios{i}"
        cursor.execute(f"SELECT * FROM \"public\".\"{tabela}\" WHERE \"Cnpj Raiz\" = '{cnpj_r}'")
        resultados = cursor.fetchall()
        for resultado in resultados:
            resultados_socios.append((resultado, tabela))

    cursor.close()
    conexao.close()

    return resultados_estabelecimentos_cnpj, resultados_estabelecimentos_cnpj_raiz, resultados_empresas, resultados_socios

def pesquisar():
    resultados_text.delete(1.0, tk.END)
    resultados_text.insert(tk.END, "Pesquisando...\n")
    resultados_text.update()

    cnpj_input = entry_cnpj.get()
    cnpj_limpo = limpar_cnpj(cnpj_input)
    cnpj_r = cnpj_limpo[:8]
    cnpj = cnpj_limpo

    resultados_estabelecimentos_cnpj, resultados_estabelecimentos_cnpj_raiz, resultados_empresas, resultados_socios = consultar_db(cnpj_r, cnpj)

    resultados_combinados = resultados_empresas + resultados_estabelecimentos_cnpj + resultados_socios + resultados_estabelecimentos_cnpj_raiz

    num_resultados_socios = len(resultados_socios)
    for i, (resultado, origem_tabela) in enumerate(resultados_combinados):
        if "empresas" in origem_tabela.lower():
            exibir_resultado_empresas(resultado, origem_tabela, resultados_text)
        elif "socios" in origem_tabela.lower():
            exibir_resultado_socios(resultado, origem_tabela, resultados_text)
        elif "estabelecimentos" in origem_tabela.lower() and i < num_resultados_socios:
            exibir_resultado_estabelecimentos(resultado, origem_tabela, resultados_text)

    if not (resultados_estabelecimentos_cnpj or resultados_estabelecimentos_cnpj_raiz or resultados_empresas or resultados_socios):
        resultados_text.insert(tk.END, "Nenhum resultado encontrado")

# Configurações de conexão com o banco de dados
conn_config = {
    "user": "Sandro",
    "password": "sandro01",
    "host": "postgresql-171633-0.cloudclusters.net",
    "port": "18857",
    "database": "Banco_Receita"
}

# CORINGA --- Função para realizar a consulta por QUALQUER DADO nas tabelas Socios0 até Socios9, Estabelecimentos0 até Estabelecimentos9, e Empresas0 até Empresas9
def consultar_por_nome(nome):
    resultados = []
    conn = psycopg2.connect(**conn_config)
    cur = conn.cursor()
    
    # Consulta nas tabelas Socios0 até Socios9
    for i in range(10):
        try:
            cur.execute(f"SELECT * FROM \"public\".\"Socios{i}\" WHERE \"Nome do Representante\" LIKE '%{nome}%' OR \"Socios\" LIKE '%{nome}%'")
            resultados.extend(cur.fetchall())
        except psycopg2.Error as e:
            print(f"Erro ao executar consulta na tabela Socios{i}: {e}")
    
    # Consulta nas tabelas Estabelecimentos0 até Estabelecimentos9
    for i in range(10):
        try:
            cur.execute(f"SELECT * FROM \"public\".\"Estabelecimentos{i}\" WHERE \"Correio Eletronico\" LIKE '%{nome}%' OR \"Telefones\" LIKE '%{nome}%'")
            resultados.extend(cur.fetchall())
        except psycopg2.Error as e:
            print(f"Erro ao executar consulta na tabela Estabelecimentos{i}: {e}")
    
    # Consulta nas tabelas Empresas0 até Empresas9
    for i in range(10):
        try:
            cur.execute(f"SELECT * FROM \"public\".\"Empresas{i}\" WHERE \"Nome da Empresa\" LIKE '%{nome}%'")
            resultados.extend(cur.fetchall())
        except psycopg2.Error as e:
            print(f"Erro ao executar consulta na tabela Empresas{i}: {e}")
    
    
    # Fechar cursor e conexão
    cur.close()
    conn.close()
    
    return resultados

# Consulta nas tabelas POR CNPJ RAIZ

# Consulta nas tabelas Socios0 até Socios9
def consultar_cnpj_raiz_socios(cnpj_raiz_socios):
    resultados_totais = []
    conn = psycopg2.connect(**conn_config)
    cur = conn.cursor()
    
    for cnpj_raiz in cnpj_raiz_socios:
        for i in range(10):
            try:
                cur.execute(f"SELECT * FROM \"public\".\"Socios{i}\" WHERE \"Cnpj Raiz\" = '{cnpj_raiz}'")
                resultados = cur.fetchall()
                resultados_totais.extend(resultados)
            except psycopg2.Error as e:
                print(f"Erro ao executar consulta na tabela Socios{i}: {e}")

    cur.close()
    conn.close()
    return resultados_totais

# Consulta nas tabelas Estabelecimentos0 até Estabelecimentos9
def consultar_cnpj_raiz_estabelecimentos(cnpj_raiz_estabelecimentos):
    resultados_totais = []
    conn = psycopg2.connect(**conn_config)
    cur = conn.cursor()
    
    for cnpj_raiz in cnpj_raiz_estabelecimentos:
        for i in range(10):
            try:
                cur.execute(f"SELECT * FROM \"public\".\"Estabelecimentos{i}\" WHERE \"Cnpj Raiz\" = '{cnpj_raiz}'")
                resultados = cur.fetchall()
                resultados_totais.extend(resultados)
            except psycopg2.Error as e:
                print(f"Erro ao executar consulta na tabela Estabelecimentos{i}: {e}")

    cur.close()
    conn.close()
    return resultados_totais

# Consulta nas tabelas Empresas0 até Empresas9
def consultar_cnpj_raiz_empresas(cnpj_raiz_empresas):
    resultados_totais = []
    conn = psycopg2.connect(**conn_config)
    cur = conn.cursor()
    
    for cnpj_raiz in cnpj_raiz_empresas:
        for i in range(10):
            try:
                cur.execute(f"SELECT * FROM \"public\".\"Empresas{i}\" WHERE \"Cnpj Raiz\" = '{cnpj_raiz}'")
                resultados = cur.fetchall()
                resultados_totais.extend(resultados)
            except psycopg2.Error as e:
                print(f"Erro ao executar consulta na tabela Empresas{i}: {e}")

    cur.close()
    conn.close()
    return resultados_totais


# Função para extrair o CNPJ raiz dos resultados da consulta por nome
def extrair_cnpj_raiz(resultado_consulta):
    cnpj_raiz_socios = [resultado[0] for resultado in resultado_consulta if resultado]
    cnpj_raiz_estabelecimentos = [resultado[0] for resultado in resultado_consulta if resultado]
    cnpj_raiz_empresas = [resultado[0] for resultado in resultado_consulta if resultado]
    return cnpj_raiz_socios, cnpj_raiz_estabelecimentos, cnpj_raiz_empresas

# Função para exibir os resultados na tela do Tkinter
def exibir_resultado_estabelecimentos(resultado, origem_tabela, widget_text):
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
    widget_text.insert(tk.END, mensagem)

def exibir_resultado_empresas(resultado, origem_tabela, widget_text):
    mensagem = ""
    cnpj_raiz, Nome_da_Empresa, Capital_Social, Ente_Federativo, Qualificacao_do_responsavel, Natureza_Juridica, Porte_da_Empresa = resultado
    mensagem += f"Nome da Empresa: {Nome_da_Empresa}\n"
    mensagem += f"Capital Social: {Capital_Social}\n"
    mensagem += f"Natureza Jurídica: {Natureza_Juridica}\n"
    mensagem += f"Porte da Empresa: {Porte_da_Empresa}\n"
    mensagem += f"Ente Federativo: {Ente_Federativo}\n"
    mensagem += f"Qualificação do responsável: {Qualificacao_do_responsavel}\n"
    mensagem += f"CNPJ Raiz: {cnpj_raiz}\n"
    widget_text.insert(tk.END, mensagem)

def exibir_resultado_socios(resultado, origem_tabela, widget_text):
    mensagem = ""
    cnpj_raiz, pais, representante_legal, nome_representante, qualificacao_representante, socios = resultado
    mensagem += f" - {socios} - "
    mensagem += f"País : {pais} - "  
    mensagem += f"Nome do Representante: {nome_representante} - "  
    mensagem += f"Doc Representante Legal: {representante_legal} - "    
    mensagem += f"Qualificação do Representante Legal: {qualificacao_representante}\n"
    mensagem += "\n"
    widget_text.insert(tk.END, mensagem)

# Função para realizar a pesquisa e exibir resultados na janela Tkinter

def pesquisar_e_mostrar():
    termo_coringa = entry_termo.get().upper()  # Convertendo o texto para letras maiúsculas
    
    # Consultar usando o termo coringa
    resultado_consulta_termo = consultar_por_nome(termo_coringa)
    
    # Limpar resultados anteriores
    resultados_text.delete(1.0, tk.END)
    resultados_text.insert(tk.END, "Pesquisando...\n")
    resultados_text.update()
    
    # Consultar por CNPJ raiz
    cnpj_raiz_socios, cnpj_raiz_estabelecimentos, cnpj_raiz_empresas = extrair_cnpj_raiz(resultado_consulta_termo)
    resultado_consulta_cnpj_raiz_socios = consultar_cnpj_raiz_socios(cnpj_raiz_socios)
    resultado_consulta_cnpj_raiz_estabelecimentos = consultar_cnpj_raiz_estabelecimentos(cnpj_raiz_estabelecimentos)
    resultado_consulta_cnpj_raiz_empresas = consultar_cnpj_raiz_empresas(cnpj_raiz_empresas)

    # Agrupar resultados por CNPJ raiz
    resultados_por_cnpj_raiz = {}
    for resultado in resultado_consulta_cnpj_raiz_empresas:
        cnpj_raiz = resultado[0]
        if cnpj_raiz not in resultados_por_cnpj_raiz:
            resultados_por_cnpj_raiz[cnpj_raiz] = {"Empresas": [], "Estabelecimentos": [], "Sócios": []}
        resultados_por_cnpj_raiz[cnpj_raiz]["Empresas"].append(resultado)

    for resultado in resultado_consulta_cnpj_raiz_estabelecimentos:
        cnpj_raiz = resultado[0]
        if cnpj_raiz not in resultados_por_cnpj_raiz:
            resultados_por_cnpj_raiz[cnpj_raiz] = {"Empresas": [], "Estabelecimentos": [], "Sócios": []}
        resultados_por_cnpj_raiz[cnpj_raiz]["Estabelecimentos"].append(resultado)

    for resultado in resultado_consulta_cnpj_raiz_socios:
        cnpj_raiz = resultado[0]
        if cnpj_raiz not in resultados_por_cnpj_raiz:
            resultados_por_cnpj_raiz[cnpj_raiz] = {"Empresas": [], "Estabelecimentos": [], "Sócios": []}
        resultados_por_cnpj_raiz[cnpj_raiz]["Sócios"].append(resultado)

    # Exibir resultados na tela do Tkinter
    for cnpj_raiz, resultados in resultados_por_cnpj_raiz.items():
        resultados_text.insert(tk.END, f"\nResultados para CNPJ Raiz: {cnpj_raiz}\n")
        
        for tipo, resultados_tipo in resultados.items():
            if resultados_tipo:
                resultados_text.insert(tk.END, f"\nResultados da consulta por CNPJ Raiz ({tipo}):\n")
                for resultado in resultados_tipo:
                    if tipo == "Empresas":
                        exibir_resultado_empresas(resultado, tipo, resultados_text)
                    elif tipo == "Estabelecimentos":
                        exibir_resultado_estabelecimentos(resultado, tipo, resultados_text)
                    elif tipo == "Sócios":
                        exibir_resultado_socios(resultado, tipo, resultados_text)


# Configuração da janela Tkinter
root = tk.Tk()
root.title("Consulta de Dados")

# Criando a aba para pesquisa por nome e CPF
aba_nome = tk.Frame(root)
aba_nome.pack(fill="both", expand=True)
nome_label = tk.Label(aba_nome, text="Nome:")
nome_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
nome_entry = tk.Entry(aba_nome)
nome_entry.grid(row=0, column=1, padx=5, pady=5)
cpf_label = tk.Label(aba_nome, text="CPF:")
cpf_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")
cpf_entry = tk.Entry(aba_nome)
cpf_entry.grid(row=0, column=3, padx=5, pady=5)
buscar_button = tk.Button(aba_nome, text="Buscar", command=consultar_nome)
buscar_button.grid(row=0, column=4, padx=5, pady=5)

# Criando a aba para pesquisa por CNPJ
aba_cnpj = tk.Frame(root)
aba_cnpj.pack(fill="both", expand=True)
cnpj_label = tk.Label(aba_cnpj, text="CNPJ:")
cnpj_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_cnpj = tk.Entry(aba_cnpj)
entry_cnpj.grid(row=0, column=1, padx=5, pady=5)
buscar_button_cnpj = tk.Button(aba_cnpj, text="Buscar", command=pesquisar)
buscar_button_cnpj.grid(row=0, column=2, padx=5, pady=5)

# Criando a aba para pesquisa com termo coringa
aba_coringa = tk.Frame(root)
aba_coringa.pack(fill="both", expand=True)
termo_label = tk.Label(aba_coringa, text="Pesquisa Coringa:")
termo_label.grid(row=0, column=5, padx=5, pady=5, sticky="e")
entry_termo = tk.Entry(aba_coringa)
entry_termo.grid(row=0, column=6, padx=5, pady=5)
buscar_button_coringa = tk.Button(aba_coringa, text="Buscar", command=pesquisar_e_mostrar)
buscar_button_coringa.grid(row=0, column=7, padx=5, pady=5)


# Criando a aba para exibir os resultados
aba_resultados = tk.Frame(root)
aba_resultados.pack(fill="both", expand=True)
resultados_text = scrolledtext.ScrolledText(aba_resultados, width=150, height=50)
resultados_text.pack()

# Exibindo a interface
root.mainloop()
