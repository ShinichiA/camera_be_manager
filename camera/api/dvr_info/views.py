from rest_framework import status, views, mixins, generics
from rest_framework.exceptions import NotFound

from ...core.permissions import IsSuperuserUser
from ...models import DvrInfo
from .serializers import DvrInfoSerializer
from django.http import JsonResponse, Http404
from rest_framework.pagination import PageNumberPagination


class DvrInfoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class DvrListCreateView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = [IsSuperuserUser]
    models = DvrInfo
    queryset = models.objects.all()
    serializer_class = DvrInfoSerializer
    pagination_class = DvrInfoPagination

    def get(self, request, *args, **kwargs):
        # Lấy các tham số từ URL
        sn = request.query_params.get('sn', None)
        connect_type = request.query_params.get('connect_type', None)
        local_ip = request.query_params.get('local_ip', None)
        public_ip = request.query_params.get('public_ip', None)
        dvr_status = request.query_params.get('status', None)

        queryset = self.get_queryset()

        if sn:
            queryset = queryset.filter(sn__icontains=sn)
        if connect_type:
            queryset = queryset.filter(connect_type=connect_type)
        if local_ip:
            queryset = queryset.filter(local_ip__icontains=local_ip)
        if public_ip:
            queryset = queryset.filter(public_ip__icontains=public_ip)
        if dvr_status:
            queryset = queryset.filter(status=dvr_status)
        # Gọi mixin để xử lý trả về danh sách
        self.queryset = queryset
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # HASH AES 256 PASSWORD
        # IV - SECRET KEY
        serializer = self.serializer_class(data=request.data, many=False)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'success': True, 'data': serializer.data},
                                status=status.HTTP_200_OK)
        return JsonResponse({'success': False, 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class DvrRetrieveUpdateDestroyView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                                   generics.GenericAPIView):
    permission_classes = [IsSuperuserUser]
    models = DvrInfo
    queryset = models.objects.all()
    serializer_class = DvrInfoSerializer

    def get(self, request, *args, **kwargs):
        try:
            response = self.retrieve(request, *args, **kwargs)
            return JsonResponse({
                'success': True,
                'data': response.data
            }, status=status.HTTP_200_OK)
        except Http404:
            return JsonResponse({
                'success': False,
                'message': 'Not found.'
            }, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        try:
            dvr_info = self.get_object()
            serializer = self.get_serializer(dvr_info, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'success': True, 'data': serializer.data},
                                    status=status.HTTP_200_OK)
            return JsonResponse({'success': False, 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Http404:
            return JsonResponse({
                'success': False,
                'message': 'Not found.'
            })

    def delete(self, request, *args, **kwargs):
        try:
            self.destroy(request, *args, **kwargs)
            return JsonResponse({
                'success': True
            }, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return JsonResponse({
                'success': False,
                'message': 'Not found.'
            }, status=status.HTTP_400_BAD_REQUEST)
