from rest_framework import viewsets
from .models import Candidate
from .serializers import CandidateSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Case, When, Value, IntegerField


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    
    """Using ModelViewset which gives all the basic functionalities of GET POST PATCH PUT and DELETE"""

    ## Creating API for Search
    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        keyword = request.query_params.get('query', None)
        q = Q()
        if keyword and type(keyword) == str:
            relevancy_expression = Value(0, output_field=IntegerField())
            for k in keyword.split(" "):
                q |= Q(name__icontains=k)
                relevancy_expression += Case(When(name__icontains=k, then=Value(1)),default=Value(0),output_field=IntegerField())
            candidates = Candidate.objects.filter(q).annotate(relevancy=relevancy_expression).order_by('-relevancy')
            print(candidates.values("name","relevancy"))
        else:
            candidates = Candidate.objects.all()
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)
