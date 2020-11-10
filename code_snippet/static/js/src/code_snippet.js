/* Javascript for CodeSnippetXBlock. */
function CodeSnippetXBlock(runtime, element, context) {

  function highlight() {
    var block = $(".code_snippet_block pre code");
    block.each((i, el) => {
      console.log(el);
      hljs.highlightBlock(el);
    });
  }

  highlight();

  // Prevent textarea content for changing
  $(element).find('.code-select').on('click', function () {
    // dont select all if the user selected a part of the code
    if (this.selectionStart === this.selectionEnd) {
      $(this).select().focus();
    }
  });
}
