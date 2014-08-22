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
    delimit = inputDict['delimit']

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
    delimiter = ' '
    if delimit == 'tab':
        delimiter = "\t"
    elif delimit == 'csv':
        delimiter = ', '
        

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
                    f.write(('{0:6.3e}{1}{2:6.3e}{3}{4:6.3e}').format(isoTVals[i],delimiter,omega,delimiter,peq) + "\n")
        elif plot == 'B':
            #
            # plot both absorption and desorption
            for i in range(len(isoTVals)):
                for j in range(len(chartData[2*i])):
                    omega, peq = chartData[2*i][j]
                    f.write(('{0:6.3e}{1}{2:6.3e}{3}{4:6.3e}').format(isoTVals[i],delimiter,omega,delimiter,peq) + "\n")

                for j in range(len(chartData[2*i+1])):
                    omega, peq = chartData[2*i+1][j]
                    f.write(('{0:6.3e}{1}{2:6.3e}{3}{4:6.3e}').format(isoTVals[i],delimiter,omega,delimiter,peq) + "\n")

        f.close()

    elif outputFile == 'multiple':
        #
        # write out multiple files with the data


        if plot in ('A','D'):
            #
            # only absorption or desorption curves
         
            for i in range(len(isoTVals)):
                outputFileName = mhName + "-" + str(isoTVals[i]) + mh.get_tunits() + "-" + mh.get_punits() + '-' + plot + "-data.txt"
                f = open(outputFileName,'w+')
                for j in range(len(chartData[i])):
                    omega, peq = chartData[i][j]
                    f.write(('{0:6.3f}{1}{2:6.3f}').format(omega,delimiter,peq) + "\n")
                f.close()
        elif plot == 'B':
            #
            # plot both absorption and desorption
            for i in range(len(isoTVals)):
                outputFileName = mhName + "-" + str(isoTVals[i]) + mh.get_tunits() + "-" + mh.get_punits() + '-' +"A-data.txt"
                f = open(outputFileName,'w+')
                for j in range(len(chartData[2*i])):
                    omega, peq = chartData[2*i][j]
                    f.write(('{0:6.3e}{1}{2:6.3e}').format(omega,delimiter,peq) + "\n")
                f.close()

                outputFileName = mhName + "-" +str(isoTVals[i]) + mh.get_tunits() + "-" + mh.get_punits() + '-' +"D-data.txt"
                f = open(outputFileName,'w+')
                for j in range(len(chartData[2*i+1])):
                    omega, peq = chartData[2*i+1][j]
                    f.write(('{0:6.3e}{1}{2:6.3e}').format(omega,delimiter,peq) + "\n")
                f.close()

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


def generate_mhrfc_cycle_data(inputDict):
    """
    generate_mhrfc_cycle_data will make a plot of the MHRFC cycle based on metal hydride data 
    for two specified metal hydride materials, one with floating temperature and one with 
    a fixed temperature.  The data can be written to a single file or multiple files

    """


    #
    # get the relevant data from the dictionary
    mhFloatName = inputDict['mhydrideFloatName']
    mhFixedName = inputDict['mhydrideFixedName']
    pUnits = inputDict['pUnits']
    tUnits = inputDict['tUnits']
    omegaStart = inputDict['omegaStart']
    omegaEnd = inputDict['omegaEnd']
    tHi = inputDict['tHi']
    tLow = inputDict['tLow']
    delOmega = inputDict['delOmega']
    outputFile = inputDict['outputFile']
    showChart = inputDict['showChart']
    delimit = inputDict['delimit']
    logPlot = 'False'

    try:
        logPlot = inputDict['logPlot']
    except:
        pass


    mhFloat = mhydride.MetalHydride()
    mhFloat.load_data(mhFloatName)
    mhFloat.set_punits(pUnits)
    mhFloat.set_tunits(tUnits)

    mhFixed = mhydride.MetalHydride()
    mhFixed.load_data(mhFixedName)
    mhFixed.set_punits(pUnits)
    mhFixed.set_tunits(tUnits)
   
    chartData = []

    #
    # There are 4 different relevant series to plot
    #
    #  [0] mhFloat Thi desorption
    #  [1] mhFLoat Tlow absorption
    #  [2] mhFixed Tlow absorption
    #  [3] mhFixed Tlow desorption
    # 
    # They will be stored in the chart data list 
    # at the stated indicies


    count = 0

    #
    # create a new list for the chart data
    
    chartData.append([])
    mhFloat.set_t(tHi)
    omega = omegaStart
    while omega <= omegaEnd:
        mhFloat.set_omega(omega)
        peq = mhFloat.calc_peq(False)
        chartData[count].append((omega,peq))
        omega = omega + delOmega

    count = count + 1
    chartData.append([])
    mhFloat.set_t(tLow)
    omega = omegaStart
    while omega <= omegaEnd:
        mhFloat.set_omega(omega)
        peq = mhFloat.calc_peq()
        chartData[count].append((omega,peq))
        omega = omega + delOmega

    count = count + 1
    chartData.append([])
    mhFixed.set_t(tLow)
    omega = omegaStart
    while omega <= omegaEnd:
        mhFixed.set_omega(omega)
        peq = mhFixed.calc_peq()
        chartData[count].append((omega,peq))
        omega = omega + delOmega

    count = count + 1
    chartData.append([])
    omega = omegaStart
    while omega <= omegaEnd:
        mhFixed.set_omega(omega)
        peq = mhFixed.calc_peq(False)
        chartData[count].append((omega,peq))
        omega = omega + delOmega


    #
    # data generation is complete
    # check if user wants to see the plots or write out the data
    delimiter = ' '
    if delimit == 'tab':
        delimiter = "\t"
    elif delimit == 'csv':
        delimiter = ', '
        

    if outputFile == 'single':
        #
        # write out one single file with the data

        outputFileName = mhFloatName + "-" + mhFixedName + "-mhrfc-data.txt"
        f = open(outputFileName,'w+')

        for count in range(4):
            if count == 0: 
                temp = tHi
            else:
                temp = tLow
            for j in range(len(chartData[count])):
                omega, peq = chartData[count][j]
                f.write(('{0:6.3e}{1}{2:6.3e}{3}{4:6.3e}').format(temp,delimiter,omega,delimiter,peq) + "\n")

        f.close()

    elif outputFile == 'multiple':
        #
        # write out multiple files with the data

        for count in range(4):
            if count == 0: 
                temp = tHi
                outputFileName = mhFloatName + "-" + str(tHi) + mhFloat.get_tunits() + "-D-mhrfc-data.txt"
            elif count == 1:
                temp = tLow
                outputFileName = mhFloatName + "-" + str(tLow) + mhFloat.get_tunits() + "-A-mhrfc-data.txt"
            elif count == 2:
                temp = tLow
                outputFileName = mhFixedName + "-" + str(tLow) + mhFixed.get_tunits() + "-A-mhrfc-data.txt"            
            else:
                temp = tLow
                outputFileName = mhFixedName + "-" + str(tLow) + mhFixed.get_tunits() + "-D-mhrfc-data.txt"       
            f = open(outputFileName,'w+')

            for j in range(len(chartData[count])):
                omega, peq = chartData[count][j]
                f.write(('{0:6.3e}{1}{2:6.3e}').format(omega,delimiter,peq) + "\n")

            f.close()

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

        plt.xlabel('omega [-]')
        plt.ylabel('Pressure [' + mhFixed.get_punits() + ']')

        if logPlot == 'True':
            plt.yscale('log')

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
    MHRFC_Cycle = False
    inputDict = {}
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "chsrf:",["help","filename="])
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
        if o == "-r":
            MHRFC_Cycle = True

    if chartData == True:
        #
        # generate chart files
        generate_chart_data(inputDict)

    elif MHRFC_Cycle == True:
        #
        # generate MHRFC cycle charts and files
        generate_mhrfc_cycle_data(inputDict)


    return


if __name__ == "__main__":
    main()
