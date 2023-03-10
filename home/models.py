from django.db import models
from django.shortcuts import render
from modelcluster.fields import ParentalKey
from rest_framework.fields import Field
from wagtail.admin.panels import TabbedInterface, ObjectList
from wagtail.api import APIField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import RichTextField, StreamField

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

    api_fields = [
        APIField("carousel_image"),
    ]


class BannerCTASerializer(Field):
    def to_representation(self, page):
        return {
            'id': page.id,
            'title': page.title,
            'first_published_at': page.first_published_at,
            'owner': page.owner,
            'slug': page.slug,
            'url': page.url,
        }


class HomePage(RoutablePageMixin, Page):
    """Home page model"""
    template = "home/home_page.html"

    subpage_types = [
        'blog.BlogListingPage',
        'contact.ContactPage',
        'flex.FlexPage',
    ]

    parent_page_type = [
        'wagtailcore.Page'
    ]

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

    api_fields = [
        APIField("banner_title"),
        APIField("banner_subtitle"),
        APIField("banner_image"),
        APIField("banner_cta", serializer=BannerCTASerializer()),
        APIField("carousel_images"),
        APIField("content"),
        APIField("a_custom_api_response"),
    ]

    @property
    def a_custom_api_response(self):
        # return ["SOMETHING CUSTOM", 3.14, [1, 2, 3, 'a', 'b', 'c']]
        # logic goes in here
        return f"Banner Title Is: {self.banner_title}"

    max_count = 1
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [InlinePanel("carousel_images", max_num=5, min_num=1, label="Image")],
            heading="Carousel Images",
        ),
        FieldPanel("content"),
    ]

    # To hide promote and settings tabs
    # promote_panels = []
    # settings_panels = []

    banner_panels = [
        MultiFieldPanel(
            [
                FieldPanel("banner_title"),
                FieldPanel("banner_subtitle"),
                FieldPanel("banner_image"),
                PageChooserPanel("banner_cta"),
            ],
            heading="Banner Options",
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading='Content'),
            ObjectList(banner_panels, heading="Banner Settings"),
            ObjectList(Page.promote_panels, heading='Promotional Stuff'),
        ]
    )

    class Meta:
        verbose_name = 'Home Page'
        verbose_name_plural = 'Home Pages'

    @route(r'^subscribe/$')
    def the_subscribe_page(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context['a_special_test'] = 'Hello World 123123'
        return render(request, "home/subscribe.html", context)

    def get_admin_display_title(self):
        return "Custom Home Page Title"

# Changes the "title" field's verbose name to "Custom Name" but is still referenced it in the template as `page.title`
# HomePage._meta.get_field("title").verbose_name = "Custom Name"
# HomePage._meta.get_field("title").help_text = None
# Only appears when creating a new page.
# HomePage._meta.get_field("title").default = "Default HomePage Title"
# To add a default `slug` value to the page.
# # This does not need to reflect the same (or similar) value that the `title` field has.
# HomePage._meta.get_field("slug").default = "default-homepage-title"
