# from django_ratelimit.decorators import ratelimit

# class RateLimitMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = ratelimit(key='ip', rate='5/s')(self.get_response)(request)
#         return response
