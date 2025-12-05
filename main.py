import gerenciador_dados
import autenticacao
import menus

def main():
    print("Iniciando o sistema...")
    db_usuarios = gerenciador_dados.carregar_usuarios('usuarios.csv')
    db_perfis = gerenciador_dados.carregar_perfis('perfis_alunos.csv')
    
    if not db_usuarios or not db_perfis:
        print("Falha ao carregar arquivos de dados.")
        return
    
    while True:
        print("\n Bem-vindo ao GymStat!")
        login = input("Digite seu login (ou 'sair' para encerrar): ")
        if login.lower() == 'sair':
            break

        senha = input("Digite a sua senha: ")
        perfil, id_aluno = autenticacao.fazer_login(db_usuarios, login, senha)

        if perfil == "Gerente":
            print(f"\nBem-vindo, gerente!") 
            menus.menu_gerente(db_usuarios, db_perfis)

        elif perfil == "Aluno":
            dados_aluno = db_perfis.get(id_aluno)
            if dados_aluno:
                nome_aluno = dados_aluno.get('nome', login)
            else:
                nome_aluno = login
            print(f"\nBem-vindo, aluno {nome_aluno}!")
            menus.menu_aluno(id_aluno, login)

        else:
            print("\n Erro: login ou senha inválidos. Tente novamente.")

    print("Obrigado por usar o GymStat!")

if __name__ == "__main__":
    main()