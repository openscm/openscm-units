Changelog
=========

master
------

v0.3.0
------

- (`#25 <https://github.com/openscm/openscm-units/pull/25>`_) Add "N2O_conversions" context to remove ambiguity in N2O conversions
- (`#23 <https://github.com/openscm/openscm-units/pull/23>`_) Add AR5 GWPs with climate-carbon cycle feedbacks (closes `#22 <https://github.com/openscm/openscm-units/issues/22>`_)
- (`#20 <https://github.com/openscm/openscm-units/pull/20>`_) Make ``openscm_units.data`` a module by adding an ``__init__.py`` file to it and add docs for ``openscm_units.data`` (closes `#19 <https://github.com/openscm/openscm-units/issues/19>`_)
- (`#18 <https://github.com/openscm/openscm-units/pull/18>`_) Made NH3 a separate dimension to avoid accidental conversion to CO2 in GWP contexts. Also added an ``nh3_conversions`` context to convert to nitrogen (closes `#12 <https://github.com/openscm/openscm-units/issues/12>`_)
- (`#16 <https://github.com/openscm/openscm-units/pull/16>`_) Added refrigerant mixtures as units, including automatic GWP calculation from the GWP of their constituents. Also added the ``unit_registry.split_gas_mixtures`` function which can be used to split quantities containing a gas mixture into their constituents (closes `#10 <https://github.com/openscm/openscm-units/issues/10>`_)

v0.2.0
------

- (`#15 <https://github.com/openscm/openscm-units/pull/15>`_) Update CI so that it runs on pull requests from forks too
- (`#14 <https://github.com/openscm/openscm-units/pull/14>`_) Renamed ``openscm_units.unit_registry`` module to ``openscm_units._unit_registry`` to avoid name collision and lift ``ScmUnitRegistry`` to ``openscm_units.ScmUnitRegistry`` (closes `#13 <https://github.com/openscm/openscm-units/issues/13>`_)

v0.1.4
------

- (`#7 <https://github.com/openscm/openscm-units/pull/7>`_) Added C7F16, C8F18 and SO2F2 AR5GWP100 (closes `#8 <https://github.com/openscm/openscm-units/issues/8>`_)

v0.1.3
------

- (`#7 <https://github.com/openscm/openscm-units/pull/7>`_) Include metric conversions data in package
- (`#6 <https://github.com/openscm/openscm-units/pull/6>`_) Add conda install instructions

v0.1.2
------

- (`#5 <https://github.com/openscm/openscm-units/pull/5>`_) Update ``MANIFEST.in`` to ensure ``LICENSE``, ``README.rst`` and ``CHANGELOG.rst`` are included in source distributions
- (`#4 <https://github.com/openscm/openscm-units/pull/4>`_) Update README and url to point to openscm organisation

v0.1.1
------

- (`#2 <https://github.com/openscm/openscm-units/pull/2>`_) Hotfix so that 'Tt' is terra tonne rather than 'tex'

v0.1.0
------

- (`#1 <https://github.com/openscm/openscm-units/pull/1>`_) Setup repository
