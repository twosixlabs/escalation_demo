function post_json_to_server(plot_index) {
    var formData = JSON.stringify($("#myForm").serializeArray());
    $.ajax({
      type: "POST",
      url: '#graphic'.concat(plot_index),
      data: formData,
      success: function(){},
      dataType: "json",
      contentType : "application/json"
    })
}