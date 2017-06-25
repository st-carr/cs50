import time

def main():
    ccNum = input("Enter a CC number: ")
    hans = hansLuhn(ccNum)

    if hans == True:
        print("This is a CC")
        company = getCompany(ccNum)
        print(company)
    else:
        print("This is not a CC")

def getCompany(cc):
    if int(cc[0]) == 5 and int(cc[1]) == 1 or int(cc[1]) == 2 or int(cc[1]) == 3 or int(cc[1]) == 4 or int(cc[1]) == 5:
        return "MasterCard"
    elif int(cc[0]) == 4:
        return "Visa"
    elif int(cc[0]) == 3 and int(cc[1]) == 4 or int(cc[1]) == 7:
        return "American Express"




def hansLuhn(cc):
    ytotal = tempInt = xtotal = 0
    index = len(cc) - 1
    start = False
    tempStr = ""
    for x in range(index-1, -1, -2):
        xtemp = int(cc[x])
        xtemp = xtemp * 2
        if xtemp > 9:
            tempStr = str(xtemp)
            for y in range(len(tempStr)):
                tempInt = tempStr[y]
                xtotal += int(tempInt)
        else:
            xtotal += xtemp

    for y in range(index, -1, -2):
        ytemp = int(cc[y])
        ytotal += ytemp

    total = xtotal + ytotal
    if (total) % 10 == 0:
        return True
    else:
        return False





    
if __name__ == "__main__":
    main()