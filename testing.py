# Testing regular expressions
import re

print('--- Testing regular expressions. ---')
testString = 'Hey can someone take a look at INC0010003? It might be the same as REQ0010002. It could also just be SCTASK0010003.'
testString2 = 'This string has no results.'
result = re.findall(r'INC\d{7}|REQ\d{7}|RITM\d{7}|SCTASK\d{7}|KB\d{7}', testString)
result2 = re.findall(r'INC\d{7}|REQ\d{7}|RITM\d{7}|SCTASK\d{7}|KB\d{7}', testString2)

print(result)
print('Result length: ' + str(len(result)))
print(result2)
print('Result 2 length: ' + str(len(result2)))

print()
print()

# Testing iterating through an array with a for loop
print('--- Testing iterating through an array with a for loop. ---')
array = ['1','2','3']
for element in array:
    print(element)


def matchText(str):
        return re.findall(r'INC\d{7}|REQ\d{7}|RITM\d{7}|SCTASK\d{7}|KB\d{7}', str)        

print()
print()
print(matchText(testString))

testMessage = {
    "text": "Your boss has approved your travel request. Book any airline you like by continuing below.",
    "channel": "C061EG9SL",
    "attachments": [
        {
            "fallback": "Book your flights at https://flights.example.com/book/r123456",
            "actions": [
                {
                    "type": "button",
                    "text": "🎫 " + "Test 123",
                    "url": "https://flights.example.com/book/r123456"
                }
            ]
        }
    ]
}