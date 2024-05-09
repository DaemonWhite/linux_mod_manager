moduledir = pkgdatadir / 'py_mod_manager'

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

modules_src = [
	'custom_widget',
	'dialout',
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
