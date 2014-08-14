import units
import math

class MetalHydride(object):
    """
    This class will represnt a metal hydride object to calculate 
    various parameters such as equilibrium pressure and diffusion rate

    Members:
        name        name of the metal hydride
        fileName    filename of the parameters
        paramDict   parameter dictionary
        omega       percntage hydrided (0,1)
        t           temperature
        p           pressure
        punits      {atm, pa, kpa, psia} pressure values are entered and returned in the units specified, default is atm
        tunits      {k, degc, degf} temperature values are entered and returned in the units specified, default is k


    Member Functions:
        load_data   loads methal hydride data from a file
        get_omega   gets the current value for omega
        set_omega   sets the current value for omega
        get_p       gets the current value for pressure
        set_p       sets the current value for pressure
        get_punits  gets the current pressure units specification
        set_punits  sets the current pressure unit specification
        get_t       gets the current value for temperature
        set_t       sets the current value for temperature
        get_tunits  gets the current temperature units specification
        set_tunits  sets the current temperature unit specification
        calc_peq    calcualte the equilibrium pressure Peq(omega, T)
        calc_rdot   calculate the absorption/desorption rate Note that a positve value is desorption while a negative value is absorption 


    """


    def __init__(self):
        self.name = ""
        self.paramDict = {}
        self.fileName = ""
        self.omega = 0.0
        self.t = 300
        self.p = 1.0
        self.punits = 'atm'
        self.tunits = 'k'

        return

    def load_data(self,filename,clear = True):
        self.fileName = filename
        """Use this function to read MH properties into the dictionary"""

        #
        # clear the dictionary
        if clear == 'True':
            self.paramDict.clear()

        #
        # filename is the metal hydride name + '.mhd'
        Filename = filename + ".mhd"
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
                                self.paramDict[tokens[0]] = float(tokens[3])
                            except:
                                print ('Error parsing file ',Filename," at line number ",linenum)
                                sys.exit(2)


                        elif tokens[2].lower() == 'int':
                            self.paramDict[tokens[0]] = int(tokens[3])
                        else:
                            self.paramDict[tokens[0]] = tokens[3].strip()

        return

    def set_omega(self, omega):
        self.omega = omega
        return

    def get_omega(self):
        return self.omega

    def set_t(self, temperature):
        self.t = temperature
        return

    def get_t(self):
        return self.t

    def set_p(self, pressure):
        self.p = pressure
        return

    def set_punits(self, newPunit):
        self.punits = newPunit
        return

    def get_punits(self):
        return self.punits

    def set_tunits(self, newTunit):
        self.tunits = newTunit
        return

    def get_tunits(self):
        return self.tunits

    def calc_peq(self, absorb = True):
        """
        calc_peq will calculate the equilibrium 
    	pressure for a given metal hydride based on formulation
	    from choi and mills paper.

	    note that the equation calculates the pressure in atm, but the 
	    function returns the value in the set pressure units

	    ln(peq) = -a/t + b + (phi(+/-)phi0 +/- beta/2

        Input:
            bool    absorb      True if absorption, False if desorption
            float   temp        temperature, default is object stored value
            float   omega       omega, default is object stored value

        """

        #
        # get the parameters from the dictionary
        A = self.paramDict['A']
        B = self.paramDict['B']
        phi = self.paramDict['phi']
        phi0 = self.paramDict['phi0']
        beta = self.paramDict['beta']

        temp = self.t
        omega = self.omega

        if absorb == True:
            sign = 1.0
        else:
            sign = -1.0

        peq = (-A/temp) + B

        if (omega > 0.0) and (omega < 1.0):
            peq = peq + (phi + sign*phi0)*math.tan(math.pi*(omega - 0.5)) 
            peq = peq + sign*(beta/2.0)

        peq = math.exp(peq)
        peq = units.convertP(peq,'atm',self.punits)

        return peq



