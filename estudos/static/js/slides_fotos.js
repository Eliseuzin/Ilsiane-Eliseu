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

const slide1 = document.getElementById("slide1");
const slide2 = document.getElementById("slide2");

slide1.classList.add("ativa");

setInterval(() => {

    indice++;

    if (indice >= fotos.length) {
        indice = 0;
    }

    if (slide1.classList.contains("ativa")) {

        slide2.src = fotos[indice];

        slide1.classList.remove("ativa");
        slide2.classList.add("ativa");

    } else {

        slide1.src = fotos[indice];

        slide2.classList.remove("ativa");
        slide1.classList.add("ativa");
    }

}, 4000);