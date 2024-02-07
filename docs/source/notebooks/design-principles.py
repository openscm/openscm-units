# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Design principles
#
# Here we provide an overview of the key design principles and choices in OpenSCM-Units.

# %% [markdown]
# Unit handling makes use of the [Pint](https://github.com/hgrecco/pint) library. This
# allows us to easily define units as well as contexts. Contexts allow us to perform
# conversions which would not normally be allowed e.g. in the 'AR4GWP100'
# context we can convert from CO2 to CH4 using the AR4GWP100 equivalence metric.
#
# An illustration of how the ``unit_registry`` can be used is shown below

# %%
import traceback

from pint.errors import DimensionalityError

from openscm_units import unit_registry

# %%
unit_registry("CO2")

# %%
emissions_aus = 0.34 * unit_registry("Gt C / yr")
emissions_aus

# %%
emissions_aus.to("Mt CO2 / yr")

# %%
with unit_registry.context("AR4GWP100"):
    print((100 * unit_registry("Mt CH4 / yr")).to("Mt CO2 / yr"))

# %% [markdown]
# ## More details on emissions unit
#
# Emissions are a flux composed of three parts: mass, the species being emitted and the
# time period e.g. "t CO2 / yr". As mass and time are part of SI units, all we need to
# define in OpenSCM-Units are emissions units i.e. the stuff.
# Here we include as many of the canonical emissions units,
# and their conversions, as possible.
#
# For emissions units, there are a few cases to be considered:
#
# - fairly obvious ones e.g. carbon dioxide emissions can be provided in 'C' or 'CO2'
#   and converting between the two is possible
# - less obvious ones e.g. NOx emissions can be provided in 'N' or 'NOx', we provide
#   conversions between these two which can be enabled if needed (see below).
# - case-sensitivity. In order to provide a simplified interface, using all uppercase
#   versions of any unit is also valid e.g. `unit_registry("HFC4310mee")` is the same as
#   `unit_registry("HFC4310MEE")`
# - hyphens and underscores in units. In order to be Pint compatible and to simplify
#   things, we strip all hyphens and underscores from units.
#
# As a convenience, we allow users to combine the mass and the type of emissions to make
# a 'joint unit' e.g. "tCO2".
# It should be recognised that this joint unit is a derived unit and not a base unit.
#
# By defining these three separate components,
# it is much easier to track what conversions are valid and which are not.
# For example, as the emissions units are all defined as
# emissions units, and not as atomic masses, we are able to prevent invalid conversions.
# If emissions units were simply atomic masses, it would be possible to convert between
# e.g. C and N2O which would be a problem. Conventions such as allowing carbon dioxide
# emissions to be reported in C or CO2, despite the fact that they are fundamentally
# different chemical species, is a convention which is particular to emissions
# (as far as we can tell).
#
# Pint's contexts are particularly useful for emissions as they facilitate
# metric conversions. With a context, a conversion which wouldn't normally be allowed
# (e.g. tCO2 --> tN2O) is allowed and will use whatever metric conversion is appropriate
# for that context (e.g. AR4GWP100).

# %% [markdown]
# ## Namespace collisions
#
# Finally, we discuss namespace collisions.

# %% [markdown]
# ### CH$_4$
#
# Methane emissions are defined as 'CH4'. In order to prevent inadvertent conversions of
# 'CH4' to e.g. 'CO2' via 'C', the conversion 'CH4' <--> 'C' is by default forbidden.
# However, it can be performed within the context 'CH4_conversions' as shown below:

# %%
try:
    unit_registry("CH4").to("C")
except DimensionalityError:
    traceback.print_exc(limit=0, chain=False)

# %% [markdown]
# With a context, the conversion becomes legal again

# %%
with unit_registry.context("CH4_conversions"):
    print(unit_registry("CH4").to("C"))

# %% [markdown]
# As an unavoidable side effect, this also becomes possible

# %%
with unit_registry.context("CH4_conversions"):
    print(unit_registry("CH4").to("CO2"))

# %% [markdown]
# ### N$_2$O
#
# Nitrous oxide emissions are typically reported with units of 'N2O'. However,
# they are also reported with units of 'N2ON' (a short-hand which indicates that
# only the mass of the nitrogen is being counted). Reporting nitrous oxide
# emissions with units of simply 'N' is ambiguous (do you mean the mass of
# nitrogen, so 1 N = 28 / 44 N2O or just the mass of a single N atom, so
# 1 N = 14 / 44 N2O). By default, converting 'N2O' <--> 'N' is forbidden to
# prevent this ambiguity. However, the conversion can be performed within the
# context 'N2O_conversions', in which case it is assumed that 'N' just means a
# single N atom i.e. 1 N = 14 / 44 N2O, as shown below:

# %%
try:
    unit_registry("N2O").to("N")
except DimensionalityError:
    traceback.print_exc(limit=0, chain=False)

# %% [markdown]
# With a context, the conversion becomes legal again:

# %%
with unit_registry.context("N2O_conversions"):
    print(unit_registry("N2O").to("N"))

# %% [markdown]
# ### NO$_x$

# %% [markdown]
# Like for methane, NOx emissions also suffer from a namespace collision. In order to
# prevent inadvertent conversions from 'NOx' to e.g. 'N2O', the conversion 'NOx' <-->
# 'N' is by default forbidden. It can be performed within the 'NOx_conversions' context:

# %%
try:
    unit_registry("NOx").to("N")
except DimensionalityError:
    traceback.print_exc(limit=0, chain=False)

# %%
with unit_registry.context("NOx_conversions"):
    print(unit_registry("NOx").to("N"))

# %% [markdown]
# ### NH$_3$
#
# In order to prevent inadvertent conversions from 'NH3' to 'CO2', the conversion
# 'NH3' <--> 'N' is by default forbidden.
# It can be performed within the 'NH3_conversions' context,
# analogous to the 'NOx_conversions' context:

# %%
try:
    unit_registry("NH3").to("N")
except DimensionalityError:
    traceback.print_exc(limit=0, chain=False)

# %%
with unit_registry.context("NH3_conversions"):
    unit_registry("NH3").to("N")
