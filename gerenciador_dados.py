import csv

def carregar_usuarios(arquivo_csv):
    """
    Carrega o arquivo de usuários e retorna um dicionário.
    A chave é o login, o valor é um dicionário que contém senha, perfil e id_aluno.
    """
    db_usuarios = {}

    try:
        with open(arquivo_csv, mode='r', encoding='utf-8') as f:
            leitor_csv = csv.reader(f)

            next(leitor_csv)

            for linha in leitor_csv:
                login = linha [0]
                senha = linha[1]
                perfil = linha [2]
                id_aluno = linha [3]

                db_usuarios[login] = {
                    'senha': senha,
                    'perfil': perfil,
                    'id_aluno': id_aluno
                }

    except FileNotFoundError:
        print(f"Erro: O arquivo {arquivo_csv} não foi encontrado.")
        return {}
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return {}
    
    print(f"Sucesso: {len(db_usuarios)} usuários foram carregados no sistema.")
    return db_usuarios

def carregar_perfis(arquivo_csv):
    """
    Carrega o arquivo de perfis de alunos, retornando um dicionário
    a chave é o id do aluno e o valor é um dicionário com nome e as informações correspondentes ao perfil.
    """
    db_perfis = {}

    try:
        with open(arquivo_csv, mode='r', encoding='utf-8') as f:
            leitor_csv = csv.DictReader(f)
            
            for linha in leitor_csv:
                id_aluno = linha ['id_aluno']
                db_perfis[id_aluno] = linha

    except FileNotFoundError:
        print(f"Erro: O arquivo {arquivo_csv} não foi encontrado.")
        return {}
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return {}
    
    print(f"Sucesso: {len(db_perfis)} perfis de alunos foram carregados no sistema.")
    return db_perfis

def registrar_presenca(id_aluno, tipo_evento):
    """
    Registra um evento (check-in ou check-out) no arquivo de log.
    Recebe:
        id_aluno(str): O ID do aluno
        tipo_evento: 'entrada' ou 'saída''
    Retorna:
        True se salvou corretamente, False se deu erro.
        """
    arquivo_log = 'log_presenca.csv'

    from datetime import datetime
    data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    try:
        with open(arquivo_log, mode='a', encoding='utf-8', newline='') as f:
            escritor_csv = csv.writer(f)
            escritor_csv.writerow([id_aluno, data_hora_atual, tipo_evento])

            return True
        
    except Exception as e:
        print(f"Erro ao salvar presença no arquivo: {e}")
        return False
    
def verificar_status_aluno(id_aluno):
    """
    Lê o log de presença e verifica qual foi o último evento registrado por um aluno.
    Retorna: 'entrada', 'saida' ou None (caso não haja nenhum registro)
    """
    arquivo = 'log_presenca.csv'
    ultimo_evento = 'saida'

    try:
        with open(arquivo, mode='r', encoding='utf-8') as f:
            leitor = csv.reader(f)
            next(leitor, None)

            for linha in leitor:
                if len(linha)>=3 and linha[0] == id_aluno:
                    ultimo_evento = linha[2]

    except FileNotFoundError:
        return 'saida'
    except Exception:
        return 'saida'

    return ultimo_evento


