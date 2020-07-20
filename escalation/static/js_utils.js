// Copyright [2020] [Two Six Labs, LLC]
// Licensed under the Apache License, Version 2.0

function post_to_server(id_on_web_page) {
    //This allows the web page to focus where the plot was updated instead of starting at the top of the web page
    let web_form=$('#form_'.concat(id_on_web_page));
    web_form.attr('action','#'.concat(id_on_web_page));
    web_form.submit();
}

function reset_form(id_on_web_page) {
    //This allows the web page to focus where the plot was updated instead of starting at the top of the web page
    $('#form_'.concat(id_on_web_page))[0].process.value='';
    post_to_server(id_on_web_page);

}