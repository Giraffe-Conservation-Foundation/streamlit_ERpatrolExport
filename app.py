import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from ecoscope.io.earthranger import EarthRangerIO
import geopandas as gpd
import tempfile
import os
from shapely.geometry import LineString

# Optional imports for map
try:
    import folium
    from streamlit_folium import folium_static
    HAS_FOLIUM = True
except ImportError:
    HAS_FOLIUM = False

# Page configuration
st.set_page_config(
    page_title="Patrol Shapefile Downloader",
    page_icon="🗺️",
    layout="wide"
)

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'er_io' not in st.session_state:
    st.session_state.er_io = None

def authenticate_earthranger(server, username, password):
    """Authenticate with EarthRanger and return EarthRangerIO instance"""
    try:
        er_io = EarthRangerIO(
            server=server,
            username=username,
            password=password
        )
        return er_io, None
    except Exception as e:
        return None, str(e)

def download_patrol_tracks(er_io, patrol_type_value, since, until):
    """Download patrol tracks as GeoDataFrame and convert to LineStrings"""
    try:
        # Get patrols based on filters
        patrols_df = er_io.get_patrols(
            since=since,
            until=until,
            patrol_type_value=patrol_type_value,
            status=['done', 'active']
        )
        
        if patrols_df.empty:
            return None, "No patrols found for the specified criteria"
        
        # Get patrol observations
        patrol_observations = er_io.get_patrol_observations(
            patrols_df=patrols_df,
            include_patrol_details=True
        )
        
        # Handle both Relocations object and GeoDataFrame
        if hasattr(patrol_observations, 'gdf'):
            points_gdf = patrol_observations.gdf
        else:
            points_gdf = patrol_observations
            
        if points_gdf.empty:
            return None, "No patrol tracks found"
        
        # Find time column for sorting points chronologically
        time_col = None
        for col in ['extra__recorded_at', 'recorded_at', 'fixtime', 'time', 'timestamp']:
            if col in points_gdf.columns:
                time_col = col
                break
        
        # Filter points to patrol segment times
        points_before_filter = len(points_gdf)
        
        if time_col and 'patrol_start_time' in points_gdf.columns and 'patrol_end_time' in points_gdf.columns:
            # Ensure time column is datetime
            if not pd.api.types.is_datetime64_any_dtype(points_gdf[time_col]):
                points_gdf[time_col] = pd.to_datetime(points_gdf[time_col], utc=True)
            
            # Convert patrol_start_time and patrol_end_time from STRING to datetime
            # These come as ISO format strings like "2025-10-25T04:59:42Z"
            if points_gdf['patrol_start_time'].dtype == 'object':  # strings
                points_gdf['patrol_start_time'] = pd.to_datetime(points_gdf['patrol_start_time'], utc=True)
            if points_gdf['patrol_end_time'].dtype == 'object':  # strings
                points_gdf['patrol_end_time'] = pd.to_datetime(points_gdf['patrol_end_time'], utc=True)
            
            # Ensure all are timezone-aware UTC
            if points_gdf[time_col].dt.tz is None:
                points_gdf[time_col] = points_gdf[time_col].dt.tz_localize('UTC')
            if points_gdf['patrol_start_time'].dt.tz is None:
                points_gdf['patrol_start_time'] = points_gdf['patrol_start_time'].dt.tz_localize('UTC')
            if points_gdf['patrol_end_time'].dt.tz is None:
                points_gdf['patrol_end_time'] = points_gdf['patrol_end_time'].dt.tz_localize('UTC')
            
            # Filter: keep only points where recorded time is between patrol start and end times
            within_patrol = (points_gdf[time_col] >= points_gdf['patrol_start_time']) & \
                           (points_gdf[time_col] <= points_gdf['patrol_end_time'])
            points_gdf = points_gdf[within_patrol].copy()
        
        total_removed = points_before_filter - len(points_gdf)
        
        if points_gdf.empty:
            return None, f"No points found within patrol time ranges (filtered out {total_removed} of {points_before_filter} points)"
        
        # Convert points to LineStrings grouped by patrol segment
        lines = []
        
        # Group by patrol_id - each patrol should be a separate track
        # Note: groupby_col in ecoscope contains subject_id, not patrol segment ID
        group_col = 'patrol_id'
        
        for group_id in points_gdf[group_col].unique():
            patrol_points = points_gdf[points_gdf[group_col] == group_id].copy()
            
            # CRITICAL: Sort by recorded time to maintain chronological order
            # Data comes sorted from EarthRanger, but filtering may have disrupted the order
            if time_col and time_col in patrol_points.columns:
                patrol_points = patrol_points.sort_values(time_col, ascending=True)
            
            if len(patrol_points) < 2:
                continue  # Skip patrols with only one point
            
            # Create LineString from points IN TIME ORDER
            coords = [(point.x, point.y) for point in patrol_points.geometry]
            line = LineString(coords)
            
            # Get patrol metadata from first point
            first_point = patrol_points.iloc[0]
            
            # Use the actual patrol_id for metadata, not groupby_col
            patrol_id = first_point['patrol_id'] if 'patrol_id' in first_point.index else group_id
            
            line_data = {
                'geometry': line,
                'patrol_id': patrol_id,
                'patrol_sn': first_point['patrol_serial_number'] if 'patrol_serial_number' in first_point.index else '',
                'patrol_type': first_point['patrol_type__display'] if 'patrol_type__display' in first_point.index else (first_point['patrol_type__value'] if 'patrol_type__value' in first_point.index else ''),
                'subject_id': first_point['extra__subject_id'] if 'extra__subject_id' in first_point.index else '',
                'num_points': len(patrol_points),
                'distance_km': line.length * 111
            }
            
            # Add time columns if available
            if time_col:
                line_data['start_time'] = str(patrol_points[time_col].min())
                line_data['end_time'] = str(patrol_points[time_col].max())
            
            # Add patrol start/end times from metadata if available
            if 'patrol_start_time' in first_point.index:
                line_data['patrol_start_time'] = str(first_point['patrol_start_time'])
            if 'patrol_end_time' in first_point.index:
                line_data['patrol_end_time'] = str(first_point['patrol_end_time'])
            
            # Add patrol_type__ columns if they exist
            for col in first_point.index:
                if col.startswith('patrol_type__') and col not in line_data:
                    line_data[col] = first_point[col]
            
            lines.append(line_data)
        
        if not lines:
            return None, "No patrols with multiple points found (need at least 2 points to create a line)"
        
        # Create GeoDataFrame from lines
        lines_gdf = gpd.GeoDataFrame(lines, crs=4326)
            
        return lines_gdf, None
            
    except Exception as e:
        import traceback
        return None, f"{str(e)}\n\n{traceback.format_exc()}"

# Main app
st.title("🗺️ Patrol shapefile downloader")
st.markdown("Download patrol tracks from EarthRanger as shapefiles")

# Sidebar for authentication
with st.sidebar:
    st.header("🔐 EarthRanger login")
    
    if not st.session_state.authenticated:
        server = st.text_input("Server URL", placeholder="https://your-server.pamdas.org")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", type="primary"):
            if server and username and password:
                with st.spinner("Authenticating..."):
                    er_io, error = authenticate_earthranger(server, username, password)
                    if er_io:
                        st.session_state.er_io = er_io
                        st.session_state.authenticated = True
                        st.success("✅ Successfully authenticated!")
                        st.rerun()
                    else:
                        st.error(f"❌ Authentication failed: {error}")
            else:
                st.warning("Please fill in all fields")
    else:
        st.success("✅ Logged in")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.er_io = None
            st.rerun()

# Main content - only show if authenticated
if st.session_state.authenticated:
    col1, col2 = st.columns(2)
    
    with col1:
        # Get available patrol types
        try:
            patrol_types_df = st.session_state.er_io.get_patrol_types()
            patrol_type_options = patrol_types_df['value'].tolist()
            
            patrol_type = st.selectbox(
                "Select patrol type",
                options=patrol_type_options,
                help="Choose the type of patrol to download"
            )
        except Exception as e:
            st.error(f"Error loading patrol types: {e}")
            patrol_type = st.text_input("Enter patrol type value")
    
    with col2:
        st.write("") # Spacing
    
    # Date range selection
    col3, col4 = st.columns(2)
    
    with col3:
        start_date = st.date_input(
            "Start date",
            value=datetime.now() - timedelta(days=30),
            help="Beginning of date range"
        )
    
    with col4:
        end_date = st.date_input(
            "End date",
            value=datetime.now(),
            help="End of date range"
        )
    
    # Combine date with start/end of day times
    since = datetime.combine(start_date, datetime.min.time()).isoformat()
    until = datetime.combine(end_date, datetime.max.time()).isoformat()
    
    st.markdown("---")
    
    # Download button
    if st.button("🔽 Download patrol tracks", type="primary", use_container_width=True):
        with st.spinner("Downloading patrol tracks..."):
            gdf, error = download_patrol_tracks(
                st.session_state.er_io,
                patrol_type,
                since,
                until
            )
            
            if error:
                st.error(f"❌ Error: {error}")
            elif gdf is not None:
                st.success(f"✅ Successfully downloaded {len(gdf)} patrol track(s)!")
                
                # Display map preview
                st.subheader("📍 Map preview")
                if HAS_FOLIUM:
                    try:
                        # Calculate center point
                        bounds = gdf.total_bounds  # [minx, miny, maxx, maxy]
                        center_lat = (bounds[1] + bounds[3]) / 2
                        center_lon = (bounds[0] + bounds[2]) / 2
                        
                        # Create map
                        m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
                        
                        # Add each track to the map
                        colors = ['blue', 'red', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen']
                        for idx, row in gdf.iterrows():
                            color = colors[idx % len(colors)]
                            coords = [(coord[1], coord[0]) for coord in row.geometry.coords]  # lat, lon
                            
                            folium.PolyLine(
                                coords,
                                color=color,
                                weight=3,
                                opacity=0.8,
                                popup=f"{row.get('patrol_title', 'Patrol')}<br>Points: {row.get('num_points', 'N/A')}<br>Distance: {row.get('distance_km', 0):.2f} km"
                            ).add_to(m)
                            
                            # Add start marker
                            folium.CircleMarker(
                                coords[0],
                                radius=5,
                                color=color,
                                fill=True,
                                popup=f"Start: {row.get('patrol_title', '')}",
                            ).add_to(m)
                            
                            # Add end marker
                            folium.CircleMarker(
                                coords[-1],
                                radius=5,
                                color=color,
                                fill=True,
                                fillColor='white',
                                popup=f"End: {row.get('patrol_title', '')}",
                            ).add_to(m)
                        
                        # Fit bounds
                        m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
                        
                        # Display map
                        folium_static(m, width=800, height=500)
                        
                    except Exception as e:
                        st.warning(f"Could not create map preview: {e}")
                else:
                    st.info("💡 Install folium and streamlit-folium to see map preview:\n```pip install folium streamlit-folium```")
                
                # Display preview
                st.subheader("Data preview")
                # Create display DataFrame without geometry and some redundant columns
                cols_to_drop = ['geometry', 'start_time', 'end_time']
                display_df = gdf.drop(columns=[col for col in cols_to_drop if col in gdf.columns]).copy()
                st.dataframe(display_df)
                
                # Show summary statistics
                col5, col6, col7 = st.columns(3)
                with col5:
                    st.metric("Total tracks", len(gdf))
                with col6:
                    st.metric("Total points", gdf['num_points'].sum())
                with col7:
                    st.metric("Total distance (km)", f"{gdf['distance_km'].sum():.2f}")
                
                # Save to shapefile
                try:
                    # Format filename: patroltype_yymmdd_yymmdd
                    start_str = start_date.strftime('%y%m%d')
                    end_str = end_date.strftime('%y%m%d')
                    # Clean patrol type for filename (remove spaces, special chars)
                    patrol_type_clean = "".join(c if c.isalnum() else "_" for c in patrol_type)
                    base_filename = f"{patrol_type_clean}_{start_str}_{end_str}"
                    
                    # Prepare shapefile-friendly column names (max 10 chars)
                    # Rename columns: patrol → ptrl to save characters
                    gdf_export = gdf.copy()
                    column_mapping = {
                        'patrol_id': 'ptrl_id',
                        'patrol_sn': 'ptrl_sn',
                        'patrol_type': 'ptrl_type',
                        'subject_id': 'subj_id',
                        'patrol_start_time': 'ptrl_start',
                        'patrol_end_time': 'ptrl_end',
                        'distance_km': 'dist_km',
                        'num_points': 'num_pts'
                    }
                    # Only rename columns that exist
                    gdf_export = gdf_export.rename(columns={k: v for k, v in column_mapping.items() if k in gdf_export.columns})
                    
                    with tempfile.TemporaryDirectory() as tmpdir:
                        shapefile_path = os.path.join(tmpdir, f"{base_filename}.shp")
                        gdf_export.to_file(shapefile_path)
                        
                        # Create a zip file with all shapefile components
                        import zipfile
                        zip_path = os.path.join(tmpdir, f"{base_filename}.zip")
                        
                        with zipfile.ZipFile(zip_path, 'w') as zipf:
                            for ext in ['.shp', '.shx', '.dbf', '.prj', '.cpg']:
                                file_path = shapefile_path.replace('.shp', ext)
                                if os.path.exists(file_path):
                                    # Add files to zip with the base filename
                                    zipf.write(file_path, f"{base_filename}{ext}")
                        
                        # Read the zip file for download
                        with open(zip_path, 'rb') as f:
                            zip_data = f.read()
                        
                        st.download_button(
                            label="📥 Download Shapefile (ZIP)",
                            data=zip_data,
                            file_name=f"{base_filename}.zip",
                            mime="application/zip",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"❌ Error creating shapefile: {e}")

else:
    st.info("👈 Please login using the sidebar to access the patrol download feature")
    
    # Show some information about the app
    st.markdown("""
    ### About this app
    
    This application allows you to download patrol track data from EarthRanger as shapefiles.
    
    **Features:**
    - Secure authentication with EarthRanger
    - Filter by patrol types unique to your EarthRanger instance
    - Download tracks as shapefiles in ZIP format
    - Preview data before downloading
    
    **How to use:**
    1. Log in with your EarthRanger credentials in the sidebar
    2. Select a patrol type from the dropdown menu
    3. Choose your date range
    4. Click "Download patrol tracks"
    5. Download the shapefile ZIP when ready
    
    ---
    *Built with Streamlit and Ecoscope*
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Created by the Giraffe Conservation Foundation, powered by Ecoscope</div>",
    unsafe_allow_html=True
)
