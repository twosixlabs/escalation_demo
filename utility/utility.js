function store_page_location_then_submit(plot_index) {
    $('#the_form').attr('action','#plot'.concat(plot_index))
  $('#the_form').submit();
}