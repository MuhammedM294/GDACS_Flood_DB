from pathlib import Path
import pandas as pd
import logging
import geopandas as gpd
from shapely.geometry import Point
import ast

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

logger = logging.getLogger(__name__)
DATA_DIR = Path(__file__).parent.parent.parent / "data"
FLOOD_DB_CORRECTED_PATH = DATA_DIR / "gdacs_flood_db_corrected.csv"
EQUI7_GRID_CODE_PATH = DATA_DIR / "Equi7Grid"
AF020M = gpd.read_file(EQUI7_GRID_CODE_PATH / "AF/GEOG" / "EQUI7_V14_AF_GEOG_TILE_T3.shp").to_crs("EPSG:4326")
AS020M = gpd.read_file(EQUI7_GRID_CODE_PATH / "AS/GEOG" / "EQUI7_V14_AS_GEOG_TILE_T3.shp").to_crs("EPSG:4326")
EU020M = gpd.read_file(EQUI7_GRID_CODE_PATH / "EU/GEOG" / "EQUI7_V14_EU_GEOG_TILE_T3.shp").to_crs("EPSG:4326")
NA020M = gpd.read_file(EQUI7_GRID_CODE_PATH / "NA/GEOG" / "EQUI7_V14_NA_GEOG_TILE_T3.shp").to_crs("EPSG:4326")
OC020M = gpd.read_file(EQUI7_GRID_CODE_PATH / "OC/GEOG" / "EQUI7_V14_OC_GEOG_TILE_T3.shp").to_crs("EPSG:4326")
SA020M = gpd.read_file(EQUI7_GRID_CODE_PATH / "SA/GEOG" / "EQUI7_V14_SA_GEOG_TILE_T3.shp").to_crs("EPSG:4326")

# -----------------------------------------------------------------------------
# Functions
# ----------------------------------------------------------------------------- 

def load_flood_db_corrected() -> pd.DataFrame:
    """Load the corrected GDACS flood database.
    """
    try:
        df = pd.read_csv(FLOOD_DB_CORRECTED_PATH)
        logger.info("Successfully loaded the corrected flood database.")
        return df
    except Exception as e:
        logger.error(f"Error loading the corrected flood database: {e}")
        raise

def get_equ7_code_lonlat(lon: float, lat: float) -> str:
    point_gdf = gpd.GeoDataFrame(
        geometry=[Point(lon, lat)],
        crs="EPSG:4326"
    )

    for grid_gdf in [AF020M, AS020M, EU020M, NA020M, OC020M, SA020M]:
        match = gpd.sjoin(
            point_gdf,
            grid_gdf,
            how="left",
            predicate="intersects"
        )

        row = match.iloc[0]
        if pd.notna(row["SHORTNAME"]):
            code = row["SHORTNAME"]
            code = code.split("_")[1] +"020M"
            return code
        

def process_row(row):
    geo = row["geometry"]

    if isinstance(geo, str):
        geo = ast.literal_eval(geo)

    lon, lat = geo["coordinates"]
    equi7_code = get_equ7_code_lonlat(lon, lat)
    row["equi7_code"] = equi7_code
    return row
if __name__ == "__main__":
    # Example usage
    df = load_flood_db_corrected()
    df = df.apply(process_row, axis=1)
    # df.to_csv(FLOOD_DB_CORRECTED_PATH, index=False)