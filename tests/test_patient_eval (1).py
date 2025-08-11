import unittest
from app.logic.patient_eval import calcular_tfg, determinar_etapa_erc

class TestPatientEval(unittest.TestCase):
    def test_calcular_tfg(self):
        # Caso de prueba para hombre de 50 años con creatinina 1.2
        self.assertAlmostEqual(
            calcular_tfg(1.2, 50, 'M', 'no_negro'), 
            67.77, 
            delta=0.1
        )
        
        # Caso de prueba para mujer de 65 años con creatinina 0.9
        self.assertAlmostEqual(
            calcular_tfg(0.9, 65, 'F', 'no_negro'), 
            66.67, 
            delta=0.1
        )
    
    def test_determinar_etapa_erc(self):
        # Etapa 1
        self.assertEqual(determinar_etapa_erc(95), 1)
        
        # Etapa 2
        self.assertEqual(determinar_etapa_erc(75), 2)
        
        # Etapa 3a
        self.assertEqual(determinar_etapa_erc(50), "3a")
        
        # Etapa 3b
        self.assertEqual(determinar_etapa_erc(35), "3b")
        
        # Etapa 4
        self.assertEqual(determinar_etapa_erc(25), 4)
        
        # Etapa 5
        self.assertEqual(determinar_etapa_erc(10), 5)


if __name__ == '__main__':
    unittest.main()

def calcular_tfg(creatinina, edad, sexo, raza):
    """
    Calcula la Tasa de Filtración Glomerular (TFG) usando la ecuación CKD-EPI.
    
    Args:
        creatinina: Nivel de creatinina en mg/dL
        edad: Edad del paciente en años
        sexo: 'M' para masculino, 'F' para femenino
        raza: 'negro' o 'no_negro'
    
    Returns:
        El valor de TFG estimado
    """
    # Factor k basado en sexo
    k = 0.9 if sexo == 'M' else 0.7
    # Factor a basado en sexo
    a = -0.411 if sexo == 'M' else -0.329
    
    # Factor de raza
    factor_raza = 1.159 if raza == 'negro' else 1.0
    
    # Cálculo de la relación creatinina/k
    ratio = creatinina / k
    
    # Determinar min(ratio, 1) ^ a
    if ratio <= 1:
        min_ratio_power = ratio ** a
    else:
        min_ratio_power = ratio ** -1.209
    
    # Calcular TFG
    tfg = 141 * min_ratio_power * 0.993 ** edad * factor_raza
    
    if sexo == 'F':
        tfg *= 1.018
        
    return tfg

def determinar_etapa_erc(tfg):
    """
    Determina la etapa de la Enfermedad Renal Crónica (ERC) basada en la TFG.
    
    Args:
        tfg: Tasa de Filtración Glomerular
    
    Returns:
        La etapa de la ERC (1, 2, "3a", "3b", 4, o 5)
    """
    if tfg >= 90:
        return 1
    elif 60 <= tfg < 90:
        return 2
    elif 45 <= tfg < 60:
        return "3a"
    elif 30 <= tfg < 45:
        return "3b"
    elif 15 <= tfg < 30:
        return 4
    else:
        return 5
