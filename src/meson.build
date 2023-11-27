pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'py_mod_manager'

gnome = import('gnome')
python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'py_mod_manager.in',
  output: 'py_mod_manager',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

py_mod_manager_sources = [
  '__init__.py',
  'main.py',
  'window.py',
]


install_subdir('modal', install_dir: pkgdatadir)
install_subdir('stack', install_dir: pkgdatadir)
install_subdir('plugin_controller', install_dir: pkgdatadir)
install_subdir('utils', install_dir: pkgdatadir)
install_data(py_mod_manager_sources, install_dir: moduledir)
