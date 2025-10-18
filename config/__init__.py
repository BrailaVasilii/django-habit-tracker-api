# -*- coding: utf-8 -*-
# Import Celery app pentru a se incarca cand Django porneste
from .celery import app as celery_app

__all__ = ('celery_app',)