from rest_framework import serializers
from noteally_app.models import Material, User, StudyArea, Download, Like, University 


# ------------------------------ User Serializers ------------------------------
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__' 
        depth = 2


class UserMaterialIDSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'sub', 'first_name', 'last_name', 'email', 'karma_score', 'description', 'tutoring_services', 'profile_picture', 'study_areas')
        depth = 1
        

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


class UniversityValueSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(source='id')
    
    class Meta:
        model = University
        fields = ('value', 'name')
        
        
# ------------------------------ Material Serializers ------------------------------
class MaterialSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = Material
            exclude = ['file']
            depth = 2
            
            
class PostMaterialSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = Material
            fields = ('user', 'name', 'description', 'price', 'university', 'file_name', 'file_size', 'file', 'study_areas')


class MaterialIDSerializer(serializers.ModelSerializer):
    upload_date = serializers.SerializerMethodField()
    user = UserMaterialIDSerializer()
    
    #format date
    def get_upload_date(self, obj):
        if obj.upload_date == None:
            return None
        return obj.upload_date.strftime("%d/%m/%Y %H:%M:%S")
        
    class Meta:
        model = Material
        fields = '__all__'
        fields = ('id', 'upload_date', 'name', 'description', 'price', 'file_name', 'file_size', 'total_likes', 'total_dislikes', 'total_downloads', 'user', 'university', 'study_areas')
        depth = 1
            
            
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
    universities = UniversityValueSerializer(many=True)
    study_areas = ValueStudyAreaSerializer(many=True)


# ------------------------------ Auth Serializers ------------------------------
class UserSessionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    sub = serializers.CharField(max_length=100)
    id_token = serializers.CharField(max_length=2000)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.CharField(max_length=100)
    premium = serializers.BooleanField()
    karma_score = serializers.IntegerField()
    tutoring_services = serializers.BooleanField()
    profile_picture = serializers.FileField()
    registered = serializers.BooleanField()
    description = serializers.CharField(max_length=2000) 
    study_areas = ValueStudyAreaSerializer(many=True)
