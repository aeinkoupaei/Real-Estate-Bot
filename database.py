"""
Real Estate Database Manager
Handles all database operations for property management.
Uses SQLAlchemy ORM for database interactions.
All code comments and docstrings are in English.
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import config

# Create base class for ORM models
Base = declarative_base()


class Property(Base):
    """
    Database model for properties
    Stores all property information including location, specs, and amenities
    """
    __tablename__ = 'properties'
    
    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    
    # Basic information
    title = Column(String(200), nullable=False)
    property_type = Column(String(50), nullable=False)  # apartment, house, villa, land, etc.
    
    # Location information
    city = Column(String(100), nullable=False, index=True)
    neighborhood = Column(String(100), index=True)
    address = Column(Text)
    
    # Physical specifications
    area = Column(Float, nullable=False, index=True)  # Size in square meters/feet
    rooms = Column(Integer, index=True)  # Number of bedrooms
    floor = Column(Integer)  # Floor number
    year_built = Column(Integer)  # Year of construction
    
    # Financial information
    price = Column(Float, nullable=False, index=True)  # Price in local currency
    
    # Amenities
    parking = Column(Boolean, default=False)
    elevator = Column(Boolean, default=False)
    storage = Column(Boolean, default=False)
    
    # Additional details
    description = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        """
        Convert model to dictionary
        Useful for JSON serialization and API responses
        
        Returns:
            Dictionary representation of the property
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'property_type': self.property_type,
            'city': self.city,
            'neighborhood': self.neighborhood,
            'address': self.address,
            'area': self.area,
            'rooms': self.rooms,
            'floor': self.floor,
            'year_built': self.year_built,
            'price': self.price,
            'parking': self.parking,
            'elevator': self.elevator,
            'storage': self.storage,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_text(self):
        """
        Convert to human-readable text in English
        Formats property information for display in Telegram messages
        
        Returns:
            Formatted text string
        """
        amenities = []
        if self.parking:
            amenities.append('Parking')
        if self.elevator:
            amenities.append('Elevator')
        if self.storage:
            amenities.append('Storage')
        
        text = f"""
🏠 {self.title}
━━━━━━━━━━━━━━━━━━━━
📍 Location: {self.city}"""
        
        if self.neighborhood:
            text += f", {self.neighborhood}"
        
        text += f"""
📐 Area: {self.area} sq m
💰 Price: ${self.price:,.0f}
🏢 Type: {self.property_type}"""
        
        if self.rooms:
            text += f"\n🛏 Bedrooms: {self.rooms}"
        
        if self.floor:
            text += f"\n🏗 Floor: {self.floor}"
        
        if self.year_built:
            text += f"\n📅 Year Built: {self.year_built}"
        
        if amenities:
            text += f"\n✨ Amenities: {' | '.join(amenities)}"
        
        if self.address:
            text += f"\n📮 Address: {self.address}"
        
        if self.description:
            text += f"\n📝 Description: {self.description}"
        
        text += f"\n\n🆔 ID: {self.id}"
        
        return text


class DatabaseManager:
    """
    Manager class for database connections and operations
    Handles all CRUD operations for properties
    """
    
    def __init__(self, database_url=None):
        """
        Initialize database manager
        Creates database engine, session factory, and tables
        
        Args:
            database_url: Database connection URL (optional, uses config if not provided)
        """
        self.database_url = database_url or config.DATABASE_URL
        self.engine = create_engine(self.database_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        
        # Create all tables if they don't exist
        Base.metadata.create_all(self.engine)
    
    def get_session(self):
        """
        Get a new database session
        
        Returns:
            SQLAlchemy session object
        """
        return self.Session()
    
    def add_property(self, user_id, property_data):
        """
        Add a new property to the database
        Creates a new property record with the provided information
        
        Args:
            user_id: Telegram user ID of the property owner
            property_data: Dictionary containing property information
            
        Returns:
            ID of the newly created property
            
        Raises:
            Exception if database operation fails
        """
        session = self.get_session()
        try:
            property_obj = Property(
                user_id=user_id,
                title=property_data.get('title', 'Untitled Property'),
                property_type=property_data.get('property_type', 'Apartment'),
                city=property_data.get('city', ''),
                neighborhood=property_data.get('neighborhood'),
                address=property_data.get('address'),
                area=float(property_data.get('area', 0)),
                rooms=property_data.get('rooms'),
                floor=property_data.get('floor'),
                year_built=property_data.get('year_built'),
                price=float(property_data.get('price', 0)),
                parking=property_data.get('parking', False),
                elevator=property_data.get('elevator', False),
                storage=property_data.get('storage', False),
                description=property_data.get('description')
            )
            session.add(property_obj)
            session.commit()
            property_id = property_obj.id
            return property_id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_property(self, property_id):
        """
        Get a property by its ID
        
        Args:
            property_id: ID of the property to retrieve
            
        Returns:
            Property object or None if not found
        """
        session = self.get_session()
        try:
            return session.query(Property).filter(Property.id == property_id).first()
        finally:
            session.close()
    
    def get_user_properties(self, user_id, limit=50):
        """
        Get all properties belonging to a specific user
        
        Args:
            user_id: Telegram user ID
            limit: Maximum number of properties to return (default: 50)
            
        Returns:
            List of Property objects
        """
        session = self.get_session()
        try:
            return session.query(Property).filter(
                Property.user_id == user_id
            ).order_by(Property.created_at.desc()).limit(limit).all()
        finally:
            session.close()
    
    def search_properties(self, filters, limit=50):
        """
        Search for properties based on filters
        Applies multiple filters to find matching properties
        
        Args:
            filters: Dictionary of search filters
                - property_type: Type of property
                - city: City name
                - neighborhood: Neighborhood name
                - min_area: Minimum area
                - max_area: Maximum area
                - min_price: Minimum price
                - max_price: Maximum price
                - rooms: Number of bedrooms
                - parking: Parking required (boolean)
                - elevator: Elevator required (boolean)
            limit: Maximum number of results (default: 50)
            
        Returns:
            List of Property objects matching the filters
        """
        session = self.get_session()
        try:
            query = session.query(Property)
            
            # Limit to a specific user if requested
            if filters.get('user_id'):
                query = query.filter(Property.user_id == filters['user_id'])

            # Apply property type filter
            if filters.get('property_type'):
                query = query.filter(Property.property_type.contains(filters['property_type']))
            
            # Apply location filters
            if filters.get('city'):
                query = query.filter(Property.city.contains(filters['city']))
            
            if filters.get('neighborhood'):
                query = query.filter(Property.neighborhood.contains(filters['neighborhood']))
            
            # Apply area range filters
            if filters.get('min_area'):
                query = query.filter(Property.area >= filters['min_area'])
            
            if filters.get('max_area'):
                query = query.filter(Property.area <= filters['max_area'])
            
            # Apply price range filters
            if filters.get('min_price'):
                query = query.filter(Property.price >= filters['min_price'])
            
            if filters.get('max_price'):
                query = query.filter(Property.price <= filters['max_price'])
            
            # Apply bedroom count filter
            if filters.get('rooms'):
                query = query.filter(Property.rooms == filters['rooms'])
            
            # Apply amenity filters
            if filters.get('parking') is not None:
                query = query.filter(Property.parking == filters['parking'])
            
            if filters.get('elevator') is not None:
                query = query.filter(Property.elevator == filters['elevator'])
            
            # Return results ordered by most recent first
            return query.order_by(Property.created_at.desc()).limit(limit).all()
        finally:
            session.close()
    
    def filter_by_keywords(self, keywords, limit=50):
        """
        Filter properties by keywords
        Searches through title, description, address, and other text fields
        
        Args:
            keywords: Search keywords (string)
            limit: Maximum number of results (default: 50)
            
        Returns:
            List of Property objects containing the keywords
        """
        session = self.get_session()
        try:
            # Search in multiple text fields using OR condition
            search_filter = or_(
                Property.title.contains(keywords),
                Property.description.contains(keywords),
                Property.address.contains(keywords),
                Property.property_type.contains(keywords),
                Property.city.contains(keywords),
                Property.neighborhood.contains(keywords)
            )
            
            return session.query(Property).filter(
                search_filter
            ).order_by(Property.created_at.desc()).limit(limit).all()
        finally:
            session.close()
    
    def update_property(self, property_id, updates):
        """
        Update property information
        Updates only the specified fields, keeps other data unchanged
        
        Args:
            property_id: ID of the property to update
            updates: Dictionary of fields to update
            
        Returns:
            True if successful, False if property not found
            
        Raises:
            Exception if database operation fails
        """
        session = self.get_session()
        try:
            property_obj = session.query(Property).filter(Property.id == property_id).first()
            if property_obj:
                # Update each specified field
                for key, value in updates.items():
                    if hasattr(property_obj, key):
                        setattr(property_obj, key, value)
                
                # Update timestamp
                property_obj.updated_at = datetime.now()
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def delete_property(self, property_id, user_id=None):
        """
        Delete a property from the database
        Optionally verify ownership by checking user_id
        
        Args:
            property_id: ID of the property to delete
            user_id: Optional user ID to verify ownership
            
        Returns:
            True if successful, False if property not found or ownership mismatch
            
        Raises:
            Exception if database operation fails
        """
        session = self.get_session()
        try:
            query = session.query(Property).filter(Property.id == property_id)
            
            # If user_id provided, verify ownership
            if user_id:
                query = query.filter(Property.user_id == user_id)
            
            property_obj = query.first()
            if property_obj:
                session.delete(property_obj)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_statistics(self):
        """
        Get overall statistics about all properties
        Calculates total count, average price, and average area
        
        Returns:
            Dictionary containing statistics:
            - total_properties: Total number of properties
            - average_price: Average property price
            - average_area: Average property area
        """
        session = self.get_session()
        try:
            # Count total properties
            total_properties = session.query(Property).count()
            
            # Calculate average price
            avg_price = session.query(Property.price).filter(Property.price > 0).all()
            avg_price_value = sum([p[0] for p in avg_price]) / len(avg_price) if avg_price else 0
            
            # Calculate average area
            avg_area = session.query(Property.area).filter(Property.area > 0).all()
            avg_area_value = sum([a[0] for a in avg_area]) / len(avg_area) if avg_area else 0
            
            return {
                'total_properties': total_properties,
                'average_price': avg_price_value,
                'average_area': avg_area_value
            }
        finally:
            session.close()
