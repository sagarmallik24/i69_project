from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import Moment,Comment,Like,Report,Story, GenericLike, \
    GenericComment, StoryVisibleTime, StoryReport, ReviewStory, ReviewMoment
from chat.models import Notification, send_notification_fcm
from django.utils.safestring import mark_safe
from django import forms
from django_object_actions import DjangoObjectActions
from django.shortcuts import HttpResponseRedirect
# Register your models here.


@admin.register(Moment)
class MomentAdmin(admin.ModelAdmin):
    list_display=['user', 'Title','created_date','view_thumbnail']
    ordering = ('Title',)
    order_by = ['user', 'Title','created_date']
    search_fields = ('Title',"user__username", "user__fullName", "user__email")
    class Media:
        js = ("admin/js/admin_paginator.js",)
        
    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop('list_per_page', [25])[0])
        self.list_per_page = page_param
        return super(MomentAdmin, self).changelist_view(request, extra_context)
    def view_thumbnail(self, obj):
        output = []
        if obj.file:
            image_url = obj.file.url
            output.append(
                u'<a href="javascript:;" class="mtooltip left">'
                u'<img src="%s" alt="" style="max-width: 30px; max-height: 30px;" />'
                u'<span><img src="%s" style="max-width: 300px; max-height: 300px;"/></span>'
                u'</a>'
                % ( image_url, image_url)
            )

            style_css = """
            <style>
            a.mtooltip { outline: none; cursor: help; text-decoration: none; position: relative;}
            a.mtooltip span {margin-left: -999em; padding:5px 6px; position: absolute; width:auto; white-space:nowrap; line-height:1.5;box-shadow:0px 0px 10px #999; -moz-box-shadow:0px 0px 10px #999; -webkit-box-shadow:0px 0px 10px #999; border-radius:3px 3px 3px 3px; -moz-border-radius:3px; -webkit-border-radius:3px;}
            a.mtooltip span img {max-width:300px;}
            a.mtooltip {background:#ffffff; text-decoration:none;cursor: help;} /*BG color is a must for IE6*/
            a.mtooltip:hover span{ right: 1em;top: 0em; margin-left: 0; z-index:99999; position:absolute; background:#ffffff; border:1px solid #cccccc; color:#6c6c6c;}

            #changelist-form .results{overflow-x: initial!important;}
            </style>
            """
            output.append( style_css )

        return mark_safe(u''.join(output))

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display=['user','created_date', 'view_thumbnail']
    ordering = ('user',)
    order_by = ['user', 'created_date']
    search_fields = ["user__username", "user__fullName", "user__email"]
    class Media:
        js = ("admin/js/admin_paginator.js",)
        
    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop('list_per_page', [25])[0])
        self.list_per_page = page_param
        return super(StoryAdmin, self).changelist_view(request, extra_context)
    
    def view_thumbnail(self, obj):
        output = []
        if obj.file:
            video_url = obj.file.url
            if obj.thumbnail and obj.thumbnail.url:
                image_url = obj.thumbnail.url
                output.append(
                    u'<a href="javascript:;" class="mtooltip left">'
                    u'<img src="%s" alt="" style="max-width: 30px; max-height: 30px;" />'
                    u'<span><video width="320" height="240" controls>'
                    u'<source src="%s">Your browser does not support the video tag.</video>'
                    u'</span>'
                    u'</a>'
                    % ( image_url, video_url)
                )

            else:
                image_url = obj.file.url
                output.append(
                    u'<a href="javascript:;" class="mtooltip left">'
                    u'<img src="%s" alt="" style="max-width: 30px; max-height: 30px;" />'
                    u'<span><img src="%s" style="max-width: 300px; max-height: 300px;"/></span>'
                    u'</a>'
                    % ( image_url, image_url)
                )

            style_css = """
            <style>
            a.mtooltip { outline: none; cursor: help; text-decoration: none; position: relative;}
            a.mtooltip span {margin-left: -999em; padding:5px 6px; position: absolute; width:auto; white-space:nowrap; line-height:1.5;box-shadow:0px 0px 10px #999; -moz-box-shadow:0px 0px 10px #999; -webkit-box-shadow:0px 0px 10px #999; border-radius:3px 3px 3px 3px; -moz-border-radius:3px; -webkit-border-radius:3px;}
            a.mtooltip span img {max-width:300px;}
            a.mtooltip {background:#ffffff; text-decoration:none;cursor: help;} /*BG color is a must for IE6*/
            a.mtooltip:hover span{ left: 1em;top: 0em; margin-left: 0; z-index:99999; position:absolute; background:#ffffff; border:1px solid #cccccc; color:#6c6c6c;}

            #changelist-form .results{overflow-x: initial!important;}
            </style>
            """
            output.append( style_css )

        return mark_safe(u''.join(output))


class ReviewStoryAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display=['user','created_date', "file_type"]
    readonly_fields = ['view_thumbnail', ]
    search_fields = ["user__username", "user__fullName", "user__email"]
    class Media:
        js = ("admin/js/admin_paginator.js",)
        
    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop('list_per_page', [25])[0])
        self.list_per_page = page_param
        return super(ReviewStoryAdmin, self).changelist_view(request, extra_context)
    def view_thumbnail(self, obj):
        output = []
        if obj.file:
            file_url = obj.file.url
            if obj.file_type == "image":
                output.append(
                    u'<a href="javascript:;" class="mtooltip left">'
                    u'<img src="%s" alt="" style="max-width: 300px; max-height: 300px;" />'
                    u'<span><img src="%s" style="max-width: 300px; max-height: 300px;"/></span>'
                    u'</a>'
                    % ( file_url, file_url)
                )
            else:
                output.append(
                    u'<a href="javascript:;" class="mtooltip left">'
                    u'<video width="600" height="600" controls>'
                    u'<source src="%s" type="video/%s">'
                    u'</video>'
                    u'</a>'
                    % (file_url, file_url.split('/')[-1].split('.')[-1])
                )

            style_css = """
            <style>
            a.mtooltip { outline: none; cursor: help; text-decoration: none; position: relative;}
            a.mtooltip span {margin-left: -999em; padding:5px 6px; position: absolute; width:auto; white-space:nowrap; line-height:1.5;box-shadow:0px 0px 10px #999; -moz-box-shadow:0px 0px 10px #999; -webkit-box-shadow:0px 0px 10px #999; border-radius:3px 3px 3px 3px; -moz-border-radius:3px; -webkit-border-radius:3px;}
            a.mtooltip span img {max-width:300px;}
            a.mtooltip {background:#ffffff; text-decoration:none;cursor: help;} /*BG color is a must for IE6*/
            a.mtooltip:hover span{ left: 1em;top: 0em; margin-left: 0; z-index:99999; position:absolute; background:#ffffff; border:1px solid #cccccc; color:#6c6c6c;}

            #changelist-form .results{overflow-x: initial!important;}
            </style>
            """
            output.append( style_css )
        return mark_safe(u''.join(output))

    def approve_story(self, request, obj):
        Story.objects.create(
            user=obj.user,
            file=obj.file,
            thumbnail=obj.thumbnail
        ) # create story again
        notification_obj=Notification(
            user=obj.user, 
            notification_setting_id="STREVIEW", 
            data={},
        ) # create notification
        send_notification_fcm(
            notification_obj=notification_obj,
            status='approved'
        ) # send push notification
        obj.delete() # delete review object
        return HttpResponseRedirect(
            "/admin/moments/reviewstory/"
        )
    def reject_story(self, request, obj):
        notification_obj=Notification(
            user=obj.user, 
            notification_setting_id="STREVIEW", 
            data={},
        ) # create notification
        send_notification_fcm(
            notification_obj=notification_obj,
            status='rejected'
        ) # send push notification
        obj.delete() # delete review object
        return HttpResponseRedirect(
            "/admin/moments/reviewstory/"
        )

    change_actions = ('approve_story', 'reject_story')


class ReviewMomentAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display=['user','created_date', "file_type", 'title']
    readonly_fields = ['view_thumbnail', ]
    search_fields = ["title", "user__username", "user__fullName", "user__email"]


    class Media:
        js = ("admin/js/admin_paginator.js",)
        
    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop('list_per_page', [25])[0])
        self.list_per_page = page_param
        return super(ReviewMomentAdmin, self).changelist_view(request, extra_context)
    def view_thumbnail(self, obj):
        output = []
        if obj.file:
            file_url = obj.file.url
            if obj.file_type == "image":
                output.append(
                    u'<a href="javascript:;" class="mtooltip left">'
                    u'<img src="%s" alt="" style="max-width: 300px; max-height: 300px;" />'
                    u'<span><img src="%s" style="max-width: 300px; max-height: 300px;"/></span>'
                    u'</a>'
                    % ( file_url, file_url)
                )
            else:
                output.append(
                    u'<a href="javascript:;" class="mtooltip left">'
                    u'<video width="600" height="600" controls>'
                    u'<source src="%s" type="video/%s">'
                    u'</video>'
                    u'</a>'
                    % (file_url, file_url.split('/')[-1].split('.')[-1])
                )

            style_css = """
            <style>
            a.mtooltip { outline: none; cursor: help; text-decoration: none; position: relative;}
            a.mtooltip span {margin-left: -999em; padding:5px 6px; position: absolute; width:auto; white-space:nowrap; line-height:1.5;box-shadow:0px 0px 10px #999; -moz-box-shadow:0px 0px 10px #999; -webkit-box-shadow:0px 0px 10px #999; border-radius:3px 3px 3px 3px; -moz-border-radius:3px; -webkit-border-radius:3px;}
            a.mtooltip span img {max-width:300px;}
            a.mtooltip {background:#ffffff; text-decoration:none;cursor: help;} /*BG color is a must for IE6*/
            a.mtooltip:hover span{ left: 1em;top: 0em; margin-left: 0; z-index:99999; position:absolute; background:#ffffff; border:1px solid #cccccc; color:#6c6c6c;}

            #changelist-form .results{overflow-x: initial!important;}
            </style>
            """
            output.append( style_css )
        return mark_safe(u''.join(output))

    def approve_moment(self, request, obj):
        Moment.objects.create(
            user=obj.user,
            file=obj.file,
            Title=obj.title,
            moment_description=obj.moment_description
        ) # create story again
        notification_obj=Notification(
            user=obj.user, 
            notification_setting_id="MMREVIEW", 
            data={},
        ) # create notification
        send_notification_fcm(
            notification_obj=notification_obj,
            status='approved'
        ) # send push notification
        obj.delete() # delete review object
        return HttpResponseRedirect(
            "/admin/moments/reviewmoment/"
        )

    def reject_moment(self, request, obj):
        notification_obj=Notification(
            user=obj.user, 
            notification_setting_id="MMREVIEW", 
            data={},
        ) # create notification
        send_notification_fcm(
            notification_obj=notification_obj,
            status='rejected'
        ) # send push notification
        obj.delete() # delete review object
        return HttpResponseRedirect(
            "/admin/moments/reviewmoment/"
        )

    change_actions = ('approve_moment', 'reject_moment')

class ReviewCommentAdmin(ModelAdmin):
    class Media:
        js = ("admin/js/admin_paginator.js",)
        
    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop('list_per_page', [25])[0])
        self.list_per_page = page_param
        return super(ReviewCommentAdmin, self).changelist_view(request, extra_context)
    
class ReviewLikeAdmin(ModelAdmin):
    class Media:
        js = ("admin/js/admin_paginator.js",)
        
    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop('list_per_page', [25])[0])
        self.list_per_page = page_param
        return super(ReviewLikeAdmin, self).changelist_view(request, extra_context)
    
class ReviewGenericLikeAdmin(ModelAdmin):
    class Media:
        js = ("admin/js/admin_paginator.js",)
        
    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop('list_per_page', [25])[0])
        self.list_per_page = page_param
        return super(ReviewGenericLikeAdmin, self).changelist_view(request, extra_context)
    

#admin.site.register(Moment)
#admin.site.register(Story)
admin.site.register(Comment, ReviewCommentAdmin)
admin.site.register(Like,ReviewLikeAdmin)
admin.site.register(Report)
admin.site.register(StoryReport)
admin.site.register(GenericLike, ReviewGenericLikeAdmin)
admin.site.register(GenericComment)
admin.site.register(ReviewStory, ReviewStoryAdmin)
admin.site.register(ReviewMoment, ReviewMomentAdmin)

class StoryVisibleAdminForm(forms.ModelForm):
    class Meta:
        model = StoryVisibleTime
        fields = ('weeks', 'days', 'hours',)




@admin.register(StoryVisibleTime)
class StoryVisibleAdmin(ModelAdmin):
    list_display = [
        "text",
        "weeks",
        "days",
        "hours"
    ]


    form = StoryVisibleAdminForm
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
