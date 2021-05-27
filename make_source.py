from pyrocko.util import stt
from pyrocko.gf import PseudoDynamicRupture

# Define source
source = PseudoDynamicRupture(
    lat=37.821, lon=26.868,
    depth=1000.,
    time=stt('2020-10-30 11:51:24.955471'),
    strike=275.0, dip=57.5, rake=90.,
    length=65000., width=25000.,
    anchor='top',
    nucleation_x=[0.28], nucleation_y=[0.66],
    gamma=0.82,
    nx=8, ny=5, decimation_factor=5)

from pyrocko.gf import LocalEngine  # for GF handling
from pyrocko.plot.dynamic_rupture import RuptureMap

# Load store
engine = LocalEngine(store_superdirs=['/home/malde/src/gf_stores'])
store = engine.get_store('ak135_2000km_1Hz')

# Define source subfaults (patches) using store
# ground model parameters
source.discretize_patches(store)

# Plot source dislocation on map and save
m = RuptureMap(
    source=source,
    lat=source.lat, lon=source.lon,
    radius=source.length)
m.draw_dislocation()  # final static dislocation
m.draw_time_contour(store)  # rupture front contour
m.draw_nucleation_point()  # hypocenter
m.save('figures/pyrocko/map_final_dislocation.svg', psconvert=True)


from pyrocko.gf.tractions import DirectedTractions
source.rake = None
source.tractions = DirectedTractions(
    rake=-90.,  # direction of the stress drop vectors
    traction=1e6)  # length of the stress drop vectors in [Nm]

print(source.get_magnitude(store))

m = RuptureMap(
    source=source,
    lat=source.lat, lon=source.lon,
    radius=source.length)
m.draw_dislocation()  # final static dislocation
m.draw_time_contour(store)  # rupture front contour
m.draw_nucleation_point()  # hypocenter
m.save('figures/pyrocko/map_final_dislocation_traction.svg')

# source.slip = 2.0  # maximum slip vector length in [m]

from pyrocko.plot.dynamic_rupture import RuptureView
view = RuptureView(source=source)
view.draw_source_dynamics('stf', store)
view.save('figures/pyrocko/stf.svg')


view = RuptureView(source=source)
view.draw_source_dynamics('cumulative_moment', store)
view.show_plot()


from pyrocko.plot.dynamic_rupture import rupture_movie

rupture_movie(
    source, store, 'dislocation',
    plot_type='map',
    lat=source.lat, lon=source.lon,
    radius=source.length, clim=(0.45, 1.2),
    fn_path='movies/pyrocko')

rupture_movie(
    source, store, 'slip_rate',
    plot_type='map',
    lat=source.lat, lon=source.lon,
    radius=source.length,
    fn_path='movies/pyrocko')
