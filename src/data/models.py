import uuid
from sqlmodel import Field, SQLModel


class LinkedinProfile(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    full_name: str
    workplace: str
    location: str
    connections: int
    photo: str
    followers: int
    about: str
    experiences: str
    number_of_experiences: int
    educations: str
    number_of_educations: int
    licenses: str
    number_of_licenses: int
    volunteering: str
    number_of_volunteering: int
    skills: str
    number_of_skills: int
    recommendations: str
    number_of_recommendations: int
    projects: str
    number_of_projects: int
    publications: str
    number_of_publications: int
    courses: str
    number_of_courses: int
    honors: str
    number_of_honors: int
    scores: str
    number_of_scores: int
    languages: str
    number_of_languages: int
    organizations: str
    number_of_organizations: int
    interests: str
    number_of_interests: int
    activities: str
    number_of_activities: int

    def __str__(self) -> str:
        return f"full_name={self.full_name}\n workplace={self.workplace}\n location={self.location}\n connections={self.connections}\n followers={self.followers}\n about={self.about}\n experiences={self.experiences}\n number_of_experiences={self.number_of_experiences}\n educations={self.educations}\n number_of_educations={self.number_of_educations}\n licenses={self.licenses}\n number_of_licenses={self.number_of_licenses}\n volunteering={self.volunteering}\n number_of_volunteering={self.number_of_volunteering}\n skills={self.skills}\n number_of_skills={self.number_of_skills}\n recommendations={self.recommendations}\n number_of_recommendations={self.number_of_recommendations}\n projects={self.projects}\n number_of_projects={self.number_of_projects}\n publications={self.publications}\n number_of_publications={self.number_of_publications}\n courses={self.courses}\n number_of_courses={self.number_of_courses}\n honors={self.honors}\n number_of_honors={self.number_of_honors}\n scores={self.scores}\n number_of_scores={self.number_of_scores}\n languages={self.languages}\n number_of_languages={self.number_of_languages}\n organizations={self.organizations}\n number_of_organizations={self.number_of_organizations}\n interests={self.interests}\n number_of_interests={self.number_of_interests}\n activities={self.activities}\n number_of_activities={self.number_of_activities})"
