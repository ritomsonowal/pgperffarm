# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from rest_framework import mixins, viewsets, permissions

from rest_framework import authentication
from rest_framework.pagination import PageNumberPagination
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from filters import MachineRecordListFilter, UserMachineListFilter
from test_records.models import TestRecord
from users.models import UserMachine, UserProfile
from serializer import UserMachineManageSerializer, UserPortalInfoSerializer, TestRecordListSerializer, \
    UserMachineSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100

class MiddleResultsSetPagination(PageNumberPagination):
    page_size = 40
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserMachineRecordByBranchListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    List machine records by branch
    """

    queryset = TestRecord.objects.all().order_by('add_time')
    serializer_class = TestRecordListSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = MachineRecordListFilter

class UserMachineListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    List test records
    """
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )
    permission_classes = (permissions.IsAuthenticated, )
    queryset = UserMachine.objects.all().order_by('add_time')
    serializer_class = UserMachineManageSerializer
    pagination_class = MiddleResultsSetPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = UserMachineListFilter

    # def perform_create(self, serializer):
    #     shop_cart = serializer.save()
    #     goods = shop_cart.goods
    #     goods.goods_num -= shop_cart.nums
    #     goods.save()

    # def get_serializer_class(self):
    #     if self.action == 'create':
    #         return UserMachineSerializer
    #     else:
    #         return UserMachineManageSerializer

class PublicMachineListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    List all machines
    """
    queryset = UserMachine.objects.all().order_by('add_time')
    serializer_class = UserMachineManageSerializer
    pagination_class = MiddleResultsSetPagination

class UserPortalInfoViewSet( mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
     user info
    """
    # authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )
    # permission_classes = (permissions.IsAuthenticated, )
    lookup_field = 'username'
    queryset = UserProfile.objects.all()
    serializer_class = UserPortalInfoSerializer

class UserMachinePermission(permissions.BasePermission):
    """
    Machine upload permission check
    """

    def has_permission(self, request, view):
        secret = request.META.get("HTTP_AUTHORIZATION")
        print(secret)
        # alias = request.data.alias
        ret = UserMachine.objects.filter(machine_secret=secret, state=1).exists()
        return ret
