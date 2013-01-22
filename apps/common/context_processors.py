def get_request_url(request):
    return {
        'full_path': request.get_full_path()
    }
