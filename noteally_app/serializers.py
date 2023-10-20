from rest_framework import serializers
from noteally_app.models import Material, User, StudyArea, Download, Like, University


# ------------------------------ User Serializers ------------------------------
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'
        

# ------------------------------ StudyArea Serializers ------------------------------
class StudyAreaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = StudyArea
        fields = '__all__'


class ValueStudyAreaSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(source='id')

    class Meta:
        model = StudyArea
        fields = ('value', 'name')


# ------------------------------ University Serializers ------------------------------
class UniversitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = University
        fields = '__all__'


class UniversitySerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(source='id')
    
    class Meta:
        model = University
        fields = ('value', 'name')
        
        
# ------------------------------ Material Serializers ------------------------------
class MaterialSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = Material
            fields = '__all__'
            depth = 1
            
            
class PostMaterialSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = Material
            fields = ('user', 'name', 'description', 'price', 'university', 'file_name', 'file', 'study_areas')
            
            
# ------------------------------ Download Serializers ------------------------------
class DownloadSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = Download
            fields = '__all__'
            
            
# ------------------------------ Like Serializers ------------------------------
class LikeSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = Like
            fields = '__all__'
            
            
# ------------------------------ Info Serializers ------------------------------
class InfoSerializer(serializers.Serializer):
    universities = UniversitySerializer(many=True)
    study_areas = ValueStudyAreaSerializer(many=True)
