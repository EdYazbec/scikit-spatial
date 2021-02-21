from hypothesis import assume
from hypothesis import given

from ..constants import ATOL
from ..strategies import arrays_fixed
from ..strategies import consistent_dim
from skspatial.objects import Plane
from skspatial.objects import Points


@given(consistent_dim(3 * [arrays_fixed], max_dim=3))
def test_from_points(arrays):

    points = Points(arrays)
    assume(not points.are_collinear(tol=ATOL))

    # The plane must contain each point.
    plane = Plane.from_points(*points)

    points = points.set_dimension(plane.dimension)

    for point in points:
        assert plane.contains_point(point, abs_tol=ATOL)

    # The plane of best fit should be the same
    # as the plane from three points.
    plane_fit = Plane.best_fit(points)
    assert plane_fit.is_close(plane, abs_tol=ATOL)
