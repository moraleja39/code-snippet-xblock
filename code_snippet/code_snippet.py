"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from django.utils import translation
from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment
from xblockutils.resources import ResourceLoader

import logging
logger = logging.getLogger(__name__)

sample_js = '''/* Javascript for CodeSnippetXBlock. */
function CodeSnippetXBlock(runtime, element) {

    function updateCount(result) {
        $('.count', element).text(result.count);
    }

    var handlerUrl = runtime.handlerUrl(element, 'increment_count');

    $('p', element).click(function(eventObject) {
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"hello": "world"}),
            success: updateCount
        });
    });

    $(function ($) {
        /*
        Use `gettext` provided by django-statici18n for static translations

        var gettext = CodeSnippetXBlocki18n.gettext;
        */

        /* Here's where you'd do things on page load. */
    });
}'''

class CodeSnippetXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    code = String(default=sample_js, scope=Scope.content)

    has_score = False
    icon_class = 'other'

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the CodeSnippetXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/code_snippet.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/code_snippet.css"))
        frag.add_css_url("//cdnjs.cloudflare.com/ajax/libs/highlight.js/10.3.2/styles/agate.min.css")

        logger.error("{}".format(context))

        # Add i18n js
        statici18n_js_url = self._get_statici18n_js_url()
        if statici18n_js_url:
            frag.add_javascript_url(self.runtime.local_resource_url(self, statici18n_js_url))

        frag.add_javascript(self.resource_string("static/js/src/code_snippet.js"))
        frag.add_javascript_url("//cdnjs.cloudflare.com/ajax/libs/highlight.js/10.3.2/highlight.min.js")
        frag.initialize_js('CodeSnippetXBlock')
        return frag

    def studio_view(self, context=None):
        """
        The primary view of the CodeSnippetXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/studio_view.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/code_snippet.css"))

        # Add i18n js
        statici18n_js_url = self._get_statici18n_js_url()
        if statici18n_js_url:
            frag.add_javascript_url(self.runtime.local_resource_url(self, statici18n_js_url))

        return frag

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def increment_count(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("CodeSnippetXBlock",
             """<code_snippet/>
             """),
            ("Multiple CodeSnippetXBlock",
             """<vertical_demo>
                <code_snippet code="var a = 1"></code_snippet>
                <code_snippet/>
                <code_snippet/>
                </vertical_demo>
             """),
        ]

    @staticmethod
    def _get_statici18n_js_url():
        """
        Returns the Javascript translation file for the currently selected language, if any.
        Defaults to English if available.
        """
        locale_code = translation.get_language()
        if locale_code is None:
            return None
        text_js = 'public/js/translations/{locale_code}/text.js'
        lang_code = locale_code.split('-')[0]
        for code in (locale_code, lang_code, 'en'):
            loader = ResourceLoader(__name__)
            if pkg_resources.resource_exists(
                    loader.module_name, text_js.format(locale_code=code)):
                return text_js.format(locale_code=code)
        return None

    @staticmethod
    def get_dummy():
        """
        Dummy method to generate initial i18n
        """
        return translation.gettext_noop('Dummy')
