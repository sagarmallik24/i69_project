from django.contrib import admin

# Register your models here.
from .models import (
    Room, 
    Message, 
    DeletedMessage, 
    Notes, 
    Broadcast, 
    FirstMessage, 
    ChatMessageImages, 
    NotificationSettings, 
    Notification, 
    DeletedMessageDate
)

class CustomRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user_from", "user_to")
    ordering = ('name',)
    list_filter = ("name",)
    search_fields = ["name", "user_id__username", "user_id__fullName", "user_id__email", "target_id__username",
                     "target_id__fullName", "target_id__email"]

    def user_from(self, obj):
        return obj.user_id

    def user_to(self, obj):
        return obj.target
    
    class Media:
        js = ("admin/js/admin_paginator.js",)
        
    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop('list_per_page', [25])[0])
        self.list_per_page = page_param
        return super(CustomRoomAdmin, self).changelist_view(request, extra_context)

class CustomMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "room_id", "user_id", "content", "read")
    ordering = ('-timestamp',)
    list_filter = ("room_id",)
    search_fields = (
        'content',
        'room_id__user_id__fullName', 
        'room_id__target__fullName'
    )

    def room_id(self, obj):
        return Room.objects.get(obj.room_id).name

    class Media:
        js = ("admin/js/admin_paginator.js",)
        
    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop('list_per_page', [25])[0])
        self.list_per_page = page_param
        return super(CustomMessageAdmin, self).changelist_view(request, extra_context)
            
class CustomBroadcastAdmin(admin.ModelAdmin):
    list_display = ("id", "by_user_id", "content", "timestamp")
    ordering = ('-timestamp',)
    search_fields = ('id','by_user_id__fullName','by_user_id__username')
    order_by = ('-timestamp',)
    
    class Media:
        js = ("admin/js/admin_paginator.js",)
        
    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop('list_per_page', [25])[0])
        self.list_per_page = page_param
        return super(CustomBroadcastAdmin, self).changelist_view(request, extra_context)

class CustomFirstMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "by_user_id", "content", "timestamp")
    ordering = ('-timestamp',)
    search_fields = ('by_user_id',)
    order_by = ('-timestamp',)
    
    class Media:
        js = ("admin/js/admin_paginator.js",)
        
    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop('list_per_page', [25])[0])
        self.list_per_page = page_param
        return super(CustomFirstMessageAdmin, self).changelist_view(request, extra_context)

class NotificationsAdmin(admin.ModelAdmin):
    list_display = ("id", "user","created_date", "sender", "seen", "notification_setting", "notification_body", "data" )
    ordering = ('-created_date',)
    search_fields = ('user__username', 'user__email', 'notification_setting__id')
    order_by = ('-created_date',)
    list_filter = ("notification_setting__id", "seen", )
    
    class Media:
        js = ("admin/js/admin_paginator.js",)
    
    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop('list_per_page', [25])[0])
        self.list_per_page = page_param
        return super(NotificationsAdmin, self).changelist_view(request, extra_context)

class MessageInline(admin.TabularInline):
    model = Message
    fields = ['content', 'user_id', 'read']
    readonly_fields = ['content', 'user_id', 'read']
    can_delete = False
    show_change_link = False
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    class Media:
        js = ("admin/js/admin_paginator.js",)
        
    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop('list_per_page', [25])[0])
        self.list_per_page = page_param
        return super(MessageInline, self).changelist_view(request, extra_context)
    
class ChatAdmin(admin.ModelAdmin):
    inlines = [
        MessageInline,
    ]
    list_display = ['name', 'user_id', 'target']
    readonly_fields = ['target', 'user_id', 'name', 'last_modified', 'deleted']
    search_fields = ('name', 'user_id__username','user_id__email','user_id__fullName','target__username','target__email','target__fullName' )
    
    def has_add_permission(self, request) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False
    
    class Media:
        js = ("admin/js/admin_paginator.js",)
        
    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop('list_per_page', [25])[0])
        self.list_per_page = page_param
        return super(ChatAdmin, self).changelist_view(request, extra_context)

class CustomDeletedMessages(admin.ModelAdmin):
    list_display = ('id', 'room_id', 'user_id', 'timestamp', 'deleted_timestamp')
    search_fields = ('room_id__name', 'user_id__username','user_id__email','user_id__fullName', )
    list_per_page = 25

    class Media:
        js = ("admin/js/admin_paginator.js",)
        
    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop('list_per_page', [25])[0])
        self.list_per_page = page_param
        return super(CustomDeletedMessages, self).changelist_view(request, extra_context)
    
class CustomNotificationSettings(admin.ModelAdmin):
    list_display = ['id', 'title', 'message_str', 'title_fr']
    search_fields = ('id', 'title', 'message_str', 'title_fr' )
    
    class Media:
        js = ("admin/js/admin_paginator.js",)
        
    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop('list_per_page', [25])[0])
        self.list_per_page = page_param
        return super(CustomNotificationSettings, self).changelist_view(request, extra_context)
    
class CustomChatMessageImages(admin.ModelAdmin):
    
    class Media:
        js = ("admin/js/admin_paginator.js",)
        
    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop('list_per_page', [25])[0])
        self.list_per_page = page_param
        return super(CustomChatMessageImages, self).changelist_view(request, extra_context)
    
class CustomNotes(admin.ModelAdmin):
    
    class Media:
        js = ("admin/js/admin_paginator.js",)
        
    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop('list_per_page', [25])[0])
        self.list_per_page = page_param
        return super(CustomNotes, self).changelist_view(request, extra_context)
    
class Chats(Room):
    class Meta:
        proxy = True
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'


admin.site.register(Chats, ChatAdmin)
admin.site.register(Message, CustomMessageAdmin)
admin.site.register(Room, CustomRoomAdmin)
admin.site.register(Broadcast, CustomBroadcastAdmin)
admin.site.register(FirstMessage, CustomFirstMessageAdmin)
admin.site.register(ChatMessageImages,CustomChatMessageImages)
admin.site.register(NotificationSettings,CustomNotificationSettings)
admin.site.register(Notification, NotificationsAdmin)
admin.site.register(DeletedMessage, CustomDeletedMessages)
admin.site.register(DeletedMessageDate)
admin.site.register(Notes, CustomNotes)
