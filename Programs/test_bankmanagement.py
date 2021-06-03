import unittest
import bankmanagement

class TestBM(unittest.TestCase):
    def test_show_records(self):
        result=bankmanagement.show_records()
        self.assertEqual(result,4)
    def test_registration(self):
        result=bankmanagement.registration()
        self.assertEqual(result,"Correct")
    def test_login(self):
        result=bankmanagement.registration()
        self.assertFalse(result,False)