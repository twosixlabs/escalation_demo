## ^\[a-zA-Z0-9\_]\*$ Type

`object` ([A single graphic](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic.md))

# A single graphic Properties

| Property                                        | Type     | Required | Nullable       | Defined by                                                                                                                                                                                                                                                                                                                                                            |
| :---------------------------------------------- | -------- | -------- | -------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [plot_manager](#plot_manager)                   | `string` | Required | cannot be null | [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-plot_manager.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/graphics/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/plot_manager")                |
| [title](#title)                                 | `string` | Required | cannot be null | [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-title.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/graphics/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/title")                              |
| [brief_desc](#brief_desc)                       | `string` | Required | cannot be null | [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-brief_desc.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/graphics/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/brief_desc")                    |
| [data_sources](#data_sources)                   | `array`  | Required | cannot be null | [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-data_sources.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/graphics/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/data_sources")                |
| [data](#data)                                   | `object` | Required | cannot be null | [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-data-dictionary.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/graphics/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/data")                     |
| [plot_specific_info](#plot_specific_info)       | `object` | Required | cannot be null | [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-plot-dictionary.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/graphics/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/plot_specific_info")       |
| [visualization_options](#visualization_options) | `array`  | Optional | cannot be null | [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-visualization-list.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/graphics/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/visualization_options") |
| [selectable_data_list](#selectable_data_list)   | `array`  | Optional | cannot be null | [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-selector-list.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/graphics/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/selectable_data_list")       |

## plot_manager

plot library you would like to use, only plotly is currently available


`plot_manager`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-plot_manager.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/graphics/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/plot_manager")

### plot_manager Type

`string`

### plot_manager Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value      | Explanation |
| :--------- | ----------- |
| `"plotly"` |             |

## title

title shown above the graph


`title`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-title.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/graphics/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/title")

### title Type

`string`

## brief_desc

description shown above the graph


`brief_desc`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-brief_desc.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/graphics/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/brief_desc")

### brief_desc Type

`string`

## data_sources

What tables are use to define this graphic


`data_sources`

-   is required
-   Type: `object[]` ([Details](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-data_sources-items.md))
-   cannot be null
-   defined in: [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-data_sources.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/graphics/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/data_sources")

### data_sources Type

`object[]` ([Details](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-data_sources-items.md))

## data

which data column goes on each axis


`data`

-   is required
-   Type: `object` ([Data Dictionary](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-data-dictionary.md))
-   cannot be null
-   defined in: [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-data-dictionary.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/graphics/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/data")

### data Type

`object` ([Data Dictionary](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-data-dictionary.md))

## plot_specific_info

this dictionary depends on the graphing library


`plot_specific_info`

-   is required
-   Type: `object` ([Plot Dictionary](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-plot-dictionary.md))
-   cannot be null
-   defined in: [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-plot-dictionary.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/graphics/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/plot_specific_info")

### plot_specific_info Type

`object` ([Plot Dictionary](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-plot-dictionary.md))

## visualization_options

modifications to the existing graph


`visualization_options`

-   is optional
-   Type: `object[]` ([visualization dict](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-visualization-list-visualization-dict.md))
-   cannot be null
-   defined in: [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-visualization-list.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/graphics/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/visualization_options")

### visualization_options Type

`object[]` ([visualization dict](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-visualization-list-visualization-dict.md))

## selectable_data_list

list of data selectors for a graphic


`selectable_data_list`

-   is optional
-   Type: `object[]` ([Selector Dict](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-selector-list-selector-dict.md))
-   cannot be null
-   defined in: [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-selector-list.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/graphics/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/selectable_data_list")

### selectable_data_list Type

`object[]` ([Selector Dict](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-selector-list-selector-dict.md))

### selectable_data_list Constraints

**maximum number of items**: the maximum number of items for this array is: `6`
