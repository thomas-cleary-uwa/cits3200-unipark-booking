""" decorators to be used in application views/routes

Authors: Thomas Cleary,
"""

from functools import wraps
from flask import abort
from flask_login import current_user
from ..models.user import Permission


def permission_required(permission):
    """ decorator @permission_required(perm)
        
    if current_user has permission do nothing, else return a 403 respoonse
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """ specific permission decorator for admin permission
        
    @admin_required
    """
    return permission_required(Permission.ADMIN)(f)