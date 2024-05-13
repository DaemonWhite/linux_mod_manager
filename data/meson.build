pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())

desktop_file = i18n.merge_file(
	input: configure_file(
		input: 'fr.daemonwhite.mod_manager.desktop.in',
    	output: app_id + '.desktop.in',
      configuration: conf
  ),
  output: app_id + '.desktop',
  type: 'desktop',
  po_dir: '../po',
  install: true,
  install_dir: get_option('datadir') / 'applications'
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils, args: [desktop_file])
endif

appstream_file = i18n.merge_file(
        input: 'fr.daemonwhite.mod_manager.metainfo.xml.in',
       output: 'fr.daemonwhite.mod_manager.metainfo.xml',
       po_dir: '../po',
      install: true,
  install_dir: get_option('datadir') / 'metainfo'
)

appstreamcli = find_program('appstreamcli', required: false, disabler: true)
test('Validate appstream file', appstreamcli,
     args: ['validate', '--no-net', '--explain', appstream_file])

blueprints = custom_target('blueprints',
  input: files(
    'ui/window.blp',
    'ui/modal/choose_games.blp',
    'ui/modal/load.blp',
    'ui/modal/prefferences.blp',
    'ui/stack/error.blp',
    'ui/stack/mod.blp',
    'ui/stack/order.blp',
    'ui/stack/settings.blp',
    'ui/widgets/install_row.blp',
    'ui/widgets/progress_row.blp',
    'ui/widgets/switch_info_row.blp',
    'ui/widgets/stape_row.blp',
    'gtk/help-overlay.blp',
   ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

gnome.compile_resources('py_mod_manager',
  configure_file(
  	input: 'py_mod_manager.gresource.xml.in',
	output: 'py_mod_manager.gresource.xml',
	configuration: conf
  ),
  dependencies: blueprints,
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

install_data(
  configure_file(
    input: 'fr.daemonwhite.mod_manager.gschema.xml.in',
    output: app_id + '.gschema.xml',
    configuration: conf
  ),
  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')
)

compile_schemas = find_program('glib-compile-schemas', required: false, disabler: true)
test('Validate schema file',
     compile_schemas,
     args: ['--strict', '--dry-run', meson.current_source_dir()])

subdir('icons')