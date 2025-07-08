## 1.0.0
First release version

## 1.1.0
### Added
- Added `.git/` to `.dockerignore` to exclude Git-related files from Docker builds.
- Installed `curl` and Microsoft ODBC SQL driver (`msodbcsql18`) in the Docker container.
- Added a non-root user (`appuser`) and group (`appgroup`) for improved security in the Dockerfile.
- Implemented SQLAlchemy connection pooling with `engine.dispose()` on exit in `__main__.py`.
- Introduced error handling with connection logging in `extract.py` and `load.py`.
- Enhanced logging with `atexit` for better resource cleanup.
- **Added `docker-compose` configuration** to define an `opm` service with environment variables and an external network.

### Fixed/Updated
- Upgraded base Python image in Dockerfile from `python:3.10-slim` to `python:3.12-slim` for better performance and compatibility.
- Refactored Dockerfile to check for Debian version compatibility before installing Microsoft repository packages.
- Changed ownership of copied files in Dockerfile to `appuser:appgroup` for improved security.
- Updated Dockerfile to switch to `appuser` before running the container to follow best security practices.
- Changed `CMD` to `ENTRYPOINT` in Dockerfile to make container execution more consistent.
- Improved `main.py` execution flow by integrating SQLAlchemy `engine` for database operations.
- Optimized `extract.py` to use direct requests with a timeout instead of a `Session`.
- Updated `load.py` to manage database transactions with SQLAlchemy instead of direct execution.

### Removed
- Removed redundant `COPY . /app` line in Dockerfile, as a new version with `--chown=appuser:appgroup` was added.
- Eliminated unnecessary try-except block in `main.py`, improving error handling consistency.
- Removed outdated manual transaction commits in `extract.py` and `load.py`, replacing them with `engine.connect()`.

## 1.1.2
### Added
- Implemented batch processing in `load.py` for improved performance with large datasets
- Added temporary table usage in `load.py` followed by stored procedure execution (`pro_lines`)
- Simplified DataFrame processing in `transform.py` by removing merge operations

### Fixed/Updated
- Removed `LogID` tracking throughout the application as it's no longer needed
- Updated `actionLog` function in `functions.py` to remove `GroupId` and simplify logging
- Changed `load.main()` to accept a single DataFrame instead of separate insert/update DataFrames
- Simplified `transform.main()` to return a single DataFrame instead of a tuple
- Updated column processing logic in `transform.py` to handle all columns uniformly
- Improved error handling with more detailed error printing in all modules

### Removed
- Removed UUID generation and namespace dependencies
- Removed complex merging functions from `functions.py`
- Eliminated separate insert/update DataFrame handling in load operations
- Removed redundant `execute` function from `functions.py`