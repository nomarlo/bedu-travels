from rest_framework import serializers

from .models import User, Zona, Tour, Salida


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'nombre', 'apellidos', 'email', 'fechaNacimiento', 'genero', 'clave', 'tipo')


class Zona2Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Zona
        fields = ('id', 'nombre')


class TourSerializer(serializers.HyperlinkedModelSerializer):
    zonaSalida = Zona2Serializer(read_only=True)

    class Meta:
        model = Tour
        fields = ('id', 'slug', 'nombre', 'operador', 'tipoDeTour',
                  'descripcion', 'img', 'pais', 'zonaSalida', 'zonaLlegada',
                  'salidas')


class ZonaSerializer(serializers.HyperlinkedModelSerializer):
    tours_salida = TourSerializer(many=True, read_only=True)
    tours_llegada = TourSerializer(many=True, read_only=True)

    class Meta:
        model = Zona
        fields = ('id', 'nombre', 'descripcion', 'longitud', 'latitud', 'tours_salida', 'tours_llegada')


class SalidaSerializer(serializers.HyperlinkedModelSerializer):
    """ Serializador para atender las conversiones para Salida """
    class Meta:
        # Se define sobre que modelo actúa
        model = Salida
        # Se definen los campos a incluir
        fields = ('id', 'fechaInicio', 'fechaFin', 'asientos', 'precio', 'tour')
