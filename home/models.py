from django.db import models
from django.shortcuts import render
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.models import Page, Orderable

from streams import blocks


class HomePageCarouselImages(Orderable):
    """Between 1 and 5 images for the home page carousel."""

    page = ParentalKey("home.HomePage", related_name="carousel_images")
    carousel_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("carousel_image")
    ]


class HomePage(RoutablePageMixin, Page):
    """Home page model"""
    templates = "home/home_page.html"
    banner_title = models.CharField(max_length=100, blank=False, null=True)
    banner_subtitle = RichTextField(features=["bold", "italic"])
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    banner_cta = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content = StreamField([
        ("cta", blocks.CTABlock()),
    ], null=True, blank=True, use_json_field=True)

    max_count = 1
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("banner_title"),
            FieldPanel("banner_subtitle"),
            PageChooserPanel('banner_cta'),
        ], heading='Banner Options'),
        MultiFieldPanel([
            InlinePanel('carousel_images', heading='Carousel Images', max_num=5, min_num=1, label="Image"),
        ]),
        FieldPanel("content"),
    ]

    promote_panels = [
        FieldPanel('banner_image')
    ]

    class Meta:
        verbose_name = 'Home Page'
        verbose_name_plural = 'Home Pages'

    @route(r'^subscribe/$')
    def the_subscribe_page(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context['a_special_test'] = 'Hello World 123123'
        return render(request, "home/subscribe.html", context)
