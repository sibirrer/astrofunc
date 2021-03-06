import numpy as np


class Gaussian(object):
    """
    class for Gaussian light profile
    """
    def __init__(self):
        pass

    def function(self, x, y, amp, sigma_x, sigma_y, center_x=0, center_y=0):
        """

        :param x:
        :param y:
        :param sigma0:
        :param a:
        :param s:
        :param center_x:
        :param center_y:
        :return:
        """
        c = amp / (2 * np.pi * sigma_x * sigma_y)
        R2 = (x - center_x) ** 2/sigma_x**2 + (y - center_y) ** 2/sigma_y**2
        return c * np.exp(-R2 / 2.)

    def light_3d(self, r, amp, sigma_x, sigma_y):
        """

        :param y:
        :param sigma0:
        :param Rs:
        :param center_x:
        :param center_y:
        :return:
        """
        amp3d = amp / np.sqrt(2* sigma_x * sigma_y) / np.sqrt(np.pi)
        sigma3d_x = sigma_x
        sigma3d_y = sigma_y
        return self.function(r, 0, amp3d, sigma3d_x, sigma3d_y)


class MultiGaussian(object):
    """
    class for elliptical pseudo Jaffe lens light (2d projected light/mass distribution
    """
    def __init__(self):
        self.gaussian = Gaussian()

    def function(self, x, y, amp, sigma, center_x=0, center_y=0):
        """

        :param x:
        :param y:
        :param sigma0:
        :param a:
        :param s:
        :param center_x:
        :param center_y:
        :return:
        """
        f_ = np.zeros_like(x)
        for i in range(len(amp)):
            f_ += self.gaussian.function(x, y, amp[i], sigma[i], sigma[i], center_x, center_y)
        return f_

    def function_split(self, x, y, amp, sigma, center_x=0, center_y=0):
        f_list = []
        for i in range(len(amp)):
            f_list.append(self.gaussian.function(x, y, amp[i], sigma[i], sigma[i], center_x, center_y))
        return f_list

    def light_3d(self, r, amp, sigma):
        """

        :param y:
        :param sigma0:
        :param Rs:
        :param center_x:
        :param center_y:
        :return:
        """
        f_ = np.zeros_like(r)
        for i in range(len(amp)):
            f_ += self.gaussian.light_3d(r, amp[i], sigma[i], sigma[i])
        return f_
