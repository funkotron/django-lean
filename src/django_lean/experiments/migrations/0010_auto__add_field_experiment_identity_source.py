# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Experiment.identity_source'
        db.add_column('experiments_experiment', 'identity_source',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'Experiment.identity_source'
        db.delete_column('experiments_experiment', 'identity_source')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'experiments.anonymousvisitor': {
            'Meta': {'object_name': 'AnonymousVisitor'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'experiments.dailyconversionreport': {
            'Meta': {'object_name': 'DailyConversionReport'},
            'confidence': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'control_group_size': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiments.Experiment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'overall_control_conversion': ('django.db.models.fields.IntegerField', [], {}),
            'overall_test_conversion': ('django.db.models.fields.IntegerField', [], {}),
            'test_group_size': ('django.db.models.fields.IntegerField', [], {})
        },
        'experiments.dailyconversionreportgoaldata': {
            'Meta': {'object_name': 'DailyConversionReportGoalData'},
            'confidence': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'control_conversion': ('django.db.models.fields.IntegerField', [], {}),
            'goal_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiments.GoalType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'goal_data'", 'to': "orm['experiments.DailyConversionReport']"}),
            'test_conversion': ('django.db.models.fields.IntegerField', [], {})
        },
        'experiments.dailyengagementreport': {
            'Meta': {'object_name': 'DailyEngagementReport'},
            'confidence': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'control_group_size': ('django.db.models.fields.IntegerField', [], {}),
            'control_score': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiments.Experiment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'test_group_size': ('django.db.models.fields.IntegerField', [], {}),
            'test_score': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        },
        'experiments.experiment': {
            'Meta': {'object_name': 'Experiment'},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity_source': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'start_date': ('django.db.models.fields.DateField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'experiments.goalrecord': {
            'Meta': {'object_name': 'GoalRecord'},
            'anonymous_visitor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiments.AnonymousVisitor']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'goal_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiments.GoalType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'experiments.goaltype': {
            'Meta': {'object_name': 'GoalType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        'experiments.participant': {
            'Meta': {'unique_together': "(('user', 'experiment'), ('anonymous_visitor', 'experiment'))", 'object_name': 'Participant'},
            'anonymous_visitor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiments.AnonymousVisitor']", 'null': 'True', 'blank': 'True'}),
            'enrollment_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiments.Experiment']"}),
            'group': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        }
    }

    complete_apps = ['experiments']