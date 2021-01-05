import re

import numpy as np
import pytest
from pint.errors import DimensionalityError

from openscm_units import unit_registry
from openscm_units.data.mixtures import MIXTURES


def test_unit_registry():
    CO2 = unit_registry("CO2")
    np.testing.assert_allclose(CO2.to("C").magnitude, 12 / 44)


def test_alias():
    CO2 = unit_registry("carbon_dioxide")
    np.testing.assert_allclose(CO2.to("C").magnitude, 12 / 44)


def test_base_unit():
    assert unit_registry("carbon") == unit_registry("C")


def test_nitrogen():
    N = unit_registry("N")
    np.testing.assert_allclose(N.to("N2ON").magnitude, 28 / 14)
    np.testing.assert_allclose(N.to("NO2").magnitude, 46 / 14)


def test_nox():
    NOx = unit_registry("NOx")

    # can only convert to N with right context
    with pytest.raises(DimensionalityError):
        NOx.to("N")

    N = unit_registry("N")
    NO2 = unit_registry("NO2")
    with unit_registry.context("NOx_conversions"):
        np.testing.assert_allclose(NOx.to("N").magnitude, 14 / 46)
        np.testing.assert_allclose(N.to("NOx").magnitude, 46 / 14)
        np.testing.assert_allclose(NO2.to("NOx").magnitude, 1)
        np.testing.assert_allclose(NOx.to("NO2").magnitude, 1)
        # this also becomes allowed, unfortunately...
        np.testing.assert_allclose(NOx.to("N2O").magnitude, 44 / 46)


def test_methane():
    CH4 = unit_registry("CH4")
    with pytest.raises(DimensionalityError):
        CH4.to("C")

    C = unit_registry("C")
    with unit_registry.context("CH4_conversions"):
        np.testing.assert_allclose(CH4.to("C").magnitude, 12 / 16)
        np.testing.assert_allclose(C.to("CH4").magnitude, 16 / 12)
        # this also becomes allowed, unfortunately...
        np.testing.assert_allclose(CH4.to("CO2").magnitude, 44 / 16)


def test_ppm():
    ppm = unit_registry("ppm")
    np.testing.assert_allclose(ppm.to("ppb").magnitude, 1000)


def test_ppt():
    ppt = unit_registry("ppt")
    np.testing.assert_allclose(ppt.to("ppb").magnitude, 1 / 1000)


def test_short_definition():
    tC = unit_registry("tC")
    np.testing.assert_allclose(tC.to("tCO2").magnitude, 44 / 12)
    np.testing.assert_allclose(tC.to("gC").magnitude, 10 ** 6)


def test_uppercase():
    tC = unit_registry("HFC4310MEE")
    np.testing.assert_allclose(tC.to("HFC4310mee").magnitude, 1)


def test_emissions_flux():
    tOC = unit_registry("tOC/day")
    np.testing.assert_allclose(tOC.to("tOC/hr").magnitude, 1 / 24)


@pytest.mark.parametrize(
    "prefix_start,prefix_end,factor",
    (
        ("Tt", "Tt", 10 ** 0),
        ("Tt", "Gt", 10 ** 3),
        ("Tt", "Mt", 10 ** 6),
        ("Tt", "kt", 10 ** 9),
        ("Gt", "Gt", 10 ** 0),
        ("Gt", "Mt", 10 ** 3),
        ("Gt", "kt", 10 ** 6),
        ("Gt", "t", 10 ** 9),
        ("Mt", "Mt", 10 ** 0),
        ("Mt", "kt", 10 ** 3),
        ("Mt", "t", 10 ** 6),
        ("kt", "kt", 10 ** 0),
        ("kt", "t", 10 ** 3),
        ("t", "t", 10 ** 0),
    ),
)
def test_emissions_prefix(prefix_start, prefix_end, factor):
    tCO2 = unit_registry("{} CO2/yr".format(prefix_start))
    np.testing.assert_allclose(
        tCO2.to("{} CO2/yr".format(prefix_end)).magnitude, factor
    )


def test_kt():
    kt = unit_registry("kt")
    np.testing.assert_allclose(kt.to("t").magnitude, 1000)


def test_h():
    h = unit_registry("h")
    np.testing.assert_allclose(h.to("min").magnitude, 60)


def test_a():
    a = unit_registry("a")
    np.testing.assert_allclose(a.to("day").magnitude, 365.25, rtol=1e-4)


def test_context():
    CO2 = unit_registry("CO2")
    N = unit_registry("N")
    with unit_registry.context("AR4GWP100"):
        np.testing.assert_allclose(CO2.to("N").magnitude, 14 / (44 * 298))
        np.testing.assert_allclose(N.to("CO2").magnitude, 44 * 298 / 14)


def test_context_with_magnitude():
    CO2 = 1 * unit_registry("CO2")
    N = 1 * unit_registry("N")
    with unit_registry.context("AR4GWP100"):
        np.testing.assert_allclose(CO2.to("N").magnitude, 14 / (44 * 298))
        np.testing.assert_allclose(N.to("CO2").magnitude, 44 * 298 / 14)


def test_context_compound_unit():
    CO2 = 1 * unit_registry("kg CO2 / yr")
    N = 1 * unit_registry("kg N / yr")
    with unit_registry.context("AR4GWP100"):
        np.testing.assert_allclose(CO2.to("kg N / yr").magnitude, 14 / (44 * 298))
        np.testing.assert_allclose(N.to("kg CO2 / yr").magnitude, 44 * 298 / 14)


def test_context_dimensionality_error():
    CO2 = unit_registry("CO2")
    with pytest.raises(DimensionalityError):
        CO2.to("N")


@pytest.mark.parametrize(
    "metric_name,species,conversion",
    (
        ["AR4GWP100", "CH4", 25],
        ["AR4GWP100", "N2O", 298],
        ["AR4GWP100", "CCl4", 1400],
        ["AR4GWP100", "HFC32", 675],
        ["AR4GWP100", "SF6", 22800],
        ["AR4GWP100", "C2F6", 12200],
        ["AR4GWP100", "HCFC142b", 2310],
        ["AR4GWP100", "HFC32", 675],
        ["AR4GWP100", "cC4F8", 10300],
        ["AR4GWP100", "cC4F8", 10300],
        ["AR4GWP100", "HFE356pcc3", 413],
        ["AR4GWP100", "CH2Cl2", 8.7],
        ["AR5GWP100", "C7F16", 7820],
        ["AR5GWP100", "C8F18", 7620],
        ["AR5GWP100", "SO2F2", 4090],
        ["SARGWP100", "CH4", 21],
        ["SARGWP100", "N2O", 310],
        ["SARGWP100", "HFC32", 650],
        ["SARGWP100", "SF6", 23900],
        ["SARGWP100", "CF4", 6500],
        ["SARGWP100", "C2F6", 9200],
    ),
)
def test_metric_conversion(metric_name, species, conversion):
    base_str_formats = ["{}", "kg {} / yr", "kg {}", "{} / yr"]
    for base_str_format in base_str_formats:
        base = unit_registry(base_str_format.format(species))
        dest = unit_registry(base_str_format.format("CO2"))
        with unit_registry.context(metric_name):
            np.testing.assert_allclose(base.to(dest).magnitude, conversion)
            np.testing.assert_allclose(dest.to(base).magnitude, 1 / conversion)


@pytest.mark.parametrize(
    "metric_name,mixture,conversion",
    (
        # mixtures that are automatically derived, final values from wikipedia
        ["AR4GWP100", "CFC400", 10_450],
        ["AR4GWP100", "HCFC401a", 1_182],
        ["AR4GWP100", "HCFC401b", 1_288],
        ["AR4GWP100", "HCFC401c", 933],
        ["AR4GWP100", "HFC404a", 3_922],
        # ["AR4GWP100", "HCFC406b", 1_893],  # mixture not yet in mixtures.yaml
        ["AR4GWP100", "HFC407a", 2_107],
        ["AR4GWP100", "HFC407b", 2_804],
        ["AR4GWP100", "HFC407c", 1_774],
        ["AR4GWP100", "HFC407d", 1_627],
        ["AR4GWP100", "HFC407e", 1_552],
        ["AR4GWP100", "HFC407f", 1_825],
        ["AR4GWP100", "HCFC408a", 3_152],
        ["AR4GWP100", "HCFC409a", 1_585],
        ["AR4GWP100", "HCFC409b", 1_560],
        ["AR4GWP100", "HFC410a", 2_088],
        ["AR4GWP100", "HFC410b", 2_229],
        # ["AR4GWP100", "HCFO411c", 1_730],  # mixture not yet in mixtures.yaml
        ["AR4GWP100", "HCFC412a", 2_286],
        ["AR4GWP100", "HCFC415a", 1_507],
        ["AR4GWP100", "HCFC415b", 546],
        # ["AR5GWP100", "HCFC420a", 1_548], inconsistent in wp
        ["AR4GWP100", "HFC421a", 2_631],
        ["AR4GWP100", "HFC421b", 3_190],
        ["AR4GWP100", "HFC423a", 2_280],
        ["AR4GWP100", "HFC425a", 1_505],
        ["AR4GWP100", "HFC427a", 2_138],
        ["AR4GWP100", "HFC458a", 1_650],
        ["AR4GWP100", "HCFC501", 4_083],
        ["AR4GWP100", "HCFC502", 4_657],
        ["AR4GWP100", "HCFC503", 14_560],
        ["AR4GWP100", "HCFC504", 4_143],
        ["AR4GWP100", "HFC507a", 3_985],
        ["AR4GWP100", "HFC508a", 13_214],
        ["AR4GWP100", "HFC508b", 13_396],
        ["AR4GWP100", "HCFC509a", 5_741],
        # ["AR4GWP100", "HFO515b", 299],  # mixture not yet in mixtures.yaml
    ),
)
def test_mixture_conversion(metric_name, mixture, conversion):
    gwp = (1 * unit_registry(mixture)).to("CO2", metric_name).magnitude
    # wikipedia values are rounded, therefore atol
    np.testing.assert_allclose(conversion, gwp, atol=0.5)


@pytest.mark.parametrize(
    "metric_name,mixture,conversion",
    (
        # mixtures for which the constituents are not reported in SAR/AR4/AR5
        # wikipedia has values nevertheless, so might come in future ARs
        ["AR4GWP100", "HCFC402a", 2_788],
        ["AR4GWP100", "HCFC402b", 2_416],
        ["AR4GWP100", "HCFC403a", 3_124],
        ["AR4GWP100", "HCFC403b", 4_457],
        ["AR4GWP100", "HCFC405a", 5_328],
        ["AR4GWP100", "HCFC406a", 1_943],
        ["AR4GWP100", "HCFO411a", 1_597],
        ["AR4GWP100", "HCFO411b", 1_705],
        ["AR4GWP100", "HFC413a", 2_053],
        ["AR4GWP100", "HCFC414a", 1_478],
        ["AR4GWP100", "HCFC414b", 1_362],
        ["AR4GWP100", "HCFC416a", 1_084],
        ["AR4GWP100", "HFC417a", 2_346],
        ["AR4GWP100", "HFC417b", 3_027],
        ["AR4GWP100", "HCFC418a", 1_741],
        ["AR4GWP100", "HFC419a", 2_967],
        ["AR4GWP100", "HFC422b", 2_526],
        ["AR4GWP100", "HFC422c", 3_085],
        ["AR4GWP100", "HFC422d", 2_729],
        ["AR4GWP100", "HFC424a", 2_440],
        ["AR4GWP100", "HFC426a", 1_508],
        ["AR4GWP100", "HFC428a", 3_607],
        ["AR4GWP100", "HFC429a", 13.9],
        ["AR4GWP100", "HFC430a", 95],
        ["AR4GWP100", "HFC431a", 38.3],
        ["AR4GWP100", "HO432a", 1.64],
        ["AR4GWP100", "HO433a", 2.85],
        ["AR4GWP100", "HO433b", 3.23],
        ["AR4GWP100", "HO433c", 2.93],
        ["AR4GWP100", "HFC434a", 3_245],
        ["AR4GWP100", "HFC435a", 25.6],
        ["AR4GWP100", "HC436a", 3.17],
        ["AR4GWP100", "HC436b", 3.16],
        ["AR4GWP100", "HFC437a", 1_805],
        ["AR4GWP100", "HFC438a", 2_265],
        ["AR4GWP100", "HFC439a", 1_983],
        ["AR4GWP100", "HFC440a", 144],
        ["AR4GWP100", "HC441a", 3.6],
        ["AR4GWP100", "HFO448a", 1_273],
        ["AR4GWP100", "HFO449a", 1_282],
        ["AR4GWP100", "HFO452b", 676],
        ["AR4GWP100", "HFO454a", 239],
        ["AR4GWP100", "HFO454b", 466],
        ["AR4GWP100", "HFO454c", 148],
        ["AR4GWP100", "HFO455a", 146],
        ["AR4GWP100", "HFO456a", 687],
        ["AR4GWP100", "HFO457a", 139],
        ["AR4GWP100", "HFO459a", 460],
        ["AR4GWP100", "HCFC500", 8_077],
        ["AR4GWP100", "HCFC506", 4_495],
        ["AR4GWP100", "HC510a", 1.24],
        ["AR4GWP100", "HC511a", 3.19],
        ["AR4GWP100", "HFO513a", 573],
    ),
)
def test_mixtures_constituents_no_gwp(metric_name, mixture, conversion):
    error_msg = re.escape(
        f"Cannot convert from '{mixture}' ([{mixture}]) to 'CO2' ([carbon])"
    )
    with pytest.raises(DimensionalityError, match=error_msg):
        gwp = (  # noqa: F841
            (1 * unit_registry(mixture)).to("CO2", metric_name).magnitude
        )


def test_mixture_constituent_sum_one():
    for mixture in MIXTURES:
        constituents = unit_registry.split_gas_mixture(1 * unit_registry(mixture))
        np.testing.assert_allclose(sum((c.magnitude for c in constituents)), 1)


def test_split_invalid():
    with pytest.raises(ValueError, match="Dimensions don't contain a gas mixture."):
        unit_registry.split_gas_mixture(1 * unit_registry("CO2"))

    with pytest.raises(
        NotImplementedError,
        match="More than one gas mixture in dimensions is not supported.",
    ):
        unit_registry.split_gas_mixture(
            1 * unit_registry("CFC400") * unit_registry("HFC423a")
        )

    with pytest.raises(
        NotImplementedError,
        match="Mixture has dimensionality 2 != 1, which is not supported.",
    ):
        unit_registry.split_gas_mixture(1 * unit_registry("CFC400") ** 2)
