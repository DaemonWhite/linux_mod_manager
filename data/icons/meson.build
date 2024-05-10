scalable_dir = 'hicolor' / 'scalable'

scalable_dir_apps = scalable_dir / 'apps'
install_data(
  scalable_dir_apps / ('@0@.svg').format(app_id),
  install_dir: get_option('datadir') / 'icons' / scalable_dir_apps
)

scalable_dir_action = scalable_dir / 'actions'

install_subdir(
	scalable_dir_action,
	install_dir: get_option('datadir') / 'icons' / scalable_dir
)

symbolic_dir = 'hicolor' / 'symbolic' / 'apps'
install_data(
  symbolic_dir / ('@0@-symbolic.svg').format(app_id),
  install_dir: get_option('datadir') / 'icons' / symbolic_dir
)
