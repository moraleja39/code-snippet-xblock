import pkg_resources

from django.utils import translation
from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from web_fragments.fragment import Fragment
from xblockutils.resources import ResourceLoader
from .supported_languages import SUPPORTED_LANGUAGES

import logging
logger = logging.getLogger(__name__)

CODE_SAMPLE = '''/* Javascript for CodeSnippetXBlock. */
function CodeSnippetXBlock(runtime, element) {

    function updateCount(result) {
        $('.count', element).text(result.count);
    }

    var handlerUrl = runtime.handlerUrl(element, 'increment_count');

    $('p', element).click(function(eventObject) {
        $.ajax({
            type: 'POST',
            url: handlerUrl,
            data: JSON.stringify({'hello': 'world'}),
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
_ = translation.gettext

loader = ResourceLoader(__name__)

@XBlock.needs("i18n")
class CodeSnippetXBlock(XBlock):
    display_name = String(default=_("Code Snippet"), scope=Scope.settings)
    max_height = Integer(default=0)
    code = String(default=u'// Your code goes here', scope=Scope.content)
    #code = String(default=CODE_SAMPLE, scope=Scope.content)
    lang = String(default=u'', scope=Scope.content)

    non_editable_metadata_fields = ['code']
    has_score = False
    icon_class = 'other'


    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def _get_context(self):
        return {
            "code": self.code,
            "max_height": self.max_height,
            "lang": self.lang,
            "supported_languages": SUPPORTED_LANGUAGES
        }

    def student_view(self, context=None):
        """
        The primary view of the CodeSnippetXBlock, shown to students
        when viewing courses.
        """
        frag = Fragment()
        frag.content = loader.render_django_template('templates/code_snippet.html', self._get_context())
        frag.add_css(self.resource_string("static/css/code_snippet.css"))
        frag.add_css_url("//cdnjs.cloudflare.com/ajax/libs/highlight.js/10.3.2/styles/agate.min.css")

        logger.info("{}".format(self._get_context()))

        # Add i18n js
        statici18n_js_url = self._get_statici18n_js_url()
        if statici18n_js_url:
            frag.add_javascript_url(self.runtime.local_resource_url(self, statici18n_js_url))

        frag.add_javascript(self.resource_string("static/js/src/code_snippet.js"))
        frag.add_javascript_url("//cdnjs.cloudflare.com/ajax/libs/highlight.js/10.3.2/highlight.min.js")
        frag.initialize_js('CodeSnippetXBlock', self._get_context())
        return frag

    def studio_view(self, context=None):
        """
        The primary view of the CodeSnippetXBlock, shown to students
        when viewing courses.
        """
        frag = Fragment()
        frag.content = loader.render_django_template('templates/studio_view.html', self._get_context())

        frag.add_css(self.resource_string("static/css/code_snippet_studio.css"))

        # Add i18n js
        statici18n_js_url = self._get_statici18n_js_url()
        if statici18n_js_url:
            frag.add_javascript_url(self.runtime.local_resource_url(self, statici18n_js_url))

        frag.add_javascript(self.resource_string("static/js/src/code_snippet_studio.js"))
        frag.initialize_js('CodeSnippetStudioXBlock')

        return frag

    @XBlock.json_handler
    def submit_studio_edits(self, data, suffix=''):
        self.code = data.get('code', u'')
        self.max_height = data.get('max_height', 0)
        self.lang = data.get('lang', u'')
        return {'result': 'success'}

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            #("CodeSnippetXBlock", u"<code_snippet code=\"{}\"></code_snippet>".format(CODE_SAMPLE)),
            ("CodeSnippetXBlock", """<code_snippet max_height="0"></code_snippet>"""),
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

