
const slides = document.querySelectorAll("#slideshow img");

let indice = 0;

const indicadores = document.getElementById("indicadores");


// ======================================
// CRIA OS PONTINHOS
// ======================================

slides.forEach((slide, i) => {

    const ponto = document.createElement("span");

    ponto.addEventListener("click", () => {

        indice = i;

        atualizarSlide();

    });

    indicadores.appendChild(ponto);

});


// ======================================
// ATUALIZA O CARROSSEL
// ======================================

function atualizarSlide() {

    slides.forEach((slide, i) => {

        // Remove todas as classes
        slide.classList.remove(
            "ativa",
            "anterior",
            "proxima",
            "distante-anterior",
            "distante-proxima"
        );


        // Calcula a posição em relação ao slide atual
        let diferenca = i - indice;


        // Corrige para o carrossel ser infinito
        if (diferenca > slides.length / 2) {
            diferenca -= slides.length;
        }

        if (diferenca < -slides.length / 2) {
            diferenca += slides.length;
        }


        // ==================================
        // SLIDE PRINCIPAL
        // ==================================

        if (diferenca === 0) {

            slide.classList.add("ativa");

        }


        // ==================================
        // SLIDE ANTERIOR
        // ==================================

        else if (diferenca === -1) {

            slide.classList.add("anterior");

        }


        // ==================================
        // PRÓXIMO SLIDE
        // ==================================

        else if (diferenca === 1) {

            slide.classList.add("proxima");

        }


        // ==================================
        // DISTANTE À ESQUERDA
        // ==================================

        else if (diferenca === -2) {

            slide.classList.add("distante-anterior");

        }


        // ==================================
        // DISTANTE À DIREITA
        // ==================================

        else if (diferenca === 2) {

            slide.classList.add("distante-proxima");

        }

    });


    // ==================================
    // ATUALIZA OS PONTINHOS
    // ==================================

    const pontos = indicadores.querySelectorAll("span");

    pontos.forEach((ponto, i) => {

        ponto.classList.toggle(
            "ativo",
            i === indice
        );

    });

}


// Inicializa
atualizarSlide();


// ======================================
// TROCA AUTOMÁTICA
// ======================================

setInterval(() => {

    indice++;

    if (indice >= slides.length) {

        indice = 0;

    }

    atualizarSlide();

}, 4000);