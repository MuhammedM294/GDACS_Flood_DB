import geopandas as gpd
from shapely.geometry import Point
from .geo_data import load_world_countries


def country_from_lonlat(lon: float, lat: float) -> dict | None:
    if lon is None or lat is None:
        return None

    world = load_world_countries()

    point_gdf = gpd.GeoDataFrame(
        geometry=[Point(lon, lat)],
        crs="EPSG:4326"
    )

    match = gpd.sjoin(
        point_gdf,
        world,
        how="left",
        predicate="intersects"
    )

    row = match.iloc[0]
    if row["SOVEREIGNT"] is None:
        return None

    return {
        "country_name": row["SOVEREIGNT"],
        "iso3": row["SOV_A3"],
        "source": "lonlat",
    }
