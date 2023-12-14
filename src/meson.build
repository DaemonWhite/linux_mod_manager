pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'py_mod_manager'

gnome = import('gnome')
python = import('python')

conf_python = configuration_data()
conf_python.set('PYTHON', python.find_installation('python3').full_path())
conf_python.set('localedir', get_option('prefix') / get_option('localedir'))
conf_python.set('pkgdatadir', pkgdatadir)

conf = configuration_data()
conf.set('VERSION', meson.project_version())
conf.set('DEVEL', devel)
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)


configure_file(
  input: 'const.in',
  output: 'const.py',
  configuration: conf,
  install: true,
  install_dir: moduledir,
  install_mode: 'r-xr--r--'
)

configure_file(
  input: 'py_mod_manager.in',
  output: 'py_mod_manager',
  configuration: conf_python,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

py_mod_manager_sources = [
  '__init__.py',
  'main.py',
  'window.py',
]

modules_src = [
	'custom_widget',
	'modal',
	'mod_handlers',
	'plugin_controller',
	'plugins',
	'stack',
	'utils',
]

foreach module : modules_src
	install_subdir(module, install_dir: pkgdatadir)
endforeach

install_data(py_mod_manager_sources, install_dir: moduledir)
