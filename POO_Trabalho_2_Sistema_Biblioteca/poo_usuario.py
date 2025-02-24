import poo_livro

class Usuario:  
    def __init__(self, nome, email, matricula, tipo):
        self._nome = nome
        self._email = email
        self._matricula = matricula
        self._tipo = tipo
        self._livros_alugados = []  

    def get_nome(self):
        return self._nome

    def set_nome(self, novo_nome):
        self._nome = novo_nome

    def get_email(self):
        return self._email

    def set_email(self, novo_email):
        self._email = novo_email

    def get_matricula(self):
        return self._matricula

    def set_matricula(self, nova_matricula):
        self._matricula = nova_matricula

    def get_tipo(self):
        return self._tipo

    def set_tipo(self, novo_tipo):
        self._tipo = novo_tipo

    def get_livros_emprestados(self):  
        return self._livros_alugados  

    def set_livros_emprestados(self, novos_livros_emprestados):  
        self._livros_alugados = novos_livros_emprestados  

    def exibir_infos(self):
        return (f'Nome: {self.get_nome()},\n'
               f'Email: {self.get_email()},\n'
               f'Matrícula: {self.get_matricula()},\n'
               f'Tipo: {self.get_tipo()}'
        )

    def pode_alugar_livros(self): 
        if self.get_tipo() == 'Estudante':
            return len(self.get_livros_emprestados()) < 3  
        elif self.get_tipo() == 'Professor':
            return len(self.get_livros_emprestados()) < 5  

    def alugar_livros(self, livro): 
        if livro.get_disponivel() and self.pode_alugar_livros():
            self.get_livros_emprestados().append(livro)  
            livro.set_disponivel(False)
            return True
        return False

    def devolver_livros(self, livro):  
        if livro in self.get_livros_emprestados():  
            self.get_livros_emprestados().remove(livro)  
            livro.set_disponivel(True)
            return True
        return False
    
class Estudante(Usuario): 
    def __init__(self, nome, email, matricula):
        super().__init__(nome, email, matricula, 'Estudante')

class Professor(Usuario):  
    def __init__(self, nome, email, matricula):
        super().__init__(nome, email, matricula, 'Professor')