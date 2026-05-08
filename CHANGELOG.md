# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-06

### Added
- Initial release of Patrol Shapefile Downloader
- EarthRanger authentication
- Patrol type filtering from server
- Date range selection (date only, no time)
- LineString track generation from patrol points
- Point filtering based on patrol segment times
- Shapefile export with custom filename format (patroltype_YYMMDD_YYMMDD)
- Folium map preview with track visualization
- Data preview table with key patrol information
- Summary statistics (total tracks, points, distance)
- Automatic field name shortening for shapefile compatibility
- Streamlit Cloud deployment configuration
- Comprehensive documentation (README, QUICKSTART, DEPLOYMENT)
- Automated setup scripts (Windows and Unix)
- Environment verification script

### Features
- Smart grouping by patrol segments (groupby_col)
- Chronological point sorting for accurate track lines
- ZIP packaging of all shapefile components
- Clean, sentence-case UI
- Professional branding for Giraffe Conservation Foundation
- Responsive layout with sidebar authentication
- Error handling and user feedback

### Technical Details
- Python 3.11+ support
- Ecoscope integration for EarthRanger data access
- GeoPandas for geospatial processing
- Streamlit for web interface
- Folium for interactive mapping (optional)

## [1.1.5] - 2026-05-08

### Fixed
- Datetime parsing failure on EarthRanger instances where `patrol_end_time` (and related columns) contain a mix of ISO 8601 timestamps with and without fractional seconds (e.g. `2026-04-03T22:43:11Z` alongside `2026-04-03T22:43:11.123Z`). Replaced the bare `pd.to_datetime(..., utc=True)` call (which infers a single format and fails on mixed variants) with `format='ISO8601'` for string columns, which handles all ISO 8601 variants in the same column.

## [Unreleased]

### Planned
- Multi-language support
- Bulk download for multiple patrol types
- Advanced filtering options
- Export to additional formats (GeoJSON, KML)
- Performance optimization for large datasets
- User preferences and settings storage

---

For more details, see the [README](README.md).
