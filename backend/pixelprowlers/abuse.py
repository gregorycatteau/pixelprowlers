"""Bounded, atomic quotas shared by Gunicorn workers in a single container.

Only HMAC address keys and counters are stored, never tokens or message bodies.
The protected local SQLite file is ephemeral across container replacements.
Multiple replicas require a separately qualified central store.
"""
import hashlib
import hmac
import ipaddress
import os
from pathlib import Path
import sqlite3
import stat
import time
from django.conf import settings
from graphql import GraphQLError

ERROR = 'Trop de demandes rapprochées. Votre saisie est conservée ; réessayez dans quelques minutes.'

def trusted_peer(request):
    try:
        address = ipaddress.ip_address(request.META.get('REMOTE_ADDR', ''))
        return any(address in ipaddress.ip_network(network) for network in settings.TRUSTED_PROXY_NETWORKS)
    except ValueError:
        return False

def client_ip(request):
    if request is None:
        return 'unknown'
    peer = request.META.get('REMOTE_ADDR', '')
    try:
        peer = str(ipaddress.ip_address(peer))
        if not trusted_peer(request):
            return peer
        chain = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')
        if len(chain) > 10:
            return peer
        for value in reversed(chain):
            address = ipaddress.ip_address(value.strip())
            if not any(address in ipaddress.ip_network(n) for n in settings.TRUSTED_PROXY_NETWORKS):
                return str(address)
        return peer
    except ValueError:
        return peer or 'unknown'

class TrustedProxyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if not trusted_peer(request):
            for header in ('HTTP_X_FORWARDED_FOR','HTTP_X_FORWARDED_PROTO','HTTP_X_FORWARDED_HOST'):
                request.META.pop(header, None)
        return self.get_response(request)

def allow(request, action, limit, window):
    path = Path(settings.RATE_LIMIT_DATABASE)
    try:
        path.parent.mkdir(mode=0o700, parents=False, exist_ok=True)
        metadata = path.parent.lstat()
        if not stat.S_ISDIR(metadata.st_mode) or metadata.st_uid != os.geteuid() or stat.S_IMODE(metadata.st_mode) != 0o700:
            return False
        descriptor = os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
        try:
            metadata = os.fstat(descriptor)
            if not stat.S_ISREG(metadata.st_mode) or metadata.st_uid != os.geteuid() or stat.S_IMODE(metadata.st_mode) != 0o600:
                return False
        finally:
            os.close(descriptor)
        key = hmac.new(settings.SECRET_KEY.encode(), (action + ':' + client_ip(request)).encode(), hashlib.sha256).hexdigest()
        now = time.time()
        with sqlite3.connect(path, timeout=2, isolation_level=None) as connection:
            connection.execute('CREATE TABLE IF NOT EXISTS quota (key TEXT PRIMARY KEY, count INTEGER NOT NULL, expires REAL NOT NULL)')
            connection.execute('BEGIN IMMEDIATE')
            connection.execute('DELETE FROM quota WHERE expires <= ?', (now,))
            row = connection.execute('SELECT count FROM quota WHERE key = ?', (key,)).fetchone()
            if row is not None:
                if row[0] >= limit:
                    connection.rollback()
                    return False
                connection.execute('UPDATE quota SET count=count+1 WHERE key=?', (key,))
            else:
                if connection.execute('SELECT count(*) FROM quota').fetchone()[0] >= 4096:
                    connection.rollback()
                    return False
                connection.execute('INSERT INTO quota VALUES (?,1,?)', (key, now + window))
            connection.commit()
            return True
    except (OSError, sqlite3.Error):
        return False

def require_quota(request, action, limit=60, window=600):
    if not allow(request, action, limit, window):
        raise GraphQLError(ERROR)
