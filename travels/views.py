# Create your views here.
from abc import ABC, abstractmethod

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tour, Zona, User, Salida, Boleto
from .serializers import UserSerializer, ZonaSerializer, TourSerializer, SalidaSerializer


@login_required()
def index(request):
    """ Vista para atender la petición de la url / """
    # Obteniendo los datos mediantes consultas
    tours = Tour.objects.all()
    zonas = Zona.objects.all()

    return render(request, "tours/index.html", {"tours": tours, "zonas": zonas})


# def login_user(request):
#     usuario_valido = ("bedutravels", "12345678")
#
#     if request.method == "POST":
#         next = request.GET.get("next", "/")
#         user = authenticate(
#             username=request.POST["username"],
#             password=request.POST["password"]
#         )
#
#         if user is not None:
#             login(request, user)
#             return redirect(next)
#         else:
#             message = "Datos incorrectos"
#     else:
#         message = "Request invalido"
#
#     return render(request, "registration/login.html", {
#         "msg": message,
#     })

def logout_user(request):
    """ Atiende las peticiones de GET /logout/ """
    # Se cierra la sesión del usuario actual
    logout(request)

    return redirect("/login/")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')

    serializer_class = UserSerializer


class ZonaViewSet(viewsets.ModelViewSet):
    queryset = Zona.objects.all().order_by('id')
    serializer_class = ZonaSerializer


class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all().order_by('id')
    serializer_class = TourSerializer


class SalidaViewSet(viewsets.ModelViewSet):
    """
    API que permite realizar operaciones con la tabla Salida
    """
    # Se define el conjunto de datos sobre el que va a operar la vista,
    # en este caso, sobre todos las salidas disponibles.
    queryset = Salida.objects.all().order_by('id')

    # Se define el serializador encargado de transformar las peticiones
    # de json a objetos django y viceversa.
    serializer_class = SalidaSerializer


STATUS_APPROVED = "approved"

STATUS_PENDING = "pending"

PAYMENT_METHOD_OXXO = "oxxo"


class BuyTicketRequestSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField()
    metodo_pago = serializers.ChoiceField(choices=['oxxo', 'debit_card', 'credit_card'])
    salida_id = serializers.IntegerField()


class BuyTicket(APIView):
    def post(self, request):
        request_serializer = BuyTicketRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        ticket_status = self._get_ticket_status(request_serializer)
        ticket = self._create_ticket(request_serializer, ticket_status)
        return Response({'id': ticket.id, 'status': ticket.status}, status=status.HTTP_201_CREATED)

    def _get_ticket_status(self, request: BuyTicketRequestSerializer):
        if request.data["metodo_pago"] == PAYMENT_METHOD_OXXO:
            return STATUS_PENDING
        return STATUS_APPROVED

    def _create_ticket(self, request: BuyTicketRequestSerializer, ticket_status):
        ticket = Boleto(metodo_pago=request.data["metodo_pago"], usuario_id=request.data["usuario_id"],
                        salida_id=request.data["salida_id"], status=ticket_status)
        ticket.save()
        return ticket



