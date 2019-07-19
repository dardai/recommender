# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CourseModel(models.Model):
    id = models.IntegerField(primary_key=True)
    course_index = models.IntegerField()
    recommend_value = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'course_ model'


class CourseDr(models.Model):
    id = models.IntegerField(primary_key=True)
    course_index = models.IntegerField()
    recommend_value = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'course_dr'


class CourseInfo(models.Model):
    id = models.BigIntegerField(primary_key=True)
    system_course_id = models.BigIntegerField(blank=True, null=True)
    course_name = models.CharField(max_length=100, blank=True, null=True)
    course_differ = models.CharField(max_length=100, blank=True, null=True)
    course_type = models.CharField(max_length=100, blank=True, null=True)
    course_key = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_info'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ExamInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    system_exam_id = models.IntegerField()
    exam_key = models.CharField(max_length=100)
    exam_name = models.CharField(max_length=100)
    exam_deadline = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'exam_info'


class ExamQuestionbank(models.Model):
    exam_id = models.IntegerField()
    questionbank_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'exam_questionbank'


class QuestionbankInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    system_questionbank_id = models.IntegerField()
    related_knowledgepoint = models.CharField(db_column='related_knowledgePoint', max_length=100)  # Field name made lowercase.
    questionbank_key = models.CharField(max_length=100)
    questionbank_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'questionbank_info'


class TaskInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    task_name = models.CharField(max_length=100)
    task_content = models.CharField(max_length=100)
    task_deadline = models.DateTimeField()
    system_course_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'task_info'


class TestDr(models.Model):
    id = models.IntegerField(primary_key=True)
    course_index = models.IntegerField()
    recommend_value = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'test_dr'


class TestInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    system_test_id = models.IntegerField()
    test_name = models.CharField(max_length=100)
    test_content = models.CharField(max_length=100)
    course_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'test_info'


class TestModel(models.Model):
    id = models.IntegerField(primary_key=True)
    course_index = models.IntegerField()
    recommend_value = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'test_model'


class TrainInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    system_train_id = models.IntegerField()
    train_name = models.CharField(max_length=100)
    exam_id = models.IntegerField()
    course_id = models.IntegerField()
    train_key = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'train_info'


class UserBasicInfo(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    user_name = models.CharField(max_length=50, blank=True, null=True)
    user_system_id = models.BigIntegerField(blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_basic_info'


class UserCourse(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(UserBasicInfo, models.DO_NOTHING, blank=True, null=True)
    course = models.ForeignKey(CourseInfo, models.DO_NOTHING, blank=True, null=True)
    learning_time = models.IntegerField(blank=True, null=True)
    click_times = models.IntegerField(blank=True, null=True)
    score = models.CharField(max_length=255, blank=True, null=True)
    collect_status = models.CharField(max_length=10, blank=True, null=True)
    commit_status = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_course'


class UserExam(models.Model):
    id = models.IntegerField(primary_key=True)
    exam_id = models.IntegerField()
    user_id = models.IntegerField()
    exam_submit_time = models.DateTimeField()
    overtime_status = models.CharField(max_length=10)
    score = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_exam'


class UserLearningTime(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user_course = models.ForeignKey(UserCourse, models.DO_NOTHING, blank=True, null=True)
    course_key = models.CharField(max_length=100, blank=True, null=True)
    learning_total_time = models.IntegerField(blank=True, null=True)
    course_total_time = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(UserBasicInfo, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_learning_time'


class UserTask(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    task_id = models.IntegerField()
    submit_datetime = models.DateTimeField()
    overtime_status = models.CharField(max_length=10)
    score = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_task'


class UserTest(models.Model):
    id = models.IntegerField(primary_key=True)
    user_course_id = models.IntegerField()
    test_content = models.CharField(max_length=100)
    test_name = models.CharField(max_length=100)
    test_id = models.IntegerField()
    test_score = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_test'


class UserTrain(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    train_id = models.IntegerField()
    train_name = models.CharField(max_length=100)
    train_start_time = models.DateTimeField()
    exam_id = models.IntegerField()
    train_time = models.IntegerField()
    course_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_train'
