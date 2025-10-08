import unittest
from parser import parser

print('Iniciando testes do parser...')
class TestParser(unittest.TestCase):
    def test_programa_simples(self):
        codigo = '''
        program exemplo;
        begin
            x := 10;
            write(x)
        end
        '''
        resultado = parser.parse(codigo)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado[0], 'programa')

    def test_declaracao_const(self):
        codigo = '''
        program exemplo;
        const PI := 3.14;
        begin
            write(PI)
        end
        '''
        resultado = parser.parse(codigo)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado[0], 'programa')

    def test_funcao(self):
        codigo = '''
        program exemplo;
        function soma(a: integer; b: integer): integer
        var resultado: integer;
        begin
            resultado := a + b;
            write(resultado)
        end
        begin
            write(soma(2,3))
        end
        '''
        resultado = parser.parse(codigo)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado[0], 'programa')

if __name__ == '__main__':
    unittest.main()