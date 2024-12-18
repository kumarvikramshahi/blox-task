# To confirm that the copied data is the same as the original data there are two ways that i can think of:-
# 1. Compare Data:- We can compare the original and migrated data row by row & column by column.
# 2. Compare Checksum:- We can use any hashing algo(say MD5 or SHA256) to generate checksum for each row of both original & migrated data, then compare them. if the checksum matched then row is properly copied else migrated row is affected.

# Below is implementation for same:-

# Original data in : list<dict<str, str>> form
originalTableData: list[dict[str, str]] = [
    {
        "id": 1,
        "name": "Alice",
        "state": "Kerala",
        "age": "25",
        "income": "50000",
        "father_name": "Rajesh",
        "occupation": "Software Engineer",
    },
    {
        "id": 2,
        "name": "Bob",
        "state": "Bihar",
        "age": "30",
        "income": "40000",
        "father_name": "Suresh",
        "occupation": "Teacher",
    },
    {
        "id": 3,
        "name": "Charlie",
        "state": "Maharashtra",
        "age": "40",
        "income": "60000",
        "father_name": "Anil",
        "occupation": "Doctor",
    },
    {
        "id": 4,
        "name": "David",
        "state": "Tamil Nadu",
        "age": "50",
        "income": "70000",
        "father_name": "Vikram",
        "occupation": "Businessman",
    },
    {
        "id": 5,
        "name": "Eva",
        "state": "Gujarat",
        "age": "30",
        "income": "55000",
        "father_name": "Ramesh",
        "occupation": "Nurse",
    },
    {
        "id": 6,
        "name": "Frank",
        "state": "Karnataka",
        "age": "60",
        "income": "80000",
        "father_name": "Kumar",
        "occupation": "Retired",
    },
    {
        "id": 7,
        "name": "Grace",
        "state": "Punjab",
        "age": "22",
        "income": "30000",
        "father_name": "Harjit",
        "occupation": "Student",
    },
    {
        "id": 8,
        "name": "Hannah",
        "state": "West Bengal",
        "age": "35",
        "income": "45000",
        "father_name": "Subhash",
        "occupation": "Accountant",
    },
    {
        "id": 9,
        "name": "Ivy",
        "state": "Uttar Pradesh",
        "age": "45",
        "income": "65000",
        "father_name": "Ajay",
        "occupation": "Engineer",
    },
    {
        "id": 10,
        "name": "Jack",
        "state": "Rajasthan",
        "age": "28",
        "income": "35000",
        "father_name": "Mohit",
        "occupation": "Marketing Executive",
    },
    {
        "id": 11,
        "name": "Mia",
        "state": "Andhra Pradesh",
        "age": "33",
        "income": "48000",
        "father_name": "Prakash",
        "occupation": "Data Analyst",
    },
    {
        "id": 12,
        "name": "Noah",
        "state": "Telangana",
        "age": "27",
        "income": "52000",
        "father_name": "Srinivas",
        "occupation": "Graphic Designer",
    },
]

# migrated data fetched to local from AWS/GCP assuming (MySQL) as DB
# below data in: list<tuple<str>>
# last 3 row's data are changes while copying
migratedTableData: list[tuple[str]] = [
    (1, "Alice", "Kerala", "25", "50000", "Rajesh", "Software Engineer"),
    (2, "Bob", "Bihar", "30", "40000", "Suresh", "Teacher"),
    (3, "Charlie", "Maharashtra", "40", "60000", "Anil", "Doctor"),
    (4, "David", "Tamil Nadu", "50", "70000", "Vikram", "Businessman"),
    (5, "Eva", "Gujarat", "30", "55000", "Ramesh", "Nurse"),
    (6, "Frank", "Karnataka", "60", "80000", "Kumar", "Retired"),
    (7, "Grace", "Punjab", "22", "30000", "Harjit", "Student"),
    (8, "Hannah", "West Bengal", "35", "45000", "Subhash", "Accountant"),
    (9, "Ivy", "Uttar Pradesh", "45", "65000", "Ajay", "Engineer"),
    (10, "Jacka", "Rajasthan", "28", "35000", "Mohit", "Marketing Executive"),
    (11, "Miaa", "Andhra Pradesh", "33", "48000", "Prakash", "Data Analyst"),
    (12, "Noaha", "Telangana", "27", "52000", "Srinivas", "Graphic Designer"),
]

# now comparing both original and migrated data using

# Method: 1 = Compare Data, row by row & column by column


def CompareByRow():
    # assuming data is sorted w.r.t id
    dataLength = len(originalTableData)
    unEqualRows = []
    for index in range(dataLength):
        tmpOriginal = originalTableData[index]
        tmpMigrated = migratedTableData[index]
        jdx = 0
        for key in tmpOriginal:
            if tmpOriginal[key] != tmpMigrated[jdx]:
                unEqualRows.append(tmpOriginal["id"])
                break
            jdx += 1

    print("Comparing by Data - row by row & column by column")
    for item in unEqualRows:
        print("row id: ", item)


# Method: 2 = Compare Checksum
import hashlib


def CompareByChecksum():
    # assuming data is sorted w.r.t id
    dataLength = len(originalTableData)
    unEqualRows = []
    rowStringMigrated = ""
    rowStringOriginal = ""
    for index in range(dataLength):
        tmpOriginal = originalTableData[index]
        for item in migratedTableData[index]:
            rowStringMigrated += str(item)
        # columns ordering are like: id, name, state, age, income, father_name, occupation
        rowStringOriginal += (
            str(tmpOriginal["id"])
            + tmpOriginal["name"]
            + tmpOriginal["state"]
            + tmpOriginal["age"]
            + tmpOriginal["income"]
            + tmpOriginal["father_name"]
            + tmpOriginal["occupation"]
        )
        hashOfOriginal = hashlib.md5(rowStringOriginal.encode()).hexdigest()
        hashOfMigrated = hashlib.md5(rowStringMigrated.encode()).hexdigest()
        if hashOfOriginal != hashOfMigrated:
            unEqualRows.append(tmpOriginal["id"])

    print("Comparing by Checksum")
    for item in unEqualRows:
        print("row id: ", item)


if __name__ == "__main__":
    print("Below rows id are affected while migrating data.")
    CompareByRow()
    CompareByChecksum()
