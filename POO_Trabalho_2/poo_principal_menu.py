from poo_livro import Livro
from poo_usuario import Estudante, Professor
from poo_biblioteca import Biblioteca

biblioteca = Biblioteca()

while True:
    print("""
    ---------- Biblioteca ----------
 [1] - Cadastrar Livro
 [2] - Exibir Livros
 [3] - Pesquisar por Livro
 [4] - Cadastrar Usuário
 [5] - exibir Usuários
 [6] - Alugar Livro
 [7] - Devolver Livro
 [8] - Sair
    """)
    opção = input('Escolha uma opção: ')
    
    if opção == '1':
        biblioteca.cadastrar_livro(Livro(input('Título: '), input('Autor: '), int(input('Ano: ')), input('Código: ')))
        print('Livro cadastrado!')
    elif opção == '2':
        biblioteca.listar_livros()
    elif opção == '3':
        resultados = biblioteca.pesquisar_livro(input('Termo de pesquisa: '))
        print('\n'.join([livro.exibir_infos() for livro in resultados]) if resultados else 'Nenhum livro encontrado.')
    elif opção == '4':
        nome, email, matricula, tipo = input('Nome: '), input('Email: '), input('Matrícula: '), input('Tipo (Estudante/Professor): ')
        usuario = Estudante(nome, email, matricula) if tipo.lower() == 'estudante' else Professor(nome, email, matricula)
        biblioteca.cadastrar_usuario(usuario)
        print('Usuário cadastrado!')
    elif opção == '5':
        biblioteca.listar_usuarios()
    elif opção == '6':
        biblioteca.alugar_livro(input('Matrícula: '), input('Código: '))
    elif opção == '7':
        biblioteca.devolver_livro(input('Matrícula: '), input('Código: '))
    elif opção == '8':
        break
    else:
        print('Opção inválida.')
        