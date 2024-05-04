# from django.http import HttpResponseForbidden
#
# class ValidateOriginMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         # Get the HTTP referer header from the request
#         referer = request.headers.get('Referer')
#         # Check if the referer is present and matches your site's domain
#         if not referer or not referer.startswith(request.scheme + '://' + request.get_host()):
#             return HttpResponseForbidden('Access Forbidden')
#         return self.get_response(request)
