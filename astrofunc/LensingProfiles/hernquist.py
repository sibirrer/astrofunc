import numpy as np


class Hernquist(object):
    """
    class to compute the DUAL PSEUDO ISOTHERMAL ELLIPTICAL MASS DISTRIBUTION
    based on Eliasdottir (2013)
    """
    _diff = 0.00001

    def density(self, x, y, rho0, Rs,  center_x=0, center_y=0):
        """
        computes the density
        :param x:
        :param y:
        :param rho0:
        :param a:
        :param s:
        :return:
        """
        x_ = x - center_x
        y_ = y - center_y
        r = np.sqrt(x_**2 + y_**2)
        rho = rho0 / (r/Rs * (1 + (r/s))**3)
        return rho

    def density_2d(self, x, y, sigma0, Rs, center_x=0, center_y=0):
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
        X = r/Rs
        sigma = sigma0 / (X**2 -1)**2 * (-3 + (2+X**2)) * self._F(X)
        return sigma

    def _F(self, X):
        """
        function 48 in https://arxiv.org/pdf/astro-ph/0102341.pdf
        :param X: r/rs
        :return:
        """
        if isinstance(X, int) or isinstance(X, float):
            if X < 1 and X > 0:
                a = 1. / np.sqrt(1 - X ** 2) * np.arctanh(np.sqrt(1 - X**2))
            elif X == 1:
                a = 1.
            elif X > 1:
                a = 1. / np.sqrt(X ** 2 - 1) * np.arctan(np.sqrt(X**2 - 1))
            else:  # X == 0:
                c = 0.0001
                a = 1. / np.sqrt(1 - c ** 2) * np.arctanh(np.sqrt((1 - c ** 2)))

        else:
            a = np.empty_like(X)
            x = X[X < 1]
            a[X < 1] = 1 / np.sqrt(1 - x ** 2) * np.arctanh(np.sqrt((1 - x**2)))

            x = X[X == 1]
            a[X == 1] = 1.

            x = X[X > 1]
            a[X > 1] = 1 / np.sqrt(x ** 2 - 1) * np.arctan(np.sqrt(x**2 - 1))
            # a[X>y] = 0

            c = 0.0001
            x = X[X == 0]
            a[X == 0] = 1. / np.sqrt(1 - c ** 2) * np.arctanh(np.sqrt((1 - c ** 2)))
        return a

    def mass_3d(self, r, rho0, a, s):
        """
        mass enclosed a 3d sphere or radius r
        :param r:
        :param a:
        :param s:
        :return:
        """
        #TODO needs to be done
        return 0

    def mass_2d(self, r, rho0, a, s):
        """
        mass enclosed projected 2d sphere of radius r
        :param r:
        :param rho0:
        :param a:
        :param s:
        :return:
        """
        #TODO needs to be done
        return 0

    def mass_tot(self, rho0, a, s):
        """
        total mass within the profile
        :param rho0:
        :param a:
        :param s:
        :return:
        """
        #TODO needs to be done
        m_tot = 0
        return m_tot

    def grav_pot(self, x, y, rho0, Rs, center_x=0, center_y=0):
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
        X = r/Rs
        pot = 0
        #TODO needs to be done
        return pot

    def function(self, x, y, sigma0, Rs, center_x=0, center_y=0):
        """
        lensing potential
        :param x:
        :param y:
        :param sigma0: sigma0/sigma_crit
        :param a:
        :param s:
        :param center_x:
        :param center_y:
        :return:
        """
        x_ = x - center_x
        y_ = y - center_y
        r = np.sqrt(x_**2 + y_**2)
        X = r / Rs
        f_ = sigma0 * Rs**2 * (np.log(X**2/4.) + 2*self._F(X))
        return f_

    def derivatives(self, x, y, sigma0, Rs, center_x=0, center_y=0):
        """

        :param x:
        :param y:
        :param sigma0: sigma0/sigma_crit
        :param a:
        :param s:
        :param center_x:
        :param center_y:
        :return:
        """
        x_ = x - center_x
        y_ = y - center_y
        r = np.sqrt(x_**2 + y_**2)
        X = r/Rs
        alpha_r = 2*sigma0 * Rs * X * (1-self._F(X)) / (X**2-1)
        f_x = alpha_r * x_/r
        f_y = alpha_r * y_/r
        return f_x, f_y

    def hessian(self, x, y, sigma0, Rs,  center_x=0, center_y=0):
        """

        :param x:
        :param y:
        :param sigma0: sigma0/sigma_crit
        :param a:
        :param s:
        :param center_x:
        :param center_y:
        :return:
        """
        alpha_ra, alpha_dec = self.derivatives(x, y, sigma0, Rs,  center_x, center_y)
        diff = self._diff
        alpha_ra_dx, alpha_dec_dx = self.derivatives(x + diff, y, sigma0, Rs,  center_x, center_y)
        alpha_ra_dy, alpha_dec_dy = self.derivatives(x, y + diff, sigma0, Rs,  center_x, center_y)

        f_xx = (alpha_ra_dx - alpha_ra)/diff
        f_xy = (alpha_ra_dy - alpha_ra)/diff
        #f_yx = (alpha_dec_dx - alpha_dec)/diff
        f_yy = (alpha_dec_dy - alpha_dec)/diff

        return f_xx, f_yy, f_xy

    def _f_A20(self, r_a, r_s):
        """
        equation A20 in Eliasdottir (2013)
        :param r_a:
        :param r_s:
        :return:
        """
        return r_a/(1+np.sqrt(1 + r_a**2)) - r_s/(1+np.sqrt(1 + r_s**2))

    def rho2sigma(self, rho0, a, s):
        """
        converts 3d density into 2d projected density parameter
        :param rho0:
        :param a:
        :param s:
        :return:
        """
        return np.pi * rho0 * a*s/(s+a)