from django.http import JsonResponse


def error_400(request, exception):
    data = {
        'Error': {
            'status_code': 400,
            'error_message': 'Invalid endpoint',
            'code': 'BAD_REQUEST'
        }
    }
    response = JsonResponse(data=data)
    response.status_code = 400

    return response


def error_404(request, exception):
    data = {
        'Error': {
            'status_code': 404,
            'error_message': 'The endpoint not found.',
            'code': 'NOT_FOUND'
        }
    }
    response = JsonResponse(data=data)
    response.status_code = 404

    return response


def error_500(request):
    data = {
        'Error': {
            'status_code': 500,
            'error_message': 'Internal Server Error.',
            'code': 'INTERNAL_ERROR'
        }
    }
    response = JsonResponse(data=data)
    response.status_code = 500

    return response