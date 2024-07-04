import pandas as pd
from queries import get_current_year
from unidecode import unidecode

def insert_data_from_excel(mysql, excel_file_path):
    # Ler o arquivo Excel até a coluna 'O'
    df = pd.read_excel(excel_file_path, usecols='A:O')

    # Obter o ano atual e o nome da tabela
    year = get_current_year()
    table_name = f'pacientes_{year}'

    # Conectar ao banco de dados e inserir dados
    cursor = mysql.connection.cursor()

    for _, row in df.iterrows():
        try:
            cursor.execute(f"""
                    INSERT INTO {table_name} (
                        Nome, Data_Nascimento, Idade, Telefone, Endereco, Tipo_Cancer, Data_Cadastro,
                        Servico_Social, Psicologia, Fisioterapia, Acupuntura, Juridico, Reiki,
                        Ginastica, Sempre_Vivas
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                row.iloc[0],  # Nome
                row.iloc[1],  # Data de Nascimento
                row.iloc[2],  # Idade
                row.iloc[3],  # Telefone
                row.iloc[4],  # Endereço
                unidecode(row.iloc[5]).strip().lower(),  # Tipo_Cancer
                row.iloc[6],  # Data de Cadastro
                bool(row.iloc[7]) if pd.notna(row.iloc[7]) else None,  # Servico_Social
                bool(row.iloc[8]) if pd.notna(row.iloc[8]) else None,  # Psicologia
                bool(row.iloc[9]) if pd.notna(row.iloc[9]) else None,  # Fisioterapia
                bool(row.iloc[10]) if pd.notna(row.iloc[10]) else None,  # Acupuntura
                bool(row.iloc[11]) if pd.notna(row.iloc[11]) else None,  # Juridico
                bool(row.iloc[12]) if pd.notna(row.iloc[12]) else None,  # Reiki
                bool(row.iloc[13]) if pd.notna(row.iloc[13]) else None,  # Ginastica
                bool(row.iloc[14]) if pd.notna(row.iloc[14]) else None  # Sempre_Vivas
            ))
        except Exception as e:
            print(f"Erro ao inserir dados na linha: {row}. Erro: {e}")

    mysql.connection.commit()
    cursor.close()

# Exemplo de uso:
# insert_data_from_excel(mysql_connection_object, '/mnt/data/Planilha estudantes.xlsx')