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
        product = charToValue(char) * weights[idx % 3]
        sum += product
    result = sum % 10
    result = str(result)
    #print(result)
    return result

# print (getCheckDigit("L898902C3"))
def scanPassport():
    #empty method
    return 'scanned'
    
def extract1(line):
    firstvalue = 1
    secondvalue = 2
    thirdvalue = 3
    val=line.split('<')
    res=[]
    for i in val:
        if i.strip():
            res.append(i)
    doctype = res[0]
    if (doctype != "P"):
        return 1
    countrycode = res[firstvalue][:thirdvalue]
    lastName = res[firstvalue][thirdvalue:]
    firstName = res[secondvalue]
    middleName = res[thirdvalue]
    givenName = firstName + " " + middleName
    
    line1 = {
        "issuing_country": countrycode,
        "last_name": lastName,
        "given_name": givenName
    }
    return line1
    
def extract2(line):
    initiallocation = 0
    passportendlocation = 9
    countrycodestartlocation = 10
    countrycodeendlocation = 13
    birthdateendlocation = 19
    birthdatechecklocation = 20
    expirydatestartlocation = 21
    expirydateendlocation = 27
    personalNumberstartlocation = 28
    personalNumberChecklocation = 1
    val=line.split('<')
    res=[]
    for i in val:
        if i.strip():
            res.append(i)
    passportNumber = res[initiallocation][:passportendlocation]
    passportNumbercheckdigit = res[initiallocation][passportendlocation]
    countryCode = res[initiallocation][countrycodestartlocation:countrycodeendlocation]
    birthdate = res[initiallocation][countrycodeendlocation:birthdateendlocation]
    birthdatecheckdigit = res[initiallocation][birthdateendlocation:birthdatechecklocation]
    sex = res[initiallocation][birthdatechecklocation]
    expirydate = res[initiallocation][expirydatestartlocation:expirydateendlocation]
    expirydatecheckdigit = res[initiallocation][expirydateendlocation]
    personalNumber = res[initiallocation][personalNumberstartlocation:]
    personalNumberCheck = res[personalNumberChecklocation]
    if (getCheckDigit(passportNumber) != passportNumbercheckdigit):
        raise ValueError("Passport Error")
    if (getCheckDigit(birthdate) != birthdatecheckdigit):
        raise ValueError("Birthday Error")
    if (getCheckDigit(expirydate) != expirydatecheckdigit):
        raise ValueError("expirydate  Error")
    if (getCheckDigit(personalNumber) != personalNumberCheck):
        raise ValueError("personalNumber Error")
    
    line2 = {
        "passport_number": passportNumber,
        "country_code": countryCode,
        "birth_date": birthdate,
        "sex": sex,
        "expiration_date": expirydate,
        "personal_number": personalNumber
    }
    return line2
    	
def decode(string):
    #takes string and parses it
    #returns data in same format as records_decoded if the string is valid, prints an error and returns false if there is an issue
    lines = string.split(";")
    line1 = extract1(lines[0])
    line2 = extract2(lines[1])
    if not (line1["issuing_country"] == line2['country_code']):
        return 1
    result = {"line1":line1, "line2":line2}
    result = json.dumps(result)
    #print("resultis: " + result)
    return result
   
def encodeLine1(data):
    #accepts dict of line1 data and generates a string
    line = "P<"
    countryCode = data['issuing_country']
    lastName = data['last_name']
    givenName = data['given_name']
    if not(countryCode):
        return 1
    if not(lastName):
        return 1
    if not(givenName):
        return 1
    
    givenName = givenName.replace(" ", "<")
    line = f'{line}{countryCode}{lastName}<<{givenName}'
    lineLength = 44
    #if (lineLength > 44):
     #   print('line is too long')
        #todo: what happens now?
    #else:
    for i in range(len(line),lineLength):
        line += "<"
    #print(line)        
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
    try:
        if not passportNumber or not passportNumberCheck or not countryCode or not birthday or not birthdayCheck or not sex or not expire or not expireCheck or not personalNumber or not personalNumberCheck:
            raise Exception
        else:    
            line += passportNumber + passportNumberCheck + countryCode + birthday + birthdayCheck + sex + expire + expireCheck + personalNumber
            for i in range(len(line), 43):
                line += "<"
            line += personalNumberCheck
            #print(line)
            return line
    except Exception:
        print("Inside Exception")
        return 1
    
def encode (data):
    #takes in json object and generates a string for the MRZ
    line1 = encodeLine1(data['line1'])
    line2 = encodeLine2(data['line2'])
    result = line1 + ";" + line2
    #print(result)
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