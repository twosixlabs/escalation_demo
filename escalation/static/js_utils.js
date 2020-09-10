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

function show_all_row_handler(selector_id) {
    let selector = $("#".concat(selector_id));
    const selected_elements = selector.val();
    if (selected_elements.length==0){
        selector.val("Show All Rows");
        selector.attr('data-show_all_rows',true)
    }
    else if (selector.attr('data-show_all_rows')=="true"){
        // If something is selected along with show all rows
        // Pop the show all rows item out using shift, then set elements to remaining
        selected_elements.shift();
        selector.val(selected_elements);
        selector.attr('data-show_all_rows',false)
    }
    else if (selected_elements.includes("Show All Rows")){
        // If the user has selected show all rows, deselect everything else
        selector.selectpicker('deselectAll');
        selector.val("Show All Rows");
        selector.attr('data-show_all_rows',true)
    }
    selector.selectpicker('refresh');
}


function edit_graphic(page_id,graphic,graphic_status) {
    //This allows the web page to focus where the plot was updated instead of starting at the top of the web page
    let graphic_form=$('#form_button_click');
    graphic_form[0].page_id.value=page_id;
    graphic_form[0].graphic.value=graphic;
    graphic_form[0].graphic_status.value=graphic_status;
    graphic_form.submit();
}

function modify_config(modification, page_id=-1,graphic=''){
    let graphic_form=$('#form_button_click');
    let add_page_form = $('#form_add_page');
    let name = document.getElementById("webpage_label_".concat(page_id)).value;

    if ((modification!='add_page' && modification!='rename_page') || name) {
        add_page_form[0].page_id.value = page_id;
        add_page_form[0].graphic.value = graphic;
        add_page_form[0].modification.value = modification;
        add_page_form[0].title.value = graphic_form[0].title.value;
        add_page_form[0].brief_desc.value = graphic_form[0].brief_desc.value;
        add_page_form[0].data_backend.value = graphic_form[0].data_backend.value;
        add_page_form[0].webpage_label.value = name;
        add_page_form.submit();
    }
}

function get_main_data_sources(data_source_dict){
    let data_sources = new Set();
    data_sources.add(data_source_dict['main_data_source']['data_source_type']);
    let additional_data_source;
    if ('additional_data_sources' in data_source_dict) {
        for (additional_data_source of data_source_dict['additional_data_sources']) {
            data_sources.add(additional_data_source['data_source_type'])
        }
    }
    return data_sources
}

function toggle_rename_page(page_id) {
    let page_div = document.getElementById("page_".concat(page_id));
    let rename_page_div = document.getElementById("rename_page_".concat(page_id));
    if (page_div.style.display === "none") {
        page_div.style.display = "block";
        rename_page_div.style.display = "none";
    } else {
        page_div.style.display = "none";
        rename_page_div.style.display = "block";
    }
}