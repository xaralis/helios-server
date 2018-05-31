# -*- coding: utf-8 -*-
"""
Forms for Helios
"""

from django import forms
from models import Election
from widgets import SplitSelectDateTimeWidget
from fields import SplitDateTimeField
from django.conf import settings


class ElectionForm(forms.Form):
  short_name = forms.SlugField(max_length=40, help_text=u'bez mezer, bude použita jako část URL vašeho hlasování, např. my-club-2010', label=u"Zkratka")
  name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size':60}), help_text=u'plný název vašeho hlasování, např. My Club 2010 Election', label=u"Název")
  description = forms.CharField(max_length=32000, widget=forms.Textarea(attrs={'cols': 70, 'wrap': 'soft'}), required=False, label=u"Popis")
  election_type = forms.ChoiceField(label=u"Typ", choices = Election.ELECTION_TYPES)
  use_voter_aliases = forms.BooleanField(required=False, initial=False, help_text=u'zvolíte-li tuto možnost, na stránce pro sledování hlasovacích lístků budou jména voličů nahrazena aliasy, např. "V12"', label=u"Použít aliasy voličů")
  #use_advanced_audit_features = forms.BooleanField(required=False, initial=True, help_text='disable this only if you want a simple election with reduced security but a simpler user interface')
  randomize_answer_order = forms.BooleanField(required=False, initial=False, help_text=u'zvolte, pokud chcete, aby se každému voliči zobrazovaly odpovědi na otázky v náhodně zvoleném pořadí', label=u"Odpovědi v náhodném pořadí")
  private_p = forms.BooleanField(required=False, initial=False, label=u"Soukromé?", help_text=u'Soukromé hlasování je viditelné jen pro registrované voliče.')
  help_email = forms.CharField(required=False, initial="", label=u"E-mail pro nápovědu", help_text=u'e-mailová adresa, na kterou se budou voliči obracet s žádostmi o pomoc.')
  voting_starts_at = SplitDateTimeField(help_text = u'datum a čas zahájení hlasování; v UTC, takže oproti časovému pásmu ČR je menší o 1, resp. 2 hodiny',
                                   widget=SplitSelectDateTimeWidget, required=False, label=u"Hlasování začíná v")
  voting_ends_at = SplitDateTimeField(help_text = u'datum a čas ukončení hlasování; v UTC, takže oproti časovému pásmu ČR je menší o 1, resp. 2 hodiny',
                                   widget=SplitSelectDateTimeWidget, required=False, label=u"Hlasování končí v")
  
  if settings.ALLOW_ELECTION_INFO_URL:
    election_info_url = forms.CharField(required=False, initial="", label=u"URL pro stažení informací o hlasování", help_text=u"URL dokumentu ve formátu PDF, obsahujícího doplňkové informace k hlasování, např. životopisy a profily kandidátů")
  
  pass
  
class ElectionTimeExtensionForm(forms.Form):
  voting_extended_until = SplitDateTimeField(help_text = u'datum a čas prodlouženého ukončení hlasování; v UTC',
                                   widget=SplitSelectDateTimeWidget, required=False, label=u"Hlasování prodlouženo do")
  
class EmailVotersForm(forms.Form):
  subject = forms.CharField(max_length=80)
  body = forms.CharField(max_length=4000, widget=forms.Textarea)
  send_to = forms.ChoiceField(label=u"Poslat", initial="all", choices= [('all', u'všem voličům'), ('voted', u'voličům, kteří již odevzdali lístek'), ('not-voted', u'voličům, kteří ještě neodevzdali lístek')])

class TallyNotificationEmailForm(forms.Form):
  subject = forms.CharField(max_length=80)
  body = forms.CharField(max_length=2000, widget=forms.Textarea, required=False)
  send_to = forms.ChoiceField(label=u"Poslat", choices= [('all', u'všem voličům'), ('voted', u'jen voličům, kteří odevzdali lístek'), ('none', u'nikomu -- jste si tím jist?')])

class VoterPasswordForm(forms.Form):
  voter_id = forms.CharField(max_length=50, label=u"ID voliče")
  password = forms.CharField(widget=forms.PasswordInput(), max_length=100)

