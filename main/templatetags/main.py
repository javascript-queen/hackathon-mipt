from django import template
from django.conf import settings as ds
from django.utils.safestring import mark_safe
from django.templatetags.static import static as django_static
import functools
import hashlib
import json
import os
from pathlib import Path


register = template.Library()


@register.filter
def dict_merge(a, b):
    return a | b


@register.filter
def json_dumps(text):
    return json.dumps(text)


_vite_manifest = {}


@register.simple_tag
def vite_debug():
    return mark_safe(f"""
        <script type="module">
            import RefreshRuntime from '{ds.VITE_SERVER_BASE_URL}/static/build/@react-refresh'
            RefreshRuntime.injectIntoGlobalHook(window)
            window.$RefreshReg$ = () => {{}}
            window.$RefreshSig$ = () => (type) => type
            window.__vite_plugin_react_preamble_installed__ = true
        </script>
        <script type="module" src="{ds.VITE_SERVER_BASE_URL}/static/build/@vite/client"></script>
        <script type="module" src="{ds.VITE_SERVER_BASE_URL}/static/build/js/main.tsx"></script>
    """)


@register.simple_tag
def vite_asset(path):
    if not _vite_manifest:
        vite_manifest_static_dir = ds.BASE_ROOT.joinpath('static') if ds.DEBUG else ds.STATIC_ROOT
        vite_manifest = vite_manifest_static_dir.joinpath('build', 'assets.json')
        if not vite_manifest.exists():
            raise RuntimeError(f"Couldn't find vite manifest file at {vite_manifest}")
        _vite_manifest.update(json.loads(vite_manifest.read_text()))
    path_data = _vite_manifest.get(path.strip('/'))
    if not path_data:
        raise RuntimeError(f"There is no {path} key in vite manifest,"
                           f" verify the corresponding asset is listed in vite config's rollupOptions.input option"
                           f" / npm run prod / manage.py collectstatic etc.")
    real_path = path_data.get('file', None) if isinstance(path_data, dict) else None
    if not real_path:
        raise RuntimeError(f"Unexpected vite manifest data for path '{path}': {path_data} (type: {type(path_data)}).")
    path = 'build/' + real_path
    if path.endswith('.js'):
        return js_file(path, js_type='module')
    elif path.endswith('.css'):
        return css_file(path)
    else:
        raise NotImplementedError(f"Vite asset with extension '{Path(path).suffix}'"
                                  f" is not supported yet (impl in main app's vite_asset template tag).")


@register.simple_tag
def static_asset(path):
    if path.endswith('.js'):
        return js_file(path)
    elif path.endswith('.css'):
        return css_file(path)
    else:
        raise NotImplementedError(f"Static asset with extension '{Path(path).suffix}'"
                                  f" is not supported yet (impl in main app's static_asset template tag).")


@register.simple_tag
def css_file(path):
    path = static_file(path)
    return mark_safe("""<link href="{}" rel="stylesheet" type="text/css">""".format(path))


@register.simple_tag
def js_file(path, js_type=None):
    path = static_file(path)
    type_part = f' type="{js_type}"' if js_type else ''
    html = f'<script{type_part} src="{path}"></script>'
    return mark_safe(html)


@register.simple_tag(name='static')
def static_file(path):
    if not is_url(path):
        static_file_hash = _get_static_hash(path)
        path = django_static(str(path))
        if static_file_hash is not None:
            path = mark_safe(f'{path}?v={static_file_hash}')
    return path


@register.simple_tag
def static_hash(path):
    return _get_static_hash(path)


def _get_static_hash(path: str) -> str:
    return _get_static_hash_dev(path) if ds.DEBUG else _get_static_hash_prod(path)


@functools.cache
def _get_static_hash_prod(path: str) -> str:
    try:
        return _get_static_file_hash_in_dir(path, ds.STATIC_ROOT)
    except FileNotFoundError:
        return _calc_not_found_path_hash(path)


def _get_static_hash_dev(path: str) -> str:
    dirs = [ds.STATIC_ROOT] if not ds.LOCAL else reversed(ds.STATICFILES_DIRS)
    for static_dir in dirs:
        try:
            return _get_static_file_hash_in_dir(path, static_dir)
        except FileNotFoundError:
            continue
    return _calc_not_found_path_hash(path)


def _calc_not_found_path_hash(path: str) -> str:
    return hashlib.md5(f'//{ds.PROJECT_NAME}{path}'.encode('utf8')).hexdigest()


def _get_static_file_hash_in_dir(path: str, directory) -> str:
    path = os.path.join(directory, *path.split('/'))
    hash_base = str(os.path.getmtime(str(path)))
    return hashlib.md5(hash_base.encode('ascii')).hexdigest()


def is_url(s):
    s = s.strip()
    for i in ['http:', 'https:', '//']:
        if s.startswith(i):
            return True
    return False
