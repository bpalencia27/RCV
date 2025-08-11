export interface DocumentMetadata {
    file_name: string;
    file_type: string;
    upload_date: string;
    processed: boolean;
    error?: string;
    warnings?: Array<{
        test: string;
        value?: number;
        date?: string;
        issue: string;
    }>;
    confidence: number;
}

export interface LabTest {
    name: string;
    value: number;
    unit: string;
    date: string;
    raw_name: string;
    raw_unit: string;
    source: 'pdf' | 'manual' | 'importado';
    confidence: number;
}

export interface ParsedDocument {
    metadata: DocumentMetadata;
    patient_data?: {
        nombre?: string;
        edad?: number;
        sexo?: string;
        peso?: number;
        talla?: number;
        fecha_nacimiento?: string;
    };
    lab_tests: LabTest[];
    raw_text?: string;
}

export interface ValidationResult {
    valid: boolean;
    issues: Array<{
        test: string;
        value?: number;
        date?: string;
        issue: string;
    }>;
    confidence: number;
}
