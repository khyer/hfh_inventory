from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializer
from django.http import Http404, HttpResponseBadRequest


class ItemViewSet(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticated,)


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticated,)


class ItemAction(generics.GenericAPIView):
    queryset = Item.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ItemSerializer
    # We will could eventually support other actions (eg un-pick would undo a pick)
    adder_actions = ['stock']
    subtractor_actions = ['pick']

    def post(self, request, pk, action, qty):
        item_instance = self.get_object()

        if qty < 1:
            return HttpResponseBadRequest('Quantity must be greater than 0')

        if action in self.adder_actions:
            item_instance.qty_in_stock += qty
        elif action in self.subtractor_actions:
            item_instance.qty_in_stock -= qty
        else:
            return HttpResponseBadRequest('Invalid action. Expecting one of: %s' % ', '.join(self.adder_actions+self.subtractor_actions ))

        item_instance.save()

        serializer = ItemSerializer(item_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)



