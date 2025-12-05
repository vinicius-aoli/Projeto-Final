import gerenciador_dados

def menu_aluno(id_aluno, login):
    """
    Exibe o menu do Aluno e mantém ele no loop até que ele escolha sair.
    Recebe o 'id_aluno' para identificar quem está usando o sistema.
    """
    while True:
        print("\n PAINEL DO ALUNO")
        status_atual = gerenciador_dados.verificar_status_aluno(id_aluno)
        estado_str = "Ausente" if status_atual == 'entrada' else "Ausente"
        print(f"Status Atual: {estado_str}")
        print("---------------------")
        print("[1]: Registrar entrada (Check-in)")
        print("[2]: Registrar saída (Check-out)")
        print("[3]: Ver meu histórico")
        print("[0]: Sair (Logout)")

        opcao = input("Escolha a opção desejada: ")

        if opcao == "1":
                if status_atual == 'entrada':
                    print("Erro: Você já registrou entrada, registre a saída antes de entrar novamente")
                else:
                    if gerenciador_dados.registrar_presenca(id_aluno, "entrada"):
                        print("Check-in realizado com suceso! Bom treino!")
                        print("Antes de entrar no sistema novamente, registre a saída")
                    else:
                        print("Erro ao registrar check-in.")

        elif opcao == "2":
            if status_atual == 'saida':
                print("Erro: Você já registrou saída, registre a entrada antes de sair novamente")
                     
            else:
                if gerenciador_dados.registrar_presenca(id_aluno, "saida"):
                    print("Check-out realizado com sucesso!")
                else:
                    print("Erro ao registrar check-out.")

        elif opcao == "3":
            print("Gerando histórico do aluno...")
                
        elif opcao == "0":
            print("Saindo do sistema...")
            break 
        else:
            print("Opção inválida.")


def menu_gerente(db_usuarios, db_perfis):
     """
     Exibe o menu do gerente.
     Recebe os bancos de dados por completo.
     """
     while True:
        print("\n PAINEL DO GERENTE")
        print("[1]: Cadastrar novo aluno")
        print("[2]: Ver lista de alunos")
        print("[3]: Acessar ou gerar relatórios")
        print("[0] Sair (Logout)")
     
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
          print("Iniciando cadastro...")
     
        elif opcao == "2":
          print("\n ALUNOS CADASTRADOS")
          
          for id_aluno, dados in db_perfis.items():
               print(f"ID: {id_aluno} | Nome: {dados['nome']} | Idade: {dados['idade']} | Plano: {dados['plano']}")
          print("-------------")

        elif opcao == "3":
            print("Gerando relatórios...")
        
        elif opcao == "0":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida.")