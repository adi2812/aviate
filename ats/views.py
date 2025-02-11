from rest_framework import viewsets
from .models import Candidate
from .serializers import CandidateSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        keyword = request.query_params.get('query', None)
        q = Q()
        if keyword and type(keyword) == str:
            for k in keyword.split(" "):
                q |= Q(name__icontains=k)
            candidates = Candidate.objects.filter(q)
        else:
            candidates = Candidate.objects.all()
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)
