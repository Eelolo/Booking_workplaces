from rest_framework.views import exception_handler


def custom_exception_handlers(exc, context):
    handlers = {
        'ValidationError': _handle_validation_error,
        'ParseError': _handle_parse_error,
        'AuthenticationFailed': _handle_authentication_failed,
        'NotAuthenticated': _handle_not_authenticated,
        'PermissionDenied': _handle_permission_denied,
        'NotFound': _handle_not_found,
        'MethodNotAllowed': _handle_method_not_allowed,
        'NotAcceptable': _handle_not_acceptable,
        'UnsupportedMediaType': _handle_unsupported_media_type,
        'Throttled': _handle_throttled,
    }

    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code

    exception_class = exc.__class__.__name__
    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    return response

def _handle_validation_error(exc, context, response):
    try:
        response.data = {
            'Error': {
                'status_code': 400,
                'error_message': response.data['Error'],
                'code': 'BAD_REQUEST'
            }
        }
    except KeyError:
        pass

    return response

def _handle_parse_error(exc, context, response):
    response.data = {
        'Error': {
            'status_code': 400,
            'error_message': 'Malformed request.',
            'code': 'BAD_REQUEST'
        }
    }
    return response

def _handle_authentication_failed(exc, context, response):
    response.data = {
        'Error': {
            'status_code': 401,
            'error_message': 'Incorrect authentication credentials. Authentication failed.',
            'code': 'UNAUTHORIZED'
        }
    }
    return response

def _handle_not_authenticated(exc, context, response):
    response.data = {
        'Error': {
            'status_code': 401,
            'error_message': 'Incorrect authentication credentials.',
            'code': 'UNAUTHORIZED'
        }
    }
    return response

def _handle_permission_denied(exc, context, response):
    response.data = {
        'Error': {
            'status_code': 403,
            'error_message': 'You do not have permission to perform this action.',
            'code': 'FORBIDDEN'
        }
    }
    return response

def _handle_not_found(exc, context, response):
    response.data = {
        'Error': {
            'status_code': 404,
            'error_message': 'Not found.',
            'code': 'NOT_FOUND'
        }
    }
    return response

def _handle_method_not_allowed(exc, context, response):
    response.data = {
        'Error': {
            'status_code': 405,
            'error_message': "Method '{}' not allowed.".format(context['request'].method),
            'code': 'METHOD_NOT_ALLOWED'
        }
    }
    return response

def _handle_not_acceptable(exc, context, response):
    response.data = {
        'Error': {
            'status_code': 406,
            'error_message': 'Could not satisfy the request Accept header.',
            'code': 'NOT_ACCEPTABLE'
        }
    }
    return response

def _handle_unsupported_media_type(exc, context, response):
    response.data = {
        'Error': {
            'status_code': 415,
            'error_message': 'Unsupported media type in request.',
            'code': 'UNSUPPORTED_MEDIA_TYPE'
        }
    }
    return response

def _handle_throttled(exc, context, response):
    response.data = {
        'Error': {
            'status_code': 429,
            'error_message': 'Request was throttled.',
            'code': 'TOO_MANY_REQUESTS'
        }
    }
    return response
