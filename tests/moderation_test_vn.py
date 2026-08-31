
_dict = {
    "text1": "Đcmm",
    "text2": "vl bạn ơi",
    "text3": "bưởi của bạn nhìn ngon thí",
    "text4": "hai quả bưởi của bạn nhìn ngon vl",
    "text5": "cho mình uống sữa của bạn điiii",
    "text6": "đm, thằng có 4 hộp sữa, thằng không hộp nào",
    "text7": "ib t share video đang hot cho",
    "text8": "Tí giờ giải lao vào nhà vệ sinh, làm tí trong nớ",
    "text9": "Người có 4 hộp sữa, người có nhiều hơn, còn người không hộp nào",
    "text10": "Bạn giỏi thế sao không làm giáo sư luôn đi cho rồi?:))"
}

from app.services.moderation.core.moderation import moderation
from time import sleep

for value in _dict.values():
    print(moderation.get_response(value))
    for i in range(20):
        print(i)
        sleep(1)
