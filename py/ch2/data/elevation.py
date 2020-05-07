
from logging import getLogger

from scipy.interpolate import UnivariateSpline

from .frame import present
from ..names import Names

log = getLogger(__name__)


def smooth_elevation(df, smooth=4):
    if not present(df, Names.ELEVATION):
        log.debug(f'Smoothing {Names.RAW_ELEVATION} to get {Names.ELEVATION}')
        unique = df.loc[~df[Names.DISTANCE].isna() & ~df[Names.RAW_ELEVATION].isna(),
                        [Names.DISTANCE, Names.RAW_ELEVATION]].drop_duplicates(Names.DISTANCE)
        # the smoothing factor is from eyeballing results only.  maybe it should be a parameter.
        # it seems better to smooth along the route rather that smooth the terrain model since
        # 1 - we expect the route to be smoother than the terrain in general (roads / tracks)
        # 2 - smoothing the 2d terrain is difficult to control and can give spikes
        # 3 - we better handle errors from mismatches between terrain model and position
        #     (think hairpin bends going up a mountainside)
        # the main drawbacks are
        # 1 - speed on loading
        # 2 - no guarantee of consistency between routes (or even on the same routine retracing a path)
        spline = UnivariateSpline(unique[Names.DISTANCE], unique[Names.RAW_ELEVATION], s=len(unique) * smooth)
        df[Names.ELEVATION] = spline(df[Names.DISTANCE])
        df[Names.GRADE] = (spline.derivative()(df[Names.DISTANCE]) * 100)  # two step to use rolling from pandas
        df[Names.GRADE] = df[Names.GRADE].rolling(5, center=True).median().ffill().bfill()
        # avoid extrapolation / interpolation
        df.loc[df[Names.RAW_ELEVATION].isna(), [Names.ELEVATION]] = None
    return df
