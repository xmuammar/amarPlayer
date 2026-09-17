import runpy

# Runtime audio permission is requested by the native AmarPlayerActivity.
# The Qt bootstrap does not bundle Kivy's android.permissions module.

runpy.run_module("amarPlayer_android", run_name="__main__")
