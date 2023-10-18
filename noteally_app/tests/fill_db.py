from noteally_app.models import Download, Like, Material, StudyArea, User

def fill_db(self):
    # Insert 5 study areas
    self.study_area1 = StudyArea.objects.create(name="Computer Science")
    self.study_area2 = StudyArea.objects.create(name="Mathematics")
    self.study_area3 = StudyArea.objects.create(name="Physics")
    self.study_area4 = StudyArea.objects.create(name="Chemistry")
    self.study_area5 = StudyArea.objects.create(name="Biology")
    
    # Insert 2 users
    self.user1 = User.objects.create(id_aws=1,
            name="John",
            email="john@ua.pt",
            premium=True,
            university="University of Lisboa",
            karma_score=0,
            description="I'm a student at the University of Aveiro.",
            tutoring_services=True,
            profile_picture_name="john.jpg",
            profile_picture_link="https://noteally.s3.eu-west-3.amazonaws.com/john.jpg",
        )
    
    self.user2 = User.objects.create(id_aws=2,
            name="Jane",
            email="jane@ua.pt",
            premium=False,
            university="University of Aveiro",
            karma_score=0,
            description="I'm a student at the University of Aveiro.",
            tutoring_services=False,
            profile_picture_name="jane.jpg",
            profile_picture_link="https://noteally.s3.eu-west-3.amazonaws.com/jane.jpg",
        )
    
    # Insert 1 materials
    self.material1 = Material.objects.create(user=self.user1,
            name="Introduction to Programming",
            description="Introduction to Programming",
            price=0,
            university="University of Aveiro",
            file_name="introduction_to_programming.pdf",
            file="https://noteally.s3.eu-west-3.amazonaws.com/introduction_to_programming.pdf",
        )
    
    # Insert 2 Download
    self.download1 = Download.objects.create(user=self.user1,
            resource=self.material1,
            download_date="2021-05-01 00:00:00",
            hidden=False,
        )
    
    self.download2 = Download.objects.create(user=self.user2,
            resource=self.material1,
            download_date="2021-05-01 00:00:00",
            hidden=False,
        )
    
    # Insert 1 Like
    self.like1 = Like.objects.create(user=self.user1,
            resource=self.material1,
            like=True,
        )
    
    return self