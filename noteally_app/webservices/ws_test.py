
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from noteally_app.models import Download, Like, Material, StudyArea, User, University


@api_view(["POST"])
def populate_db(request):
    # Insert 5 study areas
    study_area1 = StudyArea(name="Computer Science")
    study_area1.save()
    study_area2 = StudyArea(name="Mathematics")
    study_area2.save()
    study_area3 = StudyArea(name="Physics")
    study_area3.save()
    study_area4 = StudyArea(name="Chemistry")
    study_area4.save()
    study_area5 = StudyArea(name="Biology")
    study_area5.save()

    # Insert 2 universities
    university1 = University(name="University of Aveiro")
    university1.save()
    university2 = University(name="University of Porto")
    university2.save()
    
    # Insert 2 users
    user1 = User(id_aws=1,
            name="John",
            email="john@ua.pt",
            premium=True,
            university=university1,
            karma_score=0,
            description="I'm a student at the University of Aveiro.",
            tutoring_services=True,
            profile_picture_name="john.jpg",
            profile_picture_link="https://noteally.s3.eu-west-3.amazonaws.com/john.jpg",
        )
    user1.save()
    
    user2 = User(id_aws=2,
            name="Jane",
            email="jane@ua.pt",
            premium=False,
            university=university2,
            karma_score=0,
            description="I'm a student at the University of Aveiro.",
            tutoring_services=False,
            profile_picture_name="jane.jpg",
            profile_picture_link="https://noteally.s3.eu-west-3.amazonaws.com/jane.jpg",
        )
    user2.save()
    
    # Insert 1 materials
    material1 = Material(user=user1,
            name="Introduction to Programming",
            description="Introduction to Programming",
            price=0,
            university=university1,
            file_name="introduction_to_programming.pdf",
            file="https://noteally.s3.eu-west-3.amazonaws.com/introduction_to_programming.pdf",
        )
    material1.save()
    
    # Insert 2 Download
    download1 = Download(user=user1,
            resource=material1,
            download_date="2021-05-01 00:00:00",
            hidden=False,
        )
    download1.save()
    
    download2 = Download(user=user2,
            resource=material1,
            download_date="2021-05-01 00:00:00",
            hidden=False,
        )
    download2.save()
    
    # Insert 1 Like
    like1 = Like(user=user1,
            resource=material1,
            like=True,
        )
    like1.save()
    
    return Response({"message": "Database populated successfully!"}, status=status.HTTP_200_OK)