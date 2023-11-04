from noteally_app.models import Download, Like, Material, StudyArea, User, University

def fill_db(self):
    # Insert 5 study areas
    self.study_area1 = StudyArea.objects.create(name="Computer Science")
    self.study_area2 = StudyArea.objects.create(name="Mathematics")
    self.study_area3 = StudyArea.objects.create(name="Physics")
    self.study_area4 = StudyArea.objects.create(name="Chemistry")
    self.study_area5 = StudyArea.objects.create(name="Biology")

    # Insert 2 Universities
    self.university1 = University.objects.create(name="University of Aveiro")
    self.university2 = University.objects.create(name="University of Lisboa")
    
    # Insert 2 users
    self.user1 = User.objects.create(
        sub="123456789",
        first_name="John",
        last_name="Doe",
        email="john@ua.pt",
        premium=True,
        karma_score=0,
        description="I'm a student at the University of Aveiro.",
        tutoring_services=True,
        profile_picture_name="john.jpg",
        profile_picture="https://noteally.s3.eu-west-3.amazonaws.com/john.jpg",
    )
    
    self.user2 = User.objects.create(
        sub="987654321",
        first_name="Jane",
        last_name="Doe",
        email="jane@ua.pt",
        premium=False,
        karma_score=0,
        description="I'm a student at the University of Aveiro.",
        tutoring_services=False,
        profile_picture_name="jane.jpg",
        profile_picture="https://noteally.s3.eu-west-3.amazonaws.com/jane.jpg",
    )

    self.user3 = User.objects.create(
        sub="989898989",
        first_name="Peter",
        last_name="Doe",
        email="peter@ua.pt",
        premium=False,
        karma_score=0,
        description="I'm a student at the University of Aveiro.",
        tutoring_services=False,
        profile_picture_name="peter.jpg",
        profile_picture="https://noteally.s3.eu-west-3.amazonaws.com/peter.jpg",
    )

    # Insert 2 materials
    self.material1 = Material.objects.create(
        user=self.user1,
        name="Introduction to Programming",
        description="Introduction to Programming",
        price=0,
        university=self.university1,
        file_name="introduction_to_programming.pdf",
        file_size=1000,
        file="introduction_to_programming.pdf",
    )
    self.material1.study_areas.add(self.study_area1)
    
    # Insert 2 materials
    self.material2 = Material.objects.create(
        user=self.user1,
        name="Integrals Calculus",
        description="Introduction to Integrals",
        price=0,
        university=self.university2,
    )
    self.material2.study_areas.add(self.study_area2)

    # Insert 2 Download
    self.download1 = Download.objects.create(
        user=self.user1,
        resource=self.material1
    )
    
    self.download2 = Download.objects.create(
        user=self.user2,
        resource=self.material1
    )
    
    # Insert 1 Like
    self.like1 = Like.objects.create(
        user=self.user1,
        resource=self.material1,
        like=True,
    )
    
    return self