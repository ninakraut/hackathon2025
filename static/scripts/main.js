// Referenzen auf die Eingabeelemente im DOM
const generateBtn = document.getElementById('generate-aia-btn');        // Button zum Generieren
const tenderNameInput = document.getElementById('tender-name');         // Eingabefeld für Projektnamen
const tenderDescriptionTextarea = document.getElementById('tender-description'); // Eingabefeld für Beschreibung
const criteriaCheckboxes = document.querySelectorAll('#criteria-checklist .criterion'); // Alle Kriterien-Checkboxen
const idsUploadInput = document.getElementById('ids-upload');           // Datei-Upload-Feld (.ids)
const idsGUIDInput = document.getElementById('ids-guid');               // Eingabefeld für GUID (Alternative zum Upload)

const API_ENDPOINT = '/submit'; // API-Endpunkt in Flask

// Klick-Event für den "Generate"-Button
generateBtn.addEventListener('click', async (event) => {
    // Verhindert das Standardverhalten des Buttons (kein Seitenreload)
    event.preventDefault();

    // Eingaben aus Formularfeldern auslesen
    const tenderName = tenderNameInput.value;
    const tenderDescription = tenderDescriptionTextarea.value;
    const idsFile = idsUploadInput.files[0]; // Erste ausgewählte Datei (falls vorhanden)
    const idsGUID = idsGUIDInput.value;      // GUID-Wert (falls vorhanden)

    // Ausgewählte Kriterien-Checkboxen ermitteln
    const selectedCriteria = Array.from(criteriaCheckboxes)
        .filter(criterion => {
            let checkbox = criterion.querySelector("input[type=checkbox]");
            return checkbox.checked; // Nur die ausgewählten Checkboxen berücksichtigen
        })
        .map(criterion => {
            // Zu jeder Checkbox gehört auch ein Textfeld (z. B. Wert/Eingabe)
            let checkbox = criterion.querySelector("input[type=checkbox]");
            let value = criterion.querySelector("input[type=text]").value;

            // Datenstruktur für Backend: Gruppe, Kriterium, Wert
            return {
                group: criterion.dataset.group,
                criterion: criterion.dataset.criterion,
                value: value
            };
        });

    // FormData-Objekt vorbereiten (wird für Dateien benötigt)
    const formData = new FormData();
    formData.append('tenderName', tenderName);
    formData.append('tenderDescription', tenderDescription);
    formData.append('criteria', JSON.stringify(selectedCriteria)); // Array als JSON übertragen
    formData.append('idsGUID', idsGUID);

    // Falls Datei hochgeladen → hinzufügen
    if (idsFile) {
        formData.append('idsFile', idsFile);
    }

    // Debug-Ausgabe: Zeigt Payload im Browser-Log
    console.log('Payload, der gesendet wird:', formData);

    // API-Anfrage an Flask-Backend
    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            body: formData, // FormData enthält Felder + Datei
        });

        // Wenn Anfrage erfolgreich war
        if(response.ok) {
            const result = await response.json();
            console.log('Erfolgreiche Antwort:', result);

            // Weiterleitung nach erfolgreichem Submit
            window.location = "/submit";
        } else {
            console.error('Fehler bei der API-Anfrage:', response.statusText);
        }
    } catch (error) {
        // Falls Request komplett fehlschlägt (z. B. Netzwerkfehler)
        console.error('API-Anruf fehlgeschlagen:', error);
    }
});
