import datetime

from SmartDjango import models, E
from smartify import P

from Image.models import Image, ImageUploadAction


@E.register(id_processor=E.idp_cls_prefix())
class MilestoneError:
    CREATE = E("新建里程碑失败")
    NOT_BELONG = E("不是这个星球的里程碑")
    NOT_FOUND = E("里程碑不存在")


class Milestone(models.Model):
    """里程碑"""

    space = models.ForeignKey(
        'Space.Space',
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        verbose_name='里程碑信息',
        max_length=20,
        min_length=2,
    )

    start_date = models.DateField()

    cover = models.ForeignKey(
        'Image.Image',
        on_delete=models.SET_NULL,
        null=True,
        default=None,
    )

    def space_checker(self, space):
        if self.space != space:
            raise MilestoneError.NOT_BELONG

    @classmethod
    def get(cls, mid):
        try:
            return cls.objects.get(pk=mid)
        except cls.DoesNotExist:
            raise MilestoneError.NOT_FOUND

    @classmethod
    def create(cls, space, name, start_date):
        try:
            return cls.objects.create(space=space, name=name, start_date=start_date)
        except Exception:
            raise MilestoneError.CREATE

    def update(self, name, start_date):
        self.name = name
        self.start_date = start_date
        self.save()

    def delete(self, *args, **kwargs):
        if self.cover:
            self.cover.delete()
        super(Milestone, self).delete(*args, **kwargs)

    def get_duration(self):
        start_date = self.start_date  # type: datetime.date
        crt_date = datetime.date.today()
        return (crt_date - start_date).days

    def _readable_duration(self):
        return self.get_duration()

    def _readable_start_date(self):
        start_date = self.start_date  # type: datetime.date
        return start_date.strftime('%Y-%m-%d')
        # return dict(
        #     year=start_date.year,
        #     month=start_date.month,
        #     day=start_date.day
        # )

    def _readable_cover(self):
        if self.cover:
            return self.cover.d_milestone()

    def d(self):
        return self.dictify('pk->mid', 'name', 'start_date', 'duration', 'cover')

    def d_create(self):
        return dict(
            mid=self.pk,
            cover_token=self.get_image_token(),
        )

    def get_image_token(self):
        return Image.get_token(
            action=ImageUploadAction.MILESTONE,
            mid=self.pk
        )

    def set_cover(self, image: Image):
        if self.cover:
            self.cover.delete()
        self.cover = image
        self.save()


class MilestoneP:
    name, start_date = Milestone.P('name', 'start_date')
    start_date.process(lambda s: datetime.datetime.strptime(s, '%Y-%m-%d').date(), begin=True)

    id_getter = P('mid', yield_name='milestone').process(Milestone.get)
