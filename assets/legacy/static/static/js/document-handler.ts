import { ParsedDocument, LabTest, ValidationResult } from './types/document';

class DocumentHandler {
    private readonly ALLOWED_TYPES = ['application/pdf', 'text/plain'];
    private readonly API_ENDPOINTS = {
        PARSE: '/api/parse_document',
        VALIDATE: '/api/validate_results'
    };

    constructor(
        private readonly onProgress: (message: string) => void,
        private readonly onError: (error: string) => void
    ) {}

    /**
     * Procesa archivos subidos
     */
    async processFiles(files: FileList): Promise<void> {
        for (const file of files) {
            if (!this.validateFileType(file)) {
                this.onError(`Tipo de archivo no soportado: ${file.name}`);
                continue;
            }

            try {
                this.onProgress(`Procesando ${file.name}...`);
                const result = await this.uploadAndProcess(file);
                
                // Verificar confianza en los resultados
                if (result.metadata.confidence < 0.8) {
                    const shouldProceed = await this.showConfirmationDialog(result);
                    if (!shouldProceed) continue;
                }

                // Actualizar UI con resultados
                await this.updateUIWithResults(result);
                
            } catch (error) {
                this.onError(`Error procesando ${file.name}: ${error.message}`);
            }
        }
    }

    /**
     * Valida el tipo de archivo
     */
    private validateFileType(file: File): boolean {
        return this.ALLOWED_TYPES.includes(file.type);
    }

    /**
     * Sube y procesa el archivo
     */
    private async uploadAndProcess(file: File): Promise<ParsedDocument> {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(this.API_ENDPOINTS.PARSE, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${await response.text()}`);
        }

        return await response.json();
    }

    /**
     * Muestra diálogo de confirmación con preview
     */
    private async showConfirmationDialog(result: ParsedDocument): Promise<boolean> {
        // Construir mensaje detallado
        const issues = result.metadata.warnings?.map(w => `- ${w.issue}`).join('\\n') || '';
        const message = `
            Se encontraron algunos problemas al procesar el archivo:
            ${issues}
            
            Confianza en los resultados: ${(result.metadata.confidence * 100).toFixed(1)}%
            
            ¿Desea continuar con estos resultados?
        `;

        return window.confirm(message);
    }

    /**
     * Actualiza la UI con los resultados
     */
    private async updateUIWithResults(result: ParsedDocument): Promise<void> {
        // Actualizar datos del paciente
        if (result.patient_data) {
            for (const [field, value] of Object.entries(result.patient_data)) {
                const input = document.querySelector<HTMLInputElement>(`[name="${field}"]`);
                if (!input) continue;

                // Si el campo ya tiene valor, pedir confirmación
                if (input.value && input.value !== String(value)) {
                    const shouldOverwrite = await this.confirmFieldOverwrite(field, input.value, String(value));
                    if (!shouldOverwrite) continue;
                }

                input.value = String(value);
                this.markFieldAsImported(input, result.metadata.confidence);
            }
        }

        // Actualizar resultados de laboratorio
        if (result.lab_tests.length > 0) {
            this.updateLabResults(result.lab_tests);
        }
    }

    /**
     * Confirma sobrescritura de campo
     */
    private async confirmFieldOverwrite(field: string, currentValue: string, newValue: string): Promise<boolean> {
        return window.confirm(
            `El campo ${field} ya tiene un valor:\\n` +
            `Actual: ${currentValue}\\n` +
            `Nuevo: ${newValue}\\n\\n` +
            `¿Desea sobrescribir el valor actual?`
        );
    }

    /**
     * Marca un campo como importado
     */
    private markFieldAsImported(input: HTMLInputElement, confidence: number): void {
        input.classList.add('field-imported');
        
        // Aplicar estilo según nivel de confianza
        const colors = {
            high: '#e6ffe6',   // Verde claro
            medium: '#fff3e6',  // Naranja claro
            low: '#ffe6e6'     // Rojo claro
        };

        if (confidence >= 0.8) {
            input.style.backgroundColor = colors.high;
        } else if (confidence >= 0.5) {
            input.style.backgroundColor = colors.medium;
        } else {
            input.style.backgroundColor = colors.low;
        }

        // Agregar tooltip con información
        input.title = `Dato importado (Confianza: ${(confidence * 100).toFixed(1)}%)`;
    }

    /**
     * Actualiza resultados de laboratorio
     */
    private updateLabResults(tests: LabTest[]): void {
        tests.forEach(test => {
            const container = this.findOrCreateLabTestContainer(test);
            this.updateLabTestValues(container, test);
        });
    }

    /**
     * Encuentra o crea contenedor para prueba de laboratorio
     */
    private findOrCreateLabTestContainer(test: LabTest): HTMLElement {
        const existingContainer = document.querySelector(`[data-test-name="${test.name}"]`);
        if (existingContainer) return existingContainer as HTMLElement;

        // Crear nuevo contenedor
        const container = document.createElement('div');
        container.className = 'lab-test-container';
        container.setAttribute('data-test-name', test.name);

        const template = `
            <div class="lab-test-header">
                <span class="lab-test-name">${test.name}</span>
                <span class="lab-test-confidence" title="Confianza en el dato">
                    ${(test.confidence * 100).toFixed(1)}%
                </span>
            </div>
            <div class="lab-test-body">
                <input type="number" name="valor" step="0.01">
                <input type="text" name="unidad" readonly>
                <input type="date" name="fecha">
            </div>
            <div class="lab-test-footer">
                <label>
                    <input type="checkbox" class="lab-editable-toggle">
                    Editar manualmente
                </label>
            </div>
        `;

        container.innerHTML = template;
        document.querySelector('.lab-results-container')?.appendChild(container);
        return container;
    }

    /**
     * Actualiza valores de prueba de laboratorio
     */
    private updateLabTestValues(container: HTMLElement, test: LabTest): void {
        const valorInput = container.querySelector<HTMLInputElement>('[name="valor"]');
        const unidadInput = container.querySelector<HTMLInputElement>('[name="unidad"]');
        const fechaInput = container.querySelector<HTMLInputElement>('[name="fecha"]');

        if (valorInput && !valorInput.value) {
            valorInput.value = String(test.value);
            valorInput.readOnly = true;
        }

        if (unidadInput) {
            unidadInput.value = test.unit;
        }

        if (fechaInput && !fechaInput.value) {
            fechaInput.value = new Date(test.date).toISOString().split('T')[0];
            fechaInput.readOnly = true;
        }

        this.setupEditableToggle(container);
    }

    /**
     * Configura toggle de edición manual
     */
    private setupEditableToggle(container: HTMLElement): void {
        const toggle = container.querySelector<HTMLInputElement>('.lab-editable-toggle');
        const inputs = container.querySelectorAll<HTMLInputElement>('input:not(.lab-editable-toggle)');

        toggle?.addEventListener('change', (e) => {
            const isEditable = (e.target as HTMLInputElement).checked;
            inputs.forEach(input => {
                input.readOnly = !isEditable;
                input.classList.toggle('field-editable', isEditable);
            });
        });
    }
}
