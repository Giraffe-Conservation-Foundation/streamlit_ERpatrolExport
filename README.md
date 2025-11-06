# 🗺️ Patrol Shapefile Downloader

A Streamlit web application for downloading patrol track data from EarthRanger as shapefiles. Built for conservation professionals to easily export and analyze patrol data.

<div align="center">

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

---

## ✨ Features

- 🔐 **Secure authentication** - Connect directly to your EarthRanger instance
- 🎯 **Smart filtering** - Filter by patrol types unique to your organization
- 📅 **Date range selection** - Download patrols from any time period
- 🗺️ **Map preview** - Visualize tracks before downloading
- 📦 **Export ready** - Download as shapefile (ZIP with all components)
- ⚡ **Fast & efficient** - Built with Ecoscope for optimized data processing

## 🚀 Quick Start

### Option 1: Use Online (Recommended)

1. Visit the deployed app at: `[YOUR_STREAMLIT_CLOUD_URL]`
2. Log in with your EarthRanger credentials
3. Start downloading patrol tracks!

### Option 2: Run Locally

```bash
# Clone the repository
git clone https://github.com/[YOUR_USERNAME]/streamlit_patrol.git
cd streamlit_patrol

# Run automated setup (Windows)
setup.bat

# Or manual setup
pip install -r requirements.txt
streamlit run app.py
```

See [QUICKSTART.md](QUICKSTART.md) for detailed instructions.

## 📖 How to Use

1. **Login** - Enter your EarthRanger credentials in the sidebar
2. **Select patrol type** - Choose from your organization's patrol types
3. **Set date range** - Pick start and end dates
4. **Download** - Click "Download patrol tracks" and preview the data
5. **Export** - Download the shapefile ZIP for use in GIS software

## 🛠️ Technology Stack

- **[Streamlit](https://streamlit.io)** - Web application framework
- **[Ecoscope](https://github.com/wildlife-dynamics/ecoscope)** - EarthRanger data integration
- **[GeoPandas](https://geopandas.org)** - Geospatial data processing
- **[Folium](https://python-visualization.github.io/folium/)** - Interactive maps

## 📋 Requirements

- Python 3.11+
- EarthRanger account with API access
- See [requirements.txt](requirements.txt) for all dependencies

## 🚢 Deployment

Deploy to Streamlit Cloud in minutes:

1. Fork this repository
2. Sign up at [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. No secrets needed - users enter credentials in the app!

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 📁 Project Structure

```
streamlit_patrol/
├── app.py                          # Main application
├── requirements.txt                # Python dependencies
├── runtime.txt                     # Python version
├── .streamlit/
│   └── config.toml                # Streamlit configuration
├── README.md                       # This file
├── QUICKSTART.md                   # Setup guide
├── DEPLOYMENT.md                   # Deployment guide
├── PROJECT_SUMMARY.md              # Technical overview
├── setup.bat / setup.sh            # Automated setup scripts
└── test_setup.py                   # Environment verification
```

## 🔧 Configuration

### Shapefile Export

The app automatically handles shapefile field name truncation (10-character limit):

| Original Field | Shapefile Field |
|----------------|-----------------|
| patrol_id | ptrl_id |
| patrol_title | ptrl_title |
| patrol_serial_number | ptrl_sn |
| patrol_start_time | ptrl_start |
| patrol_end_time | ptrl_end |

### Custom Filename Format

Downloads are named: `patroltype_YYMMDD_YYMMDD.zip`

Example: `Foot_Patrol_251021_251028.zip`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Credits

**Created by the [Giraffe Conservation Foundation](https://giraffeconservation.org/)**

Powered by [Ecoscope](https://github.com/wildlife-dynamics/ecoscope) and [EarthRanger](https://earthranger.com/)

## 📧 Support

For questions or issues:
- Open an issue on GitHub
- Contact your EarthRanger administrator for API access issues

## 🌟 Acknowledgments

- Wildlife Conservation Society for EarthRanger
- Ecoscope development team
- Streamlit community

---

<div align="center">
Made with ❤️ for wildlife conservation
</div>
