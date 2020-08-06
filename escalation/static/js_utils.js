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


function edit_graphic(page_id,graphic,is_graphic_new) {
    //This allows the web page to focus where the plot was updated instead of starting at the top of the web page
    let web_form=$('#form_button_click');
    web_form[0].page_id.value=page_id;
    web_form[0].graphic.value=graphic;
    web_form[0].is_graphic_new.value=is_graphic_new;
    web_form.submit();
}

function new_graphic(page_id){
    let graphic_name=document.getElementById("new_graphic_name_".concat(page_id)).value
    if (graphic_name) {
        graphic_name=graphic_name.replace(/\ /g,"_");
        edit_graphic(page_id,graphic_name,true)
    }
}

function add_page(){
    let web_form = $('#form_add_page');
    if (web_form[0].webpage_label.value) {
        web_form.submit();
    }
}