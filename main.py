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
            print(f"\nBem-vindo, gerente {login}!") 
            menus.menu_gerente(db_usuarios, db_perfis)
            break


        elif perfil == "Aluno":
            print(f"\nBem-vindo, aluno {login}!")
            menus.menu_aluno(id_aluno, login)
            break

        else:
            print("\n Erro: login ou senha inválidos. Tente novamente.")

    print("Obrigado por usar o GymStat!")

if __name__ == "__main__":
    main()