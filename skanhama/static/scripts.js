// Function to handle search bar in the navigation bar
// Expands on click to cover other nav bar items
function navSearchFocus() {
    let nav = document.getElementById("nav-list");
    nav.style.display = "none";
}

window.onclick = function(event) {
    if (!event.target.matches(".search-nav")) {
        let nav = document.getElementById("nav-list");
        nav.style.display = "visible";
    }
}

// Function to handle dropdown of account menu when user is logged in
// Dropdown is shown on button click and hidden on button click or click outside of dropdown area
function dropdownAccount() {
    document.getElementById("dropdownAccount").classList.toggle("dropdown-show")
}

window.onclick = function(event) {
    if (!event.target.matches(".btn-dropdown")) {
        const dropdowns = document.getElementsByClassName("dropdown-content");
        let i;
        for (i = 0; i < dropdowns.length; i++) {
            const openDropdown = dropdowns[i];
            if (openDropdown.classList.contains("dropdown-show")) {
                openDropdown.classList.remove("dropdown-show");
            }
        }
    }
}
