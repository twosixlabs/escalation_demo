function post_to_server(plot_index) {
   $('#form_'.concat(plot_index)).attr('action','#graphic_'.concat(plot_index))
  $('#form_'.concat(plot_index)).submit();
}