[app]
source.dir = .
title = Turbo Scanner
package.name = turboscanner
package.domain = org.turboscanner
source.include_exts = py,png,jpg,kv,atlas
source.include_patterns = assets/*,images/*.png
version = 1.0
requirements = python3,kivy,aiohttp
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
