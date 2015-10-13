from django.db import models
from my_auth.models import Harambee
from django.db.models import Count

ACTIVE = 0
PASSED = 1
COMPLETE = 2

STATE_CHOICES = (
    (ACTIVE, "Active"),
    (PASSED, "Passed"),
    (COMPLETE, "Complete"),
)


class Journey(models.Model):

    name = models.CharField("Name", max_length=500, null=True, blank=False, unique=True)
    intro_text = models.TextField("Introductory Text", blank=True)

    slug = models.TextField("Slug", blank=True)
    show_menu = models.BooleanField("Show in menus", default=True)
    search = models.CharField("Search description", max_length=500, null=True)
    image = models.ImageField("Image", upload_to="img/", blank=True, null=True)

    start_date = models.DateTimeField("Go Live On", null=False, blank=False)
    end_date = models.DateTimeField("Expire On", null=False, blank=False)


class Module(models.Model):

    # Accessible To
    ALL = 1
    LPS_1_4 = 2
    LPS_5 = 3

    # Percentages
    PERCENT_0 = 0
    PERCENT_25 = 25
    PERCENT_50 = 50
    PERCENT_75 = 75
    PERCENT_80 = 80
    PERCENT_90 = 90
    PERCENT_100 = 100

    PERCENTAGE_CHOICES = (
        (PERCENT_0, "0%"),
        (PERCENT_25, "25%"),
        (PERCENT_50, "50%"),
        (PERCENT_75, "75%"),
        (PERCENT_80, "80%"),
        (PERCENT_90, "90%"),
        (PERCENT_100, "100%")
    )

    name = models.CharField("Name", max_length=500, null=True, blank=False, unique=True)
    intro_text = models.TextField("Introductory Text", blank=True)
    end_text = models.TextField("Complete Page Text", blank=True)

    journeys = models.ManyToManyField(Journey)
    accessibleTo = models.PositiveIntegerField(
        "Accessible To", choices=(
            (ALL, "All"),
            (LPS_1_4, "Learning Potential Score 1 - 4"),
            (LPS_5, "Learning Potential Score 5+")
        ),
        default=ALL)
    show_recomended = models.BooleanField("Feature in Recommended for You", default=True)
    slug = models.TextField("Slug", blank=True)
    title = models.CharField("Page Title", max_length=500, null=True)
    show_menu = models.BooleanField("Show in menus", default=True)
    search = models.CharField("Search description", max_length=500, null=True)

    minimum_questions = models.PositiveIntegerField("Minimum questions answered")
    minimum_percentage = models.PositiveIntegerField(
        "Minimum % gained for all questions answered", choices=PERCENTAGE_CHOICES)
    store_data_per_user = models.BooleanField("Data stored against User I.D.", default=True)
    start_date = models.DateTimeField("Go Live On", null=False, blank=False)
    end_date = models.DateTimeField("Expire On", null=False, blank=False)
    publish_date = models.DateTimeField("Published On", null=False, blank=False)

    def total_levels(self):
        return self.level_set.all().aggregate(Count('id'))['id__count']


class Level(models.Model):

    name = models.CharField("Name", max_length=500, null=True, blank=False, unique=True)
    text = models.TextField("Introductory Text", blank=True)
    module = models.ForeignKey(Module, null=True, blank=False)
    image = models.ImageField("Image", upload_to="img/", blank=True, null=True)


class LevelQuestion(models.Model):

    name = models.CharField("Name", max_length=500, null=True, blank=False, unique=True)
    description = models.CharField("Description", max_length=500, blank=True)
    order = models.PositiveIntegerField("Order", default=0)
    level = models.ForeignKey(Level, null=True, blank=False)
    question_content = models.TextField("Question", blank=True)
    answer_content = models.TextField("Fully Worked Solution", blank=True)
    notes = models.TextField("Additional Notes", blank=True)
    image = models.ImageField("Image", upload_to="img/", blank=True, null=True)

    class Meta:
        verbose_name = "Level Question"
        verbose_name_plural = "Level Questions"
        ordering = ['order']


class LevelQuestionOption(models.Model):

    name = models.CharField("Name", max_length=500, null=True, blank=False, unique=True)
    question = models.ForeignKey(LevelQuestion, null=True, blank=False)
    order = models.PositiveIntegerField("Order", default=0)
    content = models.TextField("Content", blank=True)
    correct = models.BooleanField("Correct")

    class Meta:
        verbose_name = "Question Option"
        verbose_name_plural = "Question Options"


class HarambeeModuleRel(models.Model):

    harambee = models.ForeignKey(Harambee, null=False, blank=False)
    module = models.ForeignKey(Module, null=False, blank=False)


class HarambeeLevelRel(models.Model):

    harambee = models.ForeignKey(Harambee, null=False, blank=False)
    level = models.ForeignKey(Level, null=False, blank=False)
    state = models.PositiveIntegerField(choices=STATE_CHOICES, default=ACTIVE)
    date_completed = models.DateTimeField("Date Completed", null=True, blank=True)


class HarambeeQuestionAnswer(models.Model):

    harambee = models.ForeignKey(Harambee, null=False, blank=False)
    question = models.ForeignKey(LevelQuestion, null=False, blank=False)
    option_selected = models.ForeignKey(LevelQuestionOption, null=False, blank=False)
    date_answered = models.DateTimeField(null=False, blank=False)

    class Meta:
        verbose_name = "Level Question Answer"
        verbose_name_plural = "Level Question Answers"