import random


def random_name():
    first_str = [
        "轻盈的", "悠闲的", "热情的", "轻快的", "深邃的", "奔放的", "悠扬的", "惊喜的", "活泼的", "温柔的",
        "沉静的", "欢乐的", "疯狂的", "美丽的", "明亮的", "快乐的", "清新的", "迷人的", "舒适的", "幸福的",
        "灵动的", "高兴的", "安详的", "静谧的", "兴奋的", "淡雅的", "柔和的", "浪漫的", "绚丽的", "清亮的",
        "缤纷的", "璀璨的", "斑斓的", "和谐的", "优雅的", "舒服的", "慵懒的", "富饶的", "欣喜的", "繁荣的",
        "欣慰的", "平和的", "宁静的", "顺心的", "甜美的", "柔软的", "悠然的", "从容的", "祥和的", "清爽的",
        "亲切的", "温馨的", "光明的", "悦耳的", "动人的", "欢愉的", "优美的", "爽朗的", "如意的", "欣快的",
        "活跃的", "愉快的", "风趣的", "开朗的", "豁达的", "洒脱的", "顺利的", "顺畅的", "鲜活的", "兴致的",
        "轻松的", "愉悦的", "细腻的", "细心的", "动听的", "和蔼的", "优越的", "健康的", "靓丽的", "爽快的",
        "淡然的", "惬意的", "心旷神怡的", "舒心的", "平顺的", "清澈的", "迷人的", "质朴的", "清秀的", "畅快的",
        "闲适的", "通畅的", "安逸的", "婉约的", "文雅的", "轻松的", "宜人的", "怡然的", "悦心的", "清澈的",
        "如意的", "欢畅的", "热情的", "喜悦的", "美好的", "和睦的", "欣慰的", "欢娱的", "欢跃的", "笑容的",
        "笑脸的", "喜气的", "欢喜的", "笑意的", "喜庆的", "狂笑的", "宁静的", "安详的", "平和的", "温柔的",
        "清新的", "明亮的", "欢乐的", "快乐的", "幸福的", "舒适的", "优雅的", "浪漫的", "绚丽的", "璀璨的",
        "斑斓的", "和谐的", "柔和的", "淡雅的", "清亮的", "缤纷的", "灵动的", "高兴的", "兴奋的", "欣喜的",
        "繁荣的", "欣慰的", "顺心的", "甜美的", "柔软的", "悠然的", "从容的", "祥和的", "清爽的", "亲切的",
        "温馨的", "光明的", "悦耳的", "动人的", "欢愉的", "优美的", "爽朗的", "如意的", "欣快的", "活跃的",
        "愉快的", "风趣的", "开朗的", "豁达的", "洒脱的", "顺利的", "顺畅的", "鲜活的", "兴致的", "轻松的",
        "愉悦的", "细腻的", "细心的", "动听的", "和蔼的", "优越的", "健康的", "靓丽的", "爽快的", "淡然的",
        "惬意的", "心旷神怡的", "舒心的", "平顺的", "清澈的", "迷人的", "质朴的", "清秀的", "畅快的", "闲适的",
        "通畅的", "安逸的", "婉约的", "文雅的", "轻松的", "宜人的", "怡然的", "悦心的", "清澈的", "如意的",
        "欢畅的", "热情的", "喜悦的", "美好的", "和睦的", "欣慰的", "欢娱的", "欢跃的", "笑容的", "笑脸的",
        "喜气的", "欢喜的", "笑意的", "喜庆的", "狂笑的"
    ]

    second_str = [
        "吃", "喝", "玩", "看", "听", "闻", "嗅", "感受", "触摸", "思考",
        "品味", "尝试", "观察", "观看", "阅读", "倾听", "思念", "追忆", "憧憬", "沉浸",
        "想象", "体验", "享受", "感知", "感悟", "领悟", "领会", "理解", "接受",
        "接纳", "承受", "忍受", "承认", "认同", "被动", "遭遇", "遭受", "蛇将"
    ]

    last_str = [
        '玩水', '看日出', '听音乐', '闻花香', '花朵', '阳光', '美食', '欣赏', '思考',
        '海浪', '山川', '星空', '彩虹', '风景', '风雨', '月光', '星辰', '微笑', '温暖',
        '微风', '波浪', '森林', '枫叶', '雪景', '雨滴', '清泉', '晨曦', '晚霞', '静谧',
        '灯火', '烛光', '火焰', '心灵', '诗意', '情感', '回忆', '幻想', '奇迹', '希望',
        '忧伤', '安慰', '拥抱', '渴望', '陪伴', '幸福', '快乐', '梦想', '自由', '宁静',
        '温柔', '力量', '勇气', '智慧', '真理', '信念', '祝福', '友情', '爱情', '家庭', '写散文'
    ]

    return random.choice(first_str) + random.choice(second_str) + random.choice(last_str)
