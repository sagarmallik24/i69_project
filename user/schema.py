import geopy

from django.db.models import fields
from django.db.models.query_utils import subclasses
from graphene_file_upload.scalars import Upload
from django.core.files import File
from framework.api.API_Exception import APIException
import graphene
from user.models import *
from chat.models import Room, Message, Notification, send_notification_fcm
#from framework.api.API_Exception import APIException
from gallery.models import Photo
from gallery.schema import PhotoObj
from user import models
from graphene.utils.resolve_only_args import resolve_only_args
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from .utils import get_gender_from_code
from datetime import datetime, timedelta
from django.utils import timesince
from django.conf import settings
from django.db import connection as conn

class CoinSettingType(DjangoObjectType):
    class Meta:
        model = models.CoinSettings
        fields = '__all__'

class CoinHistoryType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('gift_coins', 'purchase_coins',)

class UserPhotoType(graphene.ObjectType):
    id = graphene.Int()
    url = graphene.String()
    user = graphene.String()
    type = graphene.String()

    def resolve_id(self, info):
        return self.id

    def resolve_url(self, info):
        if self.file:
            try:
                url=info.context.build_absolute_uri(self.file.url)
            except:
                url=settings.DOMAIN_URL + self.file.url
            return url
        else:
            return self.file_url

    def resolve_user(self, info):
        return self.user.id

    def resolve_type(self, info):
        if str(self._meta) == 'user.userphoto':
            return "PUBLIC"
        elif str(self._meta) == 'user.privateuserphoto':
            hours = PrivatePhotoViewTime.objects.last().no_of_hours
            request = PrivatePhotoViewRequest.objects.filter(
                user_to_view=self.user,
                requested_user=info.context.user,
                status="A",
                updated_at__gte=datetime.now() - timedelta(hours=hours)
            )
            if request:
                print("REQUEST AVAILABLE")
                return "PUBLIC"
            else:
                print("REQUEST NOT AVAILABLE")
                return "PRIVATE"
        return ""

class Gender(graphene.ObjectType):
    code = graphene.String()
    name = graphene.String()

    def resolve_code(self, info):
        return self
    
    def resolve_name(self, info):
        return get_gender_from_code(self)

class isOnlineObj(graphene.ObjectType):
    id = graphene.String()
    isOnline = graphene.Boolean()
    username = graphene.String()

    def resolve_isOnline(self, info):
        return self['isOnline']

    def resolve_username(self, info):
        return self['username']

    def resolve_id(self, info):
        return self['id']

class OnlineObj(graphene.ObjectType):
    isOnline = graphene.Boolean()

    def resolve_isOnline(self, info):
        if isinstance(self, User):
            return self.isOnline

#list
class isLastLoginObj(graphene.ObjectType):
    id = graphene.String()
    username = graphene.String()
    last_login = graphene.String()

    class Meta:
        model = User
        fields = ("id", "username", 'last_login',)

#single
class lastLoginObj(graphene.ObjectType):
    id = graphene.String()
    username = graphene.String()
    last_login = graphene.String()

    class Meta:
        model = User
        fields = ("id", "username", 'last_login',)


class lastOnlineObj(graphene.ObjectType):
    id = graphene.String()
    last_seen = graphene.String()

    def resolve_last_seen(self, info):
        if self.user_last_seen:
            return timesince.timesince(self.user_last_seen)
        else:
            return timesince.timesince(self.created_at)


class locationDistance(graphene.ObjectType):
    id = graphene.String()
    distance = graphene.String()

    def resolve_distance(self, info):
        user1_location = info.context.user.location
        user2_location = self.location
        if user1_location and user2_location:
            try:
                distance = geopy.distance.geodesic(
                    user1_location.split(','), 
                    user2_location.split(',')
                ).km
                return f"{round(distance, 2)} Km"
            except:
                return "Location Undetermined."
        elif not user1_location:
            return "Location Undetermined."
            # raise Exception("Your location is not added.")
        elif not user2_location:
            return "Location Undetermined."
            # raise Exception(f'{self.fullName} has not entered their location.')


class UploadFileObj(graphene.ObjectType):
    id = graphene.String()
    success = graphene.Boolean()
    image_data = graphene.String()

class coinsResponseObj(graphene.ObjectType):
    id = graphene.String()
    coins = graphene.Int()
    success = graphene.Boolean()

class blockResponseObj(graphene.ObjectType):
    id = graphene.String()
    username = graphene.String()
    success = graphene.Boolean()

class updateCoin(graphene.Mutation):

    class Arguments:
        coins = graphene.Int()
        id = graphene.String()

    Output = coinsResponseObj

    def mutate(self, info, coins=None, id=None):
        user = User.objects.get(id=id)
        coin = user.coins
        print(coin)

        if coins is not None:
            user = user.addCoins(coins)

        user.save()
        return coinsResponseObj(id=user.id, success=True, coins=user.coins)

class privateUserPhotos(DjangoObjectType):
    class Meta:
        model = PrivateUserPhoto
        fields = ("id", "file")
    
    def resolve_file(self, obj):
        return self.file.url


class createPrivatePhotosMutation(graphene.Mutation):

    class Arguments:
        file = Upload(required=True)

    obj = graphene.Field(privateUserPhotos)

    def mutate(self, info, file):
        user = info.context.user
        private_photo = PrivateUserPhoto.objects.create(
            file=file,
            user=user
        )
        return createPrivatePhotosMutation(
            obj=private_photo
        )


class requestUserPrivatePhotosMutation(graphene.Mutation):
    msg = graphene.String()

    class Arguments:
        receiver_id = graphene.String(required=True)

    def mutate(self, info, receiver_id):
        user_obj = info.context.user
        receiver_obj = User.objects.filter(id=receiver_id).first()
        print(user_obj, receiver_obj)

        # CREATE REQUEST OBJECT
        request = PrivatePhotoViewRequest.objects.create(
            user_to_view=receiver_obj,
            requested_user=user_obj,
            status="P"
        )

        # IF NO CHAT CREATE ROOM
        room_name_a = [user_obj.username, receiver_obj.username]
        room_name_a.sort()
        room_name_str = room_name_a[0]+'_'+room_name_a[1]

        try:
            chat_room = Room.objects.get(name=room_name_str)
        except Room.DoesNotExist:
            chat_room = Room(name=room_name_str, user_id=user_obj, target=receiver_obj)
            chat_room.save()

            chat_room.last_modified = datetime.now()
            chat_room.save()

        # CREATE MESSAGE
        message = Message.objects.create(
            room_id=chat_room,
            user_id=user_obj,
            content=f"{user_obj.fullName} requested to view your private album.",
            message_type="P",
            private_photo_request_id=request.id
        )
        # SEND NOTIFICATION.
        notification_setting="SNDMSG"
        # checks for avatar_url if None
        try:
            avatar_url = user_obj.avatar().file.url
        except:
            avatar_url=None
        data={
            "roomID":chat_room.id,
            "notification_type":notification_setting,
            "message":message.content,
            "user_avatar":avatar_url,
            "title":"Sent message"
        }
        if avatar_url:
            icon=info.context.build_absolute_uri(avatar_url)
        android_channel_id=None
        notification_obj=Notification(
            user=receiver_obj, 
            sender=None,
            app_url=None,
            notification_setting_id=notification_setting,
            data=data,
            priority=None
        )
        send_notification_fcm(
            notification_obj=notification_obj, 
            android_channel_id=android_channel_id, 
            icon=icon, 
            image=icon
        )

        return requestUserPrivatePhotosMutation(
            msg='Request has been created.'
        )


class privatePhotoDecision(graphene.Mutation):
    success = graphene.Boolean()
    class Arguments:
        request_id = graphene.Int()
        decision = graphene.String()
    
    def mutate(self, info, request_id, decision):
        user_obj = info.context.user
        request = PrivatePhotoViewRequest.objects.filter(id=request_id).first()
        if request and decision in ['A', 'R']:
            if request.user_to_view == user_obj:
                # CHAT ROOM
                room_name_a = [user_obj.username, request.requested_user.username]
                room_name_a.sort()
                room_name_str = room_name_a[0]+'_'+room_name_a[1]

                try:
                    chat_room = Room.objects.get(name=room_name_str)
                except Room.DoesNotExist:
                    chat_room = Room(
                        name=room_name_str, 
                        user_id=user_obj, 
                        target=request.requested_user
                    )
                    chat_room.save()

                    chat_room.last_modified = datetime.now()
                    chat_room.save()
                if decision == 'A':
                    message = Message.objects.create(
                        room_id=chat_room,
                        user_id=user_obj,
                        content=f"{user_obj.fullName} approved your request",
                    )
                else:
                    message = Message.objects.create(
                        room_id=chat_room,
                        user_id=user_obj,
                        content=f"{user_obj.fullName} rejected your request",
                    )
                notification_setting="SNDMSG"
                # checks for avatar_url if None
                try:
                    avatar_url = user_obj.avatar().file.url
                except:
                    avatar_url=None
                data={
                    "roomID":chat_room.id,
                    "notification_type":notification_setting,
                    "message":message.content,
                    "user_avatar":avatar_url,
                    "title":"Sent message"
                }
                if avatar_url:
                    icon=info.context.build_absolute_uri(avatar_url)
                android_channel_id=None
                notification_obj=Notification(
                    user=request.requested_user, 
                    sender=None, 
                    app_url=None, 
                    notification_setting_id=notification_setting, 
                    data=data,
                    priority=None
                )
                send_notification_fcm(
                    notification_obj=notification_obj, 
                    android_channel_id=android_channel_id, 
                    icon=icon, 
                    image=icon
                )

                return privatePhotoDecision(success=True)
            else:
                return Exception("You are not allowed to approve this request.")

        else:
            return Exception("Invalid Request")

class ChatCoin(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        method = graphene.String()

    Output = coinsResponseObj

    def mutate(self, info, method=None, id=None):
        user = User.objects.get(id=id)
        if user.is_anonymous:
            return APIException("You must be logged in to use coins")
        coin = user.coins
        print(coin)
        # if method.upper() == "MESSAGE":
        #     user = user.deductCoin(19)

            
            

        # elif method.upper() == "IMAGE_MESSAGE":
        #     user = user.deductCoin(60)
            
            
        coin_settings = CoinSettings.objects.all()
        for coin_setting in coin_settings:
            if method.upper() == coin_setting.method.upper():
                if coin < coin_setting.coins_needed:
                    return APIException("Insufficient Coins")
                user.deductCoins(coin_setting.coins_needed)
                break
        else:
            return APIException("Please enter a valid method")
        if method.upper() == "PROFILE_PICTURE":
            user.photos_quota += 1
        user.save()
        return coinsResponseObj(id=user.id, success=True, coins=user.coins)

# class UpdateProfilePic(graphene.Mutation):
#     Output = UploadFileObj

#     class Arguments:
#         id = graphene.String()
#         image_data = graphene.String()

#     def mutate(self, info,  id=None, image_data=None):
#         user = User.objects.get(id=id)
#         avatar = image_data
#         user.avatar = avatar
#         user.save()
#         return UploadFileObj(id=user.id, image_data=user.avatar, success=True)

class MutationResponse(graphene.ObjectType):
    success = graphene.Boolean()
    message = graphene.String()

class DeleteAvatarPhoto(graphene.Mutation):
    Output = MutationResponse

    class Arguments:
        id = graphene.String(required=True)
        moderator_id = graphene.String()
    
    def mutate(self, info, id=None,moderator_id=None):
        user = info.context.user
        print(user)
        if not id:
            return MutationResponse(success=False, message="Id is required")

        if not user.is_authenticated:
            return MutationResponse(success=False, message="Authentication required")
        
        photos = models.UserPhoto.objects.filter(id=id)
        
        if(photos.count() == 0):
            return MutationResponse(success=False, message="Image not found")
        
        photo = photos[0]

        if moderator_id:
            fake_user = user.fake_users.all()
           
            if fake_user.count()>0:
                if fake_user.filter(id=moderator_id).count()>0:
                    photo.delete()
                    return MutationResponse(success=True, )
                else:                    
                    return MutationResponse(success=False, message="You are not authorized to delete this image")
               
        if photo.user.id != user.id:
            return MutationResponse(success=False, message="You are not authorized to delete this image")

        photo.delete()
        return MutationResponse(success=True, )

class blockUser(graphene.Mutation):
    Output = blockResponseObj

    class Arguments:
        id = graphene.String()
        blocked_id = graphene.String()

    def mutate(self, info, id, blocked_id):
        try:
            blckd_user = User.objects.get(id=blocked_id)
            user = User.objects.get(id=id)
        except Exception as e:
            raise Exception(f"User does not exist")
        if user == blckd_user:
            raise Exception("You can not block yourself")
        user.blockedUsers.add(blckd_user)
        user.save()

        return blockResponseObj(id=blckd_user.id, username=blckd_user.username, success=True)

class unblockUser(graphene.Mutation):
    Output = blockResponseObj

    class Arguments:
        id = graphene.String()
        blocked_id = graphene.String()

    def mutate(self, info, id, blocked_id):
        blckd_user = User.objects.get(id=blocked_id)
        user = User.objects.get(id=id)
        print("======================")
        print(user.blockedUsers)
        print("======================")
        user.blockedUsers.remove(blckd_user)
        user.save()

        return blockResponseObj(id=blckd_user.id, username=blckd_user.username, success=True)


class blockedUsers(graphene.ObjectType):
    id = graphene.String()
    username = graphene.String()
    def resolve_id(self, info):
        return self['id']
    
    def resolve_username(self, info):
        return self['username']

class Query(graphene.ObjectType):

    usersOnline = graphene.List(isOnlineObj)
    isOnline = graphene.Field(OnlineObj, id=graphene.String(required=True))

    inactiveUsers =  graphene.List(isLastLoginObj, from_time=graphene.String(required=True), to_time=graphene.String(required=True))
    lastLogin =  graphene.Field(lastLoginObj, id=graphene.String(required=True))
    lastOnline = graphene.Field(lastOnlineObj, id=graphene.String(required=True))
    user_location = graphene.Field(locationDistance, id=graphene.String(required=True))

    private_user_photos = graphene.List(privateUserPhotos, id=graphene.String(required=True))

    blockedUsers = graphene.List(blockedUsers)

    coinSettings = graphene.List(CoinSettingType)
    
    # depricated
    # photos = graphene.List(PhotoObj, id=graphene.String(required=True))

    def resolve_private_user_photos(self, info, **kwargs):
        user_obj = info.context.user
        user_to_view = User.objects.get(id=kwargs['id'])

        if user_obj == user_to_view:
            return PrivateUserPhoto.objects.filter(
                user=user_obj
            )
        else:
            hours = PrivatePhotoViewTime.objects.last().no_of_hours
            request = PrivatePhotoViewRequest.objects.filter(
                user_to_view=user_to_view,
                requested_user=user_obj,
                status="A",
                updated_at__gte=datetime.now() - timedelta(hours=hours)
            )
            if request:
                return PrivateUserPhoto.objects.filter(
                    user=user_to_view
                )
            else:
                return PrivateUserPhoto.objects.none()


    def resolve_usersOnline(self, info):
        try:
            return User.objects.filter(isOnline=True).values('isOnline','username','id')
        except:
            raise Exception("try again")

    def resolve_isOnline(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            user = User.objects.get(id=id)
            return user
        else:
            raise Exception('Id is a required parameter')

    def resolve_lastLogin(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                raise Exception('User not found')

            return user
        else:
            raise Exception('Id is a required parameter')

    def resolve_lastOnline(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                raise Exception('User not found')

            return user
        else:
            raise Exception('Id is a required parameter')

    def resolve_user_location(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                raise Exception('User not found')

            return user
        else:
            raise Exception('Id is a required parameter')

    def resolve_inactiveUsers(self, info, from_time='0.5', to_time='1'):
        """
        from_time and to_time is float
        30 minutes to 1 hour => 0.5 - 1
        1 hour to 5 hours => 1 - 5 
        ...
        """
        try:
            from2 = float(from_time)
        except ValueError:
            raise Exception("from_time needs to be a number of hours. can be float.")
        
        try:
            to2 = float(to_time)
        except ValueError:
            raise Exception("to_time needs to be a number of hours. can be float.")
            
        if float(from_time) > float(to_time):
            raise Exception("from_time cant be greater than to_time")

        if float(from_time) < 1:
            from_time = float(from_time) * 60
            from_time = datetime.today() - timedelta(hours=0, minutes=int(from_time))
        elif float(from_time) >= 1 and float(from_time) <= 24:
            minutes = 0
            if float(from_time) != int(from_time):
                minutes = int((float(from_time) - int(from_time))*60)
            from_time = datetime.today() - timedelta(hours=int(from_time), minutes=int(minutes))
        else:
            from_time = int(from_time) / 24
            hours = 0
            if float(from_time) != int(from_time):
                hours = int((float(from_time) - int(from_time))*24)
            from_time = datetime.today() - timedelta(days=int(from_time), hours=int(hours))

        if float(to_time) < 1:
            to_time = float(to_time) * 60
            to_time = datetime.today() - timedelta(hours=0, minutes=int(to_time))
        elif float(to_time) >= 1 and float(to_time) <= 24:
            minutes = 0
            if float(to_time) != int(to_time):
                minutes = int((float(to_time) - int(to_time))*60)
            to_time = datetime.today() - timedelta(hours=int(to_time), minutes=int(minutes))
        else:
            to_time = float(to_time) / 24
            hours = 0
            if float(to_time) != int(to_time):
                hours = int((float(to_time) - int(to_time))*24)
            to_time = datetime.today() - timedelta(days=int(to_time), hours=int(hours))
        try:
            from_time = from_time.strftime("%Y-%m-%d %H:%M:%S")
            to_time = to_time.strftime("%Y-%m-%d %H:%M:%S")
            users = User.objects.filter(last_login__range=(to_time,from_time)).values('id', 'username','last_login')
            return users
        except Exception as e:
            raise Exception("try again", e)


    def resolve_blockedUsers(self, info):
        id = info.context.user.id
        user = User.objects.get(id=id)
        return user.blockedUsers.all().values('id', 'username')
    
    def resolve_coinSettings(self, info):
        return CoinSettings.objects.all()

    # depricated
    # def resolve_photos(self, info, **kwargs):
    #     id = kwargs.get('id')
    #     if id is None:
    #         return Exception("Id is a required parameter")
    #     user = get_user_model().objects.get(id=id)
    #     return Photo.objects.filter(user=user)

class Mutation(graphene.ObjectType):
    updateCoin = updateCoin.Field()
    # depricated
    # UpdateProfilePic = UpdateProfilePic.Field()
    deleteAvatarPhoto = DeleteAvatarPhoto.Field()
    createPrivatePhoto = createPrivatePhotosMutation.Field()
    requestUserPrivatePhotos = requestUserPrivatePhotosMutation.Field()
    privatePhotoDecision = privatePhotoDecision.Field()
    blockUser = blockUser.Field()
    unblockUser = unblockUser.Field()
    deductCoin = ChatCoin.Field()
