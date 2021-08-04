import os.path

import numpy as np
import pandas as pd

from openscm_units import ScmUnitRegistry


def test_custom_context_csv(test_data_dir):
    custom_context_csv = os.path.join(test_data_dir, "custom-context.csv")
    metric_conversions = pd.read_csv(
        custom_context_csv,
        skiprows=1,  # skip source row
        header=0,
        index_col=0,
    )

    unit_registry = ScmUnitRegistry(metric_conversions=metric_conversions)
    unit_registry.add_standards()

    nitrous_oxide = unit_registry("N2O")
    methane = unit_registry("CH4")

    with unit_registry.context("TestCustomContext"):
        np.testing.assert_allclose(nitrous_oxide.to("CO2").magnitude, 345)
        np.testing.assert_allclose(methane.to("CO2").magnitude, 22)

    with unit_registry.context("SARGWP100"):
        np.testing.assert_allclose(nitrous_oxide.to("CO2").magnitude, 310)
        np.testing.assert_allclose(methane.to("CO2").magnitude, 21)


def test_custom_context():
    metric_conversions_custom = pd.DataFrame(
        [
            {
                "Species": "CH4",
                "Custom1": 20,
                "Custom2": 25,
            },
            {
                "Species": "N2O",
                "Custom1": 341,
                "Custom2": 300,
            },
        ]
    ).set_index("Species")

    unit_registry = ScmUnitRegistry(metric_conversions=metric_conversions_custom)
    unit_registry.add_standards()

    nitrous_oxide = unit_registry("N2O")
    methane = unit_registry("CH4")

    with unit_registry.context("Custom1"):
        np.testing.assert_allclose(nitrous_oxide.to("CO2").magnitude, 341)
        np.testing.assert_allclose(methane.to("CO2").magnitude, 20)

    with unit_registry.context("Custom2"):
        np.testing.assert_allclose(nitrous_oxide.to("CO2").magnitude, 300)
        np.testing.assert_allclose(methane.to("CO2").magnitude, 25)
