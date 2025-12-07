def validar_nome(nome_input):
    """
    Valida e formata um nome cadastrado de acordo com regras estabelecidas.
    As regras são:
    Caracteres permitidos: Letras, Hífens e Apóstrofos.
    Formatação permitida: Hífens e Apóstrofos não podem estar no início ou final do nome
    A função retorna: 
    Um novo nome formatado, onde a primeira letra a cada espaço do input é maiúscula e não existem espaços no final ou no começo.
    Retorna None se inválido. 
    """
    nome = nome_input.strip()
    if not nome:
        return None
    
    caracteres_extras = "-'"

    if nome[0] in caracteres_extras or nome[-1] in caracteres_extras:
        return None
    
    for i, char in enumerate(nome):
        if not (char.isalpha() or char.isspace() or char in caracteres_extras):
            return None
        
        if char in caracteres_extras:
            if i > 0 and i < len(nome) -1:
                anterior = nome[i-1]
                proximo = nome[i+1]
                if not (anterior.isalpha() and proximo.isalpha()):
                    return None
            else:
                return None
            
    return nome.title()

def validar_idade(idade_input):
    """
    Valida se a idade é um número inteiro n tal que 8 <= n < = 100.
    Aceita somente números inteiros (ex: 10).
    Entradas como 20.0 ou 'vinte' são consideradas inválidas.
    Retorna: A idade (str) ou None se inválido.
    """
    try:
        idade = int(idade_input)
        if 8 <= idade <= 100:
            return str(idade)
        else:
            return None
        
    except ValueError:
        return None
    
def validar_plano(plano_input):
    """
    Valida se o plano é 'Basico' ou 'Premium' (insensível a maiúsculas).
    Permite que digite 'Básico', com acento, no input.
    Retorna sempre o plano padronizado: 'Basico' ou 'Premium'.
    Retorna None se for inválido.
    """
    entrada = plano_input.strip().lower()

    if entrada in ["basico", "básico"]:
        return "Basico"
    
    elif entrada == "premium":
        return "Premium"
    
    else:
        return None