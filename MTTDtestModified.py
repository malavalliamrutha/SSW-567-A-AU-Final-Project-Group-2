import unittest
#from unittest import TestCase
from MRTDModified import decode
from MRTDModified import encode
from MRTDModified import encodeLine1
from MRTDModified import encodeLine2
from MRTDModified import getCheckDigit
from MRTDModified import extract1
from MRTDModified import extract2

class decodeencodeTest(unittest.TestCase):
    
   
    def testdecode(self):
        line='P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<;W620126G54CIV5910106F9707302AJ010215I<<<<<<6'
        self.assertEqual(decode(line),'{"line1": {"issuing_country": "CIV", "last_name": "LYNN", "given_name": "NEVEAH BRAM"}, "line2": {"passport_number": "W620126G5", "country_code": "CIV", "birth_date": "591010", "sex": "F", "expiration_date": "970730", "personal_number": "AJ010215I"}}','ExpectedResult3')

    def testfindval1(self):
        self.assertEqual(extract1('P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<'),{'issuing_country': 'CIV', 'last_name':'LYNN', 'given_name': 'NEVEAH BRAM'},'Got Expected result2')
    
    def testfindval2(self):
        self.assertEqual(extract1('<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<'),1,'Got Expected exception')
        
    def testfindval3(self):
        self.assertEqual(extract2("W620126G54CIV5910106F9707302AJ010215I<<<<<<6"),{'passport_number': 'W620126G5', 'country_code': 'CIV', 'birth_date': '591010', 'sex': 'F', 'expiration_date': '970730', 'personal_number': 'AJ010215I'},"Got ExpectedResult3")


    def testencode(self):
        data = {
                    "line1": {
                        "issuing_country": "CIV",
                        "last_name": "LYNN",
                        "given_name": "NEVEAH BRAM"
                    },
                    "line2": {
                        "passport_number": "W620126G5",
                        "country_code": "CIV",
                        "birth_date": "591010",
                        "sex": "F",
                        "expiration_date": "970730",
                        "personal_number": "AJ010215I"
                    }
        }  
        self.assertEqual(encode(data),'P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<;W620126G54CIV5910106F9707302AJ010215I<<<<<<6','Got Expected result4')
        
    def testencode1(self):
        data = {
                    "line": {
                        "issuing_country": "CIV",
                        "last_name": "LYNN",
                        "given_name": "NEVEAH BRAM"
                    }
        }
        self.assertEqual(encodeLine1(data['line']),'P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<','Got Expected result5')
      


    def testencode2(self):
        data = {
                    "line": {
                        "passport_number": "W620126G5",
                        "country_code": "CIV",
                        "birth_date": "591010",
                        "sex": "F",
                        "expiration_date": "970730",
                        "personal_number": "AJ010215I"
             }
        }

        self.assertEqual(encodeLine2(data['line']),'W620126G54CIV5910106F9707302AJ010215I<<<<<<6','Got Expected result6')

    def testencode3(self):
        data = {
                    "line": {
                        "passport_number": "W620126G5",
                        "country_code": "",
                        "birth_date": "591010",
                        "sex": "F",
                        "expiration_date": "970730",
                        "personal_number": "AJ010215I"
             }
        }

        self.assertEqual(encodeLine2(data['line']),1,'Exception Expected')


    def testgetCheckDigit(self):
        passportNumber="W620126G5"
        birthdate="591010"
        expiry="970730"
        personal_number="AJ010215I"
        self.assertEqual(getCheckDigit(passportNumber),'4','success')
        self.assertEqual(getCheckDigit(birthdate),'6','success')
        self.assertEqual(getCheckDigit(expiry),'2','success')
        self.assertEqual(getCheckDigit(personal_number),'6','success')   

class testCheckDigit(unittest.TestCase):
    def testCheckDigit(self):
        self.assertEqual(getCheckDigit(""), '0')
        self.assertEqual(getCheckDigit("<<<<"), '0')
        self.assertEqual(getCheckDigit("AB2134"), '5')
        self.assertNotEqual(getCheckDigit("AB2134"), '3')
        self.assertEqual(getCheckDigit("1"), '7')
                   
if __name__ == '__main__':
   print('Running unit tests')
   unittest.main()
   