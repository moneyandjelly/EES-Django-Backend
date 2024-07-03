from community.entity.models import Community
from community.repository.community_repository import CommunityRepository


class CommunityRepositoryImpl(CommunityRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def list(self):
        # models.py가 실질적으로 Django 설정과 연결되어 있음
        # 이 부분에 정의된 게시물 객체가 Community에 해당함
        # 즉 DB에서 Community를 표현하는 테이블을 읽어서 그 전체를 반환하는 작업
        return Community.objects.all().order_by('regDate')

    def create(self, communityData):
        # title, writer, content 내용을 토대로 Community 객체를 생성
        # 이 객체는 또한 models.py에 의해 구성된 객체로
        # save()를 수행하는 순간 DB에 기록됨
        community = Community(**communityData)
        community.save()
        return community

    def findByCommunityId(self, communityId):
        return Community.objects.get(communityId=communityId)

    def deleteByCommunityId(self, communityId):
        community = Community.objects.get(communityId=communityId)
        community.delete()

    def update(self, community, communityData):
        for key, value in communityData.items():
            print(f"key: {key}, value: {value}")
            # 쉽게 생각해보자면 community 라는 Entity가 가지고 있는 속성값 중
            # 현재 수정 요청에 의해 전달된 정보에 대응되는 key가 가지고 있는 value 값을 갱신시킴
            setattr(community, key, value)

        community.save()
        return community