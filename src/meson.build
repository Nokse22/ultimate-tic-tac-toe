pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'ultimate_tactic'
gnome = import('gnome')

gnome.compile_resources('ultimate-tic-tac-toe',
  'ultimate-tic-tac-toe.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'ultimate-tic-tac-toe.in',
  output: 'ultimate-tic-tac-toe',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x'
)

ultimate_tactic_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'player_id_enum.py',
  'tic_button.py',
  'tic_tac_toe_grid.py',
]

install_data(ultimate_tactic_sources, install_dir: moduledir)
