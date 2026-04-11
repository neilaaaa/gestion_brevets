from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import Utilisateur
from .serializers import UtilisateurSerializer


class UtilisateurViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is None:
        return Response(
            {'error': "Nom d'utilisateur ou mot de passe incorrect."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    token, created = Token.objects.get_or_create(user=user)

    return Response({
        'token': token.key,
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'groups': list(user.groups.values_list('name', flat=True)),
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    serializer = UtilisateurSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    token = Token.objects.filter(user=request.user).first()
    if token:
        token.delete()
    return Response({'message': 'Deconnexion reussie.'})
