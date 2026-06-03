const { createApp } = Vue;

createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            activeTab: 'upload', // 'upload' or 'guid'
            isDragging: false,
            idsFile: null,
            idsGUID: '',
            buildingType: 'verwaltungsgebaeude',
            selectedCriteria: [], // Array of { group, criterion, value }
            isSubmitting: false,
            errorMsg: ''
        };
    },
    computed: {
        isValid() {
            if (this.activeTab === 'upload') {
                return this.idsFile !== null;
            } else {
                return this.idsGUID.trim().length > 0;
            }
        }
    },
    methods: {
        isCriterionSelected(criterion) {
            return this.selectedCriteria.some(c => c.criterion === criterion);
        },
        toggleCriterion(criterion) {
            const idx = this.selectedCriteria.findIndex(c => c.criterion === criterion);
            if (idx === -1) {
                this.selectedCriteria.push({ group: '', criterion, value: '' });
            } else {
                this.selectedCriteria.splice(idx, 1);
            }
        },
        handleFileSelection(event) {
            const files = event.target.files;
            if (files && files.length > 0) {
                this.setFile(files[0]);
            }
        },
        handleFileDrop(event) {
            this.isDragging = false;
            const files = event.dataTransfer.files;
            if (files && files.length > 0) {
                this.setFile(files[0]);
            }
        },
        setFile(file) {
            if (file.name.toLowerCase().endsWith('.ids')) {
                this.idsFile = file;
                this.errorMsg = '';
            } else {
                this.errorMsg = 'Nur Dateien mit der Endung .ids sind erlaubt.';
                this.idsFile = null;
                if (this.$refs.fileInput) {
                    this.$refs.fileInput.value = '';
                }
            }
        },
        clearFile() {
            this.idsFile = null;
            if (this.$refs.fileInput) {
                this.$refs.fileInput.value = '';
            }
        },
        async submitForm() {
            if (!this.isValid) return;

            this.isSubmitting = true;
            this.errorMsg = '';

            const formData = new FormData();
            formData.append('criteria', JSON.stringify(this.selectedCriteria));
            formData.append('buildingType', this.buildingType);

            if (this.activeTab === 'upload' && this.idsFile) {
                formData.append('idsFile', this.idsFile);
                formData.append('idsGUID', '');
            } else {
                formData.append('idsGUID', this.idsGUID.trim());
            }

            try {
                const response = await fetch('/submit', {
                    method: 'POST',
                    body: formData,
                });

                if (response.ok) {
                    window.location = '/submit';
                } else {
                    const resData = await response.json().catch(() => ({}));
                    this.errorMsg = resData.error || `Fehler bei der Verarbeitung (${response.statusText})`;
                }
            } catch (error) {
                console.error('API-Anruf fehlgeschlagen:', error);
                this.errorMsg = 'Netzwerkfehler beim Senden der Daten.';
            } finally {
                this.isSubmitting = false;
            }
        }
    }
}).mount('#app');
