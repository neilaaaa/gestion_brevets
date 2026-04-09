from .models import Document, TypeDocument
from .serializers import DocumentSerializer, TypeDocumentSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class DocumentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    
    def get_queryset(self):
        # Chaque user voit seulement ses propres documents
        return Document.objects.filter(id=self.request.user)

class TypeDocumentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = TypeDocument.objects.all()
    serializer_class = TypeDocumentSerializer
