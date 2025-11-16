import gerenciador_dados

def main():
    print("Iniciando o sistema...")
    db_usuarios = gerenciador_dados.carregar_usuarios('usuarios.csv')
    db_perfis = gerenciador_dados.carregar_perfis('perfis_alunos.csv')
    
    #TESTES (apagar depois)
    print("Dados do admin:", db_usuarios.get('admin'))
    print("Dados do aluno1:", db_usuarios.get('aluno1'))

    print("Perfil do A001:", db_perfis.get('A001'))

if __name__ == "__main__":
    main()