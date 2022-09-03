# Changelog

## v1.3.0 (2022-09-02)

- GPSDClient now supports a `timeout` param
- GPSDClient now can be used as a context manager
- Code cleanup, added more tests
- parsed datetimes now contain the UTC timezone info

## v1.2.1 (2022-01-11)

- Improved type hints

## v1.2.0 (2021-10-26)

- add `filter` argument to return only the given report classes
- Fixes json parsing (gpsd emits invalid json with trailing commas in some cases)

## v1.1.0 (2021-08-1)

- Add "Climb"-column to readable output
- Standalone client code cleanups
- Updated tests

## v1.0.0 (2021-08-13)

- Tabular data output in readable mode

## v0.2.0 (2021-08-13)

- Check whether we really connect to a gpsd daemon
- Improved error messages

## v0.1.0 (2021-08-13)

- Initial release
