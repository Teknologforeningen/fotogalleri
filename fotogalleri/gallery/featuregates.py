from django.shortcuts import redirect
from gallery.models import FeatureGate


class FeatureGateView():
    feature_gate_name = ''

    def is_feature_gated(self, user):
        feature_gate = FeatureGate.objects.filter(name=self.feature_gate_name)
        return user.groups.filter(id__in=feature_gate)

    def dispatch(self, request):
        if self.is_feature_gated(request.user):
            return super().dispatch(request)
        return redirect('home')


class AlphaGate(FeatureGateView):
    feature_gate_name = 'alpha'
