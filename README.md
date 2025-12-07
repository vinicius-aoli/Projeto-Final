# GymStat

**Trabalho/Projeto Final das disciplinas:** SCC0800 - Introdução à Ciência de Computação e SSC0801 - Laboratório de Introdução à Ciência de Computação I

**Docente responsável:** Matheus Machado dos Santos

**Alunos Integrantes:**
* Rafael Antero Figueiroa (núm. usp: 16990694)
* Vinícius Alves de Oliveira (núm. usp: 15498077)

---

## Resumo
GymStat é um sistema de gerenciamento de academias criado com a intenção de auxiliar o administrador a monitorar a presença de alunos e gerenciar a academia.
O sistema conta com dois menus:
* **Menu do aluno:** Pode registrar sua presença (check-in) e saída (check-out) na academia, além de visualizar seu histórico pessoal de presença detalhado e estatísticas de treino.
* **Menu do gerente:** Pode cadastrar novos alunos, visualizar a lista de matriculados e gerar um relatório de frequência dos alunos com estatísticas de horário.

O projeto roda via texto no terminal.

## Pré-requisitos
Para conseguir rodar o sistema na sua máquina, é necessário ter instalados:
* Python 3.8 ou superior
* Gerenciador de pacotes pip

## Bibliotecas e dependências externas
O projeto utiliza duas bibliotecas externas nos seus códigos:
* 'numpy' para manipulação de dados numéricos.
* 'matplotlib' para geração (plotagem) de gráficos estatísticos.

Antes de executar o programa, é necessário abrir o terminal na pasta do projeto e executar o comando:

```bash
pip install matplotlib numpy
```

Nos sistemas operacionais Linux e macOS, talvez seja preciso usar `pip3` ao invés de `pip`.

## Estrutura de arquivos
* `main.py`: Arquivo principal do trabalho. Ele que inicia o sistema e gerencia o login do usuário, o direcionando para o menu correto com as devidas funcionalidades.
* `menus.py`: Contém a interface/painel do usuário para Aluno e Gerente.
* `gerenciador_dados.py`: Aqui estão as funções que lidam com leitura e escrita nos arquivos CSV.
* `relatorios.py`: Aqui estão definidas as funções que geram: o histórico do aluno e o relatório de frequência geral.
* `validadores.py`: Algumas funções auxiliares para validar nomes, idades e planos.
* `autenticacao.py`: Aqui está definida a função onde ocorre a autenticação de login e senha.
* `gerar_historico.py`: Função que gera os eventos de entrada e saída de aluno para o arquivo de log com parâmetros estabelecidos.

**Bancos de dados do trabalho que utilizam o id do aluno:**
* `usuarios.csv` (login, senha, tipo de perfil e id_aluno)
* `perfis_alunos.csv` (id_aluno, nome, idade e plano)
* `log_presenca.csv` (registros de entrada e saída de alunos)

## Para executar o projeto
Na pasta do projeto, abra o terminal e execute o código:

No windows:
```bash
python main.py
```

No Linux e MacOS:

```bash
python3 main.py
```

O sistema vai iniciar e solicitar o login e depois uma senha. Dependendo das credenciais inseridas, vai abrir o menu de Aluno ou de Gerente.
Os dados de login já existentes estão no arquivo `usuarios.csv`.
Para sair do sistema, é necessário digitar `sair` no input de login.

---

### Perfil de aluno

**Modelo de credenciais de aluno:**
* **Login:** `alunoX`
* **Senha:** `senhaX`

Onde X é o número desse aluno que está contido no ID no modelo: AX (com zeros para completar 4 caracteres).
Exemplo: O aluno de ID A001 tem o login aluno1 e a senha senha1.

**Opções contidas no menu:**
1. **"Registrar entrada (Check-in)"** - Registra a entrada do aluno na academia.
2. **"Registrar saída (Check-out)"** - Registra a saída do aluno na academia.
3. **"Ver meu histórico"** - Possibilita o aluno ver seu histórico de presença com:
    * Quantidade de treinos realizados.
    * Horário médio de chegada.
    * Duração média dos treinos.
0. **"Sair (Logout)"** - Sai do painel e retorna a tela de login.

Nota: O sistema faz uma verificação de qual foi o último evento registrado (check-in ou check-out) para evitar duplicidade de registro.

---

### Perfil do gerente

**Credenciais do gerente:**
* **Login:** `admin`
* **Senha:** `admin1`

**Opções contidas no menu:**
1. **"Cadastrar novo aluno"** - Possibilita cadastrar um novo aluno no sistema, salvando os novos dados nos arquivos csv.
    * Nota: Aqui, os dados inseridos passam por um processo de validação com parâmetros definidos.
2. **"Ver Lista de Alunos"** - Exibe todos os alunos matriculados com seus respectivos IDs e informações atreladas ao perfil.
3. **"Gerar e acessar relatórios de presença"** - Gera relatórios avançados de frequência, processando os dados de `log_presenca.csv`, no modelo:
    * Exibe no terminal estatísticas detalhadas de cada aluno (frequência, horários médios).
    * Gráfico Visual: Abre uma janela externa (via Matplotlib) exibindo um gráfico de barras com a Distribuição de Frequência dos alunos (com simulação estatística de curva normal).
       * Nota: Para continuar no loop, rodando o código, é preciso fechar a janela do gráfico visual.
0. **"Sair (Logout)"** - Sai do painel e retorna a tela de login.
