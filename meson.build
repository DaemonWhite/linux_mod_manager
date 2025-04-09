project('linux_mod_manager', 'rust',
          version: '0.1.0',
    meson_version: '>= 1.0.0',
  default_options: [ 'warning_level=2', 'werror=false', ],
)

base_id = 'fr.daemonwhite.mod_manager'
path_id = '/fr/daemonwhite/mod_manager'

if get_option('devel') == true
	app_id = 'fr.daemonwhite.mod_manager.Devel'
	devel='devel'
else
	app_id = 'fr.daemonwhite.mod_manager'
	devel='prod'
endif

pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()

i18n = import('i18n')
gnome = import('gnome')

conf = configuration_data()
conf.set('APP_ID', app_id)
conf.set('PREFIX', path_id)
conf.set_quoted('LOCALEDIR', get_option('prefix') / get_option('localedir'))
conf.set_quoted('PKGDATADIR', pkgdatadir)
conf.set_quoted('VERSION', meson.project_version())
conf.set_quoted('DEVEL', devel)
conf.set_quoted('GETTEXT_PACKAGE', 'linux_mod_manager')

subdir('data')
subdir('src')
subdir('po')

gnome.post_install(
     glib_compile_schemas: true,
    gtk_update_icon_cache: true,
  update_desktop_database: true,
)
