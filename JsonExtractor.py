
class JsonExtractor:
    """
    Computationally poor json string search. Searches through a string to find valid JSON(s) and returns any found in a list.
    """
    def __init__(self,toBeParsed):
        if type(toBeParsed) != str:
           raise TypeError
        self.data = toBeParsed

    def extractJson(self):
        #Iterates through data fed into class. Returns a list of jsons found in type string. If none found, list will be empty

        startIndex = 0
        temp = -1
        jsonFound = []
        while (temp != None):                                       #Repeats until none is returned from string
            temp,startIndex = self.search(startIndex)               #Searches through string for a json object, returns string containing json and index it ends at.
            if temp:
                jsonFound.append(temp)                              #Adds json string to list
        return jsonFound

    def search(self, startIndex):
        #Recieves start index in string. Goes through each char in string. Starts search at index startIndex. Returns json match string or nothing.
        lbCount = 0
        lbLocation = -1
        for index,letter in enumerate(self.data[startIndex:]):
            if letter == '{' and not lbCount and lbLocation == -1 and self.syntaxcorrect(index+startIndex):     #Checks to see if its the start of JSON
                lbLocation = index
            elif letter == '{' and lbLocation > -1:
                lbCount += 1                                                                                    #Increase left brace count
            elif letter == '}' and lbLocation > -1 and not lbCount:                                             #Checks to see if this is end of json syntax i.e No inner brace left to fulfill
                return self.data[lbLocation+startIndex:startIndex+index+1],startIndex+index+1                   #Returns json string and index in string it ends at
            elif letter == '}' and lbLocation > -1:
                lbCount -= 1                                                                                    #Decrements left brace
        return None,index                                                                                       #Nothing found

    def syntaxcorrect(self,startIndex):
        #Recieves start index in string. Lazily checks to see if this is correct json syntax. Checks to see if the format is two quatation marks and a colon. Returns boolean True if syntax is correct, or false if incorrect.
        amountToScan = 40
        if self.data[startIndex+1] != "\"":                                     #If no quotation follows { bracket then, we assume not json.
            return False
        elif amountToScan > len(self.data[startIndex + 1:]):                    #Checking for overflow
            raise OverflowError

        stringcount = 0
        for letter in self.data[startIndex + 1:startIndex + amountToScan]:      #Performing deeper syntax search, 2 quotations and colon needed within amountToScan
            if letter == "\"":
                stringcount += 1
            elif letter == ":":
                if stringcount == 2:
                    return True
            elif letter == "{" and stringcount != 2:
                return False