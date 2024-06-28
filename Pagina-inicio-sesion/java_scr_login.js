const contenedor = document.querySelector(".contenedor");
const loginlink = document.querySelector(".login-link");
const registerlink = document.querySelector(".register-link");
const btnclose = document.querySelector(".icon-close");

registerlink.addEventListener("click", ()=> {
    contenedor.classList.add("activate");
});


loginlink.addEventListener("click", ()=> {
    contenedor.classList.remove("activate");
});

btnclose.addEventListener("click", ()=> {
    contenedor.classList.add("activate-close");
});