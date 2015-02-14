# -*- coding: utf-8 -*-
from datetime import date
from CommonString import *


class Character(object):
    DB_TABLE = ['ID', 'FullName', 'Nickname', 'Profession', 'Rank', 'Active', 'ActiveCost', 'Passive1', 'Passive1Lv',
                'Passive2', 'Passive2Lv', 'Attachment', 'WeaponType', 'ExpGrown', 'AttendanceCost', 'MaxAtk', 'MaxHP',
                'AtkGrown', 'HPGrown', 'AtkSpeed', 'CriticalRate', 'Note', 'Belonged', 'AttachedCost']
    UPDATED_COLUMNS = DB_TABLE[1:len(DB_TABLE)]  # 除了 ID 外的所有欄位
    TABLE_VIEW_COLUMNS = ['ID', 'Nickname', 'Profession', 'Rank', 'Active', 'Act.Cost', 'Passive1', 'Passive2',
                          'Attachment', 'Weapon', 'MaxAtk', 'MaxHP', 'Note', 'Belonged']

    def __init__(self, infos):
        inputs = iter(infos)
        self.c_id = next(inputs)
        self.full_name = next(inputs)
        self.nickname = next(inputs)
        self.profession = next(inputs)
        self.rank = next(inputs)
        self.active = next(inputs)
        self.active_cost = next(inputs)
        self.passive_1 = next(inputs)
        self.passive_1_lv = next(inputs)
        self.passive_2 = next(inputs)
        self.passive_2_lv = next(inputs)
        self.attachment = next(inputs)
        self.weapon_type = next(inputs)
        self.exp_grown = next(inputs)
        self.attendance_cost = next(inputs)
        self.max_atk = next(inputs)
        self.max_hp = next(inputs)
        self.atk_grown = next(inputs)
        self.hp_grown = next(inputs)
        self.atk_speed = next(inputs)
        self.critical_rate = next(inputs)
        self.note = next(inputs)
        self.belonged = next(inputs)
        self.attached_cost = next(inputs)

    @staticmethod
    def create_by_cgdt_character(obj):
        if isinstance(obj, CGDTCharacter):
            return Character([obj.c_id, obj.full_name, obj.nickname, obj.profession, obj.rank, obj.active,
                              obj.active_cost, obj.passive_1, str(obj.passive_1_level), obj.passive_2,
                              str(obj.passive_2_level), obj.attachment, obj.weapon, obj.exp_grown, obj.cost,
                              obj.max_atk, obj.max_hp, obj.atk_grown, obj.hp_grown, obj.hit_rate,
                              obj.critical_rate, '', obj.belonged, obj.attached_cost])
        else:
            raise TypeError('Input object types {0}, not CGDTCharacter.'.format(type(obj)))

    @staticmethod
    def create_empty_character():
        return Character([''] * len(Character.DB_TABLE))

    @property
    def max_atk_after_break(self):
        return self.max_atk + self.atk_grown * 4

    @property
    def max_hp_after_break(self):
        return self.max_hp + self.hp_grown * 4

    def get_updated_info(self):
        return [self.full_name.encode('utf-8'), self.nickname.encode('utf-8'), self.profession.encode('utf-8'),
                self.rank, self.active.encode('utf-8'), self.active_cost, self.passive_1.encode('utf-8'),
                self.passive_1_lv.encode('utf-8'), self.passive_2.encode('utf-8'), self.passive_2_lv.encode('utf-8'),
                self.attachment.encode('utf-8'), self.weapon_type.encode('utf-8'), self.exp_grown.encode('utf-8'),
                self.attendance_cost, self.max_atk, self.max_hp, self.atk_grown, self.hp_grown, self.atk_speed,
                self.critical_rate, self.note.encode('utf-8'), self.belonged.encode('utf-8'), self.attached_cost]

    def get_table_view_info(self):
        return [self.c_id, self.nickname.encode('utf-8'), self.profession.encode('utf-8'), self.rank,
                self.active.encode('utf-8'), self.active_cost, self.passive_1.encode('utf-8'),
                self.passive_2.encode('utf-8'), self.attachment.encode('utf-8'), self.weapon_type.encode('utf-8'),
                self.max_atk, self.max_hp, self.note.encode('utf-8'), self.belonged.encode('utf-8')]

    def __getitem__(*args, **kwargs):
        return getattr(*args, **kwargs)

    def __str__(self):
        return 'Character: ID={0}, FullName={1}, Nickname={2}'.format(
            self.c_id, self.full_name.encode('utf-8'), self.nickname.encode('utf-8'))


class CGDTCharacter(object):
    # BulletSpeed 弓統基本15，法10
    # Tag [male][Log Horizon]等，應是對應網站中提供的標籤篩選功能
    # @Unknown1 總是15，懷疑是跑速，但寶石也一樣；@Unknown2 總是2；@Unknown3 總是0
    DB_TABLE = ['ID', 'Title', 'Name', 'Nickname', 'Rank', 'Cost', 'ProfessionID', 'Classification', 'Weapon',
                'GrownSpeed', 'InitAtk', 'InitHP', 'MaxAtk', 'MaxHP', 'MaxBrokenAtk', 'MaxBrokenHP', 'OwnedWay',
                'ActiveCost', 'Active', 'Passive1Level', 'Passive1', 'Passive2Level', 'Passive2', 'HitRate',
                '@Unknown1', 'BulletSpeed', 'CriticalRate', 'Artist', 'CharacterVoice', 'Tag', 'ActiveName',
                'Passive1Name', 'Passive2Name', 'ExpGrown', '@Unknown2', '@Unknown3',
                'Belonged', 'Attachment', 'AttachmentName', 'AttachedCost']

    # noinspection PyUnusedLocal
    def __init__(self, the_list):
        self.fields_number = -1  # 本身會自動被記入，故設 -1 以平衡

        properties = iter(the_list)
        self.c_id = int(next(properties))
        self.full_name = next(properties) + next(properties)
        self.nickname = next(properties)
        self.rank = int(next(properties))
        self.cost = int(next(properties))
        self.profession = PROFESSIONS[int(next(properties)) - 1]
        dropped = next(properties)  # Classification
        self.weapon = next(properties)
        dropped = next(properties)  # GrownSpeed
        dropped = next(properties)  # InitAtk
        dropped = next(properties)  # InitHP
        self.max_atk = int(next(properties))
        self.max_hp = int(next(properties))
        self.atk_grown = calculate_grown(self.max_atk, int(next(properties)))
        self.hp_grown = calculate_grown(self.max_hp, int(next(properties)))
        dropped = next(properties)  # OwnedWay
        self.active_cost = int(next(properties))
        self.active = next(properties)
        self.passive_1_level = int(next(properties))
        self.passive_1 = next(properties)
        self.passive_2_level = int(next(properties))
        self.passive_2 = next(properties)
        self.hit_rate = int(next(properties)) / 100.0
        dropped = next(properties)  # Unknown1
        dropped = next(properties)  # BulletSpeed
        self.critical_rate = int(next(properties)) / 100.0
        dropped = next(properties)  # Artist
        dropped = next(properties)  # CharacterVoice
        dropped = next(properties)  # Tag
        dropped = next(properties)  # ActiveName
        dropped = next(properties)  # Passive1Name
        dropped = next(properties)  # Passive2Name
        self.exp_grown = next(properties)
        dropped = next(properties)  # Unknown2
        dropped = next(properties)  # Unknown3
        self._init_belonged(next(properties))
        self.attachment = next(properties)
        dropped = next(properties)  # AttachmentName
        self.attached_cost = int(next(properties))

    # Make fields read-only
    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value
        self.__dict__['fields_number'] += 1

    # 除了將其命名轉成我的格式以外，也檢查不可有我預期外的名稱出現
    def _init_belonged(self, name):
        replaced_name = name.replace(u'海風之港', u'海風').replace(u'賢者之塔', u'賢塔'). \
            replace(u'迷宮山脈', u'山脈').replace(u'獸里', u'獸之里')

        if replaced_name in BELONGEDS:
            self.belonged = replaced_name
        else:
            raise ValueError('Invalid Belonged name {0} for {1}.'.format(
                name.encode('utf-8'), self.full_name.encode('utf-8')))

    def __str__(self):
        return 'CGDTCharacter: ID={0}, FullName={1}, Nickname={2}'.format(
            self.c_id, self.full_name.encode('utf-8'), self.nickname.encode('utf-8'))


def calculate_grown(origin_max, max_after_broken):
    return (max_after_broken - origin_max) / 4


class RecordOfDrawLots(object):
    DB_TABLE = ['Times', 'Event', 'Profession', 'Rank', 'Character', 'Cost']


class FriendInfo(object):
    DB_TABLE = ['ID', 'UsedNames', 'Excellence', 'Defect', 'Relation', 'Offline', 'UsedCharacters', 'CurrentRank',
                'RaisedIn3Weeks', 'RaisedIn2Months', 'AddedDate', 'LastProfession', 'LastCharacter']
    CLEANED_UP_COLUMNS = DB_TABLE[1:len(DB_TABLE)]  # 除了 ID 外的所有欄位
    SELECTED_COLUMNS = DB_TABLE[0:12]  # 除了 LastCharacter 外的所有欄位
    TABLE_VIEW_COLUMNS = ['ID', 'Names', 'Excellence', 'Defect', 'Relation', 'Offline', 'Characters', 'Rank',
                          'Ra.In3Weeks', 'Ra.In2Months', 'AddedDate', 'LastProfession']
    TABLE_VIEW_SORTABLE_COLUMNS = ['LastProfession', 'Rank', 'Ra.In3Weeks', 'Ra.In2Months', 'AddedDate']
    UPDATED_COLUMNS = DB_TABLE[1:6] + [DB_TABLE[10]]

    def __init__(self, infos):
        if infos is None:
            raise ValueError('Input infos is None.')

        properties = iter(infos)

        self.f_id = next(properties)
        self.used_names = next(properties)
        self.excellence = next(properties)
        self.defect = next(properties)
        self.relation = next(properties)
        self.offline = next(properties)
        self.used_characters = next(properties)
        self.current_rank = next(properties)
        self.raised_in_3_weeks = next(properties)
        self.raised_in_2_months = next(properties)
        self._added_date = next(properties)
        self.last_profession = next(properties)

    # 資料已存在時使用原資料，若為新好友則回傳當天日期
    @property
    def added_date(self):
        return self._added_date if self._added_date else date.today()

    @added_date.setter
    def added_date(self, value):
        self._added_date = value

    def get_table_view_info(self):
        return [self.f_id, self.used_names.encode('utf-8'), self.excellence.encode('utf-8'),
                self.defect.encode('utf-8'), self.relation.encode('utf-8'), self.offline,
                self.used_characters.encode('utf-8'), self.current_rank, self.raised_in_3_weeks,
                self.raised_in_2_months, self._added_date, self.last_profession.encode('utf-8')]

    def get_updated_info(self):
        if not self.used_names:
            raise ValueError('Used names is empty')
        return [self.used_names.encode('utf-8'), self.excellence.encode('utf-8'), self.defect.encode('utf-8'),
                self.relation.encode('utf-8'), self.offline, self.added_date]

    def __getitem__(*args, **kwargs):
        return getattr(*args, **kwargs)

    def __str__(self):
        return 'FriendInfo: ID={0}, UsedNames={1}'.format(self.f_id, self.used_names.encode('utf-8'))


class FriendRecord(object):
    DB_TABLE = ['FriendID', 'RecordedDate', 'Character', 'CharacterLevel', 'Rank']
    FRIEND_INFO_SELECTED_COLUMNS = ['ID', 'UsedNames', 'CurrentRank', 'LastProfession', 'LastCharacter']
    TABLE_VIEW_COLUMNS = ['ID', 'Names', 'Character', 'Char.Level', 'Rank', 'LastRank', 'LastProfession']

    def __init__(self, infos):
        self.f_id = infos[0]
        self.used_names = infos[1]
        self.character_nickname = None
        self.character_level = None
        self.rank = None
        self.last_rank = infos[2] if infos[2] else 0
        self.last_profession = infos[3]
        self.last_character = infos[4]

        self._status = UNRECORDED

    # 簡單檢查資料，若通過則更新記錄，並調整狀態為「已記錄」
    def record(self, nickname, level, rank):
        # 檢查 level/rank 是否大於 0
        if level < 1 or rank < 1:
            raise ValueError('Level/Rank < 1')
        # 檢查 rank 是否不小於前記錄
        if rank < self.last_rank:
            raise ValueError('Rank {0} too small, last rank is {1}'.format(rank, self.last_rank))

        self.character_nickname = nickname
        self.character_level = level
        self.rank = rank
        self._status = RECORDED

    @property
    def status(self):
        return self._status

    # 該 rank 之變化是否異常（成長過快 / 負成長）
    def is_unusual_rank(self, the_rank):
        return the_rank > self.last_rank + 3 or the_rank < self.last_rank

    # 角色名稱已指定時便套用，否則套用前角色名稱
    @property
    def current_character(self):
        return self.character_nickname if self.character_nickname is not None else \
            self.last_character if self.last_character is not None else ''

    # 角色等級未選擇時為空（方便直接填新值），已選擇便用已選擇
    @property
    def current_character_level(self):
        return self.character_level if self.character_level is not None else ''

    # Rank 等級未選擇時為空（方便直接填新值），已選擇便用已選擇
    @property
    def current_rank(self):
        return self.rank if self.rank is not None else ''

    def get_table_view_info(self):
        return [self.f_id, self.used_names.encode('utf-8'), self.current_character.encode('utf-8'),
                self.current_character_level, self.current_rank, self.last_rank, self.last_profession.encode('utf-8')]

    def get_inserted_info(self, the_date):
        if self._status != RECORDED:
            raise Exception('Haven\'t call \'record\' yet!')
        return self.f_id, the_date, self.character_nickname, self.character_level, self.rank

    def __getitem__(*args, **kwargs):
        return getattr(*args, **kwargs)

    def __str__(self):
        return 'FriendRecord: ID={0}, UsedNames={1}, Status={2}'.format(
            self.f_id, self.used_names.encode('utf-8'), self.status)


class CharacterPower(object):
    DB_TABLE = ['Account', 'CharacterID', 'Level', 'Atk', 'AtkRaisedRatio', 'HitRate', 'CriticalRatio',
                'CriticalFactor', 'ActiveFactor', 'ActiveCost', 'Addition']
    SELECTED_COLUMNS = DB_TABLE[1:len(DB_TABLE)]  # 除了 Account 外的所有欄位
    UPDATED_COLUMNS = ['CharacterID', 'Level', 'Atk', 'AtkRaisedRatio', 'HitRate', 'CriticalRatio',
                       'CriticalFactor', 'ActiveFactor', 'ActiveCost', 'Addition']
    TABLE_VIEW_FULL_COLUMNS = ['ID', 'Character', 'Lv', 'Atk', 'AtkRaised', 'HitRate', 'Cri.Ratio', 'Cri.Factor',
                               'DPS', 'Act.Factor', 'Act.Cost', 'DPM', 'Addition']
    TABLE_VIEW_SIMPLE_COLUMNS = ['ID', 'Character', 'Lv', 'Atk', 'AtkRaised', 'DPS',
                                 'Act.Factor', 'DPM', 'Addition']

    def __init__(self, record, character):
        properties = iter(record)
        self.level = next(properties)
        self.atk = next(properties)
        self.atk_raised = next(properties)
        self.hit_rate = next(properties)
        self.critical_ratio = next(properties)
        self.critical_factor = next(properties)
        self.active_factor = next(properties)
        self.active_cost = next(properties)
        self.addition = next(properties)
        self.character = character

        self._update_damages()

    @staticmethod
    def create_empty_character_power():
        return CharacterPower([''] * (len(CharacterPower.SELECTED_COLUMNS) - 1), None)

    def _update_damages(self):
        try:
            self.dps = '%.1f' % (self.atk * 0.1 * self.atk_raised / self.hit_rate * (
                1 + self.critical_ratio * (self.critical_factor - 1)))
        except StandardError:
            self.dps = 'Unknown'

        try:
            self.dpm = '%.1f' % (self.atk * 0.1 * self.atk_raised * self.active_factor / self.active_cost)
        except StandardError:
            self.dpm = 'Unknown'

    @property
    def c_id(self):
        return self.character.c_id

    @property
    def nickname(self):
        return self.character.nickname

    def get_updated_info(self):
        if self.character is None:
            raise ValueError('Character is empty!')
        return [self.c_id, self.level, self.atk, self.atk_raised, self.hit_rate, self.critical_ratio,
                self.critical_factor, self.active_factor, self.active_cost, self.addition.encode('utf-8')]

    def get_table_view_full_info(self):
        return [self.c_id, self.nickname.encode('utf-8'), self.level, self.atk, self.atk_raised, self.hit_rate,
                self.critical_ratio, self.critical_factor, self.dps, self.active_factor, self.active_cost,
                self.dpm, self.addition.encode('utf-8')]

    def get_table_view_simple_info(self):
        return [self.c_id, self.nickname.encode('utf-8'), self.level, self.atk, self.atk_raised, self.dps,
                self.active_factor, self.dpm, self.addition.encode('utf-8')]
