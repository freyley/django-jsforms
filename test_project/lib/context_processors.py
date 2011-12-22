from django.conf import settings

CONTEXT_DICT = dict(
        LOGIN_URL=settings.LOGIN_URL,
        REQUIREJS_CONFIGS=settings.REQUIREJS_CONFIGS,
)

def config(request):
    return CONTEXT_DICT
