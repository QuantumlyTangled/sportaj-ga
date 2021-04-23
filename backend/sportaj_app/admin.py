from django.contrib import admin
from django import forms
from taggit_labels import widgets

from .models import Klub, SlikaKluba, PanogaManager, TipManager, VadbaManager, StarostManager, SpolManager, CenaManager
from .tags import custom_tag_register_admin


class KlubAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["panoga_tags"].widget = widgets.LabelWidget(model=Klub.panoga_tags.through.tag_class)
        self.fields["tip_tags"].widget = widgets.LabelWidget(model=Klub.tip_tags.through.tag_class)
        self.fields["vadba_tags"].widget = widgets.LabelWidget(model=Klub.vadba_tags.through.tag_class)
        self.fields["starost_tags"].widget = widgets.LabelWidget(model=Klub.starost_tags.through.tag_class)
        self.fields["spol_tags"].widget = widgets.LabelWidget(model=Klub.spol_tags.through.tag_class)
        # self.fields["urnik_tags"].widget = widgets.LabelWidget(model=Klub.urnik_tags.through.tag_class)
        self.fields["cena_tags"].widget = widgets.LabelWidget(model=Klub.cena_tags.through.tag_class)

    class Meta:
        model = Klub
        fields = [
            "slug",
            "ime",
            "opis",
            "logo",
            "location",
            "urnik",
            "mail",
            "homepage",
            "twitter",
            "facebook",
            "panoga_tags",
            "tip_tags",
            "vadba_tags",
            "starost_tags",
            "spol_tags",
#            "urnik_tags",
            "cena_tags"
        ]

class SlikaKlubaAdmin(admin.StackedInline):
    model = SlikaKluba

@admin.register(Klub)
class KlubAdmin(admin.ModelAdmin):
    form = KlubAdminForm
    inlines = [
        SlikaKlubaAdmin
    ]

    class Meta:
        model = Klub

@admin.register(SlikaKluba)
class SlikaKlubaAdmin(admin.ModelAdmin):
    pass


custom_tag_register_admin(PanogaManager.through)
custom_tag_register_admin(TipManager.through)
custom_tag_register_admin(VadbaManager.through)
custom_tag_register_admin(StarostManager.through)
custom_tag_register_admin(SpolManager.through)
# custom_tag_register_admin(UrnikManager.through)
custom_tag_register_admin(CenaManager.through)
