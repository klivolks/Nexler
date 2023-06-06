from bson import ObjectId
from daba.Mongo import collection


class User:
    user = collection("User")

    def __init__(self, _id=None, org=None, register_number=None, username=None, password=None, email=None, phone=None, first_name=None, last_name=None, date_of_birth=None, date_joined=None, last_login=None, profile_picture=None, bio=None, location=None, country=None, website=None, gender=None, social_links=None, language=None, timezone=None, account_verified=None, last_password_reset=None, security_question=None, security_answer=None, email_verified=None, phone_verified=None, is_active=None, is_superuser=None):
        
        self._id = _id
        self.org = org
        self.register_number = register_number
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.date_joined = date_joined
        self.last_login = last_login
        self.profile_picture = profile_picture
        self.bio = bio
        self.location = location
        self.country = country
        self.website = website
        self.gender = gender
        self.social_links = social_links
        self.language = language
        self.timezone = timezone
        self.account_verified = account_verified
        self.last_password_reset = last_password_reset
        self.security_question = security_question
        self.security_answer = security_answer
        self.email_verified = email_verified
        self.phone_verified = phone_verified
        self.is_active = is_active
        self.is_superuser = is_superuser

    def save(self):
        if self._id is None:  
            data = {
                'org': self.org,
                'register_number': self.register_number,
                'username': self.username,
                'password': self.password,
                'email': self.email,
                'phone': self.phone,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'date_of_birth': self.date_of_birth,
                'date_joined': self.date_joined,
                'last_login': self.last_login,
                'profile_picture': self.profile_picture,
                'bio': self.bio,
                'location': self.location,
                'country': self.country,
                'website': self.website,
                'gender': self.gender,
                'social_links': self.social_links,
                'language': self.language,
                'timezone': self.timezone,
                'account_verified': self.account_verified,
                'last_password_reset': self.last_password_reset,
                'security_question': self.security_question,
                'security_answer': self.security_answer,
                'email_verified': self.email_verified,
                'phone_verified': self.phone_verified,
                'is_active': self.is_active,
                'is_superuser': self.is_superuser
            }
            # Remove None values from data
            data = {k: v for k, v in data.items() if v is not None}
            result = self.user.put(data)
            self._id = result.inserted_id  # Update the ID with the newly generated ID.
        else:  # This user already exists, so update it.
            data = {
                'org': self.org,
                'register_number': self.register_number,
                'username': self.username,
                'password': self.password,
                'email': self.email,
                'phone': self.phone,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'date_of_birth': self.date_of_birth,
                'date_joined': self.date_joined,
                'last_login': self.last_login,
                'profile_picture': self.profile_picture,
                'bio': self.bio,
                'location': self.location,
                'country': self.country,
                'website': self.website,
                'gender': self.gender,
                'social_links': self.social_links,
                'language': self.language,
                'timezone': self.timezone,
                'account_verified': self.account_verified,
                'last_password_reset': self.last_password_reset,
                'security_question': self.security_question,
                'security_answer': self.security_answer,
                'email_verified': self.email_verified,
                'phone_verified': self.phone_verified,
                'is_active': self.is_active,
                'is_superuser': self.is_superuser
            }
            # Remove None values from data
            data = {k: v for k, v in data.items() if v is not None}
            result = self.user.set({'_id': ObjectId(self._id)},data)

    def get(self, query):
        return self.user.get(query)

    def getOne(self, query):
        return self.user.getOne(query)

    def update(self, query, new_data):
        return self.user.set(query, new_data)

    def delete(self, query):
        return self.user.deleteOne(query)

    def count(self, query):
        return self.user.count(query)
    
    @property
    def _id(self):
        return self.__id

    @_id.setter
    def _id(self, value):
        if value is not None:
            self.__id = ObjectId(value)
        else:
            self.__id = None

    @property
    def org(self):
        return self.__id

    @org.setter
    def org(self, value):
        if value is not None:
            self._org = ObjectId(value)
        else:
            self._org = None

