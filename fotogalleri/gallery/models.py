from django.db.models import Model, CharField, ManyToManyField
from django.contrib.auth.models import Group


class FeatureGate(Model):
    name = CharField(max_length=256, blank=False, null=False)
    feature_groups = ManyToManyField(Group, blank=False, related_name='featuregate')
