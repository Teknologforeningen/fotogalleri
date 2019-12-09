from django.shortcuts import redirect
from gallery.models import FeatureGate


class FeatureGateView():
    feature_gate_name = ''

    def is_feature_gated(self, user):
        feature_gate = FeatureGate.objects.filter(name=self.feature_gate_name).first()
        groups = feature_gate.feature_groups.all() if feature_gate else []
        return user.groups.filter(id__in=groups)

    def dispatch(self, request):
        if self.is_feature_gated(request.user):
            return super().dispatch(request)
        return redirect('home')
