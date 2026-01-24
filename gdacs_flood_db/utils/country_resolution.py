import pycountry
import pycountry_convert as pc


def resolve_country_from_gdacs(props: dict) -> dict | None:
    affected = props.get("affectedcountries")

    if isinstance(affected, list) and affected:
        c = affected[0] or {}
        return {
            "country_name": c.get("countryname"),
            "iso2": c.get("iso2"),
            "iso3": c.get("iso3"),
            "source": "gdacs",
        }

    if props.get("country"):
        return {
            "country_name": props.get("country"),
            "iso2": None,
            "iso3": None,
            "source": "gdacs",
        }

    return None


def continent_from_iso3(iso3: str) -> str | None:
    try:
        country = pycountry.countries.get(alpha_3=iso3.upper())
        if not country:
            return None
        code = pc.country_alpha2_to_continent_code(country.alpha_2)
        return pc.convert_continent_code_to_continent_name(code)
    except Exception:
        return None


def continent_from_country_name(name: str) -> str | None:
    try:
        country = pycountry.countries.lookup(name)
        code = pc.country_alpha2_to_continent_code(country.alpha_2)
        return pc.convert_continent_code_to_continent_name(code)
    except Exception:
        return None


def resolve_continent(country: dict | None) -> str | None:
    if not country:
        return None

    if country.get("iso3"):
        cont = continent_from_iso3(country["iso3"])
        if cont:
            return cont

    if country.get("country_name"):
        return continent_from_country_name(country["country_name"])

    return None
