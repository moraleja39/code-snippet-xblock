/* Javascript for CodeSnippetXBlock. */
function CodeSnippetStudioXBlock(runtime, element) {

  function submit(data) {
    runtime.notify('save', {state: 'start', message: gettext("Saving")});
    var handlerUrl = runtime.handlerUrl(element, 'submit_studio_edits');
    $.ajax({
      type: "POST",
      url: handlerUrl,
      data: JSON.stringify(data),
      dataType: "json",
      global: false,  // Disable Studio's error handling that conflicts with studio's notify('save') and notify('cancel') :-/
      success: () => {
        runtime.notify('save', {state: 'end'});
      },
      error: () => {
        runtime.notify('error', {title: gettext("Unable to update settings"), message: ''});
      }
    });
  }

  var $el = $(element);

  $(element).find(".save-button").on('click', e => {
    e.preventDefault();
    var data = {
      max_height: parseInt($el.find("#max-height").val()),
      code: $el.find("#code").val(),
      lang: $el.find("#lang").val(),
    }
    submit(data);
  });

  $(element).find(".cancel-button").on('click', (e) => {
    e.preventDefault();
    runtime.notify('cancel', {});
  });
}
