function validarLogin(event) {
  event.preventDefault();

  const emailInput = document.getElementById("email");
  const senhaInput = document.getElementById("senha");
  const emailErro = document.getElementById("email-error");
  const senhaErro = document.getElementById("senha-error");

  let valido = true;
  emailErro.textContent = '';
  senhaErro.textContent = '';

  const email = emailInput.value.trim();
  const senha = senhaInput.value.trim();

  if (!email) {
    emailErro.textContent = "O e-mail é obrigatório.";
    valido = false;
  } else if (!/^\S+@\S+\.\S+$/.test(email)) {
    emailErro.textContent = "Formato de e-mail inválido.";
    valido = false;
  }

  if (!senha) {
    senhaErro.textContent = "A senha é obrigatória.";
    valido = false;
  }

  if (valido) {
    alert("Login realizado com sucesso!");
    document.getElementById("login-form").reset();
  }

  return false;
}