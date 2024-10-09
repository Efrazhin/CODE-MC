const body = document.querySelector("body"),
sidebar = body.querySelector("nav"),
toggle = body.querySelector(".toggle"),
searchtBtn = body.querySelector(".search-box"),
modeswitch = body.querySelector(".toggle-switch"), // Asegúrate de que es modeswitch
modeText = body.querySelector(".mode-text");

toggle.addEventListener("click", () => {
    sidebar.classList.toggle("close");
});

searchtBtn.addEventListener("click", () => {
    sidebar.classList.remove("close");
});

modeswitch.addEventListener("click", () => {
    const isDarkMode = body.classList.toggle("dark");
    const theme = isDarkMode ? "dark" : "light";
    localStorage.setItem("theme", theme);
    modeText.innerText = isDarkMode ? "light mode" : "dark mode";
});

// Función para cargar el tema del almacenamiento local
function loadTheme() {
    const savedTheme = localStorage.getItem("theme") || "light"; // Valor por defecto
    body.classList.toggle("dark", savedTheme === "dark");
    modeText.innerText = savedTheme === "dark" ? "light mode" : "dark mode";
}

// Cargar el tema al iniciar
window.onload = loadTheme;
