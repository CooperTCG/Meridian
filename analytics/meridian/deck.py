"""Writes the fixed-width input deck the cropmod binary expects.

The format is defined by the FORMAT statements in model/cropmod.f and
is documented in docs/DECKFMT.txt.  It is column-exact.  If you change
a width here you must change it there, and the model has to be
re-validated afterwards, which is why nobody does.

    header 1 : A8   I4   F8.3        stnid, year, latitude
    header 2 : F8.2 F8.2             awc, rooting depth
    daily    : I3   F6.1 F6.1 F6.1 F6.2   doy, tmax, tmin, rain, srad
    trailer  : ' -1'
"""
from __future__ import annotations

from typing import Iterable, Sequence

DECK_NAME = "MERIDIAN.DAT"

# Soil parameters by station.  These live here rather than in the store
# because the 2008 schema has nowhere to put them.  MRD-91 is open to
# move them into a proper table.
SOIL = {
    "KTLRIDGE": (0.148, 1200.0),
    "AUBURN":   (0.162, 900.0),
    "WELLTON":  (0.131, 1050.0),
}
DEFAULT_SOIL = (0.145, 1000.0)

LATITUDE = {
    "KTLRIDGE": 43.548,
    "AUBURN":   43.912,
    "WELLTON":  44.207,
}
DEFAULT_LAT = 43.700


def soil_for(stnid: str):
    return SOIL.get(stnid.upper(), DEFAULT_SOIL)


def latitude_for(stnid: str) -> float:
    return LATITUDE.get(stnid.upper(), DEFAULT_LAT)


def write_deck(path: str, stnid: str, year: int, readings: Sequence) -> int:
    awc, rdepth = soil_for(stnid)
    lat = latitude_for(stnid)

    lines = []
    lines.append("%-8s%4d%8.3f" % (stnid[:8], year, lat))
    lines.append("%8.2f%8.2f" % (awc, rdepth))

    n = 0
    for r in readings:
        lines.append("%3d%6.1f%6.1f%6.1f%6.2f" % (
            r.doy, r.tmax, r.tmin, r.rain, r.srad))
        n += 1

    lines.append(" -1")

    with open(path, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    return n
