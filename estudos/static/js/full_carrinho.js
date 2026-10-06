const PresentesGeral= document.getElementById("listadepresentes1");
const botaoPresentear = document.getElementById("presentear");
const abrircarrinho = document.getElementById("meucarrinho");
const dentrodomeucarrinho = document.getElementById("dentrodocarrinho");
const FooterMeusPresentes = document.getElementById("footerCarrinho");

let listPresentes=[];

// inicio abrir o carrinho de presentes

abrircarrinho.addEventListener("click", (event) => {
  // console.log("clicou no carrinho");
  dentrodomeucarrinho.style.display = "block";
});

// inicio abrir o carrinho de presentes


// Inicio eventos para abrir/fechar carrinho e com click fora dele
dentrodomeucarrinho.addEventListener("click", (event) => {
  if (event.target === dentrodomeucarrinho || event.target === voltar_carrinho) {
    dentrodomeucarrinho.style.display = "none";
  }
});
// fim eventos para abrir/fechar carrinho e com click fora dele


// inicio adicionar item ao carrinho

PresentesGeral.addEventListener("click", (event) => {
  console.log("clicou no botão de adicionar ao carrinho");
  const parentButtom = event.target.closest(".addcart");
  if (parentButtom) {
    const id = parentButtom.getAttribute("data-id");
    const name = parentButtom.getAttribute("data-name");
    const price = parseFloat(parentButtom.getAttribute("data-price"));
    addinmycar(id, name, price);
  }
});
// fim adicionar item ao carrinho


// incio funcao add quantidade ao carrinho
function addinmycar(id, name, price) {
  const checklistcar = listPresentes.find(item => item.id == id);
  if (checklistcar) {
    checklistcar.quantity += 1;
  } else {
    listPresentes.push({ id, name, price, quantity: 1 });
  }
  mostrarCarrinho();
}
// fim funcao add quantidade ao carrinho




// inicio add produtos em meu carrinho
const submeucarrinho = document.getElementById("submeucarrinho");
function mostrarCarrinho() {
let total = 0;

    submeucarrinho.innerHTML = "";

    listPresentes.forEach(item => {

        const subtotal = item.price * item.quantity;

        total += subtotal;

        const produto = document.createElement("div");

        produto.classList.add("itemcarrinho");

        produto.innerHTML = `
            <div id="itensdentrocarrinho">
                <p>${item.name}</p>
                <p>R$ ${item.price.toFixed(2)}</p>
                <p>Quantidade: ${item.quantity}</p>
                 <button
                    class="adicinaritem"
                    data-name="${item.name}">
                    Adicionar
                </button>
                <button
                    class="removeritem"
                    data-name="${item.name}">
                    Remover
                </button>
            </div>
        `;

        submeucarrinho.appendChild(produto);
    });

    const totalCarrinho = document.getElementById("valortotal");
    totalCarrinho.textContent = `Total: R$ ${total.toFixed(2)}`;

    // inicio quantidade de itens no carrinho meus presentes
    const QuantidadeTotal = document.getElementById("quantidadecarinho");
    QuantidadeTotal.textContent = listPresentes.reduce((total, item) => total + item.quantity, 0);
    if (listPresentes.length === 1) {
      FooterMeusPresentes.style.display = "block";
    } else if (listPresentes.length === 0) {
      FooterMeusPresentes.style.display = "none";
    }
// fim quantidade de itens no carrinho meus presentes

}
// fim add produtos em meu carrinho




// inicio adicionar item do carrinho
submeucarrinho.addEventListener("click", (event)=>{
  if(event.target.classList.contains("adicinaritem")){
    const name = event.target.getAttribute("data-name");
    const item = listPresentes.find(item => item.name === name);
    if (item) {
      item.quantity += 1;
      mostrarCarrinho();
    }
  }
})
// fim adicionar item do carrinho


// // inicio remover item do carrinho
submeucarrinho.addEventListener("click", (event) => {
  if (event.target.classList.contains("removeritem")) {
    const name = event.target.getAttribute("data-name");
    removeritens(name);
    mostrarCarrinho();

  }
});
// // fim remover item do carrinho


// // inicio funcao remover itens
function removeritens(name) {
  const index = listPresentes.findIndex(item => item.name === name);
  if (index !== -1) {
    if (listPresentes[index].quantity > 1) {
      listPresentes[index].quantity -= 1;
    } else {
      listPresentes.splice(index, 1);
    }
  }
  mostrarCarrinho();
}
// // fim funcao remover itens


// inico botao presentear para o checkout


botaoPresentear.addEventListener("click", async () => {

    if (listPresentes.length === 0) {
        alert("Adicione pelo menos um presente ao carrinho.");
        return;
    }

    try {

        const resposta = await fetch("/criar_pagamento", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                presentes: listPresentes
            })
        });

        const dados = await resposta.json();

        if (!resposta.ok) {
            console.error("Erro:", dados);
            alert("Não foi possível iniciar o pagamento.");
            return;
        }

        console.log("Preferência criada:", dados);

        window.location.href = dados.link;

    } catch (erro) {

        console.error("Erro ao criar pagamento:", erro);

        alert("Erro ao conectar com o servidor.");
    }

});

// fim botao presentear para o checkout

