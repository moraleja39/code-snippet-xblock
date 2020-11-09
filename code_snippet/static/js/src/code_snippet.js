/* Javascript for CodeSnippetXBlock. */
function CodeSnippetXBlock(runtime, element) {

    function highlight() {
      var block = $(".code_snippet_block pre code");
      block.each((i, el) => {
        console.log(el);
        hljs.highlightBlock(el);
      });
    }

    highlight();

    $(function ($) {});
}
