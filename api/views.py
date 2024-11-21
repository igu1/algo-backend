from dhanhq import dhanhq
from django.shortcuts import render
from django.conf import settings

# rest_framework
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated




class BuyOrder(APIView):
    # permission_classes = (IsAuthenticated,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dhan : dhanhq = dhanhq(client_id=settings.DHAN_CLIENT_ID, access_token=settings.DHAN_ACCESS_TOKEN)
    
    
    def post(self, request):
        security_id = request.data.get('security_id')
        if not security_id:
            return Response({'error': 'security_id is required (string: eg: 1333)'}, status=400)

        exchange_segment = request.data.get('exchange_segment', 'NSE')
        quantity = request.data.get('quantity')
        if quantity is None:
            return Response({'error': 'quantity is required (integer)'}, status=400)

        order_type = request.data.get('order_type', 'MARKET')
        product_type = request.data.get('product_type')
        if not product_type:
            return Response({'error': 'product_type is required (CNC, INTRA)'}, status=400)

        price = request.data.get('price')
        if price is None:
            return Response({'error': 'price is required (integer)'}, status=400)

        result = self.dhan.place_order(
            security_id=security_id,
            exchange_segment=self.dhan.NSE if exchange_segment == 'NSE' else self.dhan.BSE,
            transaction_type=self.dhan.BUY,
            quantity=int(quantity),
            order_type=self.dhan.MARKET if order_type == 'MARKET' else self.dhan.LIMIT,
            product_type=self.dhan.INTRA if product_type == 'INTRA' else self.dhan.CNC,
            price=int(price)
        )
        
        if str(result['status']).lower() == 'failure':
            return Response({'error': result['remarks']['error_message']}, status=400)
        
        return Response({'message': 'Order placed successfully'})

