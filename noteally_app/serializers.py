from rest_framework import serializers
from noteally_app.models import Material, User, StudyArea, Download, Like, University
from django.contrib.auth import authenticate 


# ------------------------------ User Serializers ------------------------------
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__' 


class UserMaterialIDSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'karma_score', 'description', 'tutoring_services', 'profile_picture_link', 'university', 'study_areas')
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
class RegisterSerializer(serializers.ModelSerializer):
    
   
    class Meta:
        model = User
        fields = ('id', 'password', 'id_aws', 'name', 'email', 'university', 'description', 'tutoring_services')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def save(self):
        user = User(
            id_aws=self.validated_data['id_aws'], 
            name=self.validated_data['name'],  
            email=self.validated_data['email'],
            premium=False,
            university=self.validated_data['university'],
            karma_score=0,
            description=self.validated_data['description'],
            tutoring_services=self.validated_data['tutoring_services'],
            profile_picture_name="",
            profile_picture_link="") 
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
