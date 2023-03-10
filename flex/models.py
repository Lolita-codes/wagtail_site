"""Flexible page"""
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.core import blocks as streamfield_blocks


from streams import blocks


class FlexPage(Page):
    """Flexible page class"""

    template = "flex/flex_page.html"

    subpage_types = ['flex.FlexPage', 'contact.ContactPage']
    parent_page_types = [
        'flex.FlexPage',
        'home.HomePage',
    ]

    content = StreamField(
        [
            ('title_and_text', blocks.TitleAndTextBlock()),
            ('full_richtext', blocks.RichTextBlock()),
            ('cardblock', blocks.CardBlock()),
            ('ctablock', blocks.CTABlock()),
            ('button', blocks.ButtonBlock()),
            ("char_block", streamfield_blocks.CharBlock(
                required=True,
                help_text='Oh wow this is help text!!',
                min_length=10,
                max_length=50,
                template="streams/char_block.html",
            ))
        ],
        null=True,
        blank=True,
        use_json_field=True
    )

    subtitle = models.CharField(max_length=100, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("content")
    ]

    class Meta:
        verbose_name = "Flex Page"
        verbose_name_plural = "Flex Pages"
