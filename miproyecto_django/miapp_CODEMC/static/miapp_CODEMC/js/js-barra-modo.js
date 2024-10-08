const body = document.querySelector("body"),
sidebar = body.querySelector("nav"),
toggle = body.querySelector(".toggle"),
searchtBtn = body.querySelector(".search-box"),
modeswitch = body.querySelector(".toggle-switch"),
modeText = body.querySelector(".mode-text");

toggle.addEventListener("click",() => {
    sidebar.classList.toggle("close");
})

searchtBtn.addEventListener("click", () =>{
    sidebar.classList.remove("close");
})
modeswitch.addEventListener("click",() => {
    body.classList.toggle("dark");
    if (body.classList.contains("dark")) {
        modeText.innerText = "light mode"
    }else{
        modeText.innerText= "Dark mode"
    }
})