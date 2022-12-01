import json
def charToValue(char):
    #returns numeric value for input char used in check digit algorithm
    charDict = {
        '<':0,
        '0':0,
        '1':1,
        '2':2,
        '3':3,
        '4':4,
        '5':5,
        '6':6,
        '7':7,
        '8':8,
        '9':9,
        'a':10,
        'b':11,
        'c':12,
        'd':13,
        'e':14,
        'f':15,
        'g':16,
        'h':17,
        'i':18,
        'j':19,
        'k':20,
        'l':21,
        'm':22,
        'n':23,
        'o':24,
        'p':25,
        'q':26,
        'r':27,
        's':28,
        't':29,
        'u':30,
        'v':31,
        'w':22,
        'x':33,
        'y':34,
        'z':35,
    }
    char = char.lower();
    return charDict[char]
    

def getCheckDigit(input):
    #takes string of alphanumeric characters and returns check digit
    sum = 0
    weights = [7,3,1]
    for idx, char  in enumerate(input):
        product = weights[idx % 3] * charToValue(char)
        sum += product
    result = sum % 10
    result = str(result)
    return result

# print (getCheckDigit("L898902C3"))
def scanPassport():
    #empty method
    return
def findNth(string, substring, n):
    parts = string.split(substring, n + 1)
    if len(parts) <= n + 1:
        return -1
    return len(string) - len(parts[-1]) - len(substring)

def extractLine1(line):
    #define breakpoints
    endOfLastName = findNth(line,"<",1)
    endOfFirstName =  findNth(line,"<",3)
    endOfMiddleName =  findNth(line,"<",4)
    #get data
    documentType = line[0]
    countryCode = line[2:5]
    lastName = line[5:endOfLastName]
    firstName = line[endOfLastName+2:endOfFirstName]
    middleName = line[endOfFirstName+1:endOfMiddleName]
  
    givenName = firstName + " " + middleName
    
    #check first digit is P
    if not (documentType == "P"):
        print ("Document Code is not P for passport")
    #check if name is complete
    if not(givenName):
        print ("first name is missing")
    if not(lastName):
        print("Name is not complete")
    #format and return dict
    line1 = {
        "issuing_country": countryCode,
        "last_name": lastName,
        "given_name": givenName
    }
    return line1

def extractLine2(line):
    #takes second line, decodes and returns a dict with all the information
    #define breakpoints
    passportCheckLocation = 9
    birthDayCheckLocation = 19
    sexLocation = 20
    expireCheckLocation = 27

    #get data
    passportNumber = line[:passportCheckLocation]
    passportCheckDigit = line[passportCheckLocation]
    countryCode = line[passportCheckLocation + 1:passportCheckLocation+4]
    birthDay = line[birthDayCheckLocation - 6:birthDayCheckLocation]
    birthDayCheck = line[birthDayCheckLocation]
    sex = line[sexLocation]
    expire = line[expireCheckLocation - 6:expireCheckLocation]
    expireCheck = line[expireCheckLocation]
    personalNumber = line[expireCheckLocation+1:-1]
    personalNumberCheck = line[-1:]
    #strip < off of personal number
    personalNumber = personalNumber[:findNth(personalNumber,"<",0)]
  
    #check check digits
    if not(getCheckDigit(passportNumber) == passportCheckDigit):
        correctDigit  = getCheckDigit(passportNumber)
        print(f"Passport number check digit is wrong: got {passportCheckDigit}, but expected {correctDigit}")
    if not(getCheckDigit(birthDay) == birthDayCheck):
        correctDigit  = getCheckDigit(birthDay)
        print(f"Passport number check digit is wrong: got {birthDayCheck}, but expected {correctDigit}")
    if not(getCheckDigit(expire) == expireCheck):
        correctDigit  = getCheckDigit(expire)
        print(f"Passport number check digit is wrong: got {expireCheck}, but expected {correctDigit}")
    if not(getCheckDigit(personalNumber) == personalNumberCheck):
        correctDigit  = getCheckDigit(personalNumber)
        print(f"Passport number check digit is wrong: got {expireCheck}, but expected {correctDigit}")
    result = {
        "passport_number": passportNumber,
        "country_code": countryCode,
        "birth_date": birthDay,
        "sex": sex,
        "expiration_date": expire,
        "personal_number": personalNumber
    }
    return result

def decode(string):
    #takes string and parses it
    #returns data in same format as records_decoded if the string is valid, prints an error and returns false if there is an issue
    lines = string.split(";")
    line1 = extractLine1(lines[0])
    line2 = extractLine2(lines[1])
    if not (line1["issuing_country"] == line2['country_code']):
        print("country codes don't match")
    result = {"line1":line1, "line2":line2}
    result = json.dumps(result)
    # print(result)
    return result
   
def encodeLine1(data):
    #accepts dict of line1 data and generates a string
    line = "P<"
    countryCode = data['issuing_country']
    lastName = data['last_name']
    givenName = data['given_name']
    if not(countryCode):
        print('issuing country is not supplied in i line 1')
    if not(lastName):
        print("last name is not supplied in line 1")
    if not(givenName):
        print('given name was not provided')
    
    givenName = givenName.replace(" ", "<")
    line += countryCode + lastName + "<<" + givenName;
    lineLength = 44
    if (lineLength > 44):
        print('line is too long')
        #todo: what happens now?
    else:
        for i in range(len(line),44):
            line += "<"
    return line
def encodeLine2(data):
    #accepts dict of line2 data and generates a MRZ string;
    line = ""
    passportNumber = data['passport_number']
    passportNumberCheck = getCheckDigit(passportNumber)
    countryCode = data['country_code']
    birthday = data['birth_date']
    birthdayCheck = getCheckDigit(birthday)
    expire = data['expiration_date']
    expireCheck = getCheckDigit(expire)
    sex = data['sex']
    personalNumber = data['personal_number']
    personalNumberCheck =getCheckDigit(personalNumber)
    line += passportNumber + passportNumberCheck + countryCode + birthday + birthdayCheck + sex + expire + expireCheck + personalNumber
    if len(line) > 43:
        print("line is too long")
        #todo: what happens now? is it even possible to be too long
    else:
        for i in range(len(line), 43):
            line += "<"
    line += personalNumberCheck
    return line
def encode (data):
    #takes in json object and generates a string for the MRZ
    line1 = encodeLine1(data['line1'])
    line2 = encodeLine2(data['line2'])
    result = line1 + ";" + line2
    # print(result)
    return result



line1 = "P<CIVLYNN<<NEVEAH<BRAM<<<<<<<<<<<<<<<<<<<<<<;W620126G54CIV5910106F9707302AJ010215I<<<<<<6"
decode(line1)

rawData = {
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
encode(rawData)


#todo: add data validation