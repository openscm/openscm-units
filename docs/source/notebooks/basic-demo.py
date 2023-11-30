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
# # Introduction
#
# Here we give a brief introduction to `openscm_units`.

# %% [markdown]
# ## The unit registry
#
# ``openscm_units.unit_registry`` extends Pint's default unit registry by adding simple climate modelling related units. We'll spare the details here (they can be found in [our documentation](https://openscm-units.readthedocs.io/en/latest/unit_registry.html)), but the short idea is that you can now do all sorts of simple climate modelling related conversions which were previously impossible.

# %%
import traceback

import pandas as pd
import seaborn as sns
from pint.errors import DimensionalityError

import openscm_units
from openscm_units import unit_registry

# %%
print(f"You are using openscm_units version {openscm_units.__version__}")

# %% [markdown]
# ## Basics
#
# ``openscm_units.unit_registry`` knows about basic units, e.g. 'CO2'.

# %%
unit_registry("CO2")

# %% [markdown]
# Standard conversions are now trivial.

# %%
unit_registry("CO2").to("C")

# %%
emissions_aus = 0.34 * unit_registry("Gt C / yr")
emissions_aus.to("Mt CO2/yr")

# %% [markdown]
# ## Contexts
#
# In general, we cannot simply convert e.g. CO$_2$ emissions into CH$_4$ emissions. 

# %%
try:
    unit_registry("CH4").to("CO2")
except DimensionalityError:
    traceback.print_exc(limit=0, chain=False)

# %% [markdown]
# However, a number of metrics exist which do allow conversions between GHG species. Pint plus OpenSCM's inbuilt metric conversions allow you to perform such conversions trivially by specifying the `context` keyword.

# %%
with unit_registry.context("AR4GWP100"):
    ch4_ar4gwp100_co2e = unit_registry("CH4").to("CO2")

ch4_ar4gwp100_co2e

# %% [markdown]
# ## Gas mixtures
#
# Some gases (mainly, refrigerants) are actually mixtures of other gases, for example HFC407a (aka R-407A). In general, they can be used like any other gas. Additionally, `openscm_units` provides the ability to split these gases into their constituents.

# %%
emissions = 20 * unit_registry('kt HFC407a / year')

with unit_registry.context("AR4GWP100"):
    print(emissions.to('Gg CO2 / year'))

# %%
unit_registry.split_gas_mixture(emissions)

# %% [markdown]
# ## Building up complexity
#
# `openscm_units` is meant to be a simple repository which does one thing, but does it well. We encourage you to use it wherever you like (and if you do please let us know via the [issue tracker](https://github.com/openscm/openscm-units/issues)). As an example of something we can do, we can quickly see how GWP100 has changed between assessment reports.

# %% pycharm={"name": "#%%\n"}
units_of_interest = ["CO2", "CH4", "N2O", "HFC32", "CFC11"]
metrics_of_interest = ["SARGWP100", "AR4GWP100", "AR5GWP100"]
data = {
    "unit": [],
    "metric": [],
    "value": [],
}
for metric in metrics_of_interest:
    with unit_registry.context(metric):
        for unit in units_of_interest:
            data["unit"].append(unit)
            data["metric"].append(metric)
            data["value"].append(unit_registry(unit).to("CO2").magnitude)

data = pd.DataFrame(data)

sns.catplot(
    data=data,
    x="metric",
    y="value",
    kind="bar",
    col="unit",
    col_wrap=5,
    sharey=False,
)
