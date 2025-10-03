
# Generated SQLAlchemy Models from Database Schema

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class Author(Base):
    __tablename__ = 'authors'
    
    _id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    games = relationship("VideoGame", back_populates="author")
    game_authors = relationship("GameAuthor", back_populates="author")
    author_repos = relationship("AuthorRepo", back_populates="author")

class Publisher(Base):
    __tablename__ = 'publishers'
    
    _id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    marketplaces = relationship("Marketplace", back_populates="publisher")

class Repo(Base):
    __tablename__ = 'repos'
    
    _id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255))
    url = Column(String(500))
    gh_metadata = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    games = relationship("VideoGame", back_populates="repo")
    game_repos = relationship("GameRepo", back_populates="repo")
    author_repos = relationship("AuthorRepo", back_populates="repo")

class Indexer(Base):
    __tablename__ = 'indexers'
    
    _id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    url = Column(String(500))
    metadata = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    games = relationship("VideoGame", back_populates="indexer")

class Marketplace(Base):
    __tablename__ = 'marketplaces'
    
    _id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255))
    publisher_id = Column(Integer, ForeignKey('publishers._id'))
    url = Column(String(500))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    publisher = relationship("Publisher", back_populates="marketplaces")
    games = relationship("VideoGame", back_populates="marketplace")

class VideoGame(Base):
    __tablename__ = 'video_games'
    
    _id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    author_id = Column(Integer, ForeignKey('authors._id'))
    repo_id = Column(Integer, ForeignKey('repos._id'))
    marketplace_id = Column(Integer, ForeignKey('marketplaces._id'))
    indexer_id = Column(Integer, ForeignKey('indexers._id'))
    description = Column(Text)
    genre = Column(String(100))
    version = Column(String(50))
    rating = Column(String(10))
    price = Column(String(20))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    is_published = Column(Boolean, default=False)
    
    # Relationships
    author = relationship("Author", back_populates="games")
    repo = relationship("Repo", back_populates="games")
    marketplace = relationship("Marketplace", back_populates="games")
    indexer = relationship("Indexer", back_populates="games")
    game_authors = relationship("GameAuthor", back_populates="game")
    game_repos = relationship("GameRepo", back_populates="game")

class Dataset(Base):
    __tablename__ = 'datasets'
    
    _id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255))
    url = Column(String(500))
    repo_id = Column(Integer, ForeignKey('repos._id'))
    video_game_id = Column(Integer, ForeignKey('video_games._id'))
    dataset_type = Column(String(100))
    file_size = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    is_active = Column(Boolean, default=True)

# MANY-TO-MANY RELATIONSHIP MODELS

class GameAuthor(Base):
    __tablename__ = 'game_authors'
    
    game_id = Column(Integer, ForeignKey('video_games._id'), primary_key=True)
    author_id = Column(Integer, ForeignKey('authors._id'), primary_key=True)
    role = Column(String(100), default='developer')
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    game = relationship("VideoGame", back_populates="game_authors")
    author = relationship("Author", back_populates="game_authors")

class GameRepo(Base):
    __tablename__ = 'game_repos'
    
    game_id = Column(Integer, ForeignKey('video_games._id'), primary_key=True)
    repo_id = Column(Integer, ForeignKey('repos._id'), primary_key=True)
    repo_type = Column(String(50), default='main')
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    game = relationship("VideoGame", back_populates="game_repos")
    repo = relationship("Repo", back_populates="game_repos")

class AuthorRepo(Base):
    __tablename__ = 'author_repos'
    
    author_id = Column(Integer, ForeignKey('authors._id'), primary_key=True)
    repo_id = Column(Integer, ForeignKey('repos._id'), primary_key=True)
    contribution_type = Column(String(100), default='owner')
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    author = relationship("Author", back_populates="author_repos")
    repo = relationship("Repo", back_populates="author_repos")

class GameDataset(Base):
    __tablename__ = 'game_datasets'
    
    game_id = Column(Integer, ForeignKey('video_games._id'), primary_key=True)
    dataset_id = Column(Integer, ForeignKey('datasets._id'), primary_key=True)
    inclusion_reason = Column(String(200))
    created_at = Column(DateTime, default=func.now())
