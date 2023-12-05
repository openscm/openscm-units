"""
Definition of our unit registry

See also `docs/source/notebooks/design-principles.py`
"""
from __future__ import annotations

import math
from typing import Any

import globalwarmingpotentials
import pandas as pd
import pint

from openscm_units.data.mixtures import MIXTURES

# Standard gases. If the value is:
# - str: this entry defines a base gas unit
# - list: this entry defines a derived unit
#    - the first entry defines how to convert from base units
#    - other entries define other names i.e. aliases
_STANDARD_GASES: dict[str, str | list[str]] = {
    # CO2, CH4, N2O
    "C": "carbon",
    "CO2": ["12/44 * C", "carbon_dioxide"],
    "CH4": "methane",
    "HC50": ["CH4"],
    "N2O": "nitrous_oxide",
    "N2ON": ["44/28 * N2O", "nitrous_oxide_farming_style"],
    "N": "nitrogen",
    "NO2": ["14/46 * N", "nitrogen_dioxide"],
    # aerosol precursors
    "NOx": "NOx",
    "nox": ["NOx"],
    "NH3": "NH3",
    "ammonia": ["NH3"],
    "S": "sulfur",
    "SO2": ["32/64 * S", "sulfur_dioxide"],
    "SOx": ["SO2"],
    "BC": "black_carbon",
    "OC": "OC",
    "CO": "carbon_monoxide",
    "VOC": "VOC",
    "NMVOC": ["VOC", "non_methane_volatile_organic_compounds"],
    # CFCs
    "CFC11": "CFC11",
    "CFC12": "CFC12",
    "CFC13": "CFC13",
    "CFC113": "CFC113",
    "CFC114": "CFC114",
    "CFC115": "CFC115",
    # hydrocarbons
    "C2H6": "ethane",
    "HC170": ["C2H6"],
    "C3H8": "propane",
    "HC290": ["C3H8"],
    "HC600": "HC600",
    "butane": ["HC600"],
    "HC600a": "HC600a",
    "isobutane": ["HC600a"],
    "HC601": "HC601",
    "pentane": ["HC601"],
    "HC601a": "HC601a",
    "isopentane": ["HC601a"],
    "HCE170": "HCE170",
    "HO1270": "HO1270",
    "propene": ["HO1270"],
    # HCFCs
    "HCFC21": "HCFC21",
    "HCFC22": "HCFC22",
    "HCFC31": "HCFC31",
    "HCFC123": "HCFC123",
    "HCFC124": "HCFC124",
    "HCFC141b": "HCFC141b",
    "HCFC142b": "HCFC142b",
    "HCFC225ca": "HCFC225ca",
    "HCFC225cb": "HCFC225cb",
    # HFCs
    "HFC23": "HFC23",
    "HFC32": "HFC32",
    "HFC41": "HFC41",
    "HFC125": "HFC125",
    "HFC134": "HFC134",
    "HFC134a": "HFC134a",
    "HFC143": "HFC143",
    "HFC143a": "HFC143a",
    "HFC152": "HFC152",
    "HFC152a": "HFC152a",
    "HFC161": "HFC161",
    "HFC227ea": "HFC227ea",
    "HFC236cb": "HFC236cb",
    "HFC236ea": "HFC236ea",
    "HFC236fa": "HFC236fa",
    "HFC245ca": "HFC245ca",
    "HFC245fa": "HFC245fa",
    "HFC365mfc": "HFC365mfc",
    "HFC4310mee": "HFC4310mee",
    "HFC4310": ["HFC4310mee"],
    "HFC1336mzz": "HFC1336mzz",
    # Halogenated gases
    "Halon1201": "Halon1201",
    "Halon1202": "Halon1202",
    "Halon1211": "Halon1211",
    "Halon1301": "Halon1301",
    "Halon2402": "Halon2402",
    # PFCs
    "CF4": "CF4",
    "C2F6": "C2F6",
    "PFC116": ["C2F6"],
    "cC3F6": "cC3F6",
    "C3F8": "C3F8",
    "PFC218": ["C3F8"],
    "cC4F8": "cC4F8",
    "PFCC318": ["cC4F8"],
    "C4F10": "C4F10",
    "C5F12": "C5F12",
    "C6F14": "C6F14",
    "C7F16": "C7F16",
    "C8F18": "C8F18",
    "C10F18": "C10F18",
    # Fluorinated ethers
    "HFE125": "HFE125",
    "HFE134": "HFE134",
    "HFE143a": "HFE143a",
    "HCFE235da2": "HCFE235da2",
    "HFE245cb2": "HFE245cb2",
    "HFE245fa2": "HFE245fa2",
    "HFE347mcc3": "HFE347mcc3",
    "HFE347pcf2": "HFE347pcf2",
    "HFE356pcc3": "HFE356pcc3",
    "HFE449sl": "HFE449sl",
    "HFE569sf2": "HFE569sf2",
    "HFE4310pccc124": "HFE4310pccc124",
    "HFE236ca12": "HFE236ca12",
    "HFE338pcc13": "HFE338pcc13",
    "HFE227ea": "HFE227ea",
    "HFE236ea2": "HFE236ea2",
    "HFE236fa": "HFE236fa",
    "HFE245fa1": "HFE245fa1",
    "HFE263fb2": "HFE263fb2",
    "HFE329mcc2": "HFE329mcc2",
    "HFE338mcf2": "HFE338mcf2",
    "HFE347mcf2": "HFE347mcf2",
    "HFE356mec3": "HFE356mec3",
    "HFE356pcf2": "HFE356pcf2",
    "HFE356pcf3": "HFE356pcf3",
    "HFE365mcf3": "HFE365mcf3",
    "HFE374pc2": "HFE374pc2",
    # Perfluoropolyethers
    "PFPMIE": "PFPMIE",
    # Hydrofluoroolefins
    "HFO1234yf": "HFO1234yf",
    "HFO1234ze": "HFO1234ze",
    # Misc
    "CCl4": "CCl4",
    "CHCl3": "CHCl3",
    "CH2Cl2": "CH2Cl2",
    "CH3CCl3": "CH3CCl3",
    "CH3Cl": "CH3Cl",
    "CH3Br": "CH3Br",
    "SF5CF3": "SF5CF3",
    "SF6": "SF6",
    "SO2F2": "SO2F2",
    "NF3": "NF3",
    "HCO1130": "HCO1130",
}


class ScmUnitRegistry(pint.UnitRegistry):
    """
    Unit registry class.

    Provides some convenience methods to add standard units and contexts.
    """

    _contexts_added = False

    def __init__(
        self,
        *args: Any,
        metric_conversions: pd.DataFrame | None = None,
        **kwargs: Any,
    ):
        """
        Initialise the unit registry

        Parameters
        ----------
        metric_conversions
            :obj:`pd.DataFrame` containing the metric conversions.
            ``metric_conversions`` must have an index named ``"Species"`` that
            contains the different species and columns which contain the
            conversion for different metrics (the name of the metrics is taken
            from the column names).If not supplied, the
            ``globalwarmingpotentials`` package is used.

        *args
            Passed to the ``__init__`` method of the super class

        **kwargs
            Passed to the ``__init__`` method of the super class
        """
        self._metric_conversions = metric_conversions
        # If we didn't call init here, we wouldn't need to rebuild the cache
        # below but that also feels like a bad pattern
        super().__init__(*args, **kwargs)

    def add_standards(self) -> None:
        """
        Add standard units.

        Has to be done separately because of pint's weird initialising.
        """
        self._add_gases(_STANDARD_GASES)

        self._add_gases({x: x for x in MIXTURES})

        self.define("a = 1 * year = annum = yr")
        self.define("h = hour")
        self.define("d = day")
        self.define("degreeC = degC")
        self.define("degreeF = degF")
        self.define("kt = 1000 * t")  # since kt is used for "knot" in the defaults
        self.define(
            "Tt = 1000000000000 * t"
        )  # since Tt is used for "tex" in the defaults

        self.define("ppm = [concentrations]")
        self.define("ppb = ppm / 1000")
        self.define("ppt = ppb / 1000")
        # Have to rebuild cache to get right units for ppm as it is defined in
        # pint
        self._build_cache()

    def enable_contexts(
        self,
        *names_or_contexts: str | pint.facets.context.objects.Context,
        **kwargs: Any,
    ) -> None:
        """
        Overload pint's :func:`enable_contexts`

        This ensures we only add contexts once (the first time they are used)
        to avoid (unnecessary) operations.

        Parameters
        ----------
        names_or_contexts
            Names of contexts or :obj:`pint.registry.UnitRegistry.Context`
            objects to enable

        kwargs
            Passed to :meth:`enable_contexts` of the parent class
        """
        if not self._contexts_added:
            self._add_contexts()
        self._contexts_added = True
        super().enable_contexts(*names_or_contexts, **kwargs)

    def _add_mass_emissions_joint_version(self, symbol: str) -> None:
        """
        Add a unit which is the combination of mass and emissions.

        This allows users to units like e.g. ``"tC"`` rather than requiring a
        space between the mass and the emissions i.e. ``"t C"``

        Parameters
        ----------
        symbol
            The unit to add a joint version for
        """
        self.define("g{symbol} = g * {symbol}".format(symbol=symbol))
        self.define("t{symbol} = t * {symbol}".format(symbol=symbol))

    def _add_gases(self, gases: dict[str, str | list[str]]) -> None:
        for symbol, value in gases.items():
            if isinstance(value, str):
                # symbol is base unit
                self.define(f"{symbol} = [{value}]")
                if value != symbol:
                    self.define(f"{value} = {symbol}")
            else:
                # symbol has conversion and aliases
                self.define(f"{symbol} = {value[0]}")
                for alias in value[1:]:
                    self.define(f"{alias} = {symbol}")

            self._add_mass_emissions_joint_version(symbol)

            # Add alias for upper case symbol:
            if symbol.upper() != symbol:
                self.define(f"{symbol.upper()} = {symbol}")
                self._add_mass_emissions_joint_version(symbol.upper())

    def _add_contexts(self) -> None:
        """
        Add contexts
        """
        _ch4_context = pint.Context("CH4_conversions")
        _ch4_context = self._add_transformations_to_context(
            _ch4_context,
            "[methane]",
            self.CH4,
            "[carbon]",
            self.C,
            12 / 16,
        )
        self.add_context(_ch4_context)

        _n2o_context = pint.Context("N2O_conversions")
        _n2o_context = self._add_transformations_to_context(
            _n2o_context,
            "[nitrous_oxide]",
            self.nitrous_oxide,
            "[nitrogen]",
            self.nitrogen,
            14 / 44,
        )
        self.add_context(_n2o_context)

        _nox_context = pint.Context("NOx_conversions")
        _nox_context = self._add_transformations_to_context(
            _nox_context,
            "[nitrogen]",
            self.nitrogen,
            "[NOx]",
            self.NOx,
            (14 + 2 * 16) / 14,
        )
        self.add_context(_nox_context)

        _nh3_context = pint.Context("NH3_conversions")
        _nh3_context = self._add_transformations_to_context(
            _nh3_context,
            "[nitrogen]",
            self.nitrogen,
            "[NH3]",
            self.NH3,
            (14 + 3) / 14,
        )
        self.add_context(_nh3_context)

        self._add_metric_conversions()

    def _add_metric_conversions(self) -> None:
        """
        Add metric conversion contexts
        """
        if self._metric_conversions is None:
            metric_conversions = globalwarmingpotentials.as_frame()
        else:
            metric_conversions = self._metric_conversions

        self._add_metric_conversions_from_df(metric_conversions)

    def _add_metric_conversions_from_df(self, metric_conversions: pd.DataFrame) -> None:
        # could make this public in future
        for col in metric_conversions:
            metric_conversion: pd.Series[float] = metric_conversions[col]
            transform_context = pint.Context(str(col))
            for label, val in metric_conversion.items():
                transform_context = self._add_gwp_to_context(
                    transform_context, str(label), val
                )

            for mixture in MIXTURES:
                constituents = self.split_gas_mixture(1 * self(mixture))
                try:
                    val = sum(
                        c.magnitude * metric_conversion[str(c.units)]
                        for c in constituents
                    )
                except KeyError:  # gwp not available for all constituents
                    continue
                if math.isnan(val):
                    continue
                transform_context = self._add_gwp_to_context(
                    transform_context, mixture, val
                )

            self.add_context(transform_context)

    def _add_gwp_to_context(
        self,
        transform_context: pint.facets.context.objects.Context,
        label: str,
        val: float,
    ) -> pint.facets.context.objects.Context:
        conv_val = (
            val
            * (self("CO2").to_base_units()).magnitude
            / (self(label).to_base_units()).magnitude
        )
        base_unit = next(
            iter(self._get_dimensionality(self(label).to_base_units()._units).keys())
        )

        base_unit_ureg = self(base_unit.replace("[", "").replace("]", ""))

        return self._add_transformations_to_context(
            transform_context,
            base_unit,
            base_unit_ureg,
            "[carbon]",
            self("carbon"),
            conv_val,
        )

    @staticmethod
    def _add_transformations_to_context(  # noqa: PLR0913
        context: pint.facets.context.objects.Context,
        base_unit: str,
        base_unit_ureg: pint.registry.UnitRegistry.Unit
        | pint.registry.UnitRegistry.Quantity,
        other_unit: str,
        other_unit_ureg: pint.registry.UnitRegistry.Unit
        | pint.registry.UnitRegistry.Quantity,
        conv_val: float,
    ) -> pint.facets.context.objects.Context:
        """
        Add all the transformations between units to a context for the two given units

        Transformations are mass x unit per time, mass x unit etc.
        """

        def _get_transform_func(
            forward: bool,
        ) -> pint.facets.context.objects.Transformation:
            if forward:

                def result_forward(
                    ureg: pint.registry.UnitRegistry,
                    value: pint.registry.UnitRegistry.Quantity,
                    **kwargs: Any,
                ) -> pint.registry.UnitRegistry.Quantity:
                    out: pint.registry.UnitRegistry.Quantity = (
                        value * other_unit_ureg / base_unit_ureg * conv_val
                    )

                    return out

                return result_forward  # type: ignore # cannot make pint behave

            def result_backward(
                ureg: pint.registry.UnitRegistry,
                value: pint.registry.UnitRegistry.Quantity,
                **kwargs: Any,
            ) -> pint.registry.UnitRegistry.Quantity:
                out: pint.registry.UnitRegistry.Quantity = (
                    value * (base_unit_ureg / other_unit_ureg) / conv_val
                )

                return out

            return result_backward  # type: ignore # cannot make pint behave

        formatters = [
            "{}",
            "[mass] * {} / [time]",
            "[mass] * {}",
            "{} / [time]",
        ]
        for fmt_str in formatters:
            context.add_transformation(
                fmt_str.format(base_unit),
                fmt_str.format(other_unit),
                _get_transform_func(forward=True),
            )
            context.add_transformation(
                fmt_str.format(other_unit),
                fmt_str.format(base_unit),
                _get_transform_func(forward=False),
            )

        return context

    def split_gas_mixture(
        self, quantity: pint.Quantity
    ) -> list[pint.registry.UnitRegistry.Quantity]:
        """
        Split a gas mixture into constituent gases.

        Parameters
        ----------
        quantity
            Pint quantity to split

        Returns
        -------
            List of constituent gases
        """
        mixture_dimensions = [
            x for x in quantity.dimensionality.keys() if x[1:-1] in MIXTURES
        ]
        if not mixture_dimensions:
            raise ValueError("Dimensions don't contain a gas mixture.")  # noqa: TRY003
        if len(mixture_dimensions) > 1:
            raise NotImplementedError(  # noqa: TRY003
                "More than one gas mixture in dimensions is not supported."
            )
        mixture_dimension = mixture_dimensions[0]
        if quantity.dimensionality[mixture_dimension] != 1:
            raise NotImplementedError(  # noqa: TRY003
                f"Mixture has dimensionality {quantity.dimensionality[mixture_dimension]}"
                " != 1, which is not supported."
            )

        mixture = MIXTURES[mixture_dimension[1:-1]]
        mixture_unit = self(mixture_dimension[1:-1])

        ret = []
        for constituent, (fraction_pct, _, _) in mixture.items():
            constituent_unit = self(constituent)
            ret.append(quantity / mixture_unit * fraction_pct / 100 * constituent_unit)

        return ret
