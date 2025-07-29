// Garante que o script só execute depois que o DOM estiver totalmente carregado
document.addEventListener('DOMContentLoaded', function() {

    // Função para submeter o formulário de cadastro
    function submitForm(event) {
        event.preventDefault(); // Impede o comportamento padrão de submissão do formulário

        const form = document.getElementById("cadastro-form");
        if (!form) {
            console.error("Formulário com ID 'cadastro-form' não encontrado.");
            return;
        }

        // Mapeamento dos campos:
        // A chave é o NOME QUE O BACKEND ESPERA (EXATAMENTE como está no Python)
        // O valor é o ID do campo HTML (EXATAMENTE como está no HTML)
        const camposBackendParaHtmlId = {
            "Nome": 'nome',
            "Nickname": 'nickname',
            "CPF": 'cpf',
            "Data de Nascimento": 'data-nascimento',
            "Email": 'email',
            "Telefone": 'telefone',
            "CEP": 'cep',
            "Endereço": 'endereco',
            "Numero da casa": 'numero', 
            "Complemento": 'complemento',
            "Bairro": 'bairro',
            "Cidade": 'cidade',
            "Estado": 'estado',
            "Plataforma Favorita": 'plataforma-favorita',
            "Genero de Jogo Favorito": 'genero-favorito', 
            "Senha": 'senha',
            "Confirmar Senha": 'confirmar-senha',
        };

        let valido = true;
        const usuario = {}; // Objeto que irá conter os dados a serem enviados para o backend

        // Limpar todas as mensagens de erro antes da validação
        for (const backendKey in camposBackendParaHtmlId) {
            const htmlId = camposBackendParaHtmlId[backendKey];
            const errorElement = document.getElementById(`${htmlId}-error`);
            if (errorElement) {
                errorElement.textContent = '';
            }
        }

        // Validação de campos e coleta de dados
        for (const backendKey in camposBackendParaHtmlId) {
            const htmlId = camposBackendParaHtmlId[backendKey];
            const inputElement = document.getElementById(htmlId);

            let value = '';
            if (inputElement) {
                value = inputElement.value.trim();
            } else {
                console.warn(`Elemento HTML com ID '${htmlId}' não encontrado.`);
                const isObrigatorioNoBackend = [
                    "Nome", "CPF", "Data de Nascimento", "Email", "Telefone", "CEP",
                    "Endereço", "Numero da casa", "Bairro", "Cidade", "Estado", "Senha", "Confirmar Senha"
                ].includes(backendKey);
                if (isObrigatorioNoBackend) {
                    valido = false;
                    console.error(`Campo obrigatório '${backendKey}' (ID HTML: '${htmlId}') não encontrado.`);
                }
            }

            // Validação de campos obrigatórios (baseado no que o backend exige)
            const isObrigatorioNoBackend = [
                "Nome", "CPF", "Data de Nascimento", "Email", "Telefone", "CEP",
                "Endereço", "Numero da casa", "Bairro", "Cidade", "Estado", "Senha", "Confirmar Senha"
            ].includes(backendKey);

            if (isObrigatorioNoBackend && !value) {
                const errorElement = document.getElementById(`${htmlId}-error`);
                if (errorElement) {
                    errorElement.textContent = 'Campo obrigatório.';
                }
                valido = false;
            }

            // Adiciona o valor ao objeto 'usuario' com a chave que o backend espera
            usuario[backendKey] = value;
        }

        // Validações específicas adicionais
        
        // Validação de senhas
        const senhaInput = document.getElementById("senha");
        const confirmarSenhaInput = document.getElementById("confirmar-senha");

        if (senhaInput && confirmarSenhaInput) {
            if (senhaInput.value !== confirmarSenhaInput.value) {
                const confirmarSenhaError = document.getElementById("confirmar-senha-error");
                if (confirmarSenhaError) {
                    confirmarSenhaError.textContent = "As senhas não coincidem.";
                }
                valido = false;
            }
            
            // Validação de tamanho mínimo da senha
            if (senhaInput.value.length < 8) {
                const senhaError = document.getElementById("senha-error");
                if (senhaError) {
                    senhaError.textContent = "A senha deve ter pelo menos 8 caracteres.";
                }
                valido = false;
            }
        } else {
            console.error("Elementos de senha não encontrados. Verifique os IDs 'senha' e 'confirmar-senha'.");
            valido = false;
        }

        // Validação de email
        const emailInput = document.getElementById("email");
        if (emailInput && emailInput.value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(emailInput.value)) {
                const emailError = document.getElementById("email-error");
                if (emailError) {
                    emailError.textContent = "Formato de e-mail inválido.";
                }
                valido = false;
            }
        }

        // Validação e limpeza de CPF
        const cpfInput = document.getElementById("cpf");
        if (cpfInput && cpfInput.value) {
            const cpfLimpo = cpfInput.value.replace(/\D/g, ''); // Remove todos os não-dígitos
            if (!/^\d{11}$/.test(cpfLimpo)) {
                const cpfError = document.getElementById("cpf-error");
                if (cpfError) {
                    cpfError.textContent = "CPF deve conter 11 dígitos numéricos.";
                }
                valido = false;
            } else {
                usuario["CPF"] = cpfLimpo; // Atribui o CPF limpo para envio
            }
        }

        // Validação e limpeza de telefone
        const telefoneInput = document.getElementById("telefone");
        if (telefoneInput && telefoneInput.value) {
            const telefoneLimpo = telefoneInput.value.replace(/\D/g, ''); // Remove todos os não-dígitos
            if (telefoneLimpo.length < 10) { // Pode ajustar o tamanho mínimo conforme o backend
                const telefoneError = document.getElementById("telefone-error");
                if (telefoneError) {
                    telefoneError.textContent = "Telefone deve ter pelo menos 10 dígitos.";
                }
                valido = false;
            } else {
                usuario["Telefone"] = telefoneLimpo; // Atribui o telefone limpo para envio
            }
        }

        // Validação e limpeza de CEP
        const cepInput = document.getElementById("cep");
        if (cepInput && cepInput.value) {
            const cepLimpo = cepInput.value.replace(/\D/g, ''); // Remove todos os não-dígitos
            if (!/^\d{8}$/.test(cepLimpo)) {
                const cepError = document.getElementById("cep-error");
                if (cepError) {
                    cepError.textContent = "CEP deve conter 8 dígitos numéricos.";
                }
                valido = false;
            } else {
                usuario["CEP"] = cepLimpo; // Atribui o CEP limpo para envio
            }
        }

        if (!valido) {
            console.log("Validação frontend falhou. Não enviando dados.");
            return false;
        }

        console.log("Dados que serão enviados para o backend:", usuario);

        // Desabilita o botão de envio para evitar múltiplos cliques
        const btnCriarConta = document.getElementById('btnCriarConta');
        if (btnCriarConta) {
            btnCriarConta.disabled = true;
            btnCriarConta.textContent = 'Enviando...';
        }

        // --- Envio para o backend Python (Flask) ---
        fetch('http://127.0.0.1:5000/cadastro', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(usuario)
        })
        .then(response => {
            // Verifica se a resposta não foi OK (status 2xx)
            if (!response.ok) {
                // Tenta ler o JSON de erro do backend para uma mensagem mais detalhada
                return response.json().then(errorData => {
                    throw new Error(errorData.mensagem || `Erro do servidor: ${response.status}`);
                });
            }
            return response.json(); // Se for OK, retorna o JSON normalmente
        })
        .then(data => {
            console.log("Resposta do servidor:", data);
            alert(data.mensagem || "Cadastro realizado com sucesso!");
            form.reset(); // Limpa o formulário após o sucesso
            
            // Opcional: redirecionar para página de login ou dashboard
            // window.location.href = 'login.html';
        })
        .catch(error => {
            console.error("Erro ao enviar dados para o backend:", error);
            alert(error.message || "Erro ao enviar cadastro ao servidor. Verifique o console para mais detalhes.");
        })
        .finally(() => {
            // Reabilita o botão independentemente do resultado
            if (btnCriarConta) {
                btnCriarConta.disabled = false;
                btnCriarConta.textContent = 'Criar Conta';
            }
        });

        return false; // Evita qualquer outra ação padrão do formulário
    }

    // Função para aplicar máscaras nos campos
    function aplicarMascaras() {
        // Máscara para CPF
        const cpfInput = document.getElementById('cpf');
        if (cpfInput) {
            cpfInput.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                value = value.replace(/(\d{3})(\d)/, '$1.$2');
                value = value.replace(/(\d{3})(\d)/, '$1.$2');
                value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
                e.target.value = value;
            });
        }

        // Máscara para telefone
        const telefoneInput = document.getElementById('telefone');
        if (telefoneInput) {
            telefoneInput.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length <= 10) {
                    value = value.replace(/(\d{2})(\d)/, '($1) $2');
                    value = value.replace(/(\d{4})(\d)/, '$1-$2');
                } else {
                    value = value.replace(/(\d{2})(\d)/, '($1) $2');
                    value = value.replace(/(\d{5})(\d)/, '$1-$2');
                }
                e.target.value = value;
            });
        }

        // Máscara para CEP
        const cepInput = document.getElementById('cep');
        if (cepInput) {
            cepInput.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                value = value.replace(/(\d{5})(\d)/, '$1-$2');
                e.target.value = value;
            });
        }
    }

    // Aplica as máscaras quando o DOM estiver carregado
    aplicarMascaras();

    // --- Adiciona evento de submit ao formulário ---
    const form = document.getElementById('cadastro-form');
    if (form) {
        form.addEventListener('submit', submitForm);
    } else {
        console.error("Formulário 'cadastro-form' não encontrado. Verifique o ID no HTML.");
    }

    // --- Adiciona evento de clique ao botão "Criar Conta" (backup) ---
    const btnCriarConta = document.getElementById('btnCriarConta');
    if (btnCriarConta) {
        btnCriarConta.addEventListener('click', function(event) {
            // Se o botão estiver dentro de um form, o evento submit já será disparado
            // Este é apenas um backup caso o evento submit não funcione
            if (event.target.form) {
                return; // Deixa o evento submit do form lidar com isso
            }
            submitForm(event);
        });
    } else {
        console.error("Botão 'btnCriarConta' não encontrado. Verifique o ID no HTML.");
    }
});