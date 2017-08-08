__author__ = 'sibirrer'

import pytest
import numpy.testing as npt
import numpy as np

from astrofunc.numerical_profile_integrals import ProfileIntegrals


class TestNumerics(object):
    """
    tests the second derivatives of various lens models
    """
    def setup(self):
        pass

    def assert_integrals(self, Model, kwargs):
        lensModel = Model()
        int_profile = ProfileIntegrals(lensModel)
        r = 2.

        density2d_num = int_profile.density_2d(r, kwargs)
        density2d = lensModel.density_2d(r, 0, **kwargs)
        npt.assert_almost_equal(density2d/density2d_num, 1., decimal=1)

        mass_2d_num = int_profile.mass_enclosed_2d(r, kwargs)
        mass_2d = lensModel.mass_2d(r, **kwargs)
        npt.assert_almost_equal(mass_2d/mass_2d_num, 1, decimal=1)

        mass_3d_num = int_profile.mass_enclosed_3d(r, kwargs)
        mass_3d = lensModel.mass_3d(r, **kwargs)
        npt.assert_almost_equal(mass_3d/mass_3d_num, 1, decimal=2)

    def test_PJaffe(self):
        kwargs = {'rho0': 1., 'Ra': 0.2, 'Rs': 2.}
        from astrofunc.LensingProfiles.p_jaffe import PJaffe as Model
        self.assert_integrals(Model, kwargs)

    def test_PJaffa_density_deflection(self):
        """
        tests whether the unit conversion between the lensing parameter 'sigma0' and the units in the density profile are ok
        :return:
        """

        from astrofunc.LensingProfiles.p_jaffe import PJaffe as Model
        lensModel = Model()
        sigma0 = 1.
        Ra = 0.2
        Rs = 2.
        rho0 = lensModel.sigma2rho(sigma0, Ra, Rs)
        kwargs_lens = {'sigma0': sigma0, 'Ra': Ra, 'Rs': Rs}
        kwargs_density = {'rho0': rho0, 'Ra': Ra, 'Rs': Rs}
        r = 1.
        mass_2d = lensModel.mass_2d(r, **kwargs_density)
        alpha_mass = mass_2d/r
        alpha_r, _ = lensModel.derivatives(r, 0, **kwargs_lens)
        npt.assert_almost_equal(alpha_mass/np.pi, alpha_r, decimal=5)

    def test_nfw(self):
        kwargs = {'rho0': 1.,  'Rs': 5.}
        from astrofunc.LensingProfiles.nfw import NFW as Model
        self.assert_integrals(Model, kwargs)

    def test_nfw_density_deflection(self):
        """
        tests whether the unit conversion between the lensing parameter 'sigma0' and the units in the density profile are ok
        :return:
        """

        from astrofunc.LensingProfiles.nfw import NFW as Model
        lensModel = Model()
        theta_Rs = 1.
        Rs = 2.
        rho0 = lensModel._alpha2rho0(theta_Rs, Rs)
        kwargs_lens = {'theta_Rs': theta_Rs, 'Rs': Rs}
        kwargs_density = {'rho0': rho0, 'Rs': Rs}
        r = 1.
        mass_2d = lensModel.mass_2d(r, **kwargs_density)
        alpha_mass = mass_2d/r
        alpha_r, _ = lensModel.derivatives(r, 0, **kwargs_lens)
        npt.assert_almost_equal(alpha_mass/np.pi, alpha_r, decimal=5)

    def test_hernquist(self):
        kwargs = {'rho0': 1.,  'Rs': 5.}
        from astrofunc.LensingProfiles.hernquist import Hernquist as Model
        self.assert_integrals(Model, kwargs)

    def test_hernquist_density_deflection(self):
        """
        tests whether the unit conversion between the lensing parameter 'sigma0' and the units in the density profile are ok
        :return:
        """

        from astrofunc.LensingProfiles.hernquist import Hernquist as Model
        lensModel = Model()
        sigma0 = 1.
        Rs = 2.
        rho0 = lensModel.sigma2rho(sigma0, Rs)
        kwargs_lens = {'sigma0': sigma0, 'Rs': Rs}
        kwargs_density = {'rho0': rho0, 'Rs': Rs}
        r = .5
        mass_2d = lensModel.mass_2d(r, **kwargs_density)
        alpha_mass = mass_2d/r
        alpha_r, _ = lensModel.derivatives(r, 0, **kwargs_lens)
        npt.assert_almost_equal(alpha_mass/np.pi, alpha_r, decimal=5)

    def test_spp(self):
        from astrofunc.LensingProfiles.spp import SPP as Model
        kwargs = {'rho0': 10., 'gamma': 2.2}
        self.assert_integrals(Model, kwargs)

        kwargs = {'rho0': 1., 'gamma': 2.0}
        self.assert_integrals(Model, kwargs)

    def test_spp_density_deflection(self):
        """
        tests whether the unit conversion between the lensing parameter 'sigma0' and the units in the density profile are ok
        :return:
        """

        from astrofunc.LensingProfiles.spp import SPP as Model
        lensModel = Model()
        theta_E = 1.
        gamma = 2.2
        rho0 = lensModel.theta2rho(theta_E, gamma)
        kwargs_lens = {'theta_E': theta_E, 'gamma': gamma}
        kwargs_density = {'rho0': rho0, 'gamma': gamma}
        r = .5
        mass_2d = lensModel.mass_2d(r, **kwargs_density)
        alpha_mass = mass_2d/r
        alpha_r, _ = lensModel.derivatives(r, 0, **kwargs_lens)
        npt.assert_almost_equal(alpha_mass/np.pi, alpha_r, decimal=5)

    """



    def test_gaussian(self):
        kwargs = {'amp': 1. / 4., 'sigma_x': 2., 'sigma_y': 2., 'center_x': 0., 'center_y': 0.}
        from astrofunc.LensingProfiles.gaussian import Gaussian as Model
        self.assert_integrals(Model, kwargs)

    def test_sis(self):
        kwargs = {'theta_E': 0.5}
        from astrofunc.LensingProfiles.sis import SIS as Model
        self.assert_integrals(Model, kwargs)

    def test_sersic(self):
        kwargs = {'n_sersic': .5, 'r_eff': 1.5, 'k_eff': 0.3}
        from astrofunc.LensingProfiles.sersic import Sersic as Model
        self.assert_integrals(Model, kwargs)

    """

if __name__ == '__main__':
    pytest.main("-k TestLensModel")