__author__ = 'sibirrer'


"""
this class contains physical constants and conversion factors between units
"""
import numpy as np

G = 6.67384*10**(-11)  # Gravitational constant [m^3 kg^-1 s^-2]
c = 299792458  # [m/s]

M_sun = 1.9891*10**30  # solar mass in [kg]
M_earth = 5.9972 * 10**24  # Earth mass in [kg]
AU = 1.495978707 * 10 **11  # Distance Earth Sun (Astronomical unit) in [m]

Mpc = 3.08567758*10**22  # Mpc in [m]
day_s = 24*3600  # day in second
arcsec = 2*np.pi/360/3600  # arc second in radian

# derived quantities

a_ES = G * M_sun / AU**2  # Earth-Sun acceleration
F_ES = G * M_sun * M_earth / AU**2


def rho_c(h=1):
    """
    critical density of the universe
    :param h: reduced hubble parameter (in 100km/s/Mpc
    :return: critical density in units of kg/m^3
    """
    H = 100 * h  # in units km/s/Mpc
    H *= 1000  # in units m/s/Mpc
    H /= Mpc  # in units m/s/m
    rho = 3. * H**2 / (8 * np.pi * G)
    return rho