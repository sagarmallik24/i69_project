from django.db import models
import time
from django.contrib.auth import get_user_model

from push_notifications.models import APNSDevice, GCMDevice
from defaultPicker.utils import language_translate_everytime


User = get_user_model()

class Room(models.Model):
    name = models.CharField(max_length=128)
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="User1") #user 1
    target = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="User2") # user 2
    last_modified = models.DateTimeField(auto_now_add=False,blank=True,null=True)
    deleted = models.PositiveSmallIntegerField(default=0)
    # if None has deleted = 0
    # if user_id has deleted = 1
    # if target has deleted = 2
    # if delete gte 0 = deleet all message of the room;

    def __str__(self):
        return f'{self.name} ({self.user_id}: {self.target}) [{self.last_modified}]'


class Message(models.Model):
    MESSAGE_TYPES = (
        ("C", 'CONVERSATIONAL'),
        ("G", 'GIFT_MESSAGE'),
        ("P", 'PrivatePhotoRequest'),
        ("GL", 'GEO_LOCATION')
    )
    room_id = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="Sender") #user 1
    content = models.CharField(max_length=5120, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.DateTimeField(auto_now_add=False,blank=True,null=True)
    sender_worker=models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,related_name="sender_worker")
    receiver_worker=models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,related_name="receiver_worker")
    message_type = models.CharField(
        choices=MESSAGE_TYPES,
        default="C",
        max_length=10
    )
    gift_message_sender = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    private_photo_request_id = models.IntegerField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return f'{self.user_id.username}: {self.content} [{self.timestamp}]'

    def delete(self):
        DeletedMessage.objects.create(
            room_id=self.room_id,
            user_id=self.user_id,
            timestamp=self.timestamp,
            content=self.content
        )
        super(Message, self).delete()


class DeletedMessage(models.Model):
    room_id = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='DeletedSender')
    timestamp = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=5120, blank=True)
    deleted_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-deleted_timestamp',)


class Notes(models.Model):
    room_id = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    content = models.CharField(max_length=5000, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    forRealUser = models.BooleanField(default=False)

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return f'{self.room_id}: {self.content} [{self.timestamp}]'


class Broadcast(models.Model):
    by_user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="Create_By") #user 1
    content = models.CharField(max_length=512, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    deleted = models.PositiveSmallIntegerField(default=0)

    content_fr = models.CharField(max_length=512, blank=True)
    content_zh_cn = models.CharField(max_length=265, null=True, blank=True)
    content_nl = models.CharField(max_length=265, null=True, blank=True)
    content_de = models.CharField(max_length=265, null=True, blank=True)
    content_sw = models.CharField(max_length=265, null=True, blank=True)
    content_it = models.CharField(max_length=265, null=True, blank=True)
    content_ar = models.CharField(max_length=265, null=True, blank=True)  
    content_iw = models.CharField(max_length=265, null=True, blank=True)
    content_ja = models.CharField(max_length=265, null=True, blank=True)
    content_ru = models.CharField(max_length=265, null=True, blank=True)
    content_fa = models.CharField(max_length=265, null=True, blank=True)
    content_pt_br = models.CharField(max_length=265, null=True, blank=True)
    content_pt_pt = models.CharField(max_length=265, null=True, blank=True)
    content_es = models.CharField(max_length=265, null=True, blank=True)
    content_es_419 = models.CharField(max_length=265, null=True, blank=True) # manually translate due to unavailability in google
    content_el = models.CharField(max_length=265, null=True, blank=True)
    content_zh_tw = models.CharField(max_length=265, null=True, blank=True)
    content_uk = models.CharField(max_length=265, null=True, blank=True)
    content_ko = models.CharField(max_length=265, null=True, blank=True)
    content_br = models.CharField(max_length=265, null=True, blank=True) # manually translate due to unavailability in google
    content_pl = models.CharField(max_length=265, null=True, blank=True)
    content_vi = models.CharField(max_length=265, null=True, blank=True)
    content_nn = models.CharField(max_length=265, null=True, blank=True) # manually translate due to unavailability in google
    content_no = models.CharField(max_length=265, null=True, blank=True)
    content_sv = models.CharField(max_length=265, null=True, blank=True)
    content_hr = models.CharField(max_length=265, null=True, blank=True)
    content_cs = models.CharField(max_length=265, null=True, blank=True)
    content_da = models.CharField(max_length=265, null=True, blank=True)
    content_tl = models.CharField(max_length=265, null=True, blank=True)
    content_fi = models.CharField(max_length=265, null=True, blank=True)
    content_sl = models.CharField(max_length=265, null=True, blank=True)
    content_sq = models.CharField(max_length=265, null=True, blank=True)
    content_am = models.CharField(max_length=265, null=True, blank=True)
    content_hy = models.CharField(max_length=265, null=True, blank=True)
    content_la = models.CharField(max_length=265, null=True, blank=True)
    content_lv = models.CharField(max_length=265, null=True, blank=True)
    content_th = models.CharField(max_length=265, null=True, blank=True)
    content_az = models.CharField(max_length=265, null=True, blank=True)
    content_eu = models.CharField(max_length=265, null=True, blank=True)
    content_be = models.CharField(max_length=265, null=True, blank=True)
    content_bn = models.CharField(max_length=265, null=True, blank=True)
    content_bs = models.CharField(max_length=265, null=True, blank=True)
    content_bg = models.CharField(max_length=265, null=True, blank=True)
    content_km = models.CharField(max_length=265, null=True, blank=True)
    content_ca = models.CharField(max_length=265, null=True, blank=True)
    content_et = models.CharField(max_length=265, null=True, blank=True)
    content_gl = models.CharField(max_length=265, null=True, blank=True)
    content_ka = models.CharField(max_length=265, null=True, blank=True)
    content_hi = models.CharField(max_length=265, null=True, blank=True)
    content_hu = models.CharField(max_length=265, null=True, blank=True)
    content_is = models.CharField(max_length=265, null=True, blank=True)
    content_id = models.CharField(max_length=265, null=True, blank=True)
    content_ga = models.CharField(max_length=265, null=True, blank=True)
    content_mk = models.CharField(max_length=265, null=True, blank=True)
    content_mn = models.CharField(max_length=265, null=True, blank=True)
    content_ne = models.CharField(max_length=265, null=True, blank=True)
    content_ro = models.CharField(max_length=265, null=True, blank=True)
    content_sr = models.CharField(max_length=265, null=True, blank=True)
    content_sk = models.CharField(max_length=265, null=True, blank=True)
    content_ta = models.CharField(max_length=265, null=True, blank=True)
    content_tg = models.CharField(max_length=265, null=True, blank=True)
    content_tr = models.CharField(max_length=265, null=True, blank=True)
    content_ur = models.CharField(max_length=265, null=True, blank=True)
    content_uz = models.CharField(max_length=265, null=True, blank=True)

    def __str__(self):
        #return f'{self.by_user_id.username}: {self.content} [{self.timestamp}]'
        return f'{self.content}'
    
    def save(self, *args, **kwargs):
        self.content_fr = language_translate_everytime(self.content_fr, self.content, "fr")
        self.content_zh_cn = language_translate_everytime(self.content_zh_cn, self.content, "zh-cn")
        self.content_nl = language_translate_everytime(self.content_nl, self.content, "nl")
        self.content_de = language_translate_everytime(self.content_de, self.content, "de")
        self.content_sw = language_translate_everytime(self.content_sw, self.content, "sw")
        self.content_it = language_translate_everytime(self.content_it, self.content, "it")
        self.content_ar = language_translate_everytime(self.content_ar, self.content, "ar")
        self.content_iw = language_translate_everytime(self.content_iw, self.content, "iw")
        self.content_ja = language_translate_everytime(self.content_ja, self.content, "ja")
        self.content_ru = language_translate_everytime(self.content_ru, self.content, "ru")
        self.content_fa = language_translate_everytime(self.content_fa, self.content, "fa")
        self.content_pt_br = language_translate_everytime(self.content_pt_br, self.content, "pt_br")
        self.content_pt_pt = language_translate_everytime(self.content_pt_pt, self.content, "pt_pt")
        self.content_es = language_translate_everytime(self.content_es, self.content, "es")
        self.content_el = language_translate_everytime(self.content_el, self.content, "el")
        self.content_zh_tw = language_translate_everytime(self.content_zh_tw, self.content, "zh-tw")
        self.content_uk = language_translate_everytime(self.content_uk, self.content, "uk")
        self.content_ko = language_translate_everytime(self.content_ko, self.content, "ko")
        self.content_pl = language_translate_everytime(self.content_pl, self.content, "pl")
        self.content_vi = language_translate_everytime(self.content_vi, self.content, "vi")
        self.content_no = language_translate_everytime(self.content_no, self.content, "no")
        self.content_sv = language_translate_everytime(self.content_sv, self.content, "sv")
        self.content_hr = language_translate_everytime(self.content_hr, self.content, "hr")
        self.content_cs = language_translate_everytime(self.content_cs, self.content, "cs")
        self.content_da = language_translate_everytime(self.content_da, self.content, "da")
        self.content_tl = language_translate_everytime(self.content_tl, self.content, "tl")
        self.content_fi = language_translate_everytime(self.content_fi, self.content, "fi")
        self.content_sl = language_translate_everytime(self.content_sl, self.content, "sl")
        self.content_sq = language_translate_everytime(self.content_sq, self.content, "sq")
        self.content_am = language_translate_everytime(self.content_am, self.content, "am")
        self.content_hy = language_translate_everytime(self.content_hy, self.content, "hy")
        self.content_la = language_translate_everytime(self.content_la, self.content, "la")
        self.content_lv = language_translate_everytime(self.content_lv, self.content, "lv")
        self.content_th = language_translate_everytime(self.content_th, self.content, "th")
        self.content_az = language_translate_everytime(self.content_az, self.content, "az")
        self.content_eu = language_translate_everytime(self.content_eu, self.content, "eu")
        self.content_be = language_translate_everytime(self.content_be, self.content, "be")
        self.content_bn = language_translate_everytime(self.content_bn, self.content, "bn")
        self.content_bs = language_translate_everytime(self.content_bs, self.content, "bs")
        self.content_bg = language_translate_everytime(self.content_bg, self.content, "bg")
        self.content_km = language_translate_everytime(self.content_km, self.content, "km")
        self.content_ca = language_translate_everytime(self.content_ca, self.content, "ca")
        self.content_et = language_translate_everytime(self.content_et, self.content, "et")
        self.content_gl = language_translate_everytime(self.content_gl, self.content, "gl")
        self.content_ka = language_translate_everytime(self.content_ka, self.content, "ka")
        self.content_hi = language_translate_everytime(self.content_hi, self.content, "hi")
        self.content_hu = language_translate_everytime(self.content_hu, self.content, "hu")
        self.content_is = language_translate_everytime(self.content_is, self.content, "is")
        self.content_id = language_translate_everytime(self.content_id, self.content, "id")
        self.content_ga = language_translate_everytime(self.content_ga, self.content, "ga")
        self.content_mk = language_translate_everytime(self.content_mk, self.content, "mk")
        self.content_mn = language_translate_everytime(self.content_mn, self.content, "mn")
        self.content_ne = language_translate_everytime(self.content_ne, self.content, "ne")
        self.content_ro = language_translate_everytime(self.content_ro, self.content, "ro")
        self.content_sr = language_translate_everytime(self.content_sr, self.content, "sr")
        self.content_sk = language_translate_everytime(self.content_sk, self.content, "sk")
        self.content_ta = language_translate_everytime(self.content_ta, self.content, "ta")
        self.content_tg = language_translate_everytime(self.content_tg, self.content, "tg")
        self.content_tr = language_translate_everytime(self.content_tr, self.content, "tr")
        self.content_ur = language_translate_everytime(self.content_ur, self.content, "ur")
        self.content_uz = language_translate_everytime(self.content_uz, self.content, "uz")

        return super().save(*args, **kwargs)

class FirstMessage(models.Model):
    by_user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="FMCreate_By") #user 1
    content = models.CharField(max_length=512, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    content_fr = models.CharField(max_length=512, blank=True)
    content_zh_cn = models.CharField(max_length=265, null=True, blank=True)
    content_nl = models.CharField(max_length=265, null=True, blank=True)
    content_de = models.CharField(max_length=265, null=True, blank=True)
    content_sw = models.CharField(max_length=265, null=True, blank=True)
    content_it = models.CharField(max_length=265, null=True, blank=True)
    content_ar = models.CharField(max_length=265, null=True, blank=True)  
    content_iw = models.CharField(max_length=265, null=True, blank=True)
    content_ja = models.CharField(max_length=265, null=True, blank=True)
    content_ru = models.CharField(max_length=265, null=True, blank=True)
    content_fa = models.CharField(max_length=265, null=True, blank=True)
    content_pt_br = models.CharField(max_length=265, null=True, blank=True)
    content_pt_pt = models.CharField(max_length=265, null=True, blank=True)
    content_es = models.CharField(max_length=265, null=True, blank=True)
    content_es_419 = models.CharField(max_length=265, null=True, blank=True) # manually translate due to unavailability in google
    content_el = models.CharField(max_length=265, null=True, blank=True)
    content_zh_tw = models.CharField(max_length=265, null=True, blank=True)
    content_uk = models.CharField(max_length=265, null=True, blank=True)
    content_ko = models.CharField(max_length=265, null=True, blank=True)
    content_br = models.CharField(max_length=265, null=True, blank=True) # manually translate due to unavailability in google
    content_pl = models.CharField(max_length=265, null=True, blank=True)
    content_vi = models.CharField(max_length=265, null=True, blank=True)
    content_nn = models.CharField(max_length=265, null=True, blank=True) # manually translate due to unavailability in google
    content_no = models.CharField(max_length=265, null=True, blank=True)
    content_sv = models.CharField(max_length=265, null=True, blank=True)
    content_hr = models.CharField(max_length=265, null=True, blank=True)
    content_cs = models.CharField(max_length=265, null=True, blank=True)
    content_da = models.CharField(max_length=265, null=True, blank=True)
    content_tl = models.CharField(max_length=265, null=True, blank=True)
    content_fi = models.CharField(max_length=265, null=True, blank=True)
    content_sl = models.CharField(max_length=265, null=True, blank=True)
    content_sq = models.CharField(max_length=265, null=True, blank=True)
    content_am = models.CharField(max_length=265, null=True, blank=True)
    content_hy = models.CharField(max_length=265, null=True, blank=True)
    content_la = models.CharField(max_length=265, null=True, blank=True)
    content_lv = models.CharField(max_length=265, null=True, blank=True)
    content_th = models.CharField(max_length=265, null=True, blank=True)
    content_az = models.CharField(max_length=265, null=True, blank=True)
    content_eu = models.CharField(max_length=265, null=True, blank=True)
    content_be = models.CharField(max_length=265, null=True, blank=True)
    content_bn = models.CharField(max_length=265, null=True, blank=True)
    content_bs = models.CharField(max_length=265, null=True, blank=True)
    content_bg = models.CharField(max_length=265, null=True, blank=True)
    content_km = models.CharField(max_length=265, null=True, blank=True)
    content_ca = models.CharField(max_length=265, null=True, blank=True)
    content_et = models.CharField(max_length=265, null=True, blank=True)
    content_gl = models.CharField(max_length=265, null=True, blank=True)
    content_ka = models.CharField(max_length=265, null=True, blank=True)
    content_hi = models.CharField(max_length=265, null=True, blank=True)
    content_hu = models.CharField(max_length=265, null=True, blank=True)
    content_is = models.CharField(max_length=265, null=True, blank=True)
    content_id = models.CharField(max_length=265, null=True, blank=True)
    content_ga = models.CharField(max_length=265, null=True, blank=True)
    content_mk = models.CharField(max_length=265, null=True, blank=True)
    content_mn = models.CharField(max_length=265, null=True, blank=True)
    content_ne = models.CharField(max_length=265, null=True, blank=True)
    content_ro = models.CharField(max_length=265, null=True, blank=True)
    content_sr = models.CharField(max_length=265, null=True, blank=True)
    content_sk = models.CharField(max_length=265, null=True, blank=True)
    content_ta = models.CharField(max_length=265, null=True, blank=True)
    content_tg = models.CharField(max_length=265, null=True, blank=True)
    content_tr = models.CharField(max_length=265, null=True, blank=True)
    content_ur = models.CharField(max_length=265, null=True, blank=True)
    content_uz = models.CharField(max_length=265, null=True, blank=True)

    def __str__(self):
        #return f'{self.by_user_id.username}: {self.content} [{self.timestamp}]'
        return f'{self.content}'
    
    def save(self, *args, **kwargs):
        self.content_fr = language_translate_everytime(self.content_fr, self.content, "fr")
        self.content_zh_cn = language_translate_everytime(self.content_zh_cn, self.content, "zh-cn")
        self.content_nl = language_translate_everytime(self.content_nl, self.content, "nl")
        self.content_de = language_translate_everytime(self.content_de, self.content, "de")
        self.content_sw = language_translate_everytime(self.content_sw, self.content, "sw")
        self.content_it = language_translate_everytime(self.content_it, self.content, "it")
        self.content_ar = language_translate_everytime(self.content_ar, self.content, "ar")
        self.content_iw = language_translate_everytime(self.content_iw, self.content, "iw")
        self.content_ja = language_translate_everytime(self.content_ja, self.content, "ja")
        self.content_ru = language_translate_everytime(self.content_ru, self.content, "ru")
        self.content_fa = language_translate_everytime(self.content_fa, self.content, "fa")
        self.content_pt_br = language_translate_everytime(self.content_pt_br, self.content, "pt_br")
        self.content_pt_pt = language_translate_everytime(self.content_pt_pt, self.content, "pt_pt")
        self.content_es = language_translate_everytime(self.content_es, self.content, "es")
        self.content_el = language_translate_everytime(self.content_el, self.content, "el")
        self.content_zh_tw = language_translate_everytime(self.content_zh_tw, self.content, "zh-tw")
        self.content_uk = language_translate_everytime(self.content_uk, self.content, "uk")
        self.content_ko = language_translate_everytime(self.content_ko, self.content, "ko")
        self.content_pl = language_translate_everytime(self.content_pl, self.content, "pl")
        self.content_vi = language_translate_everytime(self.content_vi, self.content, "vi")
        self.content_no = language_translate_everytime(self.content_no, self.content, "no")
        self.content_sv = language_translate_everytime(self.content_sv, self.content, "sv")
        self.content_hr = language_translate_everytime(self.content_hr, self.content, "hr")
        self.content_cs = language_translate_everytime(self.content_cs, self.content, "cs")
        self.content_da = language_translate_everytime(self.content_da, self.content, "da")
        self.content_tl = language_translate_everytime(self.content_tl, self.content, "tl")
        self.content_fi = language_translate_everytime(self.content_fi, self.content, "fi")
        self.content_sl = language_translate_everytime(self.content_sl, self.content, "sl")
        self.content_sq = language_translate_everytime(self.content_sq, self.content, "sq")
        self.content_am = language_translate_everytime(self.content_am, self.content, "am")
        self.content_hy = language_translate_everytime(self.content_hy, self.content, "hy")
        self.content_la = language_translate_everytime(self.content_la, self.content, "la")
        self.content_lv = language_translate_everytime(self.content_lv, self.content, "lv")
        self.content_th = language_translate_everytime(self.content_th, self.content, "th")
        self.content_az = language_translate_everytime(self.content_az, self.content, "az")
        self.content_eu = language_translate_everytime(self.content_eu, self.content, "eu")
        self.content_be = language_translate_everytime(self.content_be, self.content, "be")
        self.content_bn = language_translate_everytime(self.content_bn, self.content, "bn")
        self.content_bs = language_translate_everytime(self.content_bs, self.content, "bs")
        self.content_bg = language_translate_everytime(self.content_bg, self.content, "bg")
        self.content_km = language_translate_everytime(self.content_km, self.content, "km")
        self.content_ca = language_translate_everytime(self.content_ca, self.content, "ca")
        self.content_et = language_translate_everytime(self.content_et, self.content, "et")
        self.content_gl = language_translate_everytime(self.content_gl, self.content, "gl")
        self.content_ka = language_translate_everytime(self.content_ka, self.content, "ka")
        self.content_hi = language_translate_everytime(self.content_hi, self.content, "hi")
        self.content_hu = language_translate_everytime(self.content_hu, self.content, "hu")
        self.content_is = language_translate_everytime(self.content_is, self.content, "is")
        self.content_id = language_translate_everytime(self.content_id, self.content, "id")
        self.content_ga = language_translate_everytime(self.content_ga, self.content, "ga")
        self.content_mk = language_translate_everytime(self.content_mk, self.content, "mk")
        self.content_mn = language_translate_everytime(self.content_mn, self.content, "mn")
        self.content_ne = language_translate_everytime(self.content_ne, self.content, "ne")
        self.content_ro = language_translate_everytime(self.content_ro, self.content, "ro")
        self.content_sr = language_translate_everytime(self.content_sr, self.content, "sr")
        self.content_sk = language_translate_everytime(self.content_sk, self.content, "sk")
        self.content_ta = language_translate_everytime(self.content_ta, self.content, "ta")
        self.content_tg = language_translate_everytime(self.content_tg, self.content, "tg")
        self.content_tr = language_translate_everytime(self.content_tr, self.content, "tr")
        self.content_ur = language_translate_everytime(self.content_ur, self.content, "ur")
        self.content_uz = language_translate_everytime(self.content_uz, self.content, "uz")

        return super().save(*args, **kwargs)


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.gif', '.webp', '.xlsx', '.xls', '.csv', '.txt', '.mp3', '.mp4', '.avi', '.mpg', '.mk4', '.wav', '.zip', '.rar']
    invalid_extensions = ['.exe', '.apk', '.htaccess', '.msi', '.env', '.gitignore']
    if ext.lower() in invalid_extensions:
        raise ValidationError('Unsupported file extension.')

def upload_location(instance, filename):
    filebase, extension = filename.rsplit('.', 1)
    return f'chat_files/{filebase}_{time.time()}.{extension}'

class ChatMessageImages(models.Model):
    upload_type=models.CharField(max_length=100,null=True)
    image = models.FileField(upload_to=upload_location, validators=[validate_file_extension])

class NotificationSettings(models.Model):
    id = models.CharField(max_length=25, primary_key=True)
    title = models.CharField(max_length=50)
    title_fr = models.CharField(max_length=50)
    message_str = models.CharField(max_length=70, null=True)
    message_str_fr = models.CharField(max_length=70, null=True)

    def __str__(self):
        return self.id

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.IntegerField(null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    app_url = models.CharField(max_length=100, null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="notification_sender")
    seen = models.BooleanField(default=False)
    notification_setting = models.ForeignKey(NotificationSettings, on_delete=models.SET_NULL, null=True)
    notification_body = models.CharField(max_length=1000, null=True)
    notification_body_fr = models.CharField(max_length=1000, null=True)
    data = models.CharField(max_length=50000, null=True)


    def create_body(self):
        print('self here...', self.notification_setting)
        try:
            obj_ = NotificationSettings.objects.get(id=self.notification_setting)
            return f"{self.sender.fullName} {obj_.message_str}" if self.sender else obj_.message_str

        except NotificationSettings.DoesNotExist:
            raise Exception("Notification ID not exists.")

    def create_body_fr(self):
        print('self here...', self.notification_setting)
        try:
            obj_ = NotificationSettings.objects.get(id=self.notification_setting)
            return f"{self.sender.fullName} {obj_.message_str_fr}" if self.sender else obj_.message_str_fr

        except NotificationSettings.DoesNotExist:
            raise Exception("Notification ID not exists.")

    def set_seen(self):
        self.seen = True
        self.save()

    def user_has_read_permission(self, user):
        return self.user == user

def send_notification_fcm(notification_obj, android_channel_id=None, icon=None, image=None, **kwargs):
    user = notification_obj.user
    # print("In send Notification FCM")
    print(f"In send Notification FCM to {user}")
    body = notification_obj.create_body()
    body_fr = notification_obj.create_body_fr()
    print("Notification body created.")
    title = notification_obj.notification_setting.title
    title_fr = notification_obj.notification_setting.title_fr
    print(f"send Notification FCM: {title}")
    print(f"send Notification FCM: {title_fr}")
    data = notification_obj.data
    print(f"send Notification FCM: {data}")
    if notification_obj.notification_setting.id == "ADMIN":
        changed_coins = int(kwargs['coins'])

        if changed_coins < 0:
            if changed_coins == -1:
                body = f"{notification_obj.sender.fullName} has deducted your {abs(changed_coins)} coin and now total coins are {kwargs['current_coins']}."
                body_fr = f"{notification_obj.sender.fullName} has deducted your {abs(changed_coins)} coin and now total coins are {kwargs['current_coins']}."
            else:
                body = f"{notification_obj.sender.fullName} has deducted your {abs(changed_coins)} coins and now total coins are {kwargs['current_coins']}."
                body_fr = f"{notification_obj.sender.fullName} has deducted your {abs(changed_coins)} coins and now total coins are {kwargs['current_coins']}."
        else:
            if changed_coins == 1:
                body = f"{notification_obj.sender.fullName} has offered you {changed_coins} coin."
                body_fr = f"{notification_obj.sender.fullName} has offered you {changed_coins} coin."
            else:
                body = f"{notification_obj.sender.fullName} has offered you {changed_coins} coins."
                body_fr = f"{notification_obj.sender.fullName} has offered you {changed_coins} coins."

    if notification_obj.notification_setting.id == 'STREVIEW':
        status = kwargs['status']
        body = f"Admin {status} your story."
        body_fr = f"Admin {status} your story."

    if notification_obj.notification_setting.id == 'MMREVIEW':
        status = kwargs['status']
        body = f"Admin {status} your moment."
        body_fr = f"Admin {status} your moment."

    if notification_obj.notification_setting.id == 'USERPICREVIEW':
        status = kwargs['status']
        body = f"Admin {status} your picutre."
        body_fr = f"Admin {status} your picutre."

    if notification_obj.notification_setting.id == 'USERPICDETECT':
        body = kwargs['message']
        body_fr = kwargs['message']

    print("send Notification FCM: Calling GCM")
    print(f"send Notification FCM body: {body}")
    print(f"send Notification FCM body: {body_fr}")

    fcm_devices = GCMDevice.objects.filter(user=user).distinct("registration_id")
    print(f"FCM Devices: {fcm_devices}")
    print(f"FCM Devices body: {body}")
    if kwargs.get('message_count'):
        body = kwargs['message_count']
        body_fr = kwargs['message_count']
        print(f"FCM Devices body Message count: {body}")
    data['title_fr']=title_fr
    data['body_fr']=body_fr
    # resp = fcm_devices.send_message(message={"title": title, "body": body}, badge=1, extra={"title": title, "icon": icon, "data":data,"image":image})
    resp = fcm_devices.send_message(body, badge=1, sound="default", extra={"title": title,"icon": icon,"data": data, "image": image})
    print(f"send Notification FCM: {resp}")
    notification_obj.notification_body = body
    notification_obj.notification_body_fr = body_fr
    notification_obj.save()


class DeletedMessageDate(models.Model):
    no_of_days = models.IntegerField(default=0)

    def __str__(self):
        return f"Deleted Messages will delete after {self.no_of_days} Days."
