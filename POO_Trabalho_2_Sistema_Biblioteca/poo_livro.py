class Livro:
    def __init__(self, titulo, autor, ano_publicacao, codigo):
        self._titulo = titulo
        self._autor = autor
        self._ano_publicacao = ano_publicacao
        self._codigo = codigo
        self._disponivel = True

    def get_titulo(self):
        return self._titulo

    def set_titulo(self, titulo):
        self._titulo = titulo

    def get_autor(self):
        return self._autor

    def set_autor(self, autor):
        self._autor = autor

    def get_ano_publicacao(self):
        return self._ano_publicacao

    def set_ano_publicacao(self, ano_publicacao):
        self._ano_publicacao = ano_publicacao

    def get_codigo(self):
        return self._codigo

    def set_codigo(self, codigo):
        self._codigo = codigo

    def get_disponivel(self):
        return self._disponivel

    def set_disponivel(self, disponivel):
        self._disponivel = disponivel

    def exibir_infos(self):
        return (f'Titulo: {self.get_titulo()},\n'
               f'Autor: {self.get_autor()},\n' 
               f'Ano de publicação: {self.get_ano_publicacao()},\n' 
               f'Código: {self.get_codigo()},\n' 
               f'Disponivel: {self.get_disponivel()}'
        )