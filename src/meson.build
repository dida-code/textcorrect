pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'textcorrect'
gnome = import('gnome')

gnome.compile_resources('textcorrect',
  'textcorrect.gresource.xml',
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
  input: 'textcorrect.in',
  output: 'textcorrect',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x'
)

textcorrect_sources = [
  '__init__.py',
  'main.py',
  'window.py',
]

install_data(textcorrect_sources, install_dir: moduledir)
