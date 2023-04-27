from django.core.management.base import BaseCommand
from defaultPicker.models import *



class Command(BaseCommand):
    def handle(self, *args, **options):
        default_pickers = {
            "ages": ["18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33",
                     "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49",
                     "50", "51", "52", "53", "54", "55", "56", "57", "58", "59"],
            "ethnicity": ["American Indian", "Black/ African Descent", "East Asian", "Hispanic / Latino",
                          "Middle Eastern", "Pacific Islander", "South Asian", "White / Caucasian", "Other",
                          "Prefer Not to Say"],
            "ethnicity_fr": ["Amérindien", "Noir / Afro Descendant", "Asie de L'Est",
                             "Hispanique / latino", "Moyen-Orient", "Insulaire du Pacifique", "Sud-Asiatique",
                             "Blanc / Caucasien", "Autre", "Je préfère ne rien dire"],
            "family": ["Don’t want kids", "Want kids ", "Open to kids", "Have kids", "Prefer not to say"],
            "family_fr": ["Je ne veux pas d'enfants", "Je veux des enfants", "Ouvert aux enfants", "J'ai des enfants",
                          "Je préfère ne rien dire", ],
            "heights": ["140", "143", "146", "148", "151", "153", "156", "158", "161", "163", "166", "168", "171",
                        "173", "176", "179", "181", "184", "186", "189", "191", "194", "196", "199", "201", "204",
                        "207", "209", "212", "214", "217", "219", "222", "224", "227", "229", "232", "234", "237",
                        "240", "242", "245", "247"],
            "politics": ["Liberal", "Moderate", "Conservative", "Other", "Prefer Not to Say"],
            "politics_fr": ["Libéral", "Modéré", "Conservateur", "Autre", "Je préfère ne rien dire"],
            "religious": ["Agnostic", "Atheist", "Buddhist", "Catholic", "Christian", "Hindu", "Jewish", "Muslim",
                          "Spiritual", "Other", "Prefer Not to Say"],
            "religious_fr": ["Agnostique", "Athée", "Bouddhiste", "Catholique",
                             "Chrétien", "Hindou", "Juif", "Musulman", "Spirituel", "Autre", "Je préfère ne rien dire"],
            "genders" : ["Male", "Female"],
            "genders_fr" : ["Masculin", "féminin"],
            "searchGenders": ["Only Men", "Only Women", "Both"],
            "searchGenders_fr": ["Seuls les hommes", "Seules les femmes", "Les deux"],
            "tag": ["nature lover", "pet friendly", "sports fanatic", "haute culture", "video gamer", "gambler",
                    "otaku", "foodie", "early bird", "night owl", "musician", "nerd", "book worm", "architect",
                    "logician", "commander", "debater", "advocate", "mediator", "protagonist", "campaigner",
                    "responsible", "defender", "executive", "social butterfly", "virtuoso", "adventurer",
                    "entrepreneur", "entertainer", "mechanic", "nurturer", "artist", "idealist", "scientist",
                    "thinker", "caregiver", "visionary", "creative", "philosopher", "sensitive", "compassionate",
                    "ambitious", "traditional", "comedian", "leader", "traveler", "obnoxious", "arrogant", "impatient",
                    "sarcastic", "nihilist", "hustler", "gangster", "Vilain" ],

            "tag_fr": ["amoureux de la nature", "pet friendly", "fanatique de sport", "haute culture", "joueur vidéo", "joueur",
                    "otaku", "gourmand", "lève-tôt", "oiseau de nuit", "musicien", "nerd", "ver de livre", "architecte",
                    "logicien", "commandant", "débatteur", "avocat", "médiateur", "protagoniste", "militant","responsable", "défenseur", "exécutif", "papillon social", "virtuose", "aventurier",
                    "entrepreneur", "artiste", "mécanicien", "nourricier", "artiste", "idéaliste", "scientifique",
                    "penseur", "aidant", "visionnaire", "créatif", "philosophe", "sensible", "compassionné",
                    "ambitieux", "traditionnel", "humoriste", "leader", "voyageur", "odieux", "arrogant", "impatient",
                    "sarcastique", "nihiliste", "arnaqueur", "gangster", "Vilain"],
            "zodiacSigns": ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius",
                            "Capricorn", "Aquarius", "Pisces"],
            "zodiacSigns_fr": ["Bélier", "Taureau", "Gémeaux", "Cancer", "Lion",
                               "Vierge", "Balance", "Scorpion", "Sagittaire", "Capricorne", "Verseau", "Poissons"],
            "languages": [
                {"code": "en", "name": "English"},
                {"code": "fr", "name": "French"},
                {"code": "nl", "name": "Dutch"},
                {"code": "de", "name": "German"},
                {"code": "sw", "name": "Swahili"},
                {"code": "it", "name": "Italian"},
                {"code": "ar", "name": "Arabic"},
                {"code": "iw", "name": "Hebrew"},
                {"code": "ja", "name": "Japenese"},
                {"code": "ru", "name": "Russian"},
                {"code": "fa", "name": "Persian"},
                {"code": "es", "name": "Spanish"},
                {"code": "el", "name": "Greek"},
                {"code": "uk", "name": "Ukranian"},
                {"code": "ko", "name": "Korean"},
                {"code": "pl", "name": "Polish"},
                {"code": "vi", "name": "Vietnamese"},
                {"code": "no", "name": "Norwegian."},
                {"code": "sv", "name": "Swedish"},
                {"code": "hr", "name": "Croatian"},
                {"code": "cs", "name": "Czech"},
                {"code": "da", "name": "Danish"},
                {"code": "tl", "name": "Filipino"},
                {"code": "fi", "name": "Finnish"},
                {"code": "sl", "name": "Slovenian"},
                {"code": "sq", "name": "Albanian"},
                {"code": "am", "name": "Amharic"},
                {"code": "hy", "name": "Armenian"},
                {"code": "la", "name": "Latin"},
                {"code": "lv", "name": "Latvian"},
                {"code": "ln", "name": "Lingala"},
                {"code": "th", "name": "Thai"},
                {"code": "az", "name": "Azerbijani"},
                {"code": "eu", "name": "Basque"},
                {"code": "be", "name": "Belarusian"},
                {"code": "bn", "name": "Bengali"},
                {"code": "bs", "name": "Bosnian"},
                {"code": "bg", "name": "Bulgarian"},
                {"code": "km", "name": "Cambodian"},
                {"code": "ca", "name": "Catalan"},
                {"code": "et", "name": "Estonain"},
                {"code": "gl", "name": "Galician"},
                {"code": "ka", "name": "Georgian"},
                {"code": "zh-cn", "name": "Chinese(Simplified)"},
                {"code": "zh-tw", "name": "ChineseTraditional"},
                {"code": "pt-br", "name": "Portuges(Brazil)"},
                {"code": "pt-pt", "name": "Portugese(Portgal)"},
            ]
        }

        for ethnicity_, ethnicity_fr_ in zip(default_pickers['ethnicity'], default_pickers['ethnicity_fr']):
            e = ethnicity.objects.get_or_create(
                ethnicity=ethnicity_,
                ethnicity_fr=ethnicity_fr_,
                defaults={
                    "ethnicity": ethnicity_,
                    "ethnicity_fr": ethnicity_fr_
                }
            )[0]
            e.save()


        for searchGender_, searchGender_fr_ in zip(default_pickers['searchGenders'], default_pickers['searchGenders_fr']):
            s = searchGender.objects.get_or_create(
                searchGender=searchGender_,
                searchGender_fr=searchGender_fr_,
                defaults={
                    "searchGender": searchGender_,
                    "searchGender_fr": searchGender_fr_
                }
            )[0]
            s.save()

        for gender_, gender_fr_ in zip(default_pickers['genders'], default_pickers['genders_fr']):
            g = gender.objects.get_or_create(
                gender=gender_,
                gender_fr=gender_fr_,
                defaults={
                    "gender": gender_,
                    "gender_fr": gender_fr_
                }
            )[0]
            g.save()

        for age_ in default_pickers['ages']:
            age.objects.get_or_create(
                age = age_,
                defaults={
                    "age": age_
                }
            )


        for family_, family_fr_ in zip(default_pickers['family'], default_pickers['family_fr']):
            f = family.objects.get_or_create(
                familyPlans=family_,
                familyPlans_fr=family_fr_,
                defaults={
                    "familyPlans": family_,
                    "familyPlans_fr": family_fr_
                }
            )[0]
            f.save()

        for height_ in default_pickers['heights']:
            height.objects.get_or_create(
                height=height_,
                defaults={
                    "height": height_
                }
            )

        for politics_, politics_fr_ in zip(default_pickers['politics'], default_pickers['politics_fr']):
            p = politics.objects.get_or_create(
                politics=politics_,
                politics_fr=politics_fr_,
                defaults={
                    "politics": politics_,
                    "politics_fr": politics_fr_
                }
            )[0]
            p.save()


        for religious_, religious_fr_ in zip(default_pickers['religious'], default_pickers['religious_fr']):
            r = religious.objects.get_or_create(
                religious=religious_,
                religious_fr=religious_fr_,
                defaults={
                    "religious": religious_,
                    "religious_fr": religious_fr_
                }
            )[0]
            r.save()


        for tag_, tag_fr_ in zip(default_pickers['tag'], default_pickers['tag_fr']):
            t = tags.objects.get_or_create(
                tag=tag_,
                tag_fr=tag_fr_,
                defaults={
                    "tag": tag_,
                    "tag_fr": tag_fr_
                }
            )[0]
            t.save()



        for zodiacSign_, zodiacSign_fr_ in zip(default_pickers['zodiacSigns'], default_pickers['zodiacSigns_fr']):
            z = zodiacSign.objects.get_or_create(
                zodiacSign=zodiacSign_,
                zodiacSign_fr=zodiacSign_fr_,
                defaults={
                    "zodiacSign": zodiacSign_,
                    "zodiacSign_fr": zodiacSign_fr_
                }
            )[0]
            z.save()

        for language_ in default_pickers["languages"]:
            lang = Language.objects.get_or_create(
                language=language_['name'],
                language_code=language_['code'],
                defaults={"language": language_['name'], "language_code": language_['code']},
            )[0]
            lang.save()

    