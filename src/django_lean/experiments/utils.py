# -*- coding: utf-8 -*-
import logging, urlparse, threading
l = logging.getLogger(__name__)

from django_lean.conf import settings
from django.http import QueryDict
from django.utils.importlib import import_module

from django_lean.experiments.models import (AnonymousVisitor, Experiment,
                                            Participant)
from django_lean.experiments.exceptions import SessionNotFound

def create_url_session():
    """
    Creates a session for an url-backed experiment subject.
    """
    engine = import_module(settings.SESSION_ENGINE)
    session = engine.SessionStore()
    session.create()
    return session

# no actual implementation difference.. yet?
create_cookie_session = create_url_session

def _get_url_bits(url):
    url_parts = list(urlparse.urlparse(url))
    qs = url_parts[4]
    qd = QueryDict(qs, mutable=True)
    return url_parts, qd

def get_url_session_key(url):
    """
    Returns the url-backed experiment subject's session_key, or None.
    """

    url_parts, qd = _get_url_bits(url)
    session_key = qd.get(settings.LEAN_QUERYSTRING_NAME, '')
    if session_key == '':
        return None
    return session_key

def get_url_session(session_key):
    """
    """

    engine = import_module(settings.SESSION_ENGINE)
    store = engine.SessionStore()
    if session_key in (None, '') or (not store.exists(session_key)):
        raise SessionNotFound()
    return engine.SessionStore(session_key)

def put_url_session_key(url, session_key):
    """
    Retuns the given url with the session_key added (overwriting any existing key).
    """
    url_parts, qd = _get_url_bits(url)
    qd[settings.LEAN_QUERYSTRING_NAME] = session_key
    url_parts[4] = qd.urlencode()
    return urlparse.urlunparse(url_parts)

def remove_url_session_key(url):
    url_parts, qd = _get_url_bits(url)
    try:
        del qd[settings.LEAN_QUERYSTRING_NAME]
    except KeyError:
        pass
    url_parts[4] = qd.urlencode()
    return urlparse.urlunparse(url_parts)


class Subject(object):
    """
    A subject is a single identity which is participant in 0 or more experiments.
    """
    def __init__(self):
        self.managed = False

    def save(self):
        if self.managed and self.session.modified:
            self.session.save()
            # hack because django's session never unsets these under the presumption that 
            #  because it's tied to request cycle/cookie, it doesn't matter.
            self.session.accessed = False
            self.session.modified = False

    def is_anonymous(self):
        raise NotImplementedError

    def set_anonymous_id(self, anonymous_id):
        self.session['anonymous_id'] = anonymous_id

    def get_anonymous_id(self):
        return self.session.get('anonymous_id', None)

    def get_registered_user(self):
        if self.is_anonymous():
            return None
        return self.user

    def is_verified_human(self):
        return self.session.get('verified_human', False)

    def get_or_create_anonymous_visitor(self):
        anonymous_visitor = None
        anonymous_id = self.get_anonymous_id()
        if anonymous_id is not None:
            anonymous_visitors = AnonymousVisitor.objects.filter(
                id=anonymous_id
            )
            if len(anonymous_visitors) == 1:
                anonymous_visitor = anonymous_visitors[0]
        if not anonymous_visitor:
            anonymous_visitor = AnonymousVisitor.objects.create()
            self.set_anonymous_id(anonymous_visitor.id)
        return anonymous_visitor

    def confirm_human(self):
        """
        Until a Subject is confirmed to be human (through some means), 
          all of their enrollments are temporary.
        This is intended to ward off counting robots as Subjects, 
          which would artificially lower conversion rate and increase
          the number of observations needed to gain confidence.

        Once confirmed by calling this, we migrate temporary enrollments
          into the more structured Participant table.
        """
        self.session['verified_human'] = True
        enrollments = self.session.get('temporary_enrollments', {})
        if not enrollments:
            self.save()
            # no need to create an AnonymousVisitor.
            return

        anonymous_visitor = self.get_or_create_anonymous_visitor()
        for experiment_name, group_id in enrollments.items():
            try:
                experiment = Experiment.objects.get(name=experiment_name)
            except:
                continue
            try:
                Participant.objects.create(anonymous_visitor=anonymous_visitor,
                                           experiment=experiment,
                                           group=group_id)
            except:
                pass
            del self.session['temporary_enrollments'][experiment_name]
        self.save()

    def store_temporary_enrollment(self, experiment_name, group_id):
        enrollments = self.session.get('temporary_enrollments', {})
        enrollments[experiment_name] = group_id
        self.session['temporary_enrollments'] = enrollments
        self.save()

    def get_added_enrollments(self):
        return self.session.get('temporary_enrollments', None)

    def get_temporary_enrollment(self, experiment_name):
        added_enrollments = self.get_added_enrollments()
        if not added_enrollments:
            return None
        else:
            return added_enrollments.get(experiment_name, None)


class WebSubject(Subject):
    """
    Wrapper class that implements an 'ExperimentUser' object from a web
    request.
    """
    def __init__(self, cookie_session, user):
        super(WebSubject, self).__init__()
        self.session = cookie_session
        self.user = user

    def is_anonymous(self):
        return self.user.is_anonymous()

class UrlSubject(Subject):
    def __init__(self, url_session):
        super(UrlSubject, self).__init__()
        self.session = url_session
        self.managed = True

    def is_anonymous(self):
        return True

class StaticSubject(WebSubject):
    def __init__(self):
        super(StaticSubject, self).__init__()
        from django.contrib.auth.models import AnonymousUser
        self.request = None
        self.user = AnonymousUser()
        self.session = {}

class SubjectFactory(object):
    """
    Factory that creates 'ExperimentUser' objects from a web context.
    """
    def create_subject(self, source, context):
        request = context.get('request', None)
        if request is None:
            l.warning("no request found in context; using static participant.")
            return StaticSubject()
        return getattr(self, 'create_%s_subject' % source)(request)

    def create_cookie_subject(self, request):
        return WebSubject(request.session, request.user)

    def create_url_subject(self, request):
        return UrlSubject(request.url_session)
