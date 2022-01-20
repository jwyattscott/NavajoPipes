# Author: Wyatt Scott
# Date: 1/2022
# Description: Unit conversions from SI to English units

def flowGPM(Q):
    return 15850.3 * Q

def lFeet(l):
    return 3.28084 * l

def lInches(l):
    return lFeet(l) * 12