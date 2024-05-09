project('py_mod_manager',
          version: '0.1.0',
    meson_version: '>= 0.62.0',
  default_options: [ 'warning_level=2', 'werror=false', ],
)

if get_option('devel') == true
	app_id = 'fr.daemonwhite.mod_manager.Devel'
	prefix = '/fr/daemonwhite/mod_manager/devel'
	devel='devel'
else
	app_id = 'fr.daemonwhite.mod_manager'
	prefix = '/fr/daemonwhite/mod_manager'
	devel='prod'
endif

pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()

gnome = import('gnome')
python = import('python')
i18n = import('i18n')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('APP_ID', app_id)
conf.set('PREFIX', prefix)
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)
conf.set('VERSION', meson.project_version())
conf.set('DEVEL', devel)
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)


subdir('data')
subdir('src')
subdir('po')

gnome.post_install(
     glib_compile_schemas: true,
    gtk_update_icon_cache: true,
  update_desktop_database: true,
)
