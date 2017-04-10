# Author : Alexandre Dossin
import simplePaths
import graph

def createInputFile(g, fileName, droneSpeed=600, droneAutonomy=25, toPrint=False, printStatistics=False):
    """Returns the input file that contains the list of legs.
    A leg is represented by an id, its cost, an origin and a destination depot and a list of visited customers"""

    simplePathsList = simplePaths.exploreAllSimplePaths(g, droneSpeed, droneAutonomy, toPrint, printStatistics)
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

        time = legObject.computeLength(droneSpeed)

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

def createGENCOLInputFileRows(fileName, numberOfCustomers):
    myFile = open(fileName, 'a')
    myFile.write("Rows={\n")
    for customer in range(1, numberOfCustomers + 1):
        myFile.write("RowD{} = 1 TaskStrong;\n".format(str(customer)))
    myFile.write("RowVeh = 0;\n};\n\n")
    pass

def createGENCOLInputFileTasks(fileName, numberOfCustomers):
    myFile = open(fileName, 'a')
    myFile.write("Tasks={\n")
    for customer in range(1, numberOfCustomers + 1):
        myFile.write("D{} RowD{} Strong;\n".format(str(customer), str(customer)))
    myFile.write("};\n\n")
    pass

def createGENCOLInputFileColumns(fileName, numberOfVehicles):
    myFile = open(fileName, 'a')
    myFile.write("Columns={\n")
    myFile.write("Vehicles {} CutUp(RowVeh 1);\n".format(int(numberOfVehicles)))
    myFile.write("};\n\n")
    pass

def createGENCOLInputFileNodes(fileName, numberOfCustomers, numberOfDepots, timeIntervals):  # TODO : add source and destination
    myFile = open(fileName, 'a')
    myFile.write("Nodes={\n")
    idx = 0
    for depot in range(numberOfCustomers + 1, numberOfCustomers + numberOfDepots + 1):
        myFile.write("N{} [{} {}]; \n".format(str(depot) + "arr", timeIntervals[idx][0], timeIntervals[idx][1]))
        myFile.write("N{} [{} {}]; \n".format(str(depot) + "dep", timeIntervals[idx][0], timeIntervals[idx][1]))
        idx += 1
    myFile.write("};\n\n")
    pass

def createGENCOLInputFileArcs(fileName, g, droneSpeed=600, droneAutonomy=25, toPrint=False, printStatistics=False):  # TODO : add source and node

    simplePathsList = simplePaths.exploreAllSimplePaths(g, droneSpeed, droneAutonomy, toPrint, printStatistics)

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

        time = legObject.computeLength(droneSpeed)

        visitedNodesStr = str()
        if len(leg) > 2:
            visitedNodesStr = "D" + " D".join([node.getName() for node in leg[1:-1]])

        myFile.write("N{} N{} {} [{}] {}\n".format(dep.getName() + "dep", dest.getName() + "arr", time, time, visitedNodesStr))

    myFile.write("};\n\n")

    pass

def createGENCOLInputFileNetwork(fileName):
    myFile = open(fileName, 'a')
    myFile.write("Networks={\n")
    myFile.write("Net Source (Destination);")
    myFile.write("\n};")


