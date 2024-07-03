console.log("JavaScript-Datei erfolgreich geladen!");

// Funktion, die beim Laden der Seite aufgerufen wird
document.addEventListener('DOMContentLoaded', (event) => {
    console.log('Die Seite wurde vollständig geladen');

    // Formularvalidierung beim Absenden
    const form = document.querySelector("form");
    form.addEventListener("submit", function(event) {
        const input = document.querySelector("input[name='example']");
        if (input && input.value.trim() === "") {
            alert("Dieses Feld darf nicht leer sein.");
            event.preventDefault();
        }
    });
});
