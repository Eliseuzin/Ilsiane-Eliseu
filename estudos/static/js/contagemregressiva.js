console.log("TESTE - JavaScript carregado!");

const dataCasamento = new Date("Marc 13, 2027 19:00:00").getTime();

const contador = setInterval(() => {
    const agora = new Date().getTime();
    const diferenca = dataCasamento - agora;

    const dias = Math.floor(diferenca/(1000*60*60*24));
    const horas = Math.floor((diferenca%(1000*60*60*24))/(1000*60*60));

    const minutos = Math.floor((diferenca %(1000*60*60))/(1000*60));

    const segundos = Math.floor((diferenca%(1000*60))/1000);

    document.getElementById("dias").textContent = dias;
    document.getElementById("horas").textContent = String(horas).padStart(2,"0");
    document.getElementById("minutos").textContent = String(minutos).padStart(2,"0");
    document.getElementById("segundos").textContent = String(segundos).padStart(2,"0");

    // quando chegar o grande dia

    if(contador<=0){
        clearInterval(contador);
        document.getElementById("dias").textContent = "0";
        document.getElementById("horas").textContent = "0";
        document.getElementById("minutos").textContent = "0";
        document.getElementById("segundos").textContent = "0";
    }

}, 1000);