async function validarLogin(event) {
  event.preventDefault();


  const emailInput = document.getElementById("email");
  const senhaInput = document.getElementById("senha");
  const email = emailInput.value.trim();
  const senha = senhaInput.value;


  document.getElementById("email-error").textContent = "";
  document.getElementById("senha-error").textContent = "";

  let temErro = false;


  if (!email) {
    document.getElementById("email-error").textContent = "Informe o e-mail ou CPF.";
    temErro = true;
  }
  if (!senha) {
    document.getElementById("senha-error").textContent = "Informe a senha.";
    temErro = true;
  }

  if (temErro) return false;

  try {
    const resposta = await fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        identificador: email,
        senha: senha
      })
    });

    const dados = await resposta.json();

    if (resposta.ok) {
      localStorage.setItem("token", dados.token_acesso);
      localStorage.setItem("usuario", JSON.stringify(dados.usuario));


      window.location.href = "carrinho.html";
    } else {

      alert(dados.mensagem || "Credenciais inválidas.");
    }
  } catch (erro) {
    console.error("Erro na requisição:", erro);
    alert("Erro na conexão com o servidor.");
  }

  return false;
}
