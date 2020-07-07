function post_to_server(id_on_web_page) {
    //This allows the web page to focus where the plot was updated instead of starting at the top of the web page
    console.log(id_on_web_page)
   $('#form_'.concat(id_on_web_page)).attr('action','#'.concat(id_on_web_page))
  $('#form_'.concat(id_on_web_page)).submit();
}