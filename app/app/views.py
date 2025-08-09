import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

logger = logging.getLogger(__name__)

@login_required
def home(request):
    logger.info(f"Usuario {request.user} accedió a la página de inicio.")
    return render(request, 'home.html')