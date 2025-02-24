class Biblioteca:
    def __init__(self):
        self._livros = []
        self._usuarios = []

    def cadastrar_livro(self, livro):
        self._livros.append(livro)

    def listar_livros(self):
        for livro in self._livros:
            print(livro.exibir_infos())

    def pesquisar_livro(self, termo):
        resultados = []
        for livro in self._livros:
            if termo.lower() in livro.get_titulo().lower() or termo.lower() in livro.get_autor().lower():
                resultados.append(livro)  
        return resultados  

    def cadastrar_usuario(self, usuario):
        self._usuarios.append(usuario)

    def listar_usuarios(self):
        for usuario in self._usuarios:
            print(usuario.exibir_infos())

    def busca_livro_codigo(self, codigo): 
        for livro in self._livros:
            if livro.get_codigo() == codigo:
                return livro
        return None

    def buscar_usuario_por_matricula(self, matricula):
        for usuario in self._usuarios:
            if usuario.get_matricula() == matricula:
                return usuario
        return None

    def alugar_livro(self, matricula_usuario, codigo_livro): 
        usuario = self.buscar_usuario_por_matricula(matricula_usuario)
        livro = self.busca_livro_codigo(codigo_livro)  

        if usuario and livro:
            if usuario.alugar_livros(livro): 
                print('Livro alugado com sucesso!.')  
            else:
                print('No momento não é possível realizar o aluguel do livro!.') 
        else:
            print('Usuário ou livro não encontrado.')

    def devolver_livro(self, matricula_usuario, codigo_livro):
        usuario = self.buscar_usuario_por_matricula(matricula_usuario)
        livro = self.busca_livro_codigo(codigo_livro) 

        if usuario and livro:
            if usuario.devolver_livros(livro): 
                print('Livro devolvido com sucesso!.')
            else:
                print('Não é possível realizar a devolução do livro no momento.')
        else:
            print('Usuário ou livro não encontrado.')