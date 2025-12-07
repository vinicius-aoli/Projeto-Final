import csv
from datetime import datetime, timedelta
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

def gerar_historico_aluno(id_aluno):
    """
    Lê o arquivo 'log_presenca.csv', filtra pelo ID dos alunos e retorna:
    1. Histórico bruto
    2. Estatísticas do aluno (Total de visitas, tempo médio de permanência na academia e média de horário de entrada)
    """
    arquivo = "log_presenca.csv"
    historico = []

    try:
        with open(arquivo, mode="r", encoding="utf-8", newline='') as f:
            leitor = csv.DictReader(f)
            historico = [row for row in leitor if row.get('id_aluno') == id_aluno]
    except FileNotFoundError:
        print("\n Erro: Arquivo não encontrado.")
        return

    if not historico:
        print("\nNenhum histórico encontrado para o seu ID.\n")
        return
    
    print("\n===== HISTÓRICO DE PRESENÇA =====")

    for row in historico:
        evento_fmt = row.get('evento', '').upper()
        data_fmt = row.get('data_hora', 'N/D')
        print(f"{data_fmt}  ->  {evento_fmt}")
    print("====================================\n")

    formatos = ["%d/%m/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S"]
    eventos_processados = []

    for row in historico:
        dh_raw = row.get('data_hora', '')
        data_obj = None

        for fmt in formatos:
            try:
                data_obj = datetime.strptime(dh_raw, fmt)
                break
            except ValueError:
                continue

        if data_obj:
            eventos_processados.append((data_obj, row.get('evento').strip().lower()))
        
    eventos_processados.sort(key=lambda x: x[0])

    entradas_times = []
    tempos_treino = []
    entrada_pendente = None

    for data, tipo in eventos_processados:
        if tipo == "entrada":
            entradas_times.append(data)
            entrada_pendente = data
        elif tipo == "saída":
            if entrada_pendente:
                duracao = data - entrada_pendente
                if duracao.total_seconds() > 0:
                    tempos_treino.append(duracao)
                entrada_pendente = None
        
    visitas_completas = len(tempos_treino)
    total_entradas = len(entradas_times)

    print("===== ESTATÍSTICAS DO ALUNO =====")
    print(f"• Total de Entradas Registradas: {total_entradas}")
    print(f"• Treinos Completos (Entrada + Saída): {visitas_completas}")

    if entradas_times:
        minutos_do_dia = [t.hour * 60 + t.minute for t in entradas_times]
        media_min = sum(minutos_do_dia) / len(minutos_do_dia)
        media_h = int(media_min // 60) % 24
        media_m = int(media_min % 60)
        print(f"• Horário Médio de Chegada: {media_h:02d}:{media_m:02d}")
        horas = [t.hour for t in entradas_times]
        hora_mais_freq, freq = Counter(horas).most_common(1)[0]
        print(f"• Seu Horário Preferido: {hora_mais_freq:02d}:00 (foi {freq} vezes)")
    else:
        print("• Horário Médio: N/D")

    if tempos_treino:
        soma_tempo = sum(tempos_treino, timedelta())
        media_tempo = soma_tempo / len(tempos_treino)
        total_segundos = media_tempo.total_seconds()
        horas = int(total_segundos // 3600)
        minutos = int((total_segundos % 3600) // 60)
        print(f"• Duração Média do Treino: {horas}h {minutos}min")
    else:
        print("• Duração Média: N/D")

    print("====================================\n")

def gerar_relatorio_geral(db_perfis):
    """
    Gera um relatório completo de frequência dos alunos para o gerente.
    Calcula estatísticas gerais com numpy e plota um gráfico de distribuição desses dados.
    Recebe db_perfis para buscar os nomes dos alunos.
    """
    arquivo = "log_presenca.csv"
    
    try:
        with open(arquivo, mode="r", encoding="utf-8", newline='') as f:
            leitor = csv.DictReader(f)
            registros = list(leitor)
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return

    if not registros:
        print("Nenhum registro de presença encontrado.")
        return

    alunos_stats = {} 
    
    for row in registros:
        id_aluno = row.get('id_aluno')
        evento = row.get('evento')
        try:
            data_hora = datetime.strptime(row.get('data_hora'), "%d/%m/%Y %H:%M:%S")
        except ValueError:
            continue

        if id_aluno not in alunos_stats:
            alunos_stats[id_aluno] = {"entrada": [], "saida": []}

        if evento == "entrada":
            alunos_stats[id_aluno]["entrada"].append(data_hora)
        elif evento == "saida":
            alunos_stats[id_aluno]["saida"].append(data_hora)

    print("\n===== RELATÓRIO DE PRESENÇAS POR ALUNO =====")
    
    nomes_grafico = []
    frequencias_grafico = []

    for id_aluno, eventos in alunos_stats.items():
        qtd_visitas = len(eventos["entrada"])
        
        nome = db_perfis.get(id_aluno, {}).get('nome', id_aluno)
        nomes_grafico.append(nome)
        frequencias_grafico.append(qtd_visitas)

        horario_medio_str = "N/D"
        if eventos["entrada"]:
            segundos_dia = [dt.hour * 3600 + dt.minute * 60 + dt.second for dt in eventos["entrada"]]
            media_seg = sum(segundos_dia) / len(segundos_dia)
            h = int(media_seg // 3600)
            m = int((media_seg % 3600) // 60)
            horario_medio_str = f"{h:02d}:{m:02d}"

        tempo_treino_str = "N/D"
        tempos = []

        for e, s in zip(eventos["entrada"], eventos["saida"]):
            tempos.append((s - e).total_seconds())
        
        if tempos:
            media_treino = sum(tempos) / len(tempos)
            h = int(media_treino // 3600)
            m = int((media_treino % 3600) // 60)
            tempo_treino_str = f"{h:02d}:{m:02d}"

        print(f"{id_aluno} | Visitas: {qtd_visitas} | Chegada Média: {horario_medio_str} | Tempo médio de treino: {tempo_treino_str}")
    print("===============================================\n")

    total_entradas = sum(frequencias_grafico)
    print(f"Total Geral de Entradas: {total_entradas}")
    
    if len(nomes_grafico) > 0:
        print(">> Gerando gráfico de distribuição...")
        
        media = np.mean(frequencias_grafico)
        desvio = max(1, media / 3) 
        
        dados_normais = np.random.normal(loc=media, scale=desvio, size=len(nomes_grafico))
        dados_normais = [max(0, int(round(x))) for x in dados_normais] 

        plt.figure(figsize=(10, 6))
        plt.bar(nomes_grafico, dados_normais, color='skyblue', edgecolor='black')
        
        plt.title("Distribuição de Frequência (Simulação Normal)")
        plt.xlabel("Alunos")
        plt.ylabel("Frequência Estimada")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        plt.show()
    else:
        print("Dados insuficientes para gerar gráfico.")