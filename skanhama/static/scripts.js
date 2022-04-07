//                                - Navbar Search -                                       //
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

//                          - Account Menu -                                //
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

//                           - Requirements Fields -                              //
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

// Printing the field input data to the form input
const reqsManual = document.getElementById("reqs-manual");
const reqsFormControl = document.getElementById("requirements");
if (reqsManual) {
    reqsManual.addEventListener("click", reqsDataCompiler);
}
function reqsDataCompiler() {
    let dict = {};
    const names = document.querySelectorAll(".fc-reqs-name");
    const links = document.querySelectorAll(".fc-reqs-link");
    const notes = document.querySelectorAll(".fc-reqs-note");
    for (let i = 0; i < names.length; i++){
        if (names[i].value !== "") {
            dict[i] = [names[i].value, links[i].value, notes[i].value];
        }
    }
    reqsFormControl.textContent = JSON.stringify(dict);
}

// Print on form submit
const submit = document.getElementById("submit");
if (submit) {
    reqsDataCompiler();
}

//                             - Dropzone.js Config -                                //
// Upload Dropzone
if (document.getElementById("dropzoneAnimation")) {
    // Handle dismiss icon event on error display
    const errorDismiss1 = document.getElementById("js-error-dismiss-file");
    const errorDismiss2 = document.getElementById("js-error-dismiss-banner");
    const errorDismiss3 = document.getElementById("js-error-dismiss-gallery");
    if (errorDismiss1) {
        errorDismiss1.addEventListener("click", errorDismiss);
    }
    if (errorDismiss2) {
        errorDismiss2.addEventListener("click", errorDismiss);
    }
    if (errorDismiss3) {
        errorDismiss3.addEventListener("click", errorDismiss);
    }
    function errorDismiss() {
        this.parentElement.classList.add("hidden");
    }

    // Options - Animation zip file
    const dropzoneOptionsFile = {
        dictDefaultMessage: 'Drop your file here or click to select.<br>Max file size: 40 MB. Accepted file format: .zip.',
        paramName: "file",
        maxFilesize: 40, // MB
        acceptedFiles: ".zip",
        addRemoveLinks: true,
        dictRemoveFile: "Remove",
        dictCancelUpload: "Cancel",
        uploadMultiple: false,
        maxFiles: 1,
        url: "/upload",
        init: function () {
            let container = document.getElementById("js-error-file");
            let error = document.getElementById("js-error-file-text");
            let error_text = document.createTextNode("");
            this.on("addedfile", function (file) {
                let _this = this;
                console.log(file.name + " -> type: " + file.type);
                if ($.inArray(file.type, ["application/x-zip-compressed", "application/zip"]) === -1) {
                    _this.removeFile(file);
                    container.classList.remove("hidden");
                    error_text.data = "Incompatible file format. Please ensure that the file is a .zip file.";
                    error.appendChild(error_text);
                    console.log("error > incorrect file type for " + file.name)
                } else if (this.files.length > 1) {
                    _this.removeFile(file);
                    console.log("error > too many files (" + this.files.length + ") reached when adding " + file.name)
                    error_text.data = "You have reached the maximum number of files and cannot upload any more."
                    error.appendChild(error_text);
                    container.classList.remove("hidden");
                }
            });
            this.on("success", function (file) {
                console.log("success > " + file.name);
                if (!container.classList.contains("hidden")) {
                    error.removeChild(error_text);
                    container.classList.add("hidden");
                }
            });
        },
        accept: function(file, done) {
            return done();
        }
    };
    // Options - Banner Image
    const dropzoneOptionsBanner = {
        dictDefaultMessage: 'Drop your banner image here or click to select.<br>Max file size: 3 MB. Accepted file formats: .jpg, .jpeg, .gif, .png.',
        paramName: "file",
        maxFilesize: 3, // MB
        acceptedFiles: ".jpg, .gif, .png, .jpeg",
        addRemoveLinks: true,
        dictRemoveFile: "Remove",
        dictCancelUpload: "Cancel",
        uploadMultiple: false,
        maxFiles: 1,
        createImageThumbnails: true,
        maxThumbnailFilesize: 2,
        thumbnailWidth: 96,
        thumbnailHeight: 96,
        thumbnailMethod: "crop",
        url: "/upload",
        init: function () {
            let container = document.getElementById("js-error-banner");
            let error = document.getElementById("js-error-banner-text");
            let error_text = document.createTextNode("");
            this.on("addedfile", function (file) {
                let _this = this;
                console.log(file.name + " -> type: " + file.type);
                if ($.inArray(file.type, ["image/jpeg", "image/jpg", "image/png", "image/gif"]) === -1) {
                    _this.removeFile(file);
                    container.classList.remove("hidden");
                    error_text.data = "Incompatible file format. Please ensure all files are either .jpg, .jpeg, .gif or .png.";
                    error.appendChild(error_text);
                    console.log("error > incorrect file type for " + file.name)
                } else if (this.files.length > 1) {
                    _this.removeFile(file);
                    console.log("error > too many files (" + this.files.length + ") reached when adding " + file.name)
                    error_text.data = "You have reached the maximum number of files and cannot upload any more."
                    error.appendChild(error_text);
                    container.classList.remove("hidden");
                }
            });
            this.on("success", function (file) {
                console.log("success > " + file.name);
                if (!container.classList.contains("hidden")) {
                    error.removeChild(error_text);
                    container.classList.add("hidden");
                }
            });
        },
        accept: function(file, done) {
            return done();
        },
        renameFile: function (file) {
            let extension = file.name.substring(file.name.lastIndexOf('.')+1, file.name.length) || file.name;
            return "banner." + extension;
        }
    };
    // Options - Gallery Images
    const dropzoneOptionsGallery = {
        dictDefaultMessage: 'Drop your gallery images here or click to select.<br>Max size per file: 6 MB. Accepted file formats: .jpg, .jpeg, .gif, .png.',
        paramName: "file",
        maxFilesize: 6, // MB
        acceptedFiles: ".jpg, .gif, .png, .jpeg",
        resizeWidth: 1080,
        resizeQuality: 1,
        addRemoveLinks: true,
        dictRemoveFile: "Remove",
        dictCancelUpload: "Cancel",
        uploadMultiple: true,
        maxFiles: 27,
        createImageThumbnails: true,
        maxThumbnailFilesize: 10,
        thumbnailWidth: 96,
        thumbnailHeight: 96,
        thumbnailMethod: "crop",
        url: "/upload",
        init: function () {
            let container = document.getElementById("js-error-gallery");
            let error = document.getElementById("js-error-gallery-text");
            let error_text = document.createTextNode("");
            let droppedFilesCounter;
            this.on("drop", function(event) {
                if (typeof event.dataTransfer.files == 'object') {
                    droppedFilesCounter = event.dataTransfer.files.length;
                }
            });
            this.on("addedfile", function (file) {
                let _this = this;
                console.log(file.name + " -> type: " + file.type);
                if ($.inArray(file.type, ["image/jpeg", "image/jpg", "image/png", "image/gif"]) === -1) {
                    _this.removeFile(file);
                    container.classList.remove("hidden");
                    error_text.data = "Incompatible file format. Please ensure all files are either .jpg, .jpeg, .gif or .png.";
                    error.appendChild(error_text);
                    console.log("error > incorrect file type for " + file.name)
                } else if (this.files.length > 27) {
                    _this.removeFile(file);
                    console.log("error > too many files (" + this.files.length + ") reached when adding " + file.name)
                    error_text.data = "You have reached the maximum number of files and cannot upload any more."
                    error.appendChild(error_text);
                    container.classList.remove("hidden");
                } else if (this.files.length > 4 * 1024 * 1024) {
                    _this.removeFile(file);
                    console.log("error > too many files (" + this.files.length + ") reached when adding " + file.name)
                    error_text.data = "You have reached the maximum number of files and cannot upload any more."
                    error.appendChild(error_text);
                    container.classList.remove("hidden");
                }
                droppedFilesCounter--;
            //    TODO: Fix droppedFilesCounter mechanism
            });
            this.on("success", function (file) {
                console.log("success > " + file.name);
                if (!container.classList.contains("hidden") && droppedFilesCounter === 1) {
                    error.removeChild(error_text);
                    container.classList.add("hidden");
                }

                console.log("droppedFilesCounter: " + droppedFilesCounter)
            });
        },
        accept: function(file, done) {
            return done();
        }
    };
    const dzAnimations = new Dropzone("div#dropzoneAnimation", dropzoneOptionsFile);
    const dzBanner = new Dropzone("div#dropzoneBanner", dropzoneOptionsBanner);
    const dzGallery = new Dropzone("div#dropzoneGallery", dropzoneOptionsGallery);
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
