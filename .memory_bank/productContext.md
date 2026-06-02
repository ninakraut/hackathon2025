# Product Context

This application was created as part of the **2B-BIM Hackathon** to automate and streamline the process of checking and enhancing BIM **AIA (Auftraggeber-Informationsanforderungen)** specifications.

## The Problem
AIA specifications dictate the information requirements that contractors must deliver in their BIM models. However, mapping complex sustainability criteria to specific BIM/IFC features is a manual, error-prone, and time-consuming process.

## The Solution
This tool provides an interface to:
1. Parse a standard `.ids` (Information Delivery Specification) file.
2. Select target sustainability criteria.
3. Automatically append the required properties/attributes to the IDS file based on predefined mappings, outputting a fully conformant, extended `.ids` specification.

## Core Features & Workflow
1. **IDS Source Input**:
   - **Upload**: Directly upload a local `.ids` file.
   - **BIM Germany API**: Enter an AIA Project GUID to fetch the project's IDS directly from the official portal (`via.bund.de`).
2. **Context Selection**:
   - Select building type context (e.g., Verwaltungsgebäude).
3. **Criteria Checklist**:
   - Filter and check specific sustainability criteria (e.g., Bauteil-Volumen, Verbindungstyp, Bauteiltyp, etc.).
4. **Automated Merging & Generation**:
   - The backend maps criteria to specific properties and appends them to the specification using a BeautifulSoup-based XML editor.
   - Generates the modified `.ids` file ready for download.
