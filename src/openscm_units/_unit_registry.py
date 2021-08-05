"""
Unit handling makes use of the `Pint <https://github.com/hgrecco/pint>`_ library. This
allows us to easily define units as well as contexts. Contexts allow us to perform
conversions which would not normally be allowed e.g. in the 'AR4GWP100'
context we can convert from CO2 to CH4 using the AR4GWP100 equivalence metric.

An illustration of how the ``unit_registry`` can be used is shown below:

.. code:: python

    >>> from openscm_units import unit_registry
    >>> unit_registry("CO2")
    <Quantity(1, 'CO2')>

    >>> emissions_aus = 0.34 * unit_registry("Gt C / yr")
    >>> emissions_aus
    <Quantity(0.34, 'C * gigametric_ton / a')>

    >>> emissions_aus.to("Mt CO2 / yr")
    <Quantity(1246.666666666667, 'CO2 * megametric_ton / a')>

    >>> with unit_registry.context("AR4GWP100"):
    ...     (100 * unit_registry("Mt CH4 / yr")).to("Mt CO2 / yr")
    <Quantity(2500.0, 'CO2 * megametric_ton / a')>

**More details on emissions units**

Emissions are a flux composed of three parts: mass, the species being emitted and the
time period e.g. "t CO2 / yr". As mass and time are part of SI units, all we need to
define here are emissions units i.e. the stuff. Here we include as many of the canonical
emissions units, and their conversions, as possible.

For emissions units, there are a few cases to be considered:

- fairly obvious ones e.g. carbon dioxide emissions can be provided in 'C' or 'CO2' and
  converting between the two is possible
- less obvious ones e.g. NOx emissions can be provided in 'N' or 'NOx' (a short-hand
  which is assumed to be NO2), we provide conversions between these two
- case-sensitivity. In order to provide a simplified interface, using all uppercase
  versions of any unit is also valid e.g. ``unit_registry("HFC4310mee")`` is the same as
  ``unit_registry("HFC4310MEE")``
- hyphens and underscores in units. In order to be Pint compatible and to simplify
  things, we strip all hyphens and underscores from units.

As a convenience, we allow users to combine the mass and the type of emissions to make a
'joint unit' e.g. "tCO2". It should be recognised that this joint unit is a derived
unit and not a base unit.

By defining these three separate components, it is much easier to track what conversions
are valid and which are not. For example, as the emissions units are all defined as
emissions units, and not as atomic masses, we are able to prevent invalid conversions.
If emissions units were simply atomic masses, it would be possible to convert between
e.g. C and N2O which would be a problem. Conventions such as allowing carbon dioxide
emissions to be reported in C or CO2, despite the fact that they are fundamentally
different chemical species, is a convention which is particular to emissions (as far as
we can tell).

Pint's contexts are particularly useful for emissions as they facilitate
metric conversions. With a context, a conversion which wouldn't normally be allowed
(e.g. tCO2 --> tN2O) is allowed and will use whatever metric conversion is appropriate
for that context (e.g. AR4GWP100).

Finally, we discuss namespace collisions.

*CH4*

Methane emissions are defined as 'CH4'. In order to prevent inadvertent conversions of
'CH4' to e.g. 'CO2' via 'C', the conversion 'CH4' <--> 'C' is by default forbidden.
However, it can be performed within the context 'CH4_conversions' as shown below:

.. code:: python

    >>> from openscm_units import unit_registry
    >>> unit_registry("CH4").to("C")
    pint.errors.DimensionalityError: Cannot convert from 'CH4' ([methane]) to 'C' ([carbon])

    # with a context, the conversion becomes legal again
    >>> with unit_registry.context("CH4_conversions"):
    ...     unit_registry("CH4").to("C")
    <Quantity(0.75, 'C')>

    # as an unavoidable side effect, this also becomes possible
    >>> with unit_registry.context("CH4_conversions"):
    ...     unit_registry("CH4").to("CO2")
    <Quantity(2.75, 'CO2')>

*N2O*

Nitrous oxide emissions are typically reported with units of 'N2O'. However,
they are also reported with units of 'N2ON' (a short-hand which indicates that
only the mass of the nitrogen is being counted). Reporting nitrous oxide
emissions with units of simply 'N' is ambiguous (do you mean the mass of
nitrogen, so 1 N = 28 / 44 N2O or just the mass of a single N atom, so
1 N = 14 / 44 N2O). By default, converting 'N2O' <--> 'N' is forbidden to
prevent this ambiguity. However, the conversion can be performed within the
context 'N2O_conversions', in which case it is assumed that 'N' just means a
single N atom i.e. 1 N = 14 / 44 N2O, as shown below:

.. code:: python

    >>> from openscm_units import unit_registry
    >>> unit_registry("N2O").to("N")
    pint.errors.DimensionalityError: Cannot convert from 'N2O' ([nitrous_oxide]) to 'N' ([nitrogen])

    # with a context, the conversion becomes legal again
    >>> with unit_registry.context("N2O_conversions"):
    ...     unit_registry("N2O").to("N")
    <Quantity(0.318181818, 'N')>

*NOx*

Like for methane, NOx emissions also suffer from a namespace collision. In order to
prevent inadvertent conversions from 'NOx' to e.g. 'N2O', the conversion 'NOx' <-->
'N' is by default forbidden. It can be performed within the 'NOx_conversions' context:

.. code:: python

    >>> from openscm_units import unit_registry
    >>> unit_registry("NOx").to("N")
    pint.errors.DimensionalityError: Cannot convert from 'NOx' ([NOx]) to 'N' ([nitrogen])

    # with a context, the conversion becomes legal again
    >>> with unit_registry.context("NOx_conversions"):
    ...     unit_registry("NOx").to("N")
    <Quantity(0.30434782608695654, 'N')>

*NH3*

In order to prevent inadvertent conversions from 'NH3' to 'CO2', the conversion
'NH3' <--> 'N' is by default forbidden. It can be performed within the 'NH3_conversions'
context analogous to the 'NOx_conversions' context:

.. code:: python

    >>> from openscm_units import unit_registry
    >>> unit_registry("NH3").to("N")
    pint.errors.DimensionalityError: Cannot convert from 'NH3' ([NH3]) to 'N' ([nitrogen])

    # with a context, the conversion becomes legal again
    >>> with unit_registry.context("NH3_conversions"):
    ...     unit_registry("NH3").to("N")
    <Quantity(0.823529412, 'N')>

"""
import math

import globalwarmingpotentials
import pint

from .data.mixtures import MIXTURES

# Standard gases. If the value is:
# - str: this entry defines a base gas unit
# - list: this entry defines a derived unit
#    - the first entry defines how to convert from base units
#    - other entries define other names i.e. aliases
_STANDARD_GASES = {
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

    def __init__(self, *args, metric_conversions=None, **kwargs):
        """
        Initialise the unit registry

        Parameters
        ----------
        metric_conversions : [:obj:`pd.DataFrame`, None]
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
        super().__init__(*args, **kwargs)

    def add_standards(self):
        """
        Add standard units.

        Has to be done separately because of pint's weird initializing.
        """
        self._add_gases(_STANDARD_GASES)

        self._add_gases({x: x for x in MIXTURES.keys()})

        self.define("a = 1 * year = annum = yr")
        self.define("h = hour")
        self.define("d = day")
        self.define("degreeC = degC")
        self.define("degreeF = degF")
        self.define("kt = 1000 * t")  # since kt is used for "knot" in the defaults
        self.define(
            "Tt = 1000000000000 * t"
        )  # since Tt is used for "tex" in the defaults

        self.define("ppt = [concentrations]")
        self.define("ppb = 1000 * ppt")
        self.define("ppm = 1000 * ppb")

    def enable_contexts(self, *names_or_contexts, **kwargs):
        """
        Overload pint's :func:`enable_contexts` to add contexts once (the first time
        they are used) to avoid (unnecessary) operations.
        """
        if not self._contexts_added:
            self._add_contexts()
        self._contexts_added = True
        super().enable_contexts(*names_or_contexts, **kwargs)

    def _add_mass_emissions_joint_version(self, symbol):
        """
        Add a unit which is the combination of mass and emissions.

        This allows users to units like e.g. ``"tC"`` rather than requiring a space
        between the mass and the emissions i.e. ``"t C"``

        Parameters
        ----------
        symbol
            The unit to add a joint version for
        """
        self.define("g{symbol} = g * {symbol}".format(symbol=symbol))
        self.define("t{symbol} = t * {symbol}".format(symbol=symbol))

    def _add_gases(self, gases):
        for symbol, value in gases.items():
            if isinstance(value, str):
                # symbol is base unit
                self.define("{} = [{}]".format(symbol, value))
                if value != symbol:
                    self.define("{} = {}".format(value, symbol))
            else:
                # symbol has conversion and aliases
                self.define("{} = {}".format(symbol, value[0]))
                for alias in value[1:]:
                    self.define("{} = {}".format(alias, symbol))

            self._add_mass_emissions_joint_version(symbol)

            # Add alias for upper case symbol:
            if symbol.upper() != symbol:
                self.define("{} = {}".format(symbol.upper(), symbol))
                self._add_mass_emissions_joint_version(symbol.upper())

    def _add_contexts(self):
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

    def _add_metric_conversions(self):
        """
        Add metric conversion contexts
        """
        if self._metric_conversions is None:
            metric_conversions = globalwarmingpotentials.as_frame()
        else:
            metric_conversions = self._metric_conversions

        self._add_metric_conversions_from_df(metric_conversions)

    def _add_metric_conversions_from_df(self, metric_conversions):
        # could make this public in future
        for col in metric_conversions:
            metric_conversion = metric_conversions[col]
            transform_context = pint.Context(col)
            for label, val in metric_conversion.iteritems():
                transform_context = self._add_gwp_to_context(
                    transform_context, label, val
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
        self, transform_context: pint.Context, label: str, val: float
    ) -> pint.Context:
        conv_val = (
            val
            * (self("CO2").to_base_units()).magnitude
            / (self(label).to_base_units()).magnitude
        )
        base_unit = next(
            iter(
                self._get_dimensionality(
                    self(label)  # pylint: disable=protected-access
                    .to_base_units()
                    ._units
                ).keys()
            )
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
    def _add_transformations_to_context(
        context, base_unit, base_unit_ureg, other_unit, other_unit_ureg, conv_val
    ):
        """
        Add all the transformations between units to a context for the two
        given units

        Transformations are mass x unit per time, mass x unit etc.
        """

        def _get_transform_func(forward):
            if forward:

                def result_forward(_, strt):
                    return strt * other_unit_ureg / base_unit_ureg * conv_val

                return result_forward

            def result_backward(_, strt):
                return strt * (base_unit_ureg / other_unit_ureg) / conv_val

            return result_backward

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

    def split_gas_mixture(self, quantity: pint.Quantity) -> list:
        """
        Split a gas mixture into constituent gases.

        Given a pint quantity with the units containing a gas mixture,
        returns a list of the constituents as pint quantities.
        """
        mixture_dimensions = [
            x for x in quantity.dimensionality.keys() if x[1:-1] in MIXTURES
        ]
        if not mixture_dimensions:
            raise ValueError("Dimensions don't contain a gas mixture.")
        if len(mixture_dimensions) > 1:
            raise NotImplementedError(
                "More than one gas mixture in dimensions is not supported."
            )
        mixture_dimension = mixture_dimensions[0]
        if quantity.dimensionality[mixture_dimension] != 1:
            raise NotImplementedError(
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


unit_registry = ScmUnitRegistry()  # pylint:disable=invalid-name
"""
Standard unit registry

The unit registry contains all of the recognised units. Be careful, if you
edit this registry in one place then it will also be edited in any other
places that use ``openscm_units``. If you want multiple, separate registries,
create multiple instances of ``ScmUnitRegistry``.
"""
unit_registry.add_standards()
