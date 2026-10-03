[app]

# (str) Title of your application
title = Mushafi

# (str) Package name
package.name = mushafi

# (str) Package domain (needed for android/ios packaging)
package.domain = com.mushafi

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty list for all the files)
source.include_exts = py,png,jpg,kv,atlas,json,txt,db

# (list) List of exclusions using pattern matching
source.exclude_exts = .git,.*

# (str) Application versioning (method 1)
version = 0.1.0

# (list) Application requirements
requirements = python3,kivy,requests

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# (list) Android permissions
android.permissions = RECORD_AUDIO,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# (int) Android API to use
android.api = 34

# (int) Minimum API required
android.minapi = 21

# (str) Android SDK version
android.sdk = 24

# (str) Android NDK version
android.ndk = 26b

# (str) Android architecture
android.arch = arm64-v8a

# (bool) Android license agreement
android.accept_sdk_license = True

[pwa]
orientation = portrait
