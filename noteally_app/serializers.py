from rest_framework import serializers
from noteally_app.models import Material, User, StudyArea, Download, Like


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
        
        
# ------------------------------ Material Serializers ------------------------------
class MaterialSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = Material
            fields = '__all__'
            
            
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
            
            
