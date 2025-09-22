const generateBtn = document.getElementById('generate-aia-btn');
const tenderNameInput = document.getElementById('tender-name');
const tenderDescriptionTextarea = document.getElementById('tender-description');
const criteriaCheckboxes = document.querySelectorAll('#criteria-checklist .criterion');
const messageBox = document.getElementById('message-box');

// Fiktiver API-Endpunkt
const API_ENDPOINT = 'http://127.0.0.1:5001/submit';

generateBtn.addEventListener('click', async (event) => {
    // Verhindert das Standardverhalten, um die Seite nicht neu zu laden
    event.preventDefault();

    // Daten aus den Textfeldern auslesen
    const tenderName = tenderNameInput.value;
    const tenderDescription = tenderDescriptionTextarea.value;

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

    // Payload-Objekt für die API erstellen
    const payload = {
        tenderName: tenderName,
        tenderDescription: tenderDescription,
        criteria: selectedCriteria
    };

    // Konsolenausgabe der Payload (zur Überprüfung)
    console.log('Payload, der gesendet wird:', payload);

    // API-Anruf ausführen
    try {
        // Der Aufruf wird hier kommentiert, da es sich um einen fiktiven Endpunkt handelt.
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });
        // Beispiel einer erfolgreichen Antwort-Handhabung

        if(response.ok) {
            const result = await response.json();
            console.log('Erfolgreiche Antwort:', result);
        } else {
            console.error('Fehler bei der API-Anfrage:', response.statusText);
        }
    } catch (error) {
        console.error('API-Anruf fehlgeschlagen:', error);
    }
});