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