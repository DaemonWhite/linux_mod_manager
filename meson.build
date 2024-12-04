project('rust_linux_mod_manager', 'rust',
          version: '0.1.0',
    meson_version: '>= 1.0.0',
  default_options: [ 'warning_level=2', 'werror=false', ],
)

if get_option('devel') == 1
	app_id = 'fr.daemonwhite.mod_manager.Devel'
	prefix = '/fr/daemonwhite/mod_manager/devel'
	devel='devel'
else
	app_id = 'fr.daemonwhite.mod_manager'
	prefix = '/fr/daemonwhite/mod_manager'
	devel='prod'
endif

i18n = import('i18n')
gnome = import('gnome')

pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()

conf = configuration_data()
conf.set('APP_ID', app_id)
conf.set('PREFIX', prefix)
conf.set_quoted('VERSION', meson.project_version())
conf.set_quoted('GETTEXT_PACKAGE', 'rust_linux_mod_manager')
conf.set_quoted('LOCALEDIR', get_option('prefix') / get_option('localedir'))
conf.set_quoted('PKGDATADIR', pkgdatadir)
conf.set('DEVEL', get_option('devel'))

subdir('data')
subdir('src')
subdir('po')

gnome.post_install(
     glib_compile_schemas: true,
    gtk_update_icon_cache: true,
  update_desktop_database: true,
)
