import datetime
import os
import re
import cv2
import mimetypes
import opennsfw2 as n2
import numpy as np
from moments.models import ReviewStory, ReviewMoment, Story
from user.models import ReviewUserPhoto, BlockedImageAlternatives, UserLimit
from chat.models import Notification, send_notification_fcm

def detect_face(tempfile_name):
    face_cascade = cv2.CascadeClassifier('frontface-detection.xml')
    face = face_cascade.detectMultiScale(
        cv2.cvtColor(
            cv2.imread(tempfile_name), 
            cv2.COLOR_BGR2GRAY
        ),
        1.2,
        4
    )
    return True if not len(face) else False

def detect_video(path):
    result = False
    video = cv2.VideoCapture(path)
    success, image = video.read()
    count = 0
    while success:
        cv2.imwrite(f"frame{count}.jpg", image)
        prediction_score = n2.predict_image(f"frame{count}.jpg")
        if prediction_score > 0.5:
            result = True
            os.remove(f'frame{count}.jpg')
            break
        else:
            for i in range(int(video.get(5)*15)):
                success, image = video.read()
            os.remove(f'frame{count}.jpg')
            count +=1
    return result, prediction_score

def detect_story(obj, file):
    filetype = mimetypes.guess_type(str(obj.file.url))[0].split('/')[0]
    result = False
    # save temp file
    tempfile_name = f'/tmp/{file.name}'
    with open(tempfile_name, 'wb') as tempfile:
        tempfile.write(obj.file.read())
    print(filetype)
    if filetype == 'video':
        file_type = 'video'
        result, prediction_score = detect_video(tempfile_name)
    else:
        file_type = 'image'
        prediction_score = n2.predict_image(tempfile_name)
        result = prediction_score > 0.5

    if result:
        ReviewStory.objects.create(
                user=obj.user,
                file_type=file_type,
                file=obj.file,
                thumbnail=obj.thumbnail,
                prediction_score=prediction_score
        )
        obj.delete()
    # delete temp file
    os.remove(tempfile_name)
    return result

def detect_moment(obj, file):
    filetype = mimetypes.guess_type(str(obj.file.url))[0].split('/')[0]
    result = False
    # save temp file
    tempfile_name = f'/tmp/{file.name}'
    with open(tempfile_name, 'wb') as tempfile:
        tempfile.write(obj.file.read())

    if filetype == 'video':
        file_type = 'video'
        result, prediction_score = detect_video(tempfile_name)
    else:
        file_type = 'image'
        prediction_score = n2.predict_image(tempfile_name)
        result = prediction_score > 0.5

    if result:
        ReviewMoment.objects.create(
            user=obj.user,
            file_type=file_type,
            file=obj.file,
            title=obj.Title,
            moment_description=obj.moment_description,
            prediction_score=prediction_score
        )
        obj.delete()
        # delete temp file
        os.remove(tempfile_name)
        return result

def detect_user_image(obj):
    print('DETECT USER IMAGE')
    if not obj.is_admin_approved:
        filetype = "image"
        result = False
        tempfile_name = f"/tmp/{obj.file.name.split('/')[-1]}"
        with open(tempfile_name, 'wb') as tempfile:
            tempfile.write(obj.file.read()) # save tempfile
        result1 = n2.predict_image(tempfile_name) > 0.5
        result2 = detect_face(tempfile_name)
        
        if result1 or result2: # predict
            if result1:
                message = "Naked Photos Are Not Allowed."
            elif result2:
                message = "Upload Image with your face."
            ReviewUserPhoto.objects.create(
                user_photo=obj,
                file=obj.file
            )
            if obj.user.gender == 0:
                obj.file = BlockedImageAlternatives.objects.filter(
                    action="MALE"
                ).last().image
            elif obj.user.gender == 1:
                obj.file = BlockedImageAlternatives.objects.filter(
                    action="FEMALE"
                ).last().image
            else:
                obj.file = BlockedImageAlternatives.objects.filter(
                    action="PREFER_NOT_TO_SAY"
                ).last().image
            obj.save() # save obj with different image.
            notification_obj=Notification(
                user=obj.user, 
                notification_setting_id="USERPICDETECT", 
                data={}
            )
            send_notification_fcm(
                notification_obj=notification_obj,
                message=message
            )
        os.remove(tempfile_name)


def all_user_multi_stories_query(info):
    user = info.context.user
    story_together_limit = UserLimit.objects.get(action_name="MultiStoryLimit").limit_value
    results = []
    # find all todays stories
    all_stories = Story.objects.filter(
        created_date__gte=datetime.datetime.now()-datetime.timedelta(hours=24)
    ).exclude(user__blockedUsers__username=user.username).order_by('-created_date')

    # fetch distinct users
    users_id = set(all_stories.values_list('user__id', flat=True))
    print(users_id)
    # creating story batch
    for user_id in users_id:
        s = all_stories.filter(user__id=user_id)
        batch_number = s.count() / story_together_limit
        batch_number = batch_number if batch_number.is_integer() else batch_number + 1

        # First Batch
        prepare_first_batch_stories = s.count() % story_together_limit
        print(prepare_first_batch_stories)
        if prepare_first_batch_stories:
            print("FIRST BATCH")
            story_batch = list(s[:prepare_first_batch_stories])
            results.append(
                {
                    "user": s[0].user,
                    "stories": Story.objects.filter(id__in=[i.id for i in story_batch]),
                    "latest_time": s[0].id,
                    "batch_number": batch_number
                }
            )
            s = s.exclude(id__in=[i.id for i in story_batch])
            batch_number -= 1
        # Remaining Batch
        for i in range(0, s.count(), story_together_limit):
            story_batch = list(s[i: i+story_together_limit])
            results.append(
                {
                    "user": s[0].user,
                    "stories": Story.objects.filter(id__in=[i.id for i in story_batch]),
                    "latest_time": s[0].id,
                    "batch_number": batch_number
                }
            )
            batch_number -= 1
    # sorting
    return sorted(results, key=lambda x:x['latest_time'], reverse=True)


def modify_text(text):
    # Detect phone numbers and replace it with ****
    print(text)
    try:
        phone_numbers = []
        # phone_numbers += re.findall(r"[\d]{3}-[\d]{3}-[\d]{3}", text)
        # phone_numbers += re.findall(r"[\d]{3} [\d]{3} [\d]{3}", text)
        # phone_numbers += re.findall(r"\+?[\d]{3}-[\d]{3}-[\d]{3}", text)
        # phone_numbers += re.findall(r"\+?\b[\d]{3}-[\d]{3}-[\d]{3}\b", text)
        # phone_numbers += re.findall(r"\d\d\d\d\d\d\d\d\d\d", text)
        # phone_numbers += re.findall(r"\d \d \d \d \d \d \d \d \d \d", text)

        # for phone_number in set(phone_numbers):
        #     text = text.replace(phone_number, "*"*len(phone_number))

        total_numbers = re.findall("[0-9]", text)
        if len(total_numbers) > 9:
            for i in total_numbers:
                text = text.replace(i, "*")
        print(text)
    except Exception as e:
        print(e)
    return text
