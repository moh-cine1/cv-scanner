from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    linkedin = Column(String(255), nullable=True)
    github = Column(String(255), nullable=True)
    source_file = Column(String(500), nullable=True)

    skills = relationship("Skill", back_populates="candidate", cascade="all, delete-orphan")
    educations = relationship("Education", back_populates="candidate", cascade="all, delete-orphan")
    experiences = relationship("Experience", back_populates="candidate", cascade="all, delete-orphan")
    languages = relationship("Language", back_populates="candidate", cascade="all, delete-orphan")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)

    candidate = relationship("Candidate", back_populates="skills")


class Education(Base):
    __tablename__ = "educations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    raw_text = Column(Text, nullable=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)

    candidate = relationship("Candidate", back_populates="educations")


class Experience(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    raw_text = Column(Text, nullable=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)

    candidate = relationship("Candidate", back_populates="experiences")


class Language(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)

    candidate = relationship("Candidate", back_populates="languages")


def get_session(db_path: str = "sqlite:///cv_database.db"):
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()