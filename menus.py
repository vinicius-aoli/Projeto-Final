import gerenciador_dados
import validadores

def menu_aluno(id_aluno, login):
    """
    Exibe o menu do Aluno e mantém ele no loop até que ele escolha sair.
    Recebe o 'id_aluno' para identificar quem está usando o sistema.
    Escreve nos arquivos csv para registrar entrada ou saída de alunos.
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
                    print("Erro: Você já registrou entrada, registre a saída antes de entrar novamente.")
                else:
                    if gerenciador_dados.registrar_presenca(id_aluno, "entrada"):
                        print("Check-in realizado com suceso! Bom treino!")
                        print("Antes de entrar no sistema novamente, registre a saída.")
                    else:
                        print("Erro ao registrar check-in.")

        elif opcao == "2":
            if status_atual == 'saida':
                print("Erro: Você já registrou saída, registre a entrada antes de sair novamente.")
                     
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
    Atualiza os bancos de dados em caso de cadastro novo.
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
            while True:
                novo_login = input("Crie um Login para esse(a) aluno(a): ")
                if novo_login in db_usuarios:
                    print("Erro: Esse login já está em uso. Tente novamente")
                    continue
                elif not novo_login.strip():
                    print("Erro: Login não pode ser vazio.")
                    continue
                else:
                    break
          
            id = gerenciador_dados.gerar_proximo_id(db_perfis)
            print(f"O ID desse aluno é: {id}")

            while True:
                nova_senha = input("Crie uma Senha para o(a) aluno(a): ")
                if len(nova_senha) >= 4:
                    break
                print("Erro: A senha deve ter pelo menos 4 caracteres")

            while True:
                nome_input = input("Nome Completo: ")
                nome = validadores.validar_nome(nome_input)
                if nome:
                    break
                else:
                    print("Erro: Nome inválido")
                    print("Use apenas letras. Hífens e Apóstrofos devem estar entre as letras.")
            
            while True:
                idade_input = input("Idade: ")
                idade = validadores.validar_idade(idade_input)
                if idade:
                    break
                else:
                    print("Erro: Idade inválida.")
                    print("Use apenas números inteiros entre 8 e 100. Exemplo: 26")

            while True:
                plano_input = input("Plano (Basico/Premium): ")
                plano = validadores.validar_plano(plano_input)
                if plano:
                    break
                else:
                    print("Erro: plano inválido. Os planos válidos são: 'Basico' e 'Premium'.")

            print("\nSalvando dados...")
            if gerenciador_dados.cadastrar_aluno(novo_login, nova_senha, id, nome, idade, plano):
                print("Cadastro realizado com sucesso! ")

                db_usuarios [novo_login] = {
                  'senha': nova_senha,
                  'perfil': 'Aluno',
                  'id_aluno' : id
                }

                db_perfis[id] = {
                  'nome': nome,
                  'idade': idade,
                  'plano': plano
                }

                print("Sistema atualizado com sucesso!")
            else:
                print("Erro ao salvar dados.")
            
     
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