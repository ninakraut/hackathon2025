const generateBtn = document.getElementById('generate-aia-btn');
const tenderNameInput = document.getElementById('tender-name');
const tenderDescriptionTextarea = document.getElementById('tender-description');
const criteriaCheckboxes = document.querySelectorAll('#criteria-checklist .criterion');
const idsUploadInput = document.getElementById('ids-upload'); // Referenz zum neuen Upload-Feld
const idsGUIDInput = document.getElementById('ids-guid');

// Fiktiver API-Endpunkt
const API_ENDPOINT = '/submit';

generateBtn.addEventListener('click', async (event) => {
    // Verhindert das Standardverhalten, um die Seite nicht neu zu laden
    event.preventDefault();

    // Daten aus den Textfeldern auslesen
    const tenderName = tenderNameInput.value;
    const tenderDescription = tenderDescriptionTextarea.value;
    const idsFile = idsUploadInput.files[0]; // Das erste ausgewählte File-Objekt
    const idsGUID = idsGUIDInput.value; // Das erste ausgewählte File-Objekt

    // Ausgewählte Checkboxen auslesen
    const selectedCriteria = Array.from(criteriaCheckboxes)
        .filter(criterion => {
            let checkbox = criterion.querySelector("input[type=checkbox]")
            return checkbox.checked
        })
        .map(criterion => {
            let checkbox = criterion.querySelector("input[type=checkbox]")
            let value = criterion.querySelector("input[type=text]").value

            return {
                group: criterion.dataset.group,
                criterion: criterion.dataset.criterion,
                value: value
            };
        });

    // FormData-Objekt für die API erstellen (unterstützt Dateien)
    const formData = new FormData();
    formData.append('tenderName', tenderName);
    formData.append('tenderDescription', tenderDescription);
    formData.append('criteria', JSON.stringify(selectedCriteria));
    formData.append('idsGUID', idsGUID);

    // Fügt die Datei hinzu, wenn eine ausgewählt wurde
    if (idsFile) {
        formData.append('idsFile', idsFile);
    }

    // Konsolenausgabe der Payload (zur Überprüfung)
    console.log('Payload, der gesendet wird:', formData);

    // API-Anruf ausführen
    try {
        // Der Aufruf wird hier kommentiert, da es sich um einen fiktiven Endpunkt handelt.
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            body: formData,
        });
        // Beispiel einer erfolgreichen Antwort-Handhabung

        if(response.ok) {
            const result = await response.json();
            console.log('Erfolgreiche Antwort:', result);

            window.location = "/submit"
        } else {
            console.error('Fehler bei der API-Anfrage:', response.statusText);
        }
    } catch (error) {
        console.error('API-Anruf fehlgeschlagen:', error);
    }
});