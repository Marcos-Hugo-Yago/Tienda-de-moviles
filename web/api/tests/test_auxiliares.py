import unittest
import sys
import os

# Ajustamos el path para que pueda encontrar la carpeta 'web'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web.funciones_auxiliares import calculariva

class TestFuncionesAuxiliares(unittest.TestCase):

    def test_calcular_iva_100(self):
        # El importe es 100
        importe = 100
        # El resultado esperado es 21
        esperado = 21.0
        
        # Ejecutamos la función
        resultado = calculariva(importe)
        
        # Comprobamos (Assert)
        self.assertEqual(resultado, esperado, "El IVA de 100 debería ser 21")

if __name__ == '__main__':
    unittest.main()
