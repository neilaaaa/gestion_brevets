from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import Utilisateur
from .serializers import UtilisateurSerializer

class UtilisateurViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Utilisateur.objects.all().order_by('id')
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    old_password = request.data.get('old_password', '')
    new_password = request.data.get('new_password', '')
    confirm_password = request.data.get('confirm_password', '')

    if not old_password or not new_password or not confirm_password:
        return Response(
            {'error': 'Tous les champs sont obligatoires.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not request.user.check_password(old_password):
        return Response(
            {'old_password': ["L'ancien mot de passe est incorrect."]},
            status=status.HTTP_400_BAD_REQUEST
        )

    if new_password != confirm_password:
        return Response(
            {'confirm_password': ['La confirmation ne correspond pas au nouveau mot de passe.']},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        validate_password(new_password, user=request.user)
    except DjangoValidationError as exc:
        return Response(
            {'new_password': list(exc.messages)},
            status=status.HTTP_400_BAD_REQUEST
        )

    request.user.set_password(new_password)
    request.user.save(update_fields=['password'])

    return Response({'message': 'Mot de passe modifie avec succes.'})
