desktop_file = i18n.merge_file(
        input: 'fr.daemonwhite.mod_manager.desktop.in',
       output: 'fr.daemonwhite.mod_manager.desktop',
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
    'ui/modal/preference_mod.blp',
    'ui/stack/error.blp',
    'ui/stack/mod.blp',
    'ui/stack/order.blp',
    'ui/stack/settings.blp',
    'ui/widgets/check_row.blp',
    'ui/widgets/install_row.blp',
    'ui/widgets/progress_row.blp',
    'ui/widgets/preference_group_model.blp',
    'ui/widgets/preference_mod_stackpage.blp',
    'ui/widgets/switch_info_row.blp',
    'ui/widgets/stape_row.blp',
    'gtk/help-overlay.blp',
   ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

gnome.compile_resources('rust_linux_mod_manager',
  configure_file(
  	input: 'rust_linux_mod_manager.gresource.xml.in',
		output: 'rust_linux_mod_manager.gresource.xml',
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
  install_dir: get_option('datadir') / 'glib-2.0' / 'schemas'
)

compile_schemas = find_program('glib-compile-schemas', required: false, disabler: true)
test('Validate schema file',
     compile_schemas,
     args: ['--strict', '--dry-run', meson.current_source_dir()])


service_conf = configuration_data()
service_conf.set('bindir', get_option('prefix') / get_option('bindir'))
configure_file(
  input: 'fr.daemonwhite.mod_manager.service.in',
  output: 'fr.daemonwhite.mod_manager.service',
  configuration: service_conf,
  install_dir: get_option('datadir') / 'dbus-1' / 'services'
)

subdir('icons')
