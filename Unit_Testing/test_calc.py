import unittest
import calc

class TestCalc(unittest.TestCase):
    
    def test_add(self):                 # all tests start with "test"    test_add test_ .... etc
        self.assertEqual(calc.add(10,5),15)  # teste igualdade 10+15 =15
        self.assertEqual(calc.add(-1,1),0)
        self.assertEqual(calc.add(-1,-1),-2)
    
    def test_subtract(self):                 # all tests start with "test"    test_add test_ .... etc
        self.assertEqual(calc.subtract(10,5),5)  # teste igualdade 10+15 =15
        self.assertEqual(calc.subtract(-1,1),-2)
        self.assertEqual(calc.subtract(-1,-1),0)
        
    def test_multiply(self):                 # all tests start with "test"    test_add test_ .... etc
        self.assertEqual(calc.multiply(10,5),50)  # teste igualdade 10+15 =15
        self.assertEqual(calc.multiply(-1,1),-1)
        self.assertEqual(calc.multiply(-1,-1),1)
    
    def test_divide(self):                 # all tests start with "test"    test_add test_ .... etc
        self.assertEqual(calc.divide(10,5),2)  # teste igualdade 10+15 =15
        self.assertEqual(calc.divide(-1,1),-1)
        self.assertEqual(calc.divide(-1,-1),1)
        self.assertEqual(calc.divide(5,2),2.5)
        
        # self.assertRaises(ValueError, calc.divide, 10, 2) # (Value Error = Exception ; a funçao para testar; argument ; argument) 
        with self.assertRaises(ValueError):
            calc.divide(10,0)

if __name__ == '__main__': 
    unittest.main()