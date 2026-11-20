"use strict";

const form = document.getElementById("intake-batch");
const conditionals = Array.from(form.querySelectorAll("[data-depends-on]"));

function updateQuestions() {
    for (const row of conditionals) {
        const parent = form.elements.namedItem(row.dataset.dependsOn);
        const active = JSON.parse(row.dataset.appliesWhen).includes(
            parent ? parent.value : row.dataset.savedParent
        );
        row.querySelector("select").disabled = !active;
        row.classList.toggle("inactive", !active);
    }
}

form.addEventListener("change", updateQuestions);
window.addEventListener("pageshow", updateQuestions);
updateQuestions();
