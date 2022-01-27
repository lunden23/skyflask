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

// Handle adding of Upload Requirements input fields
// Adds a new div with inputs on icon click
const reqsAddIcon = document.getElementById("icon-reqs-add");
const rootNode = document.getElementById("upload-reqs-inner");

if (reqsAddIcon) {
    reqsAddIcon.addEventListener("click", reqsAddInputFunction);
} else {
    console.log("Icon Requirements Add button not found.")
}
function reqsAddInputFunction() {
    let div = document.createElement("div");
    div.classList.add("upload-reqs-control");
    let name = document.createElement("input");
    name.classList.add("form-control", "fc-upload", "fc-reqs", "fc-reqs-name");
    name.type = "text";
    let link = document.createElement("input");
    link.classList.add("form-control", "fc-upload", "fc-reqs", "fc-reqs-link");
    link.type = "text";
    let note = document.createElement("input");
    note.classList.add("form-control", "fc-upload", "fc-reqs", "fc-reqs-note");
    note.type = "text";
    let icon = document.createElement("i");
    icon.classList.add("fas", "fa-minus-circle", "fc-reqs-delete", "icon", "icon-sm");
    icon.addEventListener("click", reqsRemoveInputFunction);
    div.append(name, link, note, icon);
    rootNode.insertBefore(div, reqsAddIcon);
}

// Handle removal of Upload Requirements input fields
// Removes the active div when remove icon is clicked
const reqsRemove1 = document.getElementById("reqsRemove1");
const reqsRemove2 = document.getElementById("reqsRemove2");
if (reqsRemove1) {
    reqsRemove1.addEventListener("click", reqsRemoveInputFunction);
}
if (reqsRemove2) {
    reqsRemove2.addEventListener("click", reqsRemoveInputFunction);
}
function reqsRemoveInputFunction() {
    this.parentElement.remove();
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
