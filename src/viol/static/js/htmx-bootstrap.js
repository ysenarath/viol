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
