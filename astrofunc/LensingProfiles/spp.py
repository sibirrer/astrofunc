__author__ = 'sibirrer'


import numpy as np
import scipy.special as special


class SPP(object):
    """
    class for Softened power-law elliptical potential (SPEP)
    """

    def function(self, x, y, theta_E, gamma, center_x=0, center_y=0):
        """
        :param x: set of x-coordinates
        :type x: array of size (n)
        :param theta_E: Einstein radius of lense
        :type theta_E: float.
        :param gamma: power law slope of mass profifle
        :type gamma: <2 float
        :param q: Axis ratio
        :type q: 0<q<1
        :param phi_G: position angel of SES
        :type q: 0<phi_G<pi/2
        :returns:  function
        :raises: AttributeError, KeyError
        """
        if gamma < 1.6:
            gamma = 1.6
        if gamma > 2.9:
            gamma = 2.9

        x_ = x - center_x
        y_ = y - center_y
        E = theta_E / ((3 - gamma) / 2.) ** (1. / (1 - gamma))
        # E = phi_E_spp
        eta= -gamma + 3

        p2 = x_**2+y_**2
        s2 = 0. # softening
        return 2 * E**2/eta**2 * ((p2 + s2)/E**2)**(eta/2)

    def derivatives(self, x, y, theta_E, gamma, center_x=0., center_y=0.):

        # # @hope.jit
        # def xy_prime(dx, dy, eta, a, E, xt1, xt2, q):
        #     fac = 1./eta*(a/(E*E))**(eta/2-1)*2
        #     dx[:] = fac*xt1
        #     dy[:] = fac*xt2/(q*q)
        if gamma < 1.6:
            gamma = 1.6
        if gamma > 2.9:
            gamma = 2.9

        xt1 = x - center_x
        xt2 = y - center_y
        E = theta_E / ((3 - gamma) / 2.) ** (1. / (1 - gamma))
        # E = phi_E_spp
        eta = -gamma + 3

        P2=xt1*xt1+xt2*xt2
        if isinstance(P2, int) or isinstance(P2, float):
            a = max(0.000001,P2)
        else:
            a=np.empty_like(P2)
            p2 = P2[P2 > 0]  #in the SIS regime
            a[P2==0] = 0.000001
            a[P2>0] = p2

        fac = 1./eta*(a/(E*E))**(eta/2-1)*2
        f_x = fac*xt1
        f_y = fac*xt2
        return f_x, f_y

    def hessian(self, x, y, theta_E, gamma, center_x=0., center_y=0.):
        if gamma < 1.6:
            gamma = 1.6
        if gamma > 2.9:
            gamma = 2.9

        xt1 = x - center_x
        xt2 = y - center_y
        E = theta_E / ((3 - gamma) / 2.) ** (1. / (1 - gamma))
        # E = phi_E_spp
        eta = -gamma + 3

        P2 = xt1**2+xt2**2
        if isinstance(P2, int) or isinstance(P2, float):
            a = max(0.000001,P2)
        else:
            a=np.empty_like(P2)
            p2 = P2[P2>0]  #in the SIS regime
            a[P2==0] = 0.000001
            a[P2>0] = p2
        s2 = 0. # softening

        kappa = 1./eta*(a/E**2)**(eta/2-1)*((eta-2)*(xt1**2+xt2**2)/a+(1+1))
        gamma1 = 1./eta*(a/E**2)**(eta/2-1)*((eta/2-1)*(2*xt1**2-2*xt2**2)/a)
        gamma2 = 4*xt1*xt2*(1./2-1/eta)*(a/E**2)**(eta/2-2)/E**2

        f_xx = kappa + gamma1
        f_yy = kappa - gamma1
        f_xy = gamma2
        return f_xx, f_yy, f_xy

    def all(self, x, y, theta_E, gamma, center_x=0., center_y=0.):
        if gamma < 1.6:
            gamma = 1.6
        if gamma > 2.9:
            gamma = 2.9

        xt1 = x - center_x
        xt2 = y - center_y
        E = theta_E / ((3 - gamma) / 2.) ** (1. / (1 - gamma))
        # E = phi_E_spp
        eta = -gamma + 3
        P2 = xt1**2+xt2**2

        if isinstance(P2, int) or isinstance(P2, float):
            p2 = max(0.000001,P2)
        else:
            p2 = np.empty_like(P2)
            p = P2[P2>0]  #in the SIS regime
            p2[P2==0] = 0.000001
            p2[P2>0] = p
        s2 = 0. # softening
        f_ = 2 * E**2/eta**2 * ((p2 +s2)/E**2)**(eta/2)

        f_x = 1./eta*((p2)/E**2)**(eta/2-1)*2*xt1
        f_y = 1./eta*((p2)/E**2)**(eta/2-1)*2*xt2

        kappa = 1./eta*(p2/E**2)**(eta/2-1)*((eta-2)*(xt1**2+xt2**2)/p2+(1+1))
        gamma1 = 1./eta*(p2/E**2)**(eta/2-1)*((eta/2-1)*(2*xt1**2-2*xt2**2)/p2)
        gamma2 = 4*xt1*xt2*(1./2-1/eta)*(p2/E**2)**(eta/2-2)/E**2

        f_xx = kappa + gamma1
        f_yy = kappa - gamma1
        f_xy = gamma2

        return f_, f_x, f_y, f_xx, f_yy, f_xy

    def rho2theta(self, rho0, gamma):
        """
        converts 3d density into 2d projected density parameter
        :param rho0:
        :param gamma:
        :return:
        """
        fac = np.sqrt(np.pi) * special.gamma(1. / 2 * (-1 + gamma)) / special.gamma(gamma / 2.) * 2 / (3 - gamma) * rho0

        #fac = theta_E**(gamma - 1)
        theta_E = fac**(1. / (gamma - 1))
        return theta_E

    def theta2rho(self, theta_E, gamma):
        """
        converts projected density parameter (in units of deflection) into 3d density parameter
        :param theta_E:
        :param gamma:
        :return:
        """
        fac1 = np.sqrt(np.pi) * special.gamma(1. / 2 * (-1 + gamma)) / special.gamma(gamma / 2.) * 2 / (3 - gamma)
        fac2 = theta_E**(gamma - 1)
        rho0 = fac2 / fac1
        return rho0

    def mass_3d(self, r, rho0, gamma):
        """
        mass enclosed a 3d sphere or radius r
        :param r:
        :param a:
        :param s:
        :return:
        """
        mass_3d = 4 * np.pi * rho0 /(-gamma + 3) * r ** (-gamma + 3)
        return mass_3d

    def mass_2d(self, r, rho0, gamma):
        """
        mass enclosed projected 2d sphere of radius r
        :param r:
        :param rho0:
        :param a:
        :param s:
        :return:
        """
        alpha = np.sqrt(np.pi) * special.gamma(1. / 2 * (-1 + gamma)) / special.gamma(gamma / 2.) * r ** (2 - gamma)/(3 - gamma) *np.pi * 2 * rho0
        mass_2d = alpha*r
        return mass_2d

    def mass_tot(self, rho0, alpha):
        """
        total mass within the profile
        :param rho0:
        :param a:
        :param s:
        :return:
        """
        # mass enclosed is infinite
        m_tot = 0
        return m_tot

    def grav_pot(self, x, y, rho0, gamma, center_x=0, center_y=0):
        """
        gravitational potential (modulo 4 pi G and rho0 in appropriate units)
        :param x:
        :param y:
        :param rho0:
        :param a:
        :param s:
        :param center_x:
        :param center_y:
        :return:
        """
        x_ = x - center_x
        y_ = y - center_y
        r = np.sqrt(x_**2 + y_**2)
        mass_3d = self.mass_3d(r, rho0, gamma)
        pot = mass_3d/r
        return pot

    def density(self, r, rho0, gamma):
        """
        computes the density
        :param x:
        :param y:
        :param rho0:
        :param a:
        :param s:
        :return:
        """
        rho = rho0 / r**gamma
        return rho

    def density_2d(self, x, y, rho0, gamma, center_x=0, center_y=0):
        """
        projected density
        :param x:
        :param y:
        :param rho0:
        :param a:
        :param s:
        :param center_x:
        :param center_y:
        :return:
        """
        x_ = x - center_x
        y_ = y - center_y
        r = np.sqrt(x_**2 + y_**2)
        sigma = np.sqrt(np.pi) * special.gamma(1./2*(-1+gamma))/special.gamma(gamma/2.) * r**(1-gamma) * rho0
        return sigma