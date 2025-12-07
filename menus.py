import gerenciador_dados
import validadores
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from collections import Counter

def menu_aluno(id_aluno, login):
    """'
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
                print("Erro: Você já está registrado como presente. Registre a saída antes de entrar novamente.")
            else:
                if gerenciador_dados.registrar_presenca(id_aluno, "entrada"):
                    print("Check-in realizado com sucesso!")
                else:
                    print("Erro ao registrar check-in.")


        elif opcao == "2":
            if status_atual == 'saida':
                 print("Erro: Você já registrou saída, registre a entrada antes de sair novamente.")
            else:
                if gerenciador_dados.registrar_presenca(id_aluno, "saida"):
                    print("Check-out realizado com sucesso!")
                    print("Encerrando o sistema...")
                    break   # <<---- ENCERRA O MENU IMEDIATAMENTE
                else:
                    print("Erro ao registrar check-out.")


                import csv   # certifique-se de que 'import csv' está no topo do arquivo


        elif opcao == "3":
            arquivo = "log_presenca.csv"

            try:
                import csv as _csv
                from datetime import datetime, timedelta
                from collections import Counter

                with open(arquivo, mode="r", encoding="utf-8", newline='') as f:
                    leitor = _csv.DictReader(f)
                    historico = [row for row in leitor if row.get('id_aluno') == id_aluno]

                if not historico:
                    print("\n📌 Nenhum histórico encontrado para o seu ID.\n")
                else:
                    # Imprime histórico (na ordem do arquivo)
                    print("\n===== HISTÓRICO DE PRESENÇA =====")
                    for row in historico:
                        print(f"{row.get('data_hora', 'N/D')}  ->  {row.get('evento', 'N/D')}")
                        print("=================================\n")

                    # --- Parse dos timestamps (suportando formatos)
                    formatos = ["%d/%m/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S"]
                    eventos = []
                    for row in historico:
                        dh_raw = row.get('data_hora', '')
                        parsed = None
                        for fmt in formatos:
                            try:
                                parsed = datetime.strptime(dh_raw, fmt)
                                break
                            except Exception:
                                continue
                        if parsed is None:
                            # pula linha mal-formatada
                            continue
                        eventos.append((parsed, row.get('evento').strip().lower()))

                    # Ordena por data/hora (segurança)
                    eventos.sort(key=lambda x: x[0])

                    # --- Emparelha entradas e saídas cronologicamente
                    entradas_times = []
                    tempos_treino = []
                    pending_entry = None

                    for ts, ev in eventos:
                        if ev == "entrada":
                            # registra hora da entrada (mesmo que fique sem saída)
                            entradas_times.append(ts)
                            # marca uma entrada pendente para emparelhar com próxima saída
                            if pending_entry is None:
                                pending_entry = ts
                            else:
                                # já havia uma entrada pendente sem saída; 
                                # substituímos a pendente (assumimos usuário re-registrou entrada)
                                pending_entry = ts
                        elif ev == "saida":
                            if pending_entry is not None:
                                # visita completa encontrada
                                dur = ts - pending_entry
                                if dur.total_seconds() > 0:
                                    tempos_treino.append(dur)
                                pending_entry = None
                            else:
                                # saída sem entrada anterior: ignoramos
                                continue

                    # Quantidade de visitas completas
                    visitas_completas = len(tempos_treino)
                    # Também pegamos total de entradas registradas (mesmo sem saída)
                    total_entradas = len(entradas_times)

                    # --- Estatísticas
                    print("===== ESTATÍSTICAS =====")

                    print(f"Quantidade de vezes registradas (visitas completas): {visitas_completas}")
                    print(f"Total de entradas registradas (inclui não finalizadas): {total_entradas}")

                    # Horário médio de entrada (baseado nas entradas registradas)
                    if entradas_times:
                        minutos = [t.hour * 60 + t.minute for t in entradas_times]
                        media_min = sum(minutos) / len(minutos)
                        media_h = int(media_min // 60) % 24
                        media_m = int(media_min % 60)
                        print(f"Horário médio de entrada: {media_h:02d}:{media_m:02d}")

                        # Horário que ele mais entra (hora com maior frequência)
                        horas = [t.hour for t in entradas_times]
                        hora_mais_freq, freq = Counter(horas).most_common(1)[0]
                        print(f"Hora em que mais entra (hora cheia): {hora_mais_freq:02d}:00 (ocorreu {freq} vezes)")
                    else:
                        print("Horário médio de entrada: N/D")
                        print("Hora em que mais entra: N/D")

                    # Tempo médio de treino (completos)
                    if tempos_treino:
                        soma = sum((d for d in tempos_treino), timedelta())
                        media = soma / len(tempos_treino)
                        horas = int(media.total_seconds() // 3600)
                        minutos = int((media.total_seconds() % 3600) // 60)
                        print(f"Tempo médio de treino: {horas:02d}:{minutos:02d}")
                    else:
                        print("Tempo médio de treino: N/D")

                    print("=============================\n")

            except FileNotFoundError:
                print("Arquivo de histórico não encontrado:", arquivo)
            except UnicodeDecodeError:
                print("Erro de codificação ao ler o CSV.")
            except Exception as e:
                print("Erro ao ler histórico (debug):", repr(e))

        elif opcao == "0":
            print("Saindo do painel...\n")
            break

        else:
            print("Opção inválida! Tente novamente.")






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
            from datetime import datetime
            import csv as _csv

            arquivo = "log_presenca.csv"
            try:
                with open(arquivo, mode="r", encoding="utf-8", newline='') as f:
                    leitor = _csv.DictReader(f)
                    registros = list(leitor)

                if not registros:
                    print("📌 Nenhum registro de presença encontrado.")
                else:
                    # Agrupa por aluno
                    alunos = {}
                    for row in registros:
                        id_aluno = row.get('id_aluno')
                        data_hora_str = row.get('data_hora')
                        evento = row.get('evento')
                        data_hora = datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M:%S")

                        if id_aluno not in alunos:
                            alunos[id_aluno] = {"entrada": [], "saida": []}
                
                        if evento == "entrada":
                            alunos[id_aluno]["entrada"].append(data_hora)
                        elif evento == "saida":
                            alunos[id_aluno]["saida"].append(data_hora)

                    print("\n===== RELATÓRIO DE PRESENÇAS =====")
                    for id_aluno, eventos in alunos.items():
                        qtd_visitas = len(eventos["entrada"])
                
                        # Horário médio de entrada
                        if eventos["entrada"]:
                            media_hora = sum([dt.hour * 3600 + dt.minute * 60 + dt.second for dt in eventos["entrada"]]) / len(eventos["entrada"])
                            h = int(media_hora // 3600)
                            m = int((media_hora % 3600) // 60)
                            s = int(media_hora % 60)
                            horario_medio = f"{h:02d}:{m:02d}:{s:02d}"
                        else:
                            horario_medio = "N/D"

                        # Tempo médio de treino
                        tempos = []
                        for e, s in zip(eventos["entrada"], eventos["saida"]):
                            tempos.append((s - e).total_seconds())
                        if tempos:
                            media_treino = sum(tempos) / len(tempos)
                            h = int(media_treino // 3600)
                            m = int((media_treino % 3600) // 60)
                            s = int(media_treino % 60)
                            tempo_medio = f"{h:02d}:{m:02d}:{s:02d}"
                        else:
                            tempo_medio = "N/D"

                        print(f"ID: {id_aluno} | Visitas: {qtd_visitas} | Hora média entrada: {horario_medio} | Tempo médio treino: {tempo_medio}")
                    print("=================================\n")

            except FileNotFoundError:
                print("Arquivo de histórico não encontrado:", arquivo)
            except Exception as e:
                print("Erro ao gerar relatório (debug):", repr(e))


            # --- Coletar todos os eventos
            todos_eventos = []
            for row in registros:  # 'registros' é a lista de linhas do CSV já lida
                dh_raw = row.get('data_hora', '')
                evento = row.get('evento', '').strip().lower()
                id_aluno = row.get('id_aluno', 'N/D')
                try:
                    dh = datetime.strptime(dh_raw, "%d/%m/%Y %H:%M:%S")
                except Exception:
                    continue  # pula linhas mal formatadas
                todos_eventos.append((id_aluno, dh, evento))

                # --- Separar entradas e saídas
            entradas = []
            tempos_treino = []
            pendentes = {}  # chave: id_aluno, valor: datetime da última entrada pendente

            for id_aluno, dh, evento in todos_eventos:
                if evento == "entrada":
                    entradas.append(dh)
                    pendentes[id_aluno] = dh
                elif evento == "saida":
                    if id_aluno in pendentes:
                        dur = dh - pendentes[id_aluno]
                        if dur.total_seconds() > 0:
                            tempos_treino.append(dur)
                        del pendentes[id_aluno]

            # --- Estatísticas gerais
            total_entradas = len(entradas)

            if entradas:
             # Horário médio de entrada
                minutos = [t.hour*60 + t.minute for t in entradas]
                media_min = sum(minutos)/len(minutos)
                media_h = int(media_min // 60)
                media_m = int(media_min % 60)
                horario_medio = f"{media_h:02d}:{media_m:02d}"
            else:
                horario_medio = "N/D"

            if tempos_treino:
                soma = sum((d for d in tempos_treino), timedelta())
                media = soma / len(tempos_treino)
                h = int(media.total_seconds() // 3600)
                m = int((media.total_seconds() % 3600) // 60)
                tempo_medio = f"{h:02d}:{m:02d}"
            else:
                tempo_medio = "N/D"

            # --- Imprime resumo geral
            print("\n===== RESUMO GERAL MENSAL =====")
            print(f"Total de entradas registradas: {total_entradas}")
            print(f"Horário médio de entrada: {horario_medio}")
            print(f"Tempo médio de treino: {tempo_medio}")
            print("===============================\n")


            nomes_alunos = []
            frequencias = []

            # Preencher com os dados reais dos alunos
            for id_aluno, eventos in alunos.items():
                qtd_visitas = len(eventos["entrada"])  # número de entradas registradas
                frequencias.append(qtd_visitas)
    
                # Pega o nome do aluno se existir, senão usa o ID
                nome = db_perfis.get(id_aluno, {}).get('nome', id_aluno)
                nomes_alunos.append(nome)

                num_alunos = len(nomes_alunos)

            if num_alunos > 0:
                # Criar dados simulados com distribuição normal
                media = np.mean(frequencias)
                desvio = max(1, media / 3)  # evitar desvio zero
                dados_normais = np.random.normal(loc=media, scale=desvio, size=num_alunos)

                # Limita valores a inteiros >= 0
                dados_normais = [max(0, int(round(x))) for x in dados_normais]

                # Gerar gráfico
                plt.figure(figsize=(12, 6))
                plt.bar(nomes_alunos, dados_normais, color='skyblue')
                plt.xticks(rotation=90)
                plt.ylabel("Frequência simulada (normal)")
                plt.xlabel("Alunos")
                plt.title("Distribuição Normal das Presenças dos Alunos")
                plt.tight_layout()
                plt.show()
            else:
                print("Não há dados de alunos para gerar gráfico.")


            
        elif opcao == "0":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida.")