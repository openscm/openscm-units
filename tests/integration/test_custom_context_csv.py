import os.path

import numpy as np

from openscm_units import ScmUnitRegistry


def test_custom_context_csv(test_data_dir):
    custom_context_csv = os.path.join(test_data_dir, "custom-context.csv")

    unit_registry = ScmUnitRegistry(metric_conversions_csv=custom_context_csv)
    unit_registry.add_standards()

    nitrous_oxide = unit_registry("N2O")
    methane = unit_registry("CH4")

    with unit_registry.context("TestCustomContext"):
        np.testing.assert_allclose(nitrous_oxide.to("CO2").magnitude, 345)
        np.testing.assert_allclose(methane.to("CO2").magnitude, 22)

    with unit_registry.context("SARGWP100"):
        np.testing.assert_allclose(nitrous_oxide.to("CO2").magnitude, 310)
        np.testing.assert_allclose(methane.to("CO2").magnitude, 21)
