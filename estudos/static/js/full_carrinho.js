const PresentesGeral= document.getElementById("listadepresentes1");
const abrircarrinho = document.getElementById("meucarrinho");
const dentrodomeucarrinho = document.getElementById("dentrodocarrinho");

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
            <div>
                <p>${item.name}</p>
                <p>R$ ${item.price.toFixed(2)}</p>
                <p>Quantidade: ${item.quantity}</p>
                <p>Subtotal: R$ ${subtotal.toFixed(2)}</p>

                <button
                    class="removeritem"
                    data-name="${item.name}"
                >
                    Remover
                </button>
            </div>
        `;

        submeucarrinho.appendChild(produto);
    });

    const totalCarrinho = document.createElement("p");

    totalCarrinho.innerHTML = `
        <strong>Total: R$ ${total.toFixed(2)}</strong>
    `;

    submeucarrinho.appendChild(totalCarrinho);
}
// fim add produtos em meu carrinho


// // inicio remover item do carrinho
submeucarrinho.addEventListener("click", (event) => {
  if (event.target.classList.contains("removeritem")) {
    const name = event.target.getAttribute("data-name");
    removeritens(name);
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









// // inicio calcular subtotal e total 

// function updatecarrinho() {
//   let subtotal = 0;
//   let total= 0;
//   submeucarrinho.innerHTML = "";

//   listcar.forEach((item) => {
//     const incluirosprodutos = document.createElement("div");
//     incluirosprodutos.className = "estilizarprodutos";
//     incluirosprodutos.innerHTML = `
//       <div>
//         <p>${item.name}</p>
//         <p>Qtds: ${item.quantity}</p>
//         <p>R$: ${item.price.toFixed(2)}</p>
//         <button class='removeritem' data-name="${item.name}">Remover</button>
//       </div>`;

//     subtotal += item.price * item.quantity;
//     submeucarrinho.appendChild(incluirosprodutos);
//   });


//   Subtotal.textContent = `Sub total: ${subtotal.toLocaleString("pt-BR", {
//     style: "currency",
//     currency: "BRL"
//   })}`;


//   total+=subtotal + taxa ;
//   Valortotal.textContent = `Total:${total.toLocaleString("pt-BR",{
//     style:"currency",
//     currency: "BRL"
//   })}`;


// }

