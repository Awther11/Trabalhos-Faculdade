function validarLogin(event) {
  event.preventDefault();

  const email = document.getElementById("email").value.trim();
  const senha = document.getElementById("senha").value.trim();
  const emailErro = document.getElementById("email-error");
  const senhaErro = document.getElementById("senha-error");

  emailErro.textContent = '';
  senhaErro.textContent = '';

  if (!email) {
    emailErro.textContent = "O e-mail é obrigatório.";
    return false;
  }

  if (!senha) {
    senhaErro.textContent = "A senha é obrigatória.";
    return false;
  }

  const dados = localStorage.getItem(`usuario_${email}`);

  if (!dados) {
    emailErro.textContent = "Usuário não encontrado.";
    return false;
  }

  const usuario = JSON.parse(dados);

  if (usuario.senha !== senha) {
    senhaErro.textContent = "Senha incorreta.";
    return false;
  }

  alert(`Bem-vindo, ${usuario.nome}!`);
  // Exemplo: você pode salvar no localStorage que o usuário está logado
  localStorage.setItem("usuario_logado", usuario.email);
  // window.location.href = "index.html"; // Redirecionamento opcional

  return false;
}