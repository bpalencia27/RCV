export const patientState = {
  medications: new Set(),
  addMedication(name){
    const norm = name.trim().toLowerCase();
    if(!norm) return false;
    const sizeBefore = this.medications.size;
    this.medications.add(norm);
    return this.medications.size > sizeBefore;
  },
  list(){ return Array.from(this.medications).sort(); }
};
