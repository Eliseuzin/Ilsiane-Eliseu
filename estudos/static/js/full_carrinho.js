const Meucarrinho = document.getElementById("meucarrinho");



// inicio adicionar item ao carrinho
Menugeral.addEventListener("click", (event) => {
  const parentButtom = event.target.closest(".addcart");
  if (parentButtom) {
    const name = parentButtom.getAttribute("data-name");
    const price = parseFloat(parentButtom.getAttribute("data-price"));
    addinmycar(name, price);
  }
});
// fim adicionar item ao carrinho


// incio funcao add ao carrinho
// function addinmycar(name, price) {
//   const checklistcar = listcar.find(item => item.name === name);
//   if (checklistcar) {
//     checklistcar.quantity += 1;
//   } else {
//     listcar.push({ name, price, quantity: 1 });
//   }
// }
// fim funcao add ao carrinho


// // inicio remover item do carrinho
// submeucarrinho.addEventListener("click", (event) => {
//   if (event.target.classList.contains("removeritem")) {
//     const name = event.target.getAttribute("data-name");
//     removeritens(name);
//   }
// });
// // fim remover item do carrinho


// // inicio funcao remover itens
// function removeritens(name) {
//   const index = listcar.findIndex(item => item.name === name);
//   if (index !== -1) {
//     if (listcar[index].quantity > 1) {
//       listcar[index].quantity -= 1;
//     } else {
//       listcar.splice(index, 1);
//     }
//     EsperarDistancia()
//   }
// }
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

