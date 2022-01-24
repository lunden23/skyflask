// Handle opening and closing of the navbar search input
// Opens on search icon click and closes when user presses outside the search input
const navSearchIcon = document.getElementById("nav-search-icon");
const navSearchInput = document.getElementById("nav-search-input");
const navBar = document.getElementById("nav-list");

navSearchIcon.addEventListener("click", navSearchFunction);
function navSearchFunction() {
    navSearchIcon.style.display = "none";
    navBar.style.display = "none";
    navSearchInput.style.display = "inline-flex";
    navSearchInput.focus();
    window.addEventListener("click", navSearchClickOut);
}

const navSearchClickOut = (e) => {
  if (!e.target.id.includes("nav-search-input") && !e.target.id.includes("nav-search-icon")) {
    navSearchInput.style.display = "none";
    navSearchIcon.style.display = "block";
    navBar.style.display = "inline-flex";
    window.removeEventListener("click", navSearchClickOut);
  }
};

// Handle opening and closing of the Account Menu
// Opens on Account icon click and closes when user presses outside the menu
const accountMenuIcon = document.getElementById("accountMenuIcon");
const accountMenu = document.getElementById("dropdownAccount");

accountMenuIcon.addEventListener("click", accountMenuFunction);
function accountMenuFunction() {
    accountMenu.classList.toggle("dropdown-show");
    window.addEventListener("click", accountMenuClickOut);
}

const accountMenuClickOut = (e) => {
    if (!e.target.matches(".btn-dropdown")) {
        const dropdowns = document.getElementsByClassName("dropdown-content");
        let i;
        for (i = 0; i < dropdowns.length; i++) {
            const openDropdown = dropdowns[i];
            if (openDropdown.classList.contains("dropdown-show")) {
                openDropdown.classList.remove("dropdown-show");
            }
        }
        window.removeEventListener("click", accountMenuClickOut);
    }
}

// Live (Active) Search function in the search bar in the nav menu
// $(function (){
//     $("#nav-search-input").on("input", function(e){
//         let textFrontEnd = $("#nav-search-input").val();
//         // console.log(textFrontEnd);
//         $.ajax({
//             method:"post",
//             url:"/livesearch",
//             data:{text:textFrontEnd},
//             success:function (res){
//                 console.log(res);
//             }
//         })
//     })
// })
