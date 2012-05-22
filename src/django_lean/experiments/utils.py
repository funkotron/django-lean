# -*- coding: utf-8 -*-
import logging
l = logging.getLogger(__name__)

from django_lean.experiments.models import (AnonymousVisitor, Experiment,
                                            Participant)

class Subject(object):
    """
    A subject is a single identity which is participant in 0 or more experiments.
    """
    def __init__(self, session):
        """
        Note that .session may not be a contrib.session - it is just assumed
          to be a dict-like object which handles persisting itself.
        """
        self.session = session

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
        self.session['verified_human'] = True
        enrollments = self.session.get('temporary_enrollments', {})
        if not enrollments:
            # nothing to do - no need to create an AnonymousVisitor.
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

    def store_temporary_enrollment(self, experiment_name, group_id):
        enrollments = self.session.get('temporary_enrollments', None)
        if enrollments is None:
            self.session['temporary_enrollments'] = {}
        self.session['temporary_enrollments'][experiment_name] = group_id

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
    def __init__(self, session, user):
        super(WebSubject, self).__init__(session)
        self.user = user

    def is_anonymous(self):
        return self.user.is_anonymous()


class StaticParticipant(WebSubject):
    def __init__(self):
        from django.contrib.auth.models import AnonymousUser
        self.request = None
        self.user = AnonymousUser()
        self.session = {}


class WebSubjectFactory(object):
    """
    Factory that creates 'ExperimentUser' objects from a web context.
    """
    def create_user(self, context):
        request = context.get('request', None)
        if request is None:
            return StaticParticipant()
        return WebSubject(request.session, request.user)

