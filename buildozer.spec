[app]

# (str) Title of your application
title = Turbo Scanner

# (str) Package name
package.name = turboscanner

# (str) Package domain (needed for android packaging)
package.domain = org.turboscanner

# (list) Source files to include (let it include python files etc)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of directory to include/exclude from source dir
source.include_patterns = assets/*,images/*.png

# (str) Application versioning
version = 1.0

# (list) Application requirements
requirements = python3,kivy,aiohttp

# (str) Custom source directory for your project
source.dir = .

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (int) Android NDK version to use
android.ndk = 25b

# (str) Android arch to build for
android.archs = arm64-v8a

# Automatically accept SDK licenses
android.accept_sdk_license = True


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
