let violConfirmModalInstance = new bootstrap.Modal("#violConfirmModal");
let violConfirmModalInstanceElement = document.getElementById(
    "violConfirmModal",
);
let violConfirmModalConfirmButton = document.getElementById(
    "violConfirmModalConfirmButton",
);

let violConfirmModalMessage = document.getElementById(
    "violConfirmModalMessage",
);

// once hidden.bs.modal remove the event listener
violConfirmModalInstanceElement.addEventListener(
    "hidden.bs.modal",
    () => {
        violConfirmModalConfirmButton.onclick = null;
    },
);

document.body.addEventListener("htmx:confirm", function (evt) {
    // check hx-confirm attribute to see if it should use the native alert
    if ("hx-confirm" in evt.target.attributes) {
        if (~evt.target.matches("[confirm-with-native-alert='true']")) {
            evt.preventDefault();
            // update message in the model (#violConfirmModalMessage)
            violConfirmModalMessage.innerText = evt.detail.question;
            violConfirmModalInstance.show();
            // add new event listener to the confirm button
            violConfirmModalConfirmButton.onclick = () => {
                violConfirmModalInstance.hide();
                evt.detail.issueRequest(true);
            };
        }
    }
});

document.body.addEventListener("violAlert", function (evt) {
    // add alert to the page (bootstrap alert)
    let alert = document.createElement("div");
    alert.classList.add("alert", "alert-" + evt.detail.level);
    alert.innerText = evt.detail.message;
    // position the alert at the top right corner
    alert.style.position = "fixed";
    alert.style.left = 0;
    alert.style.bottom = 0;
    alert.style.width = "20em";
    alert.style.margin = "1em";
    alert.style.zIndex = 1000;
    document.body.appendChild(alert);
    // remove the alert after 5 seconds
    setTimeout(() => {
        alert.remove();
    }, 3000);
});
