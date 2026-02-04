[app]
title = Nexus Wordlist
package.name = nexuswordlist
package.domain = org.ibomiri
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy==2.2.1,pillow

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET

# (int) Target Android API
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) The log level (logcat)
log_level = 2
