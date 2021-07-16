from django.utils.deprecation import MiddlewareMixin


class LastRequestMiddleware(MiddlewareMixin):
    """
    Middleware for update last request field after every authenticated request
    """

    def process_response(self, request, response, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.update_last_request()
        return response
