from django.shortcuts import render
from functools import reduce
from django.db.models import Q, Count, Value
from django.db.models.functions import Concat
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Candidate
from .serializers import CandidateSerializer

# Create your views here.

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'], url_path='search-candidate')
    def search_candidates(self, request):
        query = request.query_params.get('name', '').strip().split()

        if not query:
            return Response({"message": "Name is required to search"}, status=status.HTTP_400_BAD_REQUEST)
        
        candidates = (Candidate.objects
                     .annotate(
                         full_name=Concat('name', Value(' ')),
                         relevancy=Count(
                             'id',
                             filter=Q(
                                reduce(lambda x, y: x | y, [Q(name__icontains=word) for word in query])
                             )
                         )
                     )
                     .filter(relevancy__gt=0)
                     .order_by('-relevancy'))

        serializer = self.get_serializer(candidates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

