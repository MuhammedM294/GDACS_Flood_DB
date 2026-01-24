from pathlib import Path
import urllib.request
import zipfile
import geopandas as gpd

_DATA_DIR = Path(__file__).parent.parent.parent / "data" / "admin_0_countries"
_SHP_NAME = "ne_110m_admin_0_countries.shp"
_URL = "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"

_WORLD = None


def load_world_countries() -> gpd.GeoDataFrame:
    global _WORLD

    if _WORLD is not None:
        return _WORLD

    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    shp_path = _DATA_DIR / _SHP_NAME

    if not shp_path.exists():
        zip_path = _DATA_DIR / "countries.zip"
        urllib.request.urlretrieve(_URL, zip_path)

        with zipfile.ZipFile(zip_path) as z:
            z.extractall(_DATA_DIR)

    _WORLD = (
        gpd.read_file(shp_path)
        .to_crs("EPSG:4326")[["SOVEREIGNT", "SOV_A3", "geometry"]]
    )

    return _WORLD
