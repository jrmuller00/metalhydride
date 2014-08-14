import mhydride
import units
import sys
import getopt
import math
import numpy as np
import matplotlib.pyplot as plt





def load_input_data(inputDict, Filename, clear = True):
    """Use this function to read MH properties into the dictionary"""

    #
    # clear the dictionary
    if clear == 'True':
        inputDict.clear()

    linenum = 0

    #
    # loop over lines in file
    #
    # comment lines start with '#' character
    #
    # data lines are of the form [key] = [type] [value]
    #
    #   where 
    #       key is the name of the parameter, e.g. MW for molecular weight
    #       type is the value type, e.g., float, int, str
    #       value is the actual value
    #
    for line in open(Filename,"r"):
        # print (line)
        tokens = line.split()
        linenum = linenum + 1
        # print (tokens)
        #
        # check to see if there are tokens on the line
        if len(tokens) > 1:
            if tokens[0] == "#":
                # comment line ignore
                # print ('Comment ',line)
                pass
            elif len(tokens) > 2:
                if tokens[1] == "=":
                    # print ('data:   ',line)
                    # line contains data
                    if tokens[2].lower() == 'float':
                        # print (tokens[0], tokens[2], tokens[3])
                        try:
                            inputDict[tokens[0]] = float(tokens[3])
                        except:
                            print ('Error parsing file ',Filename," at line number ",linenum)
                            sys.exit(2)


                    elif tokens[2].lower() == 'int':
                        inputDict[tokens[0]] = int(tokens[3])
                    else:
                        inputDict[tokens[0]] = tokens[3].strip()

    return inputDict


def generate_chart_data(inputDict):
    """
    generate_chart_data will make a plot of the metal hydride data for a specified (input card)
    metal hydride.  The data can be written to a single file or multiple files

    """


    #
    # get the relevant data from the dictionary
    mhName = inputDict['mhydrideName']
    pUnits = inputDict['pUnits']
    tUnits = inputDict['tUnits']
    omegaStart = inputDict['omegaStart']
    omegaEnd = inputDict['omegaEnd']
    tStart = inputDict['tStart']
    tEnd = inputDict['tEnd']
    delT = inputDict['delT']
    delOmega = inputDict['delOmega']
    plot = inputDict['plot']
    outputFile = inputDict['outputFile']
    showChart = inputDict['showChart']

    mh = mhydride.MetalHydride()
    mh.load_data(mhName)
    mh.set_punits(pUnits)
    mh.set_tunits(tUnits)

    temperature = tStart
    isoTVals = []
    chartData = []

    #
    # set a counter for the number of data series
    count = 0

    #
    # loop over all the requested temperatures

    while temperature <= tEnd:
        #
        # set the temperature
        mh.set_t(temperature)
        isoTVals.append(temperature)

        #
        # check if use wants absorption or both
        if plot in ('A','B'):
            #
            # create a new list for the chart data
            chartData.append([])

            omega = omegaStart
            while omega <= omegaEnd:
                mh.set_omega(omega)
                peq = mh.calc_peq()
                chartData[count].append((omega,peq))
                omega = omega + delOmega

            count = count + 1
            #
            # end omega <= omegaEnd:
            #


        if plot in ('D','B'):
            
            #
            # create a new list for the chart data
            chartData.append([])

            omega = omegaStart
            while omega <= omegaEnd:
                mh.set_omega(omega)
                peq = mh.calc_peq(False)
                chartData[count].append((omega,peq))
                omega = omega + delOmega
            count = count + 1

            #
            # end omega <= omegaEnd:
            #
        


        #
        # advance T and repeat
        temperature = temperature + delT
        #
        # end   if plot in ('A','B'):
        #       elif plot in ('D','B'):

    # end while temperature <= tEnd:

    #
    # data generation is complete
    # check if user wants to see the plots or write out the data

    if outputFile == 'single':
        #
        # write out one single file with the data

        outputFileName = mhName + "-data.txt"
        f = open(outputFileName,'w+')

        if plot in ('A','D'):
            #
            # only absorption or desorption curves
            
            for i in range(len(isoTVals)):
                for j in range(len(chartData[i])):
                    omega, peq = chartData[i][j]
                    f.write('{0:6.3f}, {1:6.3f}, {2:6.3f}'.format(isoTVals[i],omega,peq) + "\n")
        elif plot == 'B':
            #
            # plot both absorption and desorption
            for i in range(len(isoTVals)):
                for j in range(len(chartData[2*i])):
                    omega, peq = chartData[2*i][j]
                    f.write('{0:6.3f}, {1:6.3f}, {2:6.3f}'.format(isoTVals[i],omega,peq) + "\n")

                for j in range(len(chartData[2*i+1])):
                    omega, peq = chartData[2*i+1][j]
                    f.write('{0:6.3f}, {1:6.3f}, {2:6.3f}'.format(isoTVals[i],omega,peq) + "\n")

        f.close()

    elif outputFile == 'multiple':
        print ('not implemented yet')

    #
    # check if user asked for plot to be shown

    if showChart == 'True':
        #
        # loop over data pairs and create xvals and yvals vectors for matplot

        for i in range(len(chartData)):
            xvals = []
            yvals= []
            for j in range(len(chartData[i])):
                omega, peq = chartData[i][j]
                xvals.append(omega)
                yvals.append(peq)
            line = plt.plot(xvals,yvals)

        plt.show()

    return







def main():
    """
    main is the main function for the metalhydride program.  it will take several 
    command line arguments to either create a set of data files or run a simulation
    
    arguments:
        -h              :   help on running the code
        -c              :   create data for plotting
        -s              :   system simulation
        -f [filename]   :   input filename

    """
    inputFile = ""
    chartData = False
    simulation = False
    inputDict = {}
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "chsf:",["help","filename="])
    except getopt.error as msg:
        print (msg)
        print ("for help use --help")
        sys.exit(2)

    for o, arg in opts:
#        print (o, arg)
        if o == "-h":
            print ("python metalhydride.py")
        if o == "-f":
            inputFile = arg
            inputDict = load_input_data(inputDict,inputFile)
        if o == "-s":
            simulation = True
        if o == "-c":
            chartData = True

    hystor = mhydride.MetalHydride()

    hystor.load_data('hystor207')

    hystor.set_t(300)
    hystor.set_omega(0.5)

    peqa = hystor.calc_peq()
    peqd = hystor.calc_peq(False)

    print (peqa,peqd)

    if chartData == True:
        #
        # generate chart files
        generate_chart_data(inputDict)

    return


if __name__ == "__main__":
    main()
