from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Model

from apps.ava_core.models import TimeStampedModel, ReferenceModel
from apps.ava_test.models import Test, TestResult
from apps.ava_test.helpers import generate_hex_token


class EmailTest(Test):
    fromaddr = models.EmailField(null=False)
    subject = models.CharField(max_length=200, null=False)
    body = models.TextField(null=False)
    html_body = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name or u''

    def get_absolute_url(self):
        return reverse('email-test-detail',kwargs={'pk': self.pk})


class EmailTestTarget(TimeStampedModel):
    emailtest = models.ForeignKey('EmailTest', null=False, related_name='targets')
    target = models.ForeignKey('ava_core_identity.Identifier', null=False)
    token = models.CharField(max_length=100, null=False, unique=True, default=generate_hex_token)

    class Meta:
        unique_together = ("emailtest", "target", "token")

    def __unicode__(self):
        return unicode(self.target)

    def get_absolute_url(self):
        return reverse('email-test-target-detail',kwargs={'pk': self.pk})


class EmailTestResult(TestResult):
    target = models.ForeignKey('EmailTestTarget', null=False, related_name='results')


class EmailTemplate(Model):
    subject = models.CharField(max_length=200, null=False)
    message = models.TextField(null=False)
    message_html = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.subject or u''

    def get_absolute_url(self):
        return reverse('email-template-detail',kwargs={'pk': self.pk})
