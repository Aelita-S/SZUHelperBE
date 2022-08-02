from rest_framework import serializers

from document.models import Document


class DocumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        exclude = ('content',)


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
