# Changelog

Versions follow [Semantic Versioning](https://semver.org/) (`<major>.<minor>.<patch>`).

Backward incompatible (breaking) changes will only be introduced in major versions
with advance notice in the **Deprecations** section of releases.


<!--
You should *NOT* be adding new changelog entries to this file, this
file is managed by towncrier. See changelog/README.md.

You *may* edit previous changelogs to fix problems like typo corrections or such.
To add a new changelog entry, please see
https://pip.pypa.io/en/latest/development/contributing/#news-entries,
noting that we use the `changelog` directory instead of news, md instead
of rst and use slightly different categories.
-->

<!-- towncrier release notes start -->

## OpenSCM-Units v0.6.2 (2024-10-17)

### Improvements

- Added the unit "NO" for NOx to support the units used for NOx in CMIP's biomass burning emissions. ([#55](https://github.com/openscm/openscm-units/pull/55))

### Improved Documentation

- Wrote basic usage notebook and included all notebooks in docs. ([#54](https://github.com/openscm/openscm-units/pull/54))

### Trivial/Internal Changes

- [#54](https://github.com/openscm/openscm-units/pull/54)


## OpenSCM-Units v0.6.1 (2024-07-09)


### Bug Fixes

- Fixed accidental aliasing of "yr" to "a".

  We had accidentally assigned "yr" to be an alias for "a".
  This meant we had the following behaviour

  ```python
  >>> from openscm_units import unit_registry
  >>> val = unit_registry.Quantity(1, "yr")
  >>> val
  <Quantity(1, 'a')>
  ```

  This PR fixes this so that if you pass in "yr", it stays as yr i.e. you get

  ```python
  >>> from openscm_units import unit_registry
  >>> val = unit_registry.Quantity(1, "yr")
  >>> val
  <Quantity(1, 'yr')>
  ``` ([#53](https://github.com/openscm/openscm-units/pull/53))


## OpenSCM-Units v0.6.0 (2024-06-15)


### Features

- Added support for the new version of {py:mod}`globalwarmingpotentials`.

  This means that {py:mod}`globalwarmingpotentials` >= 10.0.1 can be used,
  so support for metrics from the third assessment report (TAR)
  are now provided too. ([#51](https://github.com/openscm/openscm-units/pull/51))

### Trivial/Internal Changes

- [#49](https://github.com/openscm/openscm-units/pull/49), [#50](https://github.com/openscm/openscm-units/pulls/50), [#51](https://github.com/openscm/openscm-units/pulls/51)


## OpenSCM-Units v0.5.4 (2023-12-11)


### Trivial/Internal Changes

- [#48](https://github.com/openscm/openscm-units/pull/48)


## OpenSCM-Units v0.5.3 (2023-12-06)


### Improved Documentation

- Move docs on design decisions out of `src/openscm_units/_unit_registry.py` into a dedicated notebook ([#47](https://github.com/openscm/openscm-units/pull/47))

### Trivial/Internal Changes

- [#44](https://github.com/openscm/openscm-units/pull/44), [#46](https://github.com/openscm/openscm-units/pulls/46), [#47](https://github.com/openscm/openscm-units/pulls/47)


## OpenSCM-Units 0.5.2

- Fixed broken definition of ppm, caused by regression in Pint where [\'ppm\' was added to Pint](https://github.com/hgrecco/pint/pull/1661) ([#40](https://github.com/openscm/openscm-units/pull/40))

## OpenSCM-Units 0.5.1

- Generate static usage documentation from the introduction notebook ([#33](https://github.com/openscm/openscm-units/pull/33))
- Update documentation regarding NOx conversions. ([#34](https://github.com/openscm/openscm-units/pull/34))
- Fixed Series.iteritems() removal in pandas, see e.g. [#150 in primap2](https://github.com/pik-primap/primap2/issues/150) ([#38](https://github.com/openscm/openscm-units/pull/38))

## OpenSCM-Units 0.5.0

- Custom metrics are now to be provided as :obj:`pd.DataFrame` rather than being read off disk ([#30](https://github.com/openscm/openscm-units/pull/30))
- Load Global Warming Potentials from [globalwarmingpotentials](https://github.com/openclimatedata/globalwarmingpotentials) package. ([#29](https://github.com/openscm/openscm-units/pull/29))

## OpenSCM-Units 0.4.0

- Add ability to use a custom metrics csv with :obj:`ScmUnitRegistry` ([#28](https://github.com/openscm/openscm-units/pull/28))
- Drop Python3.6 support ([#28](https://github.com/openscm/openscm-units/pull/28))
- Add github action to automatically draft a github release from a git tag. ([#27](https://github.com/openscm/openscm-units/pull/27))

## OpenSCM-Units 0.3.0

- Add \"N2O_conversions\" context to remove ambiguity in N2O conversions ([#25](https://github.com/openscm/openscm-units/pull/25))
- Add AR5 GWPs with climate-carbon cycle feedbacks (closes [#22](https://github.com/openscm/openscm-units/issues/22)) ([#23](https://github.com/openscm/openscm-units/pull/23))
- Make `openscm_units.data` a module by adding an `__init__.py` file to it and add docs for `openscm_units.data` (closes [#19](https://github.com/openscm/openscm-units/issues/19)) ([#20](https://github.com/openscm/openscm-units/pull/20))
- Made NH3 a separate dimension to avoid accidental conversion to CO2 in GWP contexts. Also added an `nh3_conversions` context to convert to nitrogen (closes [#12](https://github.com/openscm/openscm-units/issues/12)) ([#18](https://github.com/openscm/openscm-units/pull/18))
- Added refrigerant mixtures as units, including automatic GWP calculation from the GWP of their constituents. Also added the `unit_registry.split_gas_mixtures` function which can be used to split quantities containing a gas mixture into their constituents (closes [#10](https://github.com/openscm/openscm-units/issues/10)) ([#16](https://github.com/openscm/openscm-units/pull/16))

## OpenSCM-Units 0.2.0

- Update CI so that it runs on pull requests from forks too ([#15](https://github.com/openscm/openscm-units/pull/15))
- Renamed `openscm_units.unit_registry` module to `openscm_units._unit_registry` to avoid name collision and lift `ScmUnitRegistry` to `openscm_units.ScmUnitRegistry` (closes [#13](https://github.com/openscm/openscm-units/issues/13)) ([#14](https://github.com/openscm/openscm-units/pull/14))

## OpenSCM-Units 0.1.4

- Added C7F16, C8F18 and SO2F2 AR5GWP100 (closes [#8](https://github.com/openscm/openscm-units/issues/8)) ([#7](https://github.com/openscm/openscm-units/pull/7))

## OpenSCM-Units 0.1.3

- Include metric conversions data in package ([#7](https://github.com/openscm/openscm-units/pull/7))
- Add conda install instructions ([#6](https://github.com/openscm/openscm-units/pull/6))

## OpenSCM-Units 0.1.2

- Update `MANIFEST.in` to ensure `LICENSE`, `README.rst` and `CHANGELOG.rst` are included in source distributions ([#5](https://github.com/openscm/openscm-units/pull/5))
- Update README and url to point to openscm organisation ([#4](https://github.com/openscm/openscm-units/pull/4))

## OpenSCM-Units 0.1.1

- Hotfix so that \'Tt\' is terra tonne rather than \'tex\' ([#2](https://github.com/openscm/openscm-units/pull/2))

## OpenSCM-Units 0.1.0

- Setup repository ([#1](https://github.com/openscm/openscm-units/pull/1))
