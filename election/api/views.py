from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import RetrieveAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import *
from election.models import *

class CountryListAPIView(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CountryDetailAPIView(RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = 'name'


class VoivodeshipListAPIView(ListAPIView):
    queryset = Voivodeship.objects.all()
    serializer_class = VoivodeshipSerializer


class VoivodeshipDetailAPIView(RetrieveAPIView):
    queryset = Voivodeship.objects.all()
    serializer_class = VoivodeshipSerializer
    lookup_field = 'no'


class DistrictListAPIView(ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class DistrictDetailAPIView(RetrieveAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    lookup_field = 'no'


class CommuneListAPIView(ListAPIView):
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer


class CommuneDetailAPIView(RetrieveAPIView):
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer
    lookup_field = 'code'


class AuthenticatedWrite(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated()

class VoteDetailAPIView(RetrieveUpdateAPIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [AuthenticatedWrite]

    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    lookup_field = 'id'

class ResultsSetPagination(PageNumberPagination):

    page_size = 20

    def get_paginated_response(self, data):
        return Response({
                'count': self.page.paginator.count,
                'numPages': self.page.paginator.num_pages ,
                'pageSize': 20,
                'results': data
        })


class CommuneSearchList(ListAPIView):
    serializer_class = CommuneSearchSerializer
    pagination_class = ResultsSetPagination

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query != '':
            return Commune.objects.filter(name__icontains=query)
        else:
            return []

@csrf_exempt
def logout_token(request):
    return HttpResponse('')
