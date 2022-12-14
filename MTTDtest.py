import unittest
import MRTD
import sqlite3 
from unittest.mock import MagicMock,Mock

class decodeencodeTest(unittest.TestCase):

    ##This test method is used to test the decode function for line 1 and line 2   
    def testdecode(self):
        line='P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<;W620126G54CIV5910106F9707302AJ010215I<<<<<<6'
        self.assertEqual(MRTD.decode(line),'{"line1": {"issuing_country": "CIV", "last_name": "LYNN", "given_name": "NEVEAH BRAM"}, "line2": {"passport_number": "W620126G5", "country_code": "CIV", "birth_date": "591010", "sex": "F", "expiration_date": "970730", "personal_number": "AJ010215I"}}','Line 1 and line 2 decoded successfully')
    
    ##This test method is used to test the decode function containing country code
    def testdecode2(self):
        line='P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<;W620126G54RIS5910106F9707302AJ010215I<<<<<<6'
        self.assertEqual(MRTD.decode(line),1,'Differentcountrycode')

    ##This test method is used to check the extract1 function for line 1     
    def testfindval1(self):
        self.assertEqual(MRTD.extract1('P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<'),{'issuing_country': 'CIV', 'last_name':'LYNN', 'given_name': 'NEVEAH BRAM'},'Got Expected result2')
    
    ##This test method is used to check the extract function if no document is type give
    def testfindval2(self):
        self.assertEqual(MRTD.extract1('<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<'),1,'Got Expected exception')

    ##This test method is used to check the extract2 function for line 2    
    def testfindval3(self):
        self.assertEqual(MRTD.extract2("W620126G54CIV5910106F9707302AJ010215I<<<<<<6"),{'passport_number': 'W620126G5', 'country_code': 'CIV', 'birth_date': '591010', 'sex': 'F', 'expiration_date': '970730', 'personal_number': 'AJ010215I'},"Got ExpectedResult3")

    ##This test method is used to check the extract1 function if middle name is not given
    def testfindval4(self):
        self.assertEqual(MRTD.extract1('P<ABWMALDONADO<<CAMILLA<<<<<<<<<<<<<<<<<<<<<'),{'issuing_country': 'ABW', 'last_name':'MALDONADO', 'given_name': 'CAMILLA'},'Got Expected result2 if not given middle name')
        # added test case for the new fix as a part of performance testing. COndtion where middle name not given

    ##This test method is used to check the encode functionality for given data
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
    
    ##This test method is used to check the encodeLine1 functionality for given data
    def testencode1(self):
        data = {
                    "line": {
                        "issuing_country": "CIV",
                        "last_name": "LYNN",
                        "given_name": "NEVEAH BRAM"
                    }
        }
        self.assertEqual(MRTD.encodeLine1(data['line']),'P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<','Got Expected result5')

    ##This test method is used to check the encodeLine1 functionality if not provided any given name 
    def testencodeline1(self):
        data = {
                    "line": {
                        "issuing_country": "CIV",
                        "last_name": "LYNN",
                        "given_name": ""
                    }
        }
        self.assertEqual(MRTD.encodeLine1(data['line']),1,'Returns 1 if not given name')

    ##This test method is used to check the encodeLine1 functionality if not provided last name    
    def testencodeline2(self):
        data = {
                    "line": {
                        "issuing_country": "CIV",
                        "last_name": "",
                        "given_name": "NEVEAH BRAM"
                    }
        }
        self.assertEqual(MRTD.encodeLine1(data['line']),1,'returns 1 if not given last name')

    ##This test method is used to check the encodeLine1 functionality if not provided issuing country
    def testencodeline3(self):
        data = {
                    "line": {
                        "issuing_country": "",
                        "last_name": "LYNN",
                        "given_name": "NEVEAH BRAM"
                    }
        }
        self.assertEqual(MRTD.encodeLine1(data['line']),1,'Returns 1 if not given issuing country')

    ##This test method is used to check the encodeLine1 if none of the values are given for attributes
    def testencodeline4(self):
        data = {
                    "line": {
                        "issuing_country": "",
                        "last_name": "",
                        "given_name": ""
                    }
        }
        self.assertEqual(MRTD.encodeLine1(data['line']),1,'Returns 1 if no values are provided')
    
    ##This test method is used to check the encodeLine2 functionality if all the part 2 data is given
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

        self.assertEqual(MRTD.encodeLine2(data['line']),'W620126G54CIV5910106F9707302AJ010215I<<<<<<6','Returns encoded part 2 data')

    ##This test method is used to check the encodeLine2 functionality if not provided country code
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

        self.assertEqual(MRTD.encodeLine2(data['line']),1,'Returns 1 if country code is missing')
    
    ##This test method is used to check the encodeLine2 functionality and to kill mutants
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
    
    ##This test method is used to check the encodeLine2 functionality and to kill mutants
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

    ##This test method is used to check the encodeLine2 functionality and to kill mutants               
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

    ##This test method is used to check the encodeLine2 functionality and to kill mutants        
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

    ##This test method is used to check the scan passport return
    def testScan(self):
        self.assertEqual(MRTD.scanPassport(),'scanned','Scanned Successfully')
    
    ##This test method is used to check the extract2 function if passport check digit is improper
    def testPassportCheckDigit(self):
    	with self.assertRaises(ValueError):
    		MRTD.extract2('W620126G59CIV5910106F9707302AJ010215I<<<<<<6')
    
    ##This test method is used to check the extract2 function if birthday check digit is improper
    def testBirthdayCheckDigit(self):
    	with self.assertRaises(ValueError):
    		MRTD.extract2('W620126G54CIV5910105F9707302AJ010215I<<<<<<6')

    ##This test method is used to check the extract2 function if expiry date check digit is improper			
    def testExpirydateCheckDigit(self):
    	with self.assertRaises(ValueError):
    		MRTD.extract2('W620126G54CIV5910106F9707303AJ010215I<<<<<<6')
    
    ##This test method is used to check the extract2 function if personal number check digit is improper
    def testPersonalNumberCheckDigit(self):
    	with self.assertRaises(ValueError):
    		MRTD.extract2('W620126G54CIV5910106F9707302AJ010215I<<<<<<5')
    
    ##This test method is used to check the getCheckDigit function if it returns the given correct value
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
    ##This test method is used to check the getCheckDigit function if it returns the given correct value
    def testCheckDigit(self):
        self.assertEqual(MRTD.getCheckDigit(""), '0')
        self.assertEqual(MRTD.getCheckDigit("<<<<"), '0')
        self.assertEqual(MRTD.getCheckDigit("AB2134"), '5')
        self.assertNotEqual(MRTD.getCheckDigit("AB2134"), '3')

###Mock DAtabase here: # Entire DB mock to be commented before running the pylint check
class MockSqlite3Database(unittest.TestCase):

    ##Note this mock database code needs to be commented if you run Pylint
    ##This SqlLite mock works for python unittest
    ##Mocks database successful connection
    def test_sqlite3_success(self):

        sqlite3.connect = MagicMock(return_value='connection succeeded')

        dbc = DataBaseClass()
        sqlite3.connect.assert_called_with('test_database')
        self.assertEqual(dbc.connection,'connection succeeded')

    ##Mocks database failed connection
    def test_sqlite3_fail(self):

        sqlite3.connect = MagicMock(return_value='connection failed')

        dbc = DataBaseClass()
        sqlite3.connect.assert_called_with('test_database')
        self.assertEqual(dbc.connection, 'connection failed')

    ##Mocks assert true
    def test_sqlite3_connect_with_sideaffect(self):

        self._setup_mock_sqlite3_connect()

        dbc = DataBaseClass('good_connection_string')
        self.assertTrue(dbc.connection)
        sqlite3.connect.assert_called_with('good_connection_string')

        dbc = DataBaseClass('bad_connection_string')
        self.assertFalse(dbc.connection)
        sqlite3.connect.assert_called_with('bad_connection_string')

    ##Mocks assert false
    def _setup_mock_sqlite3_connect(self):

        values = {'good_connection_string':True,
                  'bad_connection_string':False}

        def side_effect(arg):
            return values[arg]

        sqlite3.connect = Mock(side_effect=side_effect)

class DataBaseClass():

    ##Innitiates database connection system
    def _init_(self,connection_string='test_database'):        
        self.connection = sqlite3.connect(connection_string)

if __name__ == '__main__':
   print('Running unit tests')
   unittest.main()