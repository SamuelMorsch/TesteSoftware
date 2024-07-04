
import pytest
from unittest.mock import Mock, patch
from datetime import datetime
import pandas as pd
import os

# Importing the modules to be tested
from excel_to_mysql import insert_data_from_excel
from queries import get_current_year, create_table_for_year, check_and_create_table, contar_quantidade_total, contar_quantidade_diferentes, pessoas_por_tipo_de_cancer

# Test get_current_year
def test_get_current_year():
    assert get_current_year() == datetime.now().year

# Mocking MySQL connection
@pytest.fixture
def mock_mysql():
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_conn.connection.cursor.return_value = mock_cursor
    return mock_conn

# Test insert_data_from_excel
def test_insert_data_from_excel(mock_mysql):
    # Creating a mock DataFrame
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

# Test create_table_for_year
def test_create_table_for_year(mock_mysql):
    create_table_for_year(mock_mysql, 2024)
    assert mock_mysql.connection.cursor().execute.called
    assert mock_mysql.connection.commit.called

# Test check_and_create_table
def test_check_and_create_table(mock_mysql):
    with patch('queries.get_current_year', return_value=2024):
        year = check_and_create_table(mock_mysql)
    assert year == 2024
    assert mock_mysql.connection.cursor().execute.called
    assert mock_mysql.connection.commit.called

# Test contar_quantidade_total
def test_contar_quantidade_total(mock_mysql):
    mock_mysql.connection.cursor().fetchone.return_value = [10]
    total = contar_quantidade_total(mock_mysql, 'Nome')
    assert total == 10
    assert mock_mysql.connection.cursor().execute.called
    assert mock_mysql.connection.cursor().fetchone.called

# Test contar_quantidade_diferentes
def test_contar_quantidade_diferentes(mock_mysql):
    mock_mysql.connection.cursor().fetchall.return_value = [('Tipo1', 5), ('Tipo2', 3)]
    tipos_cancer, contagens = contar_quantidade_diferentes(mock_mysql, 'Tipo_Cancer')
    assert tipos_cancer == ['Tipo1', 'Tipo2']
    assert contagens == [5, 3]
    assert mock_mysql.connection.cursor().execute.called
    assert mock_mysql.connection.cursor().fetchall.called

# Test pessoas_por_tipo_de_cancer
def test_pessoas_por_tipo_de_cancer(mock_mysql):
    mock_mysql.connection.cursor().fetchone.return_value = ('Tipo1', 5)
    resultado = pessoas_por_tipo_de_cancer(mock_mysql)
    assert resultado == ('Tipo1', 5)
    assert mock_mysql.connection.cursor().execute.called
    assert mock_mysql.connection.cursor().fetchone.called