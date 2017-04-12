# Author : Alexandre Dossin
import simplePaths
import graph

def createInputFile(g, fileName, droneSpeed=600, droneAutonomy=25, printStatistics=False):
    """Returns the input file that contains the list of legs.
    A leg is represented by an id, its cost, an origin and a destination depot and a list of visited customers"""

    simplePathsList = simplePaths.exploreAllSimplePaths(g, droneSpeed, droneAutonomy, printStatistics)
    myFile = open(fileName, "w")
    myFile.write("Number of customers: {}   Number of Depots: {}    Drone Autonomy: {} min  Drone Speed:{} m/min"
                 .format(len(g.getCustomers()), int(len(g.getDepots()) / 2), droneAutonomy, droneSpeed))
    myFile.write('\n \n')

    # description of the columns
    myFile.write("leg_id    time    originDepot destinationDepot    visitedNodes")
    myFile.write('\n')

    # filling the file with legs
    for i, leg in enumerate(simplePathsList):
        leg_id = i

        if leg[0] in g.getOtherDepots():  # associate a real depot to the virtual one
            dep = g.getNode(int(leg[0].getName()) - 1)
        else:
            dep = leg[0]

        if leg[-1] in g.getOtherDepots():
            dest = g.getNode(int(leg[-1].getName()) - 1)
        else:
            dest = leg[-1]

        legObject = graph.Path(leg)  # more OOP way

        # converting time from minutes to seconds for more precision
        time = int(legObject.computeLength(droneSpeed) * 60)

        visitedNodesStr = str()
        if len(leg) > 2:
            visitedNodesStr = " ".join([node.getName() for node in leg[1:-1]])


        myFile.write(str(leg_id) + '        ' + str(round(time, 1)) + '         ' + str(dep.getName())
                     + '           ' + str(dest.getName()) + '                   '
                     '[' + visitedNodesStr + ']')
        myFile.write('\n')
    pass

def createGENCOLInputFile(fileName):
    myFile = open(fileName, 'w')
    pass

def createGENCOLInputFileResources(fileName):
    myFile = open(fileName, 'a')
    myFile.write("Resources={\nTime Strong;\n};\n\n")
    pass

def createGENCOLInputFileRows(fileName, g):
    myFile = open(fileName, 'a')
    myFile.write("Rows={\n")
    for customer in range(1, len(g.getCustomers()) + 1):
        myFile.write("RowD{} = 1 TaskStrong;\n".format(str(customer)))
    myFile.write("RowVeh = 0;\n};\n\n")
    pass

def createGENCOLInputFileTasks(fileName, g):
    myFile = open(fileName, 'a')
    myFile.write("Tasks={\n")
    for customer in range(1, len(g.getCustomers()) + 1):
        myFile.write("D{} RowD{} Strong;\n".format(str(customer), str(customer)))
    myFile.write("};\n\n")
    pass

def createGENCOLInputFileColumns(fileName, fixedCost):
    myFile = open(fileName, 'a')
    myFile.write("Columns={\n")
    myFile.write("Vehicles {} Int(RowVeh 1);\n".format(int(fixedCost)))
    myFile.write("};\n\n")
    pass

def createGENCOLInputFileNodes(fileName, g, timeIntervals):
    myFile = open(fileName, 'a')
    myFile.write("Nodes={\n")

    myFile.write("Source [0 0];\n")

    for i, depot in enumerate(g.getRealDepots()):
        myFile.write("N{} [{} {}]; \n".format(str(depot.getName()) + "arr", timeIntervals[i][0], timeIntervals[i][1]))
        myFile.write("N{} [{} {}]; \n".format(str(depot.getName()) + "dep", timeIntervals[i][0], timeIntervals[i][1]))

    myFile.write("Destination [0 1440];\n")

    myFile.write("};\n\n")
    pass

def createGENCOLInputFileArcs(fileName, g, droneSpeed=600, droneAutonomy=25, printStatistics=False):

    simplePathsList = simplePaths.exploreAllSimplePaths(g, droneSpeed, droneAutonomy, printStatistics)

    myFile = open(fileName, 'a')
    myFile.write("Arcs={\n")

    for leg in simplePathsList:

        if leg[0] in g.getOtherDepots():  # associate a real depot to the virtual one
            dep = g.getNode(int(leg[0].getName()) - 1)
        else:
            dep = leg[0]

        if leg[-1] in g.getOtherDepots():
            dest = g.getNode(int(leg[-1].getName()) - 1)
        else:
            dest = leg[-1]

        legObject = graph.Path(leg)  # more OOP way

        # converting time from minutes to seconds for more precision
        time = int(legObject.computeLength(droneSpeed) * 60)

        visitedNodesStr = str()
        if len(leg) > 2:
            visitedNodesStr = "D" + " D".join([node.getName() for node in leg[1:-1]])

        myFile.write("N{} N{} {} [{}] {};\n".format(dep.getName() + "dep", dest.getName() + "arr", time, time, visitedNodesStr))

    for depot in g.getRealDepots():
        myFile.write("Source N{} 0 [0] (RowVeh -1);\n".format(depot.getName() + "dep"))  # we add the sources arcs
        myFile.write("N{} Destination 0 [0];\n".format(depot.getName() + "arr"))  # and the destination arcs

    myFile.write("};\n\n")

    pass

def createGENCOLInputFileNetwork(fileName):
    myFile = open(fileName, 'a')
    myFile.write("Networks={\n")
    myFile.write("Net Source (Destination);")
    myFile.write("\n};")

def createCompleteGENCOLInputFile(fileName, g, fixedCost, timeIntervals,
                                  droneSpeed=600, droneAutonomy=25, printStatistics=False):
    """Creates the complete GENCOL input file"""
    createGENCOLInputFile(fileName)
    createGENCOLInputFileResources(fileName)
    createGENCOLInputFileRows(fileName, g)  #TODO : put numberOfCustomers argument in a graph method
    createGENCOLInputFileTasks(fileName, g)
    createGENCOLInputFileColumns(fileName, fixedCost)
    createGENCOLInputFileNodes(fileName, g, timeIntervals)
    createGENCOLInputFileArcs(fileName, g, droneSpeed, droneAutonomy, printStatistics)
    createGENCOLInputFileNetwork(fileName)
    pass


def generateGENCOLInputFiles(numberOfCustomers, numberOfDepots, fixedCost,
                                  droneSpeed=600, droneAutonomy=25, printStatistics=False):

    for i, customer in enumerate(range(1, numberOfCustomers + 1)):
        for j, depot in enumerate(range(2, numberOfDepots + 1)):
            g = graph.buildGraph(customer, depot, maxDistance=1000, explorationTime=5)
            timeIntervals = [[0, 1440]] * numberOfDepots
            createCompleteGENCOLInputFile("input{}_{}.txt".format(customer, depot), g, fixedCost,
                                          timeIntervals, droneSpeed, droneAutonomy, printStatistics)

    pass
