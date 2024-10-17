# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Basic demo
#
# This notebook gives a basic demonstration of how to use OpenSCM-Units.
#
# For further details, see the rest of the notebooks.

# %%
import numpy as np

import openscm_units

# %%
UR = openscm_units.unit_registry

# %%
print(f"You are using openscm_units version {openscm_units.__version__}")

# %% [markdown]
# ## Usage
#
# With OpenSCM-Units it is possible to attach units to quantities.
# This is all based on the the [Pint](https://github.com/hgrecco/pint) library.
# For full details, see [Pint's docs](https://pint.readthedocs.io/en/stable/).
#
# OpenSCM-Units adds
# a number of units relevant to simple climate modelling to Pint's standard registry.

# %% [markdown]
# ### Emissions
#
# For example, we can define quantities with emissions units.

# %%
emissions_aus = UR.Quantity(np.array([350, 355, 358]), "Mt CO2 / yr")
emissions_aus

# %% [markdown]
# We can then trivially convert these units to other, equivalent, units.

# %%
emissions_aus.to("GtC / yr")

# %% [markdown]
# ### Concentrations
#
# We can also define quantities with concentrations units.

# %%
annual_co2_increase = UR.Quantity(2.2, "ppm / yr")
annual_co2_increase

# %% [markdown]
# We can then trivially convert these units to other, equivalent, units.

# %%
annual_co2_increase.to("ppb / yr")


# %% [markdown]
# ### Operations
#
# Thanks to Pint, units are then carried through operations.

# %%
annual_co2_increase_erf_equiv = (
    UR.Quantity(4.0, "W / m^2")
    / np.log(2)
    / UR.Quantity(1, "yr")
    * np.log(1 + annual_co2_increase * UR.Quantity(1, "yr") / UR.Quantity(278, "ppm"))
)
annual_co2_increase_erf_equiv

# %% [markdown]
# ## Further details
#
# This provides a very brief overview to the basic principles.
# For further details, see
# [design principles](../../further-background/design-principles)
# and [Pint's docs](https://pint.readthedocs.io/en/stable/).
# The notebook on design principles is a good starting point.
