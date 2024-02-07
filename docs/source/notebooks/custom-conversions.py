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
# # Custom conversions
#
# Here we show how custom conversions can be passed to OpenSCM-Units' `ScmUnitRegistry`.

# %%
import pandas as pd

from openscm_units import ScmUnitRegistry

# %% [markdown]
# ## Custom conversions DataFrame
#
# On initialisation, a `pd.DataFrame` can be provided which contains the custom
# conversions. This `pd.DataFrame` should be formatted as shown below, with an
# index that contains the different species and columns which contain the
# conversion for different metrics.

# %%
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
metric_conversions_custom

# %% [markdown]
# With such a `pd.DataFrame`,
# we can use custom conversions in our unit registry as shown.

# %%
# initialise the unit registry with custom conversions
unit_registry = ScmUnitRegistry(metric_conversions=metric_conversions_custom)
# add standard conversions before moving on
unit_registry.add_standards()

# start with e.g. N2O
nitrous_oxide = unit_registry("tN2O / yr")

# our unit registry allows us to make conversions using the
# conversion factors we previously defined
for context in ["Custom1", "Custom2"]:
    with unit_registry.context(context):
        print(
            f"{nitrous_oxide} in CO2-equivalent in context {context} "
            "is {nitrous_oxide.to('tCO2 / yr')}"
        )
