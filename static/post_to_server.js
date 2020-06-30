function post_to_server(plot_index) {
    //This allows the web page to focus where the plot was updated instead of starting at the top of the web page
   $('#form_'.concat(plot_index)).attr('action','#graphic_'.concat(plot_index))
  $('#form_'.concat(plot_index)).submit();
}