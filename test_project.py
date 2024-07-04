import pytest
from unittest.mock import Mock, patch
from datetime import datetime
import pandas as pd
import os

# Importando os módulos
from excel_to_mysql import insert_data_from_excel
from queries import get_current_year, create_table_for_year, check_and_create_table, contar_quantidade_total, contar_quantidade_diferentes, pessoas_por_tipo_de_cancer

#Este teste verifica se a função get_current_year retorna o ano atual. 
#Ele compara o valor retornado pela função com o ano atual obtido pela função datetime.now().year.
def test_get_current_year():
    assert get_current_year() == datetime.now().year

#Este fixture cria um mock para a conexão MySQL. 
#Ele simula a conexão e o cursor do MySQL, permitindo que os testes que interagem com o banco de dados sejam executados sem um banco de dados real.
@pytest.fixture
def mock_mysql():
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_conn.connection.cursor.return_value = mock_cursor
    return mock_conn

#Este teste verifica se a função insert_data_from_excel insere os dados corretamente no banco de dados. 
#Ele cria um DataFrame mock e usa patch para simular a leitura de um arquivo Excel. Após chamar a função, ele verifica se os métodos "execute" e "commit" do cursor do MySQL foram chamados.
def test_insert_data_from_excel(mock_mysql):
    # Criar um DataFrame mock
    data = {
        'Nome': ['Teste Nome'],
        'Data_Nascimento': [datetime(2000, 1, 1)],
        'Idade': [20],
        'Telefone': ['123456789'],
        'Endereco': ['Teste Endereço'],
        'Tipo_Cancer': ['Tipo1'],
        'Data_Cadastro': [datetime(2020, 1, 1)],
        'Servico_Social': [True],
        'Psicologia': [False],
        'Fisioterapia': [True],
        'Acupuntura': [False],
        'Juridico': [True],
        'Reiki': [False],
        'Ginastica': [True],
        'Sempre_Vivas': [False]
    }
    df = pd.DataFrame(data)
    
    with patch('pandas.read_excel', return_value=df):
        insert_data_from_excel(mock_mysql, 'mock_excel_path')
    
    assert mock_mysql.connection.cursor().execute.called
    assert mock_mysql.connection.commit.called

#Este teste verifica se a função create_table_for_year cria a tabela para o ano especificado. 
#Ele verifica se os métodos execute e commit do cursor do MySQL foram chamados.
def test_create_table_for_year(mock_mysql):
    create_table_for_year(mock_mysql, 2024)
    assert mock_mysql.connection.cursor().execute.called
    assert mock_mysql.connection.commit.called

#Este teste verifica se a função check_and_create_table cria a tabela para o ano atual. 
#Ele usa patch para simular o ano atual e verifica se a tabela foi criada, confirmando que os métodos execute e commit do cursor do MySQL foram chamados.
def test_check_and_create_table(mock_mysql):
    with patch('queries.get_current_year', return_value=2024):
        year = check_and_create_table(mock_mysql)
    assert year == 2024
    assert mock_mysql.connection.cursor().execute.called
    assert mock_mysql.connection.commit.called

#Este teste verifica se a função contar_quantidade_total retorna o total correto de registros para uma coluna específica. 
#Ele simula o valor de retorno do método fetchone do cursor do MySQL e verifica se o total retornado pela função está correto.
def test_contar_quantidade_total(mock_mysql):
    mock_mysql.connection.cursor().fetchone.return_value = [10]
    total = contar_quantidade_total(mock_mysql, 'Nome')
    assert total == 10
    assert mock_mysql.connection.cursor().execute.called
    assert mock_mysql.connection.cursor().fetchone.called

#Este teste verifica se a função contar_quantidade_diferentes retorna as contagens corretas para cada tipo de câncer. 
#Ele simula o valor de retorno do método fetchall do cursor do MySQL e verifica se os tipos de câncer e as contagens retornadas estão corretos.
def test_contar_quantidade_diferentes(mock_mysql):
    mock_mysql.connection.cursor().fetchall.return_value = [('Tipo1', 5), ('Tipo2', 3)]
    tipos_cancer, contagens = contar_quantidade_diferentes(mock_mysql, 'Tipo_Cancer')
    assert tipos_cancer == ['Tipo1', 'Tipo2']
    assert contagens == [5, 3]
    assert mock_mysql.connection.cursor().execute.called
    assert mock_mysql.connection.cursor().fetchall.called

#Este teste verifica se a função pessoas_por_tipo_de_cancer retorna o tipo de câncer com a maior quantidade de pessoas. 
#Ele simula o valor de retorno do método fetchone do cursor do MySQL e verifica se o tipo de câncer e a contagem retornada estão corretos.
def test_pessoas_por_tipo_de_cancer(mock_mysql):
    mock_mysql.connection.cursor().fetchone.return_value = ('Tipo1', 5)
    resultado = pessoas_por_tipo_de_cancer(mock_mysql)
    assert resultado == ('Tipo1', 5)
    assert mock_mysql.connection.cursor().execute.called
    assert mock_mysql.connection.cursor().fetchone.called

#Este teste verifica se a função insert_data_from_excel trata exceções corretamente durante a inserção de dados no banco de dados. 
#Ele simula uma exceção no método execute do cursor do MySQL e verifica se a mensagem de erro correta é impressa.
def test_insert_data_from_excel_with_exception(mock_mysql, capsys):
    data = {
        'Nome': ['Teste Nome'],
        'Data_Nascimento': [datetime(2000, 1, 1)],
        'Idade': [20],
        'Telefone': ['123456789'],
        'Endereco': ['Teste Endereço'],
        'Tipo_Cancer': ['Tipo1'],
        'Data_Cadastro': [datetime(2020, 1, 1)],
        'Servico_Social': [True],
        'Psicologia': [False],
        'Fisioterapia': [True],
        'Acupuntura': [False],
        'Juridico': [True],
        'Reiki': [False],
        'Ginastica': [True],
        'Sempre_Vivas': [False]
    }
    df = pd.DataFrame(data)
    
    with patch('pandas.read_excel', return_value=df):
        with patch.object(mock_mysql.connection.cursor(), 'execute', side_effect=Exception("Insert error")):
            insert_data_from_excel(mock_mysql, 'mock_excel_path')
    
    captured = capsys.readouterr()
    assert "Erro ao inserir dados na linha" in captured.out
    assert "Insert error" in captured.out
