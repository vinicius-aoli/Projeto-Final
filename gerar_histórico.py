import csv
import random
from datetime import datetime, timedelta

def gerar_historico_novembro():
    print("Gerando histórico de novembro... Aguarde.")
    
    student_ids = [f"A{i:03d}" for i in range(1, 51)] # Gera A001 até A050
    start_date = datetime(2025, 11, 1)
    days_in_month = 30
    
    min_visits = 3
    max_visits = 30
    min_duration = 45  
    max_duration = 135 
    
    registros = []

    for student in student_ids:
        
        num_visits = random.randint(min_visits, max_visits)
        
        days_visited = random.sample(range(days_in_month), num_visits)
        
        for day_offset in days_visited:
            current_day = start_date + timedelta(days=day_offset)
            
            start_hour = random.randint(6, 20)
            start_minute = random.randint(0, 59)
            entry_time = current_day.replace(hour=start_hour, minute=start_minute)
            
            duration = random.randint(min_duration, max_duration)
            exit_time = entry_time + timedelta(minutes=duration)

            registros.append((entry_time, student, "entrada"))
            registros.append((exit_time, student, "saida"))

    registros.sort(key=lambda x: x[0])

    with open('log_presenca.csv', mode='w', encoding='utf-8', newline='') as f:
        escritor = csv.writer(f)
        escritor.writerow(['id_aluno', 'data_hora', 'evento']) 
        
        fmt = "%d/%m/%Y %H:%M:%S"
        for data, aluno, evento in registros:
            escritor.writerow([aluno, data.strftime(fmt), evento])
            
    print(f"Sucesso! {len(registros)} registros gerados em log_presenca.csv.")

if __name__ == "__main__":
    gerar_historico_novembro()