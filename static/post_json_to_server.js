function post_json_to_server(plot_index) {
    var formData = $('#the_form').serializeJSON();
    var jsonString = JSON.stringify(formData);
    $.ajax({
      type: "POST",
      url: '#graphic'.concat(plot_index),
      data: jsonString,
      success: function(){},
      dataType: "json",
      contentType : "application/json"
    })
}