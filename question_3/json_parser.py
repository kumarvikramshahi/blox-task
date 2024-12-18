# Below is implementation for JSON parser, below one is not working properly.
# tried implementing the functionaly with help of perplexity.ai
# but its taking time for me to complete


class JSONParseError(Exception):
    pass


def parseValue(jsonString, index):
    jsonString = jsonString.strip()
    if jsonString[index] == "{":
        return parseObject(jsonString, index)
    elif jsonString[index] == "[":
        return parseArray(jsonString, index)
    elif jsonString[index] == '"':
        return parseString(jsonString, index)
    elif jsonString[index].isdigit() or jsonString[index] == "-":
        return parseNumber(jsonString, index)
    elif jsonString.startswith("true", index):
        return True, index + 4
    elif jsonString.startswith("false", index):
        return False, index + 5
    elif jsonString.startswith("null", index):
        return None, index + 4
    else:
        raise JSONParseError(f"Unexpected character: {jsonString[index]}")


def parseObject(jsonString, index):
    obj = {}
    index += 1

    while True:
        jsonString = jsonString.strip()

        if index >= len(jsonString):
            raise JSONParseError("Unexpected end of string in object")

        if jsonString[index] == "}":
            return obj, index + 1

        key, index = parseString(jsonString, index)

        jsonString = jsonString.strip()

        if index >= len(jsonString) or jsonString[index] != ":":
            raise JSONParseError("Expected ':' after key")

        index += 1
        value, index = parseValue(jsonString, index)

        obj[key] = value

        jsonString = jsonString.strip()

        if index >= len(jsonString):
            raise JSONParseError("Unexpected end of string in object")

        if jsonString[index] == "}":
            return obj, index + 1
        elif jsonString[index] != ",":
            raise JSONParseError("Expected ',' or '}'")

        index += 1


def parseArray(jsonString, index):
    arr = []
    index += 1

    while True:
        jsonString = jsonString.strip()

        if index >= len(jsonString):
            raise JSONParseError("Unexpected end of string in array")

        if jsonString[index] == "]":
            return arr, index + 1

        value, index = parseValue(jsonString, index)
        arr.append(value)

        jsonString = jsonString.strip()

        if index >= len(jsonString):
            raise JSONParseError("Unexpected end of string in array")

        if jsonString[index] == "]":
            return arr, index + 1
        elif jsonString[index] != ",":
            raise JSONParseError("Expected ',' or ']'")

        index += 1


def parseString(jsonString, index):
    endIndex = index + 1
    while endIndex < len(jsonString):
        if jsonString[endIndex] == '"':
            return jsonString[index + 1 : endIndex], endIndex + 1
        elif jsonString[endIndex] == "\\":
            endIndex += 2
            continue
        endIndex += 1
    raise JSONParseError("Unterminated string")


def parseNumber(jsonString, index):
    endIndex = index
    while endIndex < len(jsonString) and (
        jsonString[endIndex].isdigit()
        or jsonString[endIndex] in ["-", "+", ".", "e", "E"]
    ):
        endIndex += 1

    numberStr = jsonString[index:endIndex]

    if "." in numberStr or "e" in numberStr or "E" in numberStr:
        return float(numberStr), endIndex

    return int(numberStr), endIndex


def parseJson(jsonInput):
    jsonInput = jsonInput.strip()

    if not jsonInput:
        raise JSONParseError("Empty string")

    value, nextIndex = parseValue(jsonInput, 0)

    if nextIndex != len(jsonInput):
        raise JSONParseError("Extra data after valid JSON")

    return value


jsonData = '{"name": "Alice", "age": 30, "is_student": false, "courses": ["Math", "Science"], "address": {"city": "Wonderland"}}'
parsedData = parseJson(jsonData)
print(parsedData)
