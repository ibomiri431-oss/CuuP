[app]

# (str) Title of your application
title = Nexus Wordlist

# (str) Package name
package.name = nexus

# (str) Package domain (needed for android/ios packaging)
package.domain = org.nexus

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible (min 21)
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
#private_storage = True

# (str) Android NDK version to use
#android.ndk = 23b

# (bool) Skip byte compile for .py files
#android.skip_byte_compile = False

# (str) The log level (logcat)
log_level = 2
