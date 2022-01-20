# From the Pentair spec sheet

import sys
sys.path.append('..')
from src import interpolate as ip

def pcurve(Q):
    if (Q < 3.1545e-5):
        return ip.linear([0,42.25429452176524],[3.1545e-5,35.21191210147103],Q)
    elif (Q < 7.5708e-5):
        return ip.linear([3.1545e-5,35.21191210147103],[7.5708e-5,28.169529681176826],Q)
    elif (Q < 9.4635e-5):
        return ip.linear([7.5708e-5,28.169529681176826],[9.4635e-5,21.12714726088262],Q)
    elif (Q < 0.000113562):
        return ip.linear([9.4635e-5,21.12714726088262],[0.000113562,14.084764840588413],Q)
    elif (Q < 0.000138798):
        return ip.linear([0.000113562,14.084764840588413],[0.000138798,7.0423824202942065],Q)    
    elif (Q < 0.000189271):
        return ip.linear([0.000138798,7.0423824202942065],[0.000189271,0],Q)   
    else:
        return 0