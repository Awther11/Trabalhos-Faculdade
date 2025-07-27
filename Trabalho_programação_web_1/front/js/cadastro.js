function submitForm(event) {
    event.preventDefault();

    const form = document.getElementById("cadastro-form");

    const campos = [
        { id: 'nome', obrigatorio: true },
        { id: 'cpf', obrigatorio: true },
        { id: 'data-nascimento', obrigatorio: true },
        { id: 'email', obrigatorio: true },
        { id: 'telefone', obrigatorio: true },
        { id: 'cep', obrigatorio: true },
        { id: 'endereco', obrigatorio: true },
        { id: 'numero', obrigatorio: true },
        { id: 'bairro', obrigatorio: true },
        { id: 'cidade', obrigatorio: true },
        { id: 'estado', obrigatorio: true },
        { id: 'senha', obrigatorio: true },
        { id: 'confirmar-senha', obrigatorio: true },
    ];

    let valido = true;

    campos.forEach(campo => {
        const input = document.getElementById(campo.id);
        const erro = document.getElementById(`${campo.id}-error`);
        erro.textContent = '';

        if (campo.obrigatorio && !input.value.trim()) {
            erro.textContent = 'Campo obrigatório.';
            valido = false;
        }
    });

    const senha = document.getElementById("senha").value;
    const confirmarSenha = document.getElementById("confirmar-senha").value;
    if (senha !== confirmarSenha) {
        document.getElementById("confirmar-senha-error").textContent = "As senhas não coincidem.";
        valido = false;
    }

    if (!valido) return false;

    // Salvando no localStorage
    const usuario = {
        nome: form.nome.value,
        email: form.email.value,
        senha: form.senha.value, // CUIDADO: aqui está sem criptografia!
    };

    localStorage.setItem(`usuario_${usuario.email}`, JSON.stringify(usuario));
    alert("Cadastro salvo com sucesso!");
    form.reset();
    return false;
}