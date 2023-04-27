from itertools import chain
from googletrans import Translator
import graphene
from graphene_django import DjangoObjectType
from .models import *
from graphene_file_upload.scalars import Upload
from rest_framework.authtoken.models import Token
import mimetypes
import datetime
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay
from django_filters import FilterSet, OrderingFilter, CharFilter
from user.schema import UserPhotoType
from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from .tasks import createThumbnail
from chat.models import Notification, send_notification_fcm
import channels_graphql_ws
from django.contrib.auth.models import AnonymousUser

from defaultPicker.utils import custom_translate
from user.models import UserLimit
from moments.utils import detect_story, detect_moment, modify_text
from moments.utils import all_user_multi_stories_query
import traceback,json

EXPIRE_TIME =  24 #hours
translator = Translator()

class UserTypeone(DjangoObjectType):
    class Meta:
        model = User
        exclude = ('password',)
    avatar_photos = graphene.List(UserPhotoType)
    avatar = graphene.Field(UserPhotoType)

    def resolve_avatar(self, info):
        return self.avatar()

    def resolve_avatar_photos(self, info):
        print("WORKING")
        return list(chain(
            self.avatar_photos.all(), self.private_avatar_photos.all()
        ))

class GenericLikeType(DjangoObjectType):
    pk = graphene.Int(source='pk')
    class Meta:
        model=GenericLike
        filter_fields={}
        fields = '__all__'
        interfaces = (relay.Node,)

class GenericReplyType(DjangoObjectType):
    pk = graphene.Int(source='pk')

    class Meta:
        model=GenericComment
        filter_fields={}
        fields = '__all__'
        interfaces = (relay.Node,)

class GenericCommentType(DjangoObjectType):
    pk = graphene.Int(source='pk')
    replys = DjangoFilterConnectionField(GenericReplyType)
    class Meta:
        model=GenericComment
        filter_fields={}
        fields = '__all__'
        interfaces = (relay.Node,)


    def resolve_replys(self, info):
        return self.comments.all().order_by("-created_date")

class ReplyType(DjangoObjectType):
    class Meta:
        model= Comment
        filter_fields=('reply_to',)
        fields= ('id','user','momemt','comment_description', 'created_date', 'reply_to')
        interfaces = (relay.Node,)

class CommentFilter(FilterSet):
    pk = CharFilter(field_name='id', lookup_expr='exact')
    class Meta:
        model= Comment
        fields= ['momemt__id','id',]
    @property
    def qs(self):
        # The query context can be found in self.request.
        return super(CommentFilter, self).qs.filter(reply_to=None).order_by('-created_date')

class CommentType(DjangoObjectType):
    pk = graphene.Int(source='pk')
    class Meta:
        model= Comment
        fields= ('id','user','momemt','comment_description', 'created_date')
        filterset_class = CommentFilter
        interfaces = (relay.Node,)
    # replys = DjangoFilterConnectionField(ReplyType)
    replys = graphene.List(ReplyType)
    like = graphene.Int()
    def resolve_like(self, info):
        return CommentLike.objects.filter(comment=self).count()

    def resolve_replys(self,info):
        return Comment.objects.filter(reply_to=self).order_by('-created_date')

class MomentFilter(FilterSet):
    pk = CharFilter(field_name='id', lookup_expr='exact')
    class Meta:
        model= Moment
        fields= ['user__id','id',]
    @property
    def qs(self):
        # The query context can be found in self.request.
        return super(MomentFilter, self).qs.order_by("-created_date")

class MomentsTyps(DjangoObjectType):
    pk = graphene.Int(source='pk')
    class Meta:
        model= Moment
        fields=('id','Title','file','created_date','user','moment_description')
        filterset_class = MomentFilter
        interfaces = (relay.Node, )
    user = graphene.Field(UserTypeone)
    like = graphene.Int()
    comment = graphene.Int()
    moment_description_paginated = graphene.List(graphene.String, width=graphene.Int(), character_size=graphene.Int())


    def resolve_moment_description_paginated(self, info, width=None, character_size=None):

        try:
            max_length = int(width/character_size)

            description_length = len(self.moment_description)

            if max_length >= description_length:
                return [self.moment_description]
            char = None
            while max_length > 0:

                if char == ' ':
                    max_length = max_length+1

                    break
                char = self.moment_description[max_length]
                max_length = max_length-1
            desc_list = []
            desc_list.append(f"{self.moment_description[0:max_length]}")
            desc_list.append(self.moment_description[max_length:description_length-1])
            return desc_list
        except Exception as e:
            print(e)
            return [self.moment_description]




    def resolve_like(self, info):
        return Like.objects.filter(momemt=self).count()

    def resolve_comment(self, info):
        return Comment.objects.filter(momemt=self, reply_to=None).count()

class StoryFilter(FilterSet):
    pk = CharFilter(field_name='id', lookup_expr='exact')
    class Meta:
        model= Story
        fields= ['user__id','id',]
    @property
    def qs(self):
        # The query context can be found in self.request.
        try:
            visible_time = StoryVisibleTime.objects.all().first()
            hours=visible_time.hours+visible_time.days*24+visible_time.weeks*7*24

        except:
            hours = 24
        return super(StoryFilter, self).qs.filter(created_date__gte=datetime.datetime.now()-datetime.timedelta(hours=hours)).order_by('-created_date')


class StoryType(DjangoObjectType):
    pk = graphene.Int(source='pk')
    likes = DjangoFilterConnectionField(GenericLikeType)
    likes_count = graphene.Int()
    comments_count = graphene.Int()
    comments = DjangoFilterConnectionField(GenericCommentType)
    class Meta:
        model = Story
        fields = '__all__'
        interfaces = (relay.Node,)
        filterset_class=StoryFilter
    user = graphene.Field(UserTypeone)
    file_type  = graphene.String()

    def resolve_likes_count(self, info):
        return self.likes.all().count()
    def resolve_comments_count(self, info):
        return self.comments.all().count()

    def resolve_likes(self, info):
        return self.likes.all()
    def resolve_comments(self, info):
        return self.comments.all().order_by("-created_date")

    def resolve_file_type(self, info):
        if self.file:
            file_type,t =mimetypes.guess_type(str(self.file))
            return file_type.split('/')[0]
        return "unknown"


class MultiStoryType(graphene.ObjectType):
    user = graphene.Field(UserTypeone)
    stories = DjangoFilterConnectionField(StoryType)
    batch_number = graphene.Int()


class LikeType(DjangoObjectType):
    class Meta:
        model = Like
        fields = ('id','user','momemt')

class CommentLikeType(DjangoObjectType):
    class Meta:
        model = CommentLike
        fields = '__all__'




class ReportType(DjangoObjectType):
    class Meta:
        model = Report
        fields = ('id','user','momemt','Report_msg')


class StoryReportType(DjangoObjectType):
    class Meta:
        model = StoryReport
        fields = '__all__'



class MomentsUpdateResponse(graphene.ObjectType):
    success = graphene.Boolean()
    message = graphene.String()


class UpdateMomentMutation(graphene.Mutation):
    Output = MomentsUpdateResponse

    class Arguments:
        pk = graphene.Int(required=True)
        moment_description = graphene.String(required=True)

    def mutate(self,info,pk,moment_description):
        muser = info.context.user
        try:
            moment = Moment.objects.get(pk=pk,user=muser)
            print(moment)
            moment.moment_description=modify_text(moment_description)
            moment.save()
            NotifyUpdateMoment.broadcast(payload=moment, group="moments")
            return MomentsUpdateResponse(success=True, message="Moment Updated Successfuly!")
        except:
            return MomentsUpdateResponse(success=False,message="Moment not found!")



class Momentmutation(graphene.Mutation):
    class Arguments:
        user=graphene.String(required=True)
        Title=graphene.String(required=True)
        moment_description=graphene.String(required=True)
        file = Upload(required=True)
        moderator_id = graphene.String(required=False)
        # moment_description=graphene.String(required=True)

    moment=graphene.Field(MomentsTyps)

    @classmethod
    def mutate(cls,root,info,Title, moment_description, file, user,moderator_id=None):
        try:
            muser = info.context.user

            if moderator_id:  # if request sent my moderator then set user to moderator user.
                roles = [r.role for r in muser.roles.all()]
                if "ADMIN" in roles or "CHATTER" in roles or "REGULAR" in roles:
                    if not muser.fake_users.filter(id=moderator_id).exists():
                        raise Exception("Invalid moderator id")
                    muser = User.objects.filter(id=moderator_id).first()
                else:
                    return Exception("User cannot create moderator story")

            active_package = False
            active_package = muser.packages.filter(is_active=True).exists()


            if not active_package:
                user_story_count = Moment.objects.filter(user=muser).count()
                moments_limit = UserLimit.objects.get(action_name="Moments").limit_value

                if user_story_count >= moments_limit:
                    return Exception(
                        custom_translate(
                            info.context.user, 
                            "You have reached your free limit. Please purchase a package to post more moments."
                        )
                    )

            icon=None
            avatar_url = None
            # checks for avatar_url if None
            try:
                avatar_url = user.avatar().file.url
            except:
                avatar_url=None
            if avatar_url:
                icon=info.context.build_absolute_uri(avatar_url)

            new_moment = Moment(
                user=muser,
                Title=Title,
                moment_description=modify_text(moment_description),
                file=file
            )
            new_moment.save()

            status = detect_moment(new_moment, file) # if nude
            if status:
                return Exception("Your Moment has been submitted for admin review.")

            send_moment_broadcast_fcm(moment_obj=new_moment,icon=icon,image=icon)
            NotifyNewMoment.broadcast(payload=new_moment, group="moments")
            return Momentmutation(moment=new_moment)

        except Exception as e:
            print(e)
            raise Exception("error found")


class NotifyMoment(channels_graphql_ws.Subscription):
    moment = graphene.Field(MomentsTyps)
    id = graphene.ID()

    class Arguments:
        token = graphene.String()
        moderator_id = graphene.String()

    @staticmethod
    def subscribe(root, info, token, moderator_id=None):
        try:
            token = Token.objects.get(key=token)
            print("token user schema: ", token.user.username)
            user = token.user
            user.last_login=datetime.datetime.now()
            user.save()
            if user.fake_users.all().count()>0:
                if moderator_id:
                    if not user.fake_users.filter(id=moderator_id).exists():
                        raise Exception("Invalid moderator_id")
                    user=User.objects.get(id=moderator_id)
                    user.last_login=datetime.datetime.now()
                    user.save()
                else:
                    raise Exception("moderator_id required")

        except Token.DoesNotExist:
            print("token user schema: not found ")
            user = AnonymousUser()

        # return [str(user.id)] if user is not None and user.is_authenticated else []
        return ["moments"]

    @staticmethod
    def publish(payload, info, token=None, moderator_id=None):
        return NotifyNewMoment(
            moment=payload
        )



class NotifyNewMoment(NotifyMoment):
    pass


class NotifyUpdateMoment(NotifyMoment):
    pass


class NotifyDeleteMoment(channels_graphql_ws.Subscription):
    moment =graphene.JSONString()
    id = graphene.ID()

    class Arguments:
        token = graphene.String()
        moderator_id = graphene.String()

    @staticmethod
    def subscribe(root, info, token, moderator_id=None):
        try:
            token = Token.objects.get(key=token)
            print("token user schema: ", token.user.username)
            user = token.user
            user.last_login=datetime.datetime.now()
            user.save()
            if user.fake_users.all().count()>0:
                if moderator_id:
                    if not user.fake_users.filter(id=moderator_id).exists():
                        raise Exception("Invalid moderator_id")
                    user=User.objects.get(id=moderator_id)
                    user.last_login=datetime.datetime.now()
                    user.save()
                else:
                    raise Exception("moderator_id required")

        except Token.DoesNotExist:
            print("token user schema: not found ")
            user = AnonymousUser()

        # return [str(user.id)] if user is not None and user.is_authenticated else []
        return ["moments"]

    @staticmethod
    def publish(payload, info, token=None, moderator_id=None):
        return NotifyDeleteMoment(
            moment=payload,
            id=payload["id"]
        )


class OnDeleteStory(channels_graphql_ws.Subscription):
    """Subscription triggers on a delete story occurs."""

    user_id = graphene.String()
    story_id = graphene.Int()

    def subscribe(cls, info):
        user = info.context.user
        return [str(user.id)] if user is not None and user.is_authenticated else []

    def publish(self, info):
        return OnDeleteStory(
            user_id=self['user_id'],
            story_id=self['story_id'],
        )


class OnNewStory(channels_graphql_ws.Subscription):
    """Subscription triggers on a new story occurs."""

    user = graphene.Field(UserTypeone)
    stories = DjangoFilterConnectionField(StoryType)
    batch_number = graphene.Int()

    def subscribe(cls, info):
        user = info.context.user
        return [str(user.id)] if user is not None and user.is_authenticated else []

    def publish(self, info):
        limit = UserLimit.objects.get(action_name="MultiStoryLimit").limit_value
        total_stories = Story.objects.filter(
            user__id=self['user_id'],
            created_date__gte=datetime.datetime.now()-datetime.timedelta(hours=24)
        ).order_by('-created_date')
        batch_number = total_stories.count() / limit
        batch_number = batch_number if batch_number.is_integer() else batch_number + 1
        stories_to_send = total_stories.count() % limit
        if stories_to_send:
            results = {
                "user": User.objects.get(id=self['user_id']),
                "stories": total_stories[:stories_to_send],
                "batch_number": batch_number
            }
        else:
            results = {
                "user": User.objects.get(id=self['user_id']),
                "stories": total_stories[:limit],
                "batch_number": batch_number
            }
        return OnNewStory(
            user=results['user'],
            stories = Story.objects.filter(id__in=[i.id for i in results['stories']]),
            batch_number=results['batch_number']
        )

# def createThumbnail(**kwargs):
#     file=kwargs['file']
#     story=kwargs['story']
#     print(file)
#     print(story)
#     with tempfile.NamedTemporaryFile(mode="wb") as vid:


#                 vidcap = cv2.VideoCapture(story.file.path)

#                 success,image = vidcap.read()

#                 if success:
#                     _, img = cv2.imencode('.jpeg', image)
#                     img.tobytes()
#                     file = ContentFile(img)
#                     story.thumbnail.save('thumbnail.jpeg', file , save=True)
#                     return


class Storymutation(graphene.Mutation):
    class Arguments:
        file=Upload(required=True)
        moderator_id = graphene.String(required=False)


    story=graphene.Field(StoryType)

    @classmethod
    def mutate(cls,root,info,file,moderator_id=None):
        user = info.context.user
        if moderator_id:  # if request sent my moderator then set user to moderator user.
            roles = [r.role for r in user.roles.all()]
            if "ADMIN" in roles or "CHATTER" in roles or "REGULAR" in roles:
                if not user.fake_users.filter(id=moderator_id).exists():
                    raise Exception("Invalid moderator id")
                user = User.objects.filter(id=moderator_id).first()
            else:
                return Exception("User cannot create moderator story")
        
        active_package = False
        active_package = user.packages.filter(is_active=True).exists()

        if not active_package:
            user_story_count = Story.objects.filter(user=user).count()
            stories_limit = UserLimit.objects.get(action_name="Stories").limit_value

            if user_story_count > stories_limit:
                return Exception(
                    custom_translate(
                        info.context.user, 
                        "You have reached your free limit. Please purchase a package to post more stories."
                    )
                )

        new_story = Story(user=user, file=file)
        file_type, t = mimetypes.guess_type(str(file))
        if file_type.split('/')[0] == "video":
            try:
                with open('static/img/thumbnail.png', "rb") as f:
                    thumbnail = File(f)
                    new_story.thumbnail.save('thumbnail.jpeg', thumbnail , save=True)
            except FileNotFoundError:
                raise Exception("Thumbnail image does not exist")
            createThumbnail.delay(new_story.id)

        new_story.save()

        status = detect_story(new_story, file) # if nude
        if status:
            return Exception("Your Story has been submitted for admin review.")

        OnNewStory.broadcast(
            group=None,
            payload={
                "user_id": str(new_story.user.id),
                "story_id": new_story.id
            }
        )
        return Storymutation(story=new_story)


class DeleteMomentType(graphene.ObjectType):
    id = graphene.Int()


class MomentDeleteMutation(graphene.Mutation):

    id = graphene.Int()
    success = graphene.String()
    
    class Arguments:
        id=graphene.ID()
        
    @classmethod
    def mutate(cls,root,info,id):
        try:
            delete_moment=Moment.objects.filter(id=id).first()
            delete_moment.delete()
   
            NotifyDeleteMoment.broadcast(payload={"id": id}, group="moments")
            return MomentDeleteMutation(success="delete successfully",id=id)
        
        except Exception as e:
            print(e,traceback.print_exc())
            raise Exception("invalid moment id")

class Storydeletemutation(graphene.Mutation):
    success=graphene.String()
    id = graphene.Int()
    
    class Arguments:
        id=graphene.ID()


    @classmethod
    def mutate(cls,root,info,id):
        # print(request.user)
        user = info.context.user

        try:
            if  user.roles.filter(role__in=["ADMIN"]):
                delete_story=Story.objects.filter(id=id).first()
            else:
                delete_story=Story.objects.filter(id=id,user=user).first()
                
            story_id = delete_story.id
            delete_story.delete()

            OnDeleteStory.broadcast(
                group=None,
                payload={
                    "user_id": str(user.id),
                    "story_id": story_id
                }
            )
            return Storydeletemutation(success="Story deleted successfully",id=story_id )
        except:
            raise Exception("invalid story id or not have access to delete")


class Momentlikemutation(graphene.Mutation):
    class Arguments:
        # user=graphene.String(required=True)
        moment_id=graphene.ID()

    like=graphene.Field(LikeType)

    @classmethod
    def mutate(cls,root,info,moment_id):

        user = info.context.user
        try:
            moment=Moment.objects.get(id=moment_id)
        except Moment.DoesNotExist:
            return Exception("Invalid moment_id")

        like=Like.objects.filter(user=user, momemt_id=moment_id)
        if like.exists():
            like=like[0]
            like.delete()
            return Momentlikemutation(like=like)
        new_like=Like(user=user, momemt_id=moment_id)
        new_like.save()
        # new_like.save()
        # TODO: set data payload, user avtar as icon
        notification_setting="LIKE"
        data={
            "momentId": moment.id,
            "likeID": new_like.id,
            "notification_type":notification_setting,
        }
        priority=None
        icon=None
        app_url=None
        android_channel_id=None

        notification_obj=Notification(user=moment.user, sender=user, app_url=app_url, notification_setting_id=notification_setting, data=data,priority=priority)
        send_notification_fcm(notification_obj=notification_obj, android_channel_id=android_channel_id, icon=icon)

        return Momentlikemutation(like=new_like)

class CommentLikeMutation(graphene.Mutation):
    class Arguments:
        comment_id = graphene.String()

    comment_like=graphene.Field(CommentLikeType)
    @classmethod
    def mutate(cls,root,info,comment_id):
        user = info.context.user
        commentlike=CommentLike.objects.filter(user=user, comment_id=comment_id)
        if commentlike.exists():
            commentlike=commentlike[0]
            commentlike.delete()
            return CommentLikeMutation(commentlike)

        new_commentlike=CommentLike(user=user, comment_id=comment_id)
        new_commentlike.save()
        notification_to=new_commentlike.comment.user

        # TODO: set data payload, user avtar as icon
        data={}
        priority=None
        icon=None
        app_url=None
        android_channel_id=None
        notification_setting="CMNTLIKE"

        notification_obj=Notification(user=notification_to, sender=user, app_url=app_url, notification_setting_id=notification_setting, data=data,priority=priority)
        send_notification_fcm(notification_obj=notification_obj, android_channel_id=android_channel_id, icon=icon)

        return CommentLikeMutation(new_commentlike)

class Momentcommentmutation(graphene.Mutation):
    class Arguments:
        # user=graphene.String(required=True)
        moment_id=graphene.ID()
        comment_description=graphene.String(required=True)
        reply_to=graphene.String(required=False)

    comment=graphene.Field(CommentType)

    @classmethod
    def mutate(cls,root,info,moment_id,comment_description, reply_to=None):
        user=info.context.user
        comment_description = modify_text(comment_description)
        new_comment=Comment(user=user, momemt_id=moment_id,comment_description=comment_description, reply_to_id=reply_to)
        new_comment.save()

        notification_to=new_comment.momemt.user

        # TODO: set data payload, user avtar as icon
        notification_setting="CMNT"
        data={
            "momentId": int(moment_id),
            "commentID": new_comment.id,
            "notification_type":notification_setting,
        }
        priority=None
        icon=None
        app_url=None
        android_channel_id=None

        notification_obj=Notification(user=notification_to, sender=user, app_url=app_url, notification_setting_id=notification_setting, data=data,priority=priority)
        send_notification_fcm(notification_obj=notification_obj, android_channel_id=android_channel_id, icon=icon)

        return Momentcommentmutation(comment=new_comment)

class Momentreportmutation(graphene.Mutation):
    class Arguments:
        # user=graphene.String(required=True)
        moment_id=graphene.ID()
        Report_msg=graphene.String(required=True)

    report=graphene.Field(ReportType)

    @classmethod
    def mutate(cls,root,info,moment_id,Report_msg):
        user=info.context.user
        moment = None
        try:
            moment = Moment.objects.get(id=moment_id)
        except Moment.DoesNotExist:
            raise Exception("Moment does not exist")
        if moment.user == user:
            raise Exception("You cannot report your moments")
        new_report=Report(user=user, momemt_id=moment_id,Report_msg=Report_msg )
        new_report.save()
        return Momentreportmutation(report=new_report)

class Storyreportmutation(graphene.Mutation):
    class Arguments:
        # user=graphene.String(required=True)
        story_id=graphene.ID()
        Report_msg=graphene.String(required=True)

    story_report=graphene.Field(StoryReportType)

    @classmethod
    def mutate(cls,root,info,story_id,Report_msg):
        user=info.context.user
        story = None
        try:
            story = Story.objects.get(id=story_id)
        except Story.DoesNotExist:
            raise Exception("Story does not exist")
        if story.user == user:
            raise Exception("You cannot report your story")
        new_report=StoryReport(user=user, story_id=story_id,Report_msg=Report_msg )
        new_report.save()
        return Storyreportmutation(story_report=new_report)



class TranslateMomentMutation(graphene.Mutation):
    class Arguments:
        moment_id = graphene.Int()

    translated_text = graphene.String()

    @classmethod
    def mutate(cls, root, info, moment_id):
        moment = Moment.objects.get(id=moment_id)

        return TranslateMomentMutation(
            translated_text=custom_translate(
                info.context.user, 
                moment.moment_description
            )
        )

class GenericCommentMutation(graphene.Mutation):
    generic_comment = graphene.Field(GenericCommentType)
    class Arguments:
        object_type=graphene.String()
        comment_description=graphene.String()
        object_id=graphene.Int()


    @classmethod
    def mutate(cls, root, info, object_type, object_id,comment_description):
        user = info.context.user
        content_type=ContentType.objects.get(app_label="moments", model=object_type)
        comment_description = modify_text(comment_description)
        new_comment=GenericComment(user=user, comment_description=comment_description, content_type=content_type, object_id=object_id)
        new_comment.save()
        story=Story.objects.get(id=object_id)
        notification_to=story.user
        # TODO: set data payload, user avtar as icon

        notification_setting="STCMNT"
        data={
            'comment_comment_description':comment_description,
            "pk": story.id,
            "commentID": new_comment.id,
            "notification_type":notification_setting,
            "comment_description":comment_description,
        }
        priority=None
        icon=None
        app_url=None
        android_channel_id=None

        notification_obj=Notification(user=notification_to, sender=user, app_url=app_url, notification_setting_id=notification_setting, data=data,priority=priority)
        send_notification_fcm(notification_obj=notification_obj, android_channel_id=android_channel_id, icon=icon)
        return GenericCommentMutation(new_comment)

class GenericLikeMutation(graphene.Mutation):
    generic_like = graphene.Field(GenericLikeType)
    class Arguments:
        object_type=graphene.String()
        object_id=graphene.Int()


    @classmethod
    def mutate(cls, root, info, object_type, object_id):
        user = info.context.user
        content_type=ContentType.objects.get(app_label="moments", model=object_type)
        like=GenericLike.objects.filter(user=user, content_type=content_type, object_id=object_id)
        if like.exists():
            like=like[0]
            like.delete()
            return GenericLikeMutation(like)
        new_like=GenericLike(user=user, content_type=content_type, object_id=object_id)
        new_like.save()
        story=Story.objects.get(id=object_id)
        notification_to=story.user
        # TODO: set data payload, user avtar as icon
        notification_setting="STLIKE"
        data={
            "pk":story.id,
            "storyID": story.id,
            "likeID": new_like.id,
            "notification_type":notification_setting,
        }
        priority=None
        icon=None
        app_url=None
        android_channel_id=None

        notification_obj=Notification(user=notification_to, sender=user, app_url=app_url, notification_setting_id=notification_setting, data=data,priority=priority)
        send_notification_fcm(notification_obj=notification_obj, android_channel_id=android_channel_id, icon=icon)
        return GenericLikeMutation(new_like)


class Mutation(graphene.ObjectType):
    insert_moment=Momentmutation.Field()
    insert_story=Storymutation.Field()
    delete_moment=MomentDeleteMutation.Field()
    delete_story=Storydeletemutation.Field()
    update_moment=UpdateMomentMutation.Field()
    like_moment=Momentlikemutation.Field()
    comment_moment=Momentcommentmutation.Field()
    report_moment=Momentreportmutation.Field()
    report_story=Storyreportmutation.Field()
    like_comment=CommentLikeMutation.Field()
    generic_comment=GenericCommentMutation.Field()
    generic_like=GenericLikeMutation.Field()
    translate_moment=TranslateMomentMutation.Field()


class Query(graphene.ObjectType):

    # all_user_stories=DjangoFilterConnectionField(StoryType)
    # all_user_moments = DjangoFilterConnectionField(MomentsTyps)
    # all_user_comments = DjangoFilterConnectionField(CommentType)


    # def resolve_all_user_stories(root, info):
    #     return Story.objects.filter(created_date__gte=datetime.datetime.now()-datetime.timedelta(hours=EXPIRE_TIME)).order_by('-created_date','user')

    current_user_moments=graphene.List(MomentsTyps)
    all_moments=graphene.List(MomentsTyps)
    current_user_stories=graphene.List(StoryType)
    all_user_stories=DjangoFilterConnectionField(StoryType)
    all_user_multi_stories=graphene.List(MultiStoryType)
    all_comments = graphene.List(CommentType, moment_id=graphene.String(required=True))
    self_moment_likes = graphene.List(LikeType, moment_pk=graphene.Int(required=True))
    all_user_moments = DjangoFilterConnectionField(MomentsTyps)
    all_user_comments = DjangoFilterConnectionField(CommentType)

    def resolve_all_user_moments(self, info, **kwargs):
        user = info.context.user
        return Moment.objects.exclude(
                user__blockedUsers__username=user.username
            ).order_by("-created_date")

    def resolve_all_user_stories(self, info, **kwargs):
        user = info.context.user
        return Story.objects.exclude(
                user__blockedUsers__username=user.username
            ).order_by("-created_date")

    def resolve_all_user_multi_stories(self, info, **kwargs):
        return all_user_multi_stories_query(info)

    def resolve_all_comments(self,info, **kwargs):
        momentId=kwargs.get('moment_id')
        return Comment.objects.filter(momemt_id=momentId, reply_to=None).order_by('-created_date')

    def resolve_self_moment_likes(self,info, **kwargs):
        user = info.context.user
        momentPk=kwargs.get('moment_pk')
        # print('moment id = ',momentId)
        # print(Like.objects.filter(momemt__pk=momentId))
        return Like.objects.filter(momemt__pk=momentPk,momemt__user=user).order_by('-id')

    def resolve_all_moments(self, info):
        return Moment.objects.all().order_by('-created_date')

    # def resolve_all_user_stories(root, info):
    #     return Story.objects.filter(created_date__gte=datetime.datetime.now()-datetime.timedelta(hours=EXPIRE_TIME)).order_by('-created_date','user')

    def resolve_current_user_stories(root, info):

        user=info.context.user
        return Story.objects.filter(user=user, created_date__gte=datetime.datetime.now()-datetime.timedelta(seconds=EXPIRE_TIME)).order_by('-created_date')



    def resolve_current_user_moments(root,info):

        user = info.context.user
        return Moment.objects.filter(user=user).all().order_by("-created_date")


class Subscription(graphene.ObjectType):
    on_new_story = OnNewStory.Field()
    on_delete_story = OnDeleteStory.Field()
    on_new_moment = NotifyNewMoment.Field()
    on_update_moment = NotifyUpdateMoment.Field()
    on_delete_moment = NotifyDeleteMoment.Field()