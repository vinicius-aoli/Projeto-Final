def fazer_login(db_usuarios, login, senha):
    """
    Verifica se um login e senha são válidos no nosso banco de dados.
    Caso contrário, retorna Inválido
    """
    
    usuario = db_usuarios.get(login)

    if not usuario:
        return "Inválido", None
    
    if usuario['senha'] == senha:
        perfil = usuario['perfil']
        id_aluno = usuario['id_aluno']
        return perfil, id_aluno
    
    else: 
        return "Invalido", None
    
    