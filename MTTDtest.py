import unittest
import MRTD

class decodeencodeTest(unittest.TestCase):
       
    def testdecode(self):
        line='P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<;W620126G54CIV5910106F9707302AJ010215I<<<<<<6'
        self.assertEqual(MRTD.decode(line),'{"line1": {"issuing_country": "CIV", "last_name": "LYNN", "given_name": "NEVEAH BRAM"}, "line2": {"passport_number": "W620126G5", "country_code": "CIV", "birth_date": "591010", "sex": "F", "expiration_date": "970730", "personal_number": "AJ010215I"}}','ExpectedResult3')
    
    def testdecode2(self):
        line='P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<;W620126G54RIS5910106F9707302AJ010215I<<<<<<6'
        self.assertEqual(MRTD.decode(line),1,'Differentcountrycode')
        
    def testfindval1(self):
        self.assertEqual(MRTD.extract1('P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<'),{'issuing_country': 'CIV', 'last_name':'LYNN', 'given_name': 'NEVEAH BRAM'},'Got Expected result2')
    
    def testfindval2(self):
        self.assertEqual(MRTD.extract1('<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<'),1,'Got Expected exception')
        
    def testfindval3(self):
        self.assertEqual(MRTD.extract2("W620126G54CIV5910106F9707302AJ010215I<<<<<<6"),{'passport_number': 'W620126G5', 'country_code': 'CIV', 'birth_date': '591010', 'sex': 'F', 'expiration_date': '970730', 'personal_number': 'AJ010215I'},"Got ExpectedResult3")

    def testfindval4(self):
        self.assertEqual(MRTD.extract1('P<ABWMALDONADO<<CAMILLA<<<<<<<<<<<<<<<<<<<<<'),{'issuing_country': 'ABW', 'last_name':'MALDONADO', 'given_name': 'CAMILLA'},'Got Expected result2 if not given middle name')
        # added test case for the new fix as a part of performance testing. COndtion where middle name not given

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
        self.assertEqual(MRTD.encode(data),'P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<;W620126G54CIV5910106F9707302AJ010215I<<<<<<6','Got Expected result4')
        
    def testencode1(self):
        data = {
                    "line": {
                        "issuing_country": "CIV",
                        "last_name": "LYNN",
                        "given_name": "NEVEAH BRAM"
                    }
        }
        self.assertEqual(MRTD.encodeLine1(data['line']),'P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<','Got Expected result5')

    def testencodeline1(self):
        data = {
                    "line": {
                        "issuing_country": "CIV",
                        "last_name": "LYNN",
                        "given_name": ""
                    }
        }
        self.assertEqual(MRTD.encodeLine1(data['line']),1,'Got Expected result5')
        
    def testencodeline2(self):
        data = {
                    "line": {
                        "issuing_country": "CIV",
                        "last_name": "",
                        "given_name": "NEVEAH BRAM"
                    }
        }
        self.assertEqual(MRTD.encodeLine1(data['line']),1,'Got Expected result5')

    def testencodeline3(self):
        data = {
                    "line": {
                        "issuing_country": "",
                        "last_name": "LYNN",
                        "given_name": "NEVEAH BRAM"
                    }
        }
        self.assertEqual(MRTD.encodeLine1(data['line']),1,'Got Expected result5')

    def testencodeline4(self):
        data = {
                    "line": {
                        "issuing_country": "",
                        "last_name": "",
                        "given_name": ""
                    }
        }
        self.assertEqual(MRTD.encodeLine1(data['line']),1,'Got Expected result5')
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

        self.assertEqual(MRTD.encodeLine2(data['line']),'W620126G54CIV5910106F9707302AJ010215I<<<<<<6','Got Expected result6')

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

        self.assertEqual(MRTD.encodeLine2(data['line']),1,'Exception Expected')
    def testencode4(self):#added new
        data = {
                    "line": {
                        "passport_number": "W620126G5",
                        "country_code": "CIV",
                        "birth_date": "591010",
                        "sex": "F",
                        "expiration_date": "970730",
                        "personal_number": "mutpy"
             }
        }

        self.assertEqual(MRTD.encodeLine2(data['line']),'W620126G54CIV5910106F9707302mutpy<<<<<<<<<<0','Got Expected result6')
    
    def testencode5(self):#added new
        data = {
                    "line": {
                        "passport_number": "W620126G5",
                        "country_code": "CIV",
                        "birth_date": "591010",
                        "sex": "F",
                        "expiration_date": "mutpy",
                        "personal_number": "AJ010215I"
             }
        }

        self.assertEqual(MRTD.encodeLine2(data['line']),'W620126G54CIV5910106Fmutpy0AJ010215I<<<<<<<6','Got Expected result6')
                   
    def testencode6(self):#added new
        data = {
                    "line": {
                        "passport_number": "W620126G5",
                        "country_code": "CIV",
                        "birth_date": "591010",
                        "sex": "mutpy",
                        "expiration_date": "970730",
                        "personal_number": "AJ010215I"
             }
        }

        self.assertEqual(MRTD.encodeLine2(data['line']),'W620126G54CIV5910106mutpy9707302AJ010215I<<6','Got Expected result6')
            
    def testencode7(self):#added new
        data = {
                    "line": {
                        "passport_number": "W620126G5",
                        "country_code": "CIV",
                        "birth_date": "591010",
                        "sex": "mutpy",
                        "expiration_date": "970730",
                        "personal_number": "AJ010215I"
             }
        }

        self.assertEqual(MRTD.encodeLine2(data['line']),'W620126G54CIV5910106mutpy9707302AJ010215I<<6','Got Expected result6')
        
    def testScan(self):
        self.assertEqual(MRTD.scanPassport(),'scanned','Scanned Successfully')
    
    def testPassportCheckDigit(self):
    	with self.assertRaises(ValueError):
    		MRTD.extract2('W620126G59CIV5910106F9707302AJ010215I<<<<<<6')
    
    def testBirthdayCheckDigit(self):
    	with self.assertRaises(ValueError):
    		MRTD.extract2('W620126G54CIV5910105F9707302AJ010215I<<<<<<6')
    			
    def testExpirydateCheckDigit(self):
    	with self.assertRaises(ValueError):
    		MRTD.extract2('W620126G54CIV5910106F9707303AJ010215I<<<<<<6')
    
    def testPersonalNumberCheckDigit(self):
    	with self.assertRaises(ValueError):
    		MRTD.extract2('W620126G54CIV5910106F9707302AJ010215I<<<<<<5')
    
    def testgetCheckDigit(self):
        passportNumber="W620126G5"
        birthdate="591010"
        expiry="970730"
        personal_number="AJ010215I"
        self.assertEqual(MRTD.getCheckDigit(passportNumber),'4','success')
        self.assertEqual(MRTD.getCheckDigit(birthdate),'6','success')
        self.assertEqual(MRTD.getCheckDigit(expiry),'2','success')
        self.assertEqual(MRTD.getCheckDigit(personal_number),'6','success')   

class testCheckDigit(unittest.TestCase):
    def testCheckDigit(self):
        self.assertEqual(MRTD.getCheckDigit(""), '0')
        self.assertEqual(MRTD.getCheckDigit("<<<<"), '0')
        self.assertEqual(MRTD.getCheckDigit("AB2134"), '5')
        self.assertNotEqual(MRTD.getCheckDigit("AB2134"), '3')
        self.assertEqual(MRTD.getCheckDigit("1"), '7')
                                   
if __name__ == '__main__':
   print('Running unit tests')
   unittest.main()