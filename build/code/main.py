# Author : Alexandre Dossin

import graph, simplePaths, inputWithLegs, inputWithoutLegs
import time, pickle, random
import sys

def main():

    numberOfCustomersList = [1]
    numberOfDepotsList = [2]
    droneAutonomyList = [45]
    timeWindowsList = ["tight50"]

    for numberOfCustomersItr in numberOfCustomersList:
        for droneAutonomyItr in droneAutonomyList:
            for timeWindowsTypeItr in timeWindowsList:
                for numberOfDepotsItr in numberOfDepotsList:

                    random.seed(123)  # useful for debugging purposes - leave as "123"
                    maxDistance = 5000  # in meters
                    numberOfCustomers = numberOfCustomersItr
                    numberOfDepots = numberOfDepotsItr
                    droneAutonomy = droneAutonomyItr  # in minutes
                    timeWindowsType = timeWindowsTypeItr  # user-defined time windows in minutes
                    print('Time windows type : ', timeWindowsType)
                    print('Autonomy : ', droneAutonomy)
                    droneSpeed = 666  # in meters per minute (666 m/min -> 40 km/h)

                    if "tight" in timeWindowsType:
                        timeWindows = simplePaths.buildTimeWindows(numberOfDepots, tightTW=True, TWspacing=int(timeWindowsType[5:]))
                    elif timeWindowsType == "random":
                        timeWindows = simplePaths.buildTimeWindows(numberOfDepots, randomTW=True)
                    elif timeWindowsType == "separated":
                        timeWindows = simplePaths.buildTimeWindows(numberOfDepots, separatedTW=True)
                    else:
                        raise ValueError("Time windows not specified.")

                    if numberOfCustomers >= 1 and numberOfDepots >= 1:
                        g = graph.buildGraph(numberOfCustomers, numberOfDepots, maxDistance, timeWindows)  # building a random graph
                        pickle.dump(g, open("../temp/graph.p", "wb"))
                    else:
                        raise ValueError("The network must have at least 1 customer and 1 depot.")

                    #print(g)

                    #allSimplePathsNonRecursive = simplePaths.exploreAllSimplePaths(g, recursiveAlgorithm=False, printStatistics=True)[0]
                    #allSimplePathsNonRecursiveLeg = simplePaths.exploreAllSimplePaths(g, recursiveAlgorithm=False, printStatistics=True)[1]
                    #allSimplePathsRecursive = simplePaths.exploreAllSimplePaths(g, recursiveAlgorithm=True, printStatistics=True)
                    #print([[node.getName() for node in trip] for trip in allSimplePathsRecursive])
                    #print([[node.getName() for node in trip] for trip in allSimplePathsNonRecursive])
                    #print([[node.getName() for node in trip.nodesList] for trip in allSimplePathsNonRecursiveLeg])

                    generateInputFileForVrpGencol = True  # boolean used to decide if the input files are generated for GENCOL or VrpGencol
                    generateInputFileWithLegs = True  # boolean used to decide if the input files are generated with the the legs enumeration or not
                    antiSymmetryBool = True  # boolean used to decide if the input file is generated with the anti symmetry nodes and arcs
                    #timeWindows = [[0, 86400]] * numberOfDepots  # for the moment the time windows are not restrictive
                    fixedCost = 10000  # if high value, the problem is the minimization of the number of vehicles
                    if generateInputFileWithLegs:
                        if generateInputFileForVrpGencol:
                            if not antiSymmetryBool:
                                fileName = "problemVrp{}_{}_{}_{}.out".format(numberOfCustomers, numberOfDepots, timeWindowsType, droneAutonomy)
                            else:
                                fileName = "problemVrp{}_{}_{}_{}_as.out".format(numberOfCustomers, numberOfDepots, timeWindowsType, droneAutonomy)
                        else:
                            fileName = "problem{}_{}_{}.out".format(numberOfCustomers, numberOfDepots, timeWindowsType)

                        # if uncommented, returns an informative text file on the generated legs (can take a long time)
                        #input.createInputFile(g, "clients.txt", recursiveAlgorithm=False, printStatistics=False)

                        if generateInputFileForVrpGencol:
                            inputWithLegs.createCompleteVrpGENCOLInputFile(fileName, g, fixedCost, timeWindows, droneSpeed=droneSpeed, droneAutonomy=droneAutonomy, recursiveAlgorithm=False, printStatistics=True, antiSymmetry=antiSymmetryBool)
                        else:
                            inputWithLegs.createCompleteGENCOLInputFile(fileName, g, fixedCost, timeWindows, droneSpeed=droneSpeed, droneAutonomy=droneAutonomy, recursiveAlgorithm=False, printStatistics=True)
                    else:
                        if generateInputFileForVrpGencol:
                            fileName = "problemVrp{}_{}_{}_{}_p.out".format(numberOfCustomers, numberOfDepots, timeWindowsType, droneAutonomy)
                        else:
                            fileName = "problem{}_{}_{}_{}_p.out".format(numberOfCustomers, numberOfDepots, timeWindowsType, droneAutonomy)

                        if generateInputFileForVrpGencol:
                            inputWithoutLegs.createCompleteVrpGENCOLInputFile(fileName, g, fixedCost, timeWindows, serviceTime=5,
                                                                              droneSpeed=droneSpeed, droneAutonomy=droneAutonomy)
                        else:
                            inputWithoutLegs.createCompleteGENCOLInputFile(fileName, g, fixedCost, timeWindows, serviceTime=5,
                                                                           droneSpeed=droneSpeed, droneAutonomy=droneAutonomy)


if __name__ == '__main__':
    #sys.stdout = open('stdout.txt', 'w')  # writes the standard output to a stdout.txt
    start_time = time.time()
    main()
    print("\n Time used for main function : --- %s seconds ---" % (time.time() - start_time))