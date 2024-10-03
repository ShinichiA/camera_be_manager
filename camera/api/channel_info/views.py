from rest_framework import status, mixins, generics
from ...core.permissions import IsSuperuserUser
from ...models import ChannelInfo
from .serializers import ChannelInfoSerializer
from django.http import JsonResponse, Http404, HttpResponseBadRequest
from rest_framework.pagination import PageNumberPagination


class ChannelInfoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ChannelListCreateView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = [IsSuperuserUser]
    models = ChannelInfo
    queryset = models.objects.all()
    serializer_class = ChannelInfoSerializer
    pagination_class = ChannelInfoPagination

    def get(self, request, *args, **kwargs):
        # Lấy các tham số từ URL
        channel_no = request.query_params.get('channel_no', None)
        channel_name = request.query_params.get('channel_name', None)
        channel_status = request.query_params.get('status', None)

        queryset = self.get_queryset()

        if channel_no:
            queryset = queryset.filter(channel_no=channel_no)
        if channel_name:
            queryset = queryset.filter(channel_name__icontains=channel_name)
        if channel_status:
            queryset = queryset.filter(status=channel_status)

        # Gọi mixin để xử lý trả về danh sách
        self.queryset = queryset
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, many=False)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'success': True, 'data': serializer.data},
                                status=status.HTTP_200_OK)
        return JsonResponse({'success': False, 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ChannelRetrieveUpdateDestroyView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                                       generics.GenericAPIView):
    permission_classes = [IsSuperuserUser]
    models = ChannelInfo
    queryset = models.objects.all()
    serializer_class = ChannelInfoSerializer

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
