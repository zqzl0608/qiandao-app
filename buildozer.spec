[app]
title = 签到助手
package.name = qiandao
package.domain = org.qiandao
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

requirements = python3,kivy,requests,pillow,ddddocr,onnxruntime

orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1

android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 23b
android.arch = arm64-v8a

# 添加额外的依赖
android.add_dependencies = onnxruntime

[buildozer]
log_level = 2
warn_on_root = 1 