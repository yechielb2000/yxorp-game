from geoip2fast import GeoIP2Fast

_geoip = GeoIP2Fast("GeoLite2-Country.mmdb")


def get_geoip() -> GeoIP2Fast:
    return _geoip
