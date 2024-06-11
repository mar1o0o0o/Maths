from math import sqrt as sqrt

def getFactor():
    print("Your factor should be of the form ax^2 + bx + c. 0-degree factors (where a = 0, b = 0 and c =/= 0) will not be specified (in the case of negative constants, the sign of the inequality will be flipped).")
    while True:
        try:
            coefficients = [float(input("a = ")), float(input("b = ")), float(input("c = "))]
            break
        except TypeError:
            print("Enter a numeric value for the coefficients.")
    if coefficients[0] == 0 and coefficients[1] == 0 and coefficients[2] < 0:
        return coefficients, True
    else:
        return coefficients, False

def main():
    print("""Enter the sign of the inequality:
      1 - >   (greater)
      2 - <   (less than)
      3 - >=  (greater or equal)
      4 - <=  (less than or equal)""")
    sign = input()
    while sign not in ("1", "2", "3", "4"):
        print("Enter a choice between 1 and 4!")
        sign = input()
    if sign in ("3", "4"): noZeroes = False
    else: 
        noZeroes = True
        bannedValues = []
    print("Insert factors, then enter all 0s to continue.")

    arrFactors = []
    inequalityString = ""
    originalSign = sign
    factor, changeSign = getFactor()
    while factor != [0,0,0]:
        if changeSign:
            if sign == "1": sign = "2"
            elif sign == "2": sign = "1"
            elif sign == "3": sign = "4"
            else: sign = "3"
        if factor[0] != 0 or factor[1] != 0:
            # writing the expression down
            inequalityString += "("
            if factor[0] != 0: 
                if factor[0] == -1: inequalityString += "-"
                elif factor[0] != 1: inequalityString += str(factor[0])
                inequalityString += "x^2"
            if factor[1] > 0:
                if factor[0] != 0: inequalityString += " +"
                if factor[1] != 1: inequalityString += str(factor[1])
                inequalityString += "x"
            elif factor[1] < 0: 
                if factor[0] != 0: inequalityString += " "
                if factor[1] == -1: inequalityString += "-"
                else: inequalityString += str(factor[1])
                inequalityString += "x"
            if factor[2] > 0: 
                if factor[1] != 0 or (factor[1] == 0 and factor[0] != 0): inequalityString += " +"
                inequalityString += str(factor[2])
            elif factor[2] < 0:
                if factor[1] != 0 or (factor[1] == 0 and factor[0] != 0): inequalityString += " "
                if factor[1] == -1: inequalityString += "-"
                else: inequalityString += str(factor[2])
            inequalityString += ")"

            trinomial = []
            if factor[0] == 0:
                trinomial = [factor]
            else:
                delta = factor[1]**2 - 4*factor[0]*factor[2]
                if delta < 0 and factor[0] < 0:
                    if sign == "1": sign = "2"
                    elif sign == "2": sign = "1"
                    elif sign == "3": sign = "4"
                    else: sign = "3"
                elif delta == 0 and noZeroes:
                    bannedValues.append(-factor[1]/(2*factor[0]))
                elif delta > 0:
                    if factor[0] < 0:
                        if sign == "1": sign = "2"
                        elif sign == "2": sign = "1"
                        elif sign == "3": sign = "4"
                        else: sign = "3"
                        factor[0] = -factor[0]
                        factor[1] = -factor[1]
                        factor[2] = -factor[2]
                    trinomial = [[0,1,(factor[1]+sqrt(delta))/(2*factor[0])],[0,1,(factor[1]-sqrt(delta))/(2*factor[0])]]
                    
            for factor in trinomial:
                if factor in arrFactors: 
                    arrFactors.remove(factor)
                    if noZeroes: bannedValues.append(-factor[2]/factor[1])
                else:
                    arrFactors.append(factor)
        factor, changeSign = getFactor()
    if sign != originalSign:
        inequalityString = "-" + inequalityString
    print("\nYour inequality is: ")
    print(inequalityString, end = "")
    if originalSign == "1": print(" > 0")
    elif originalSign == "2": print(" < 0")
    elif originalSign == "3": print(" >= 0")
    else: print(" <= 0")

    singleSolutions = []
    for i in arrFactors:
        if i[1] < 0: singleSolutions.append([-i[2]/i[1], 0]) # 0 is for pos-left values, 1 is for pos-right
        else: singleSolutions.append([-i[2]/i[1], 1])

    roots = []            
    for i in singleSolutions: roots.append(i[0])
    roots.sort()  # looks like [root1, root2, root3, ..., rootn] where roots are ordered

    spaces = []
    for i in range(0, len(roots)+1): spaces.append(1) # [-inf spaces[0] root1 spaces[1] ... rootn spaces[n+1] +inf]

    for i in singleSolutions:
        if i[1] == 0:
            for j in range(roots.index(i[0])+1, len(spaces)):
                spaces[j] *= -1
        else:
            for j in range(0, roots.index(i[0])+1):
                spaces[j] *= -1

    if sign in ("1", "3"): searchedValue = 1
    else: searchedValue = -1

    if noZeroes: equal = ""
    else: equal = "="

    roots.insert(0, "-inf")
    roots.append("+inf")

    print("\nThe solution is: ")
    c = 0
    printOr = False
    intervals = 0
    while c < len(spaces):
        if printOr: 
            print(" or ", end = "")
            printOr = False
        if spaces[c] == searchedValue:
            leftLimit = roots[c]
            try:
                while spaces[c+1] == searchedValue and c < len(spaces)-1:
                    c += 1
            except IndexError:
                pass
            rightLimit = roots[c+1]
            if leftLimit == "-inf" and rightLimit == "+inf":
                print("R", end="")
            elif leftLimit == "-inf":
                print("x < " + str(rightLimit), end="")
            elif rightLimit == "+inf":
                print("x > " + str(leftLimit), end="")
            else:
                print(str(leftLimit) + " <" + equal + " x <" + equal + " " + str(rightLimit), end="")
            intervals += 1
            printOr = True
        c += 1
    if intervals == 0:
        print("Impossible")
        return
    if noZeroes and bannedValues != []:
        bannedValues.sort()
        for i in bannedValues:
            while bannedValues.count(i) != 1:
                bannedValues.remove(i)
        print(", x ≠ ", end="")
        for i in range(0, len(bannedValues)):
            if i != len(bannedValues)-1:
                print(bannedValues[i], end=", ")
            else:
                print(bannedValues[i])
    return


main()