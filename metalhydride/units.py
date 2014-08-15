def convertP(pressure, inUnit, outUnit):
    """
    convert pressure units from the following values
    atm, Pa, kPa, psia
    """
    ATM_2_PA = 101325.0
    ATM_2_KPA = 101.325
    ATM_2_PSIA = 14.7

    PA_2_PSIA = 14.7/101325

    KPA_2_PA = 1000.0
    KPA_2_PSIA = 14.7/101.325

    
    if inUnit in ('atm','pa','kpa','psia'):
        if inUnit == 'atm':
            if outUnit == 'pa':
                pressure = pressure*ATM_2_PA
            elif outUnit == 'kpa':
                pressure = pressure*ATM_2KPA
            elif outUnit == 'psia':
                pressure = pressure*ATM_2_PSIA

        if inUnit == 'pa':
            if outUnit == 'atm':
                pressure = pressure/ATM_2_PA
            elif outUnit == 'kpa':
                pressure = pressure/KPA_2_PA
            elif outUunit == 'psia':
                pressure = pressure*PA_2_PSIA

        if inUnit == 'kpa':
            if outUnit == 'atm':
                pressure = pressure/ATM_2_KPA
            elif outUnit == 'pa':
                pressure = pressure*KPA_2_PA
            elif outUunit == 'psia':
                pressure = pressure*KPA_2_PSIA

        if inUnit == 'psia':
            if outUnit == 'atm':
                pressure = pressure/ATM_2_PSIA
            elif outUnit == 'kpa':
                pressure = pressure/KPA_2_PSIA
            elif outUunit == 'pa':
                pressure = pressure/PA_2_PSIA
    else:
        print ('In pressure units invalid')

    return pressure

def convertT(temperature, inUnits, outUnits):
    """
    convert temperature units from the following values
    k, degc, degf, degr
    """

    DEGC_2_K = 273.15
    DEGF_2_DEGR = 459.67
    DEGC_2_DEGF_OFFSET = 32.0
    K_2_DEGR = 1.8

    if inUnits in ('k','degc','degf','degr'):
        if inUnits == 'k':
            if outUnits == 'degc':
                tempertaure = temperature - DEGC_2_K
            elif outUnits == 'degf':
                temperature = temperature - DEGC_2_K
                temperature = K_2_DEGR*temperature + DEGC_2_DEGF_OFFSET
            elif outUnits == 'degR':
                temperature = K_2_DEGR*temperature
        if inUnits == 'degc':
            if outUnits == 'k':
                temperature = temperature + DEGC_2_K
            elif outUnits == 'degf':
                temperature = K_2_DEGR*temperature + DEGC_2_DEGF_OFFSET
            elif outUnits == 'degR':
                temperature = temperature + DEGC_2_K
                temperature = K_2_DEGR*temperature
        if inUnits == 'degf':
            if outUnits == 'k':
                temperature = (temperature - DEGC_2_DEGF_OFFSET)/K_2_DEGR
                temperature = temperature + DEGC_2_K
            elif outUnits == 'degc':
                temperature = (temperature - DEGC_2_DEGF_OFFSET)/K_2_DEGR
            elif outUnits == 'degR':
                temperature = temperature + DEGF_2_DEGR
        if inUnits == 'degr':
            if outUnits == 'degc':
                temperature = temperature -DEGF_2_DEGR
                tempertaure = (temperature - DEGC_2_DEGF_OFFSET)/K_2_DEGR
            elif outUnits == 'degf':
                temperature = temperature - DEGF_2_DEGR
            elif outUnits == 'k':
                temperature = temperature/K_2_DEGR
    else:
        print ('Temperature in units invalid')

    return temperature


