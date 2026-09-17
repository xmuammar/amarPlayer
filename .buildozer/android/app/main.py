import runpy

try:
    from android.permissions import Permission, request_permissions

    request_permissions([
        Permission.READ_MEDIA_AUDIO,
        Permission.READ_MEDIA_VIDEO,
        Permission.READ_EXTERNAL_STORAGE,
    ])
except Exception as error:
    print("Android permission request skipped:", error, flush=True)

runpy.run_module("amarPlayer_android", run_name="__main__")
