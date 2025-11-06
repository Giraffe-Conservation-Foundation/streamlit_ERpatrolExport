# Screenshots Guide

To make your GitHub repository more professional, add screenshots to a `screenshots/` folder.

## Recommended Screenshots

### 1. Login Screen
**Filename**: `screenshots/01-login.png`
- Shows the sidebar with EarthRanger login form
- Demonstrates the clean UI

### 2. Main Interface
**Filename**: `screenshots/02-main-interface.png`
- Shows patrol type selector
- Date range inputs
- Download button

### 3. Map Preview
**Filename**: `screenshots/03-map-preview.png`
- Interactive Folium map with patrol tracks
- Multiple tracks in different colors
- Start/end markers

### 4. Data Preview Table
**Filename**: `screenshots/04-data-preview.png`
- Table showing patrol information
- Summary statistics
- Download button

### 5. Downloaded Shapefile
**Filename**: `screenshots/05-shapefile-output.png`
- ZIP file contents
- Opened in QGIS or ArcGIS showing the tracks

## How to Add Screenshots

1. **Take screenshots** while using the app
2. **Create folder**: `mkdir screenshots`
3. **Add images** to the folder
4. **Update README** with images:

```markdown
## Screenshots

### Login
![Login Screen](screenshots/01-login.png)

### Main Interface
![Main Interface](screenshots/02-main-interface.png)

### Map Preview
![Map Preview](screenshots/03-map-preview.png)

### Data Preview
![Data Preview](screenshots/04-data-preview.png)
```

## Tips for Good Screenshots

- Use a clean, simple patrol dataset for demos
- Take screenshots at 1920x1080 or similar resolution
- Crop to show only relevant parts
- Remove any sensitive/confidential information
- Use tools like Snipping Tool (Windows) or Screenshot (Mac)
- Consider using a tool like [Carbon](https://carbon.now.sh) for code snippets

## Adding to README

After creating screenshots, add this section to your README.md:

```markdown
## 📸 Screenshots

<details>
<summary>Click to view screenshots</summary>

### Login Interface
![Login](screenshots/01-login.png)

### Patrol Selection
![Main Interface](screenshots/02-main-interface.png)

### Interactive Map
![Map Preview](screenshots/03-map-preview.png)

### Data Preview
![Data Preview](screenshots/04-data-preview.png)

</details>
```

The `<details>` tag keeps the README clean while allowing users to expand and see the screenshots.
