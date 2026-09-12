console.log("slides_fotos.js carregado");

const fotos = [
    "../img/slide1.jpeg",
    "../img/slide2.jpg",
    "../img/slide3.jpg",
    "../img/slide4.jpg",
    "../img/slide5.jpg",
    "../img/slide6.jpg",
    "../img/slide7.jpg",
    "../img/slide8.jpg",
    "../img/slide9.jpg",
    "../img/slide10.jpg"
];

let indice = 0;

const slides = document.querySelectorAll("#slideshow img");

// Mostra apenas o primeiro
slides.forEach((slide, i) => {
    slide.style.display = i === 0 ? "block" : "none";
});

setInterval(() => {

    // Esconde a foto atual
    slides[indice].style.display = "none";

    // Vai para a próxima
    indice++;

    // Volta para a primeira depois da última
    if (indice >= slides.length) {
        indice = 0;
    }

    // Mostra a nova foto
    slides[indice].style.display = "block";

}, 4000);