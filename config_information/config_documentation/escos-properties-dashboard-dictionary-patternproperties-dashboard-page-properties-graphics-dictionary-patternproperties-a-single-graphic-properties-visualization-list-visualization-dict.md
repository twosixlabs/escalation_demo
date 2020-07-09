## items Type

`object` ([visualization dict](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-visualization-list-visualization-dict.md))

# visualization dict Properties

| Property            | Type     | Required | Nullable       | Defined by                                                                                                                                                                                                                                                                                                                                                                                                                           |
| :------------------ | -------- | -------- | -------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [type](#type)       | `string` | Required | cannot be null | [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-visualization-list-visualization-dict-properties-type.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/graphics/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/visualization_options/items/properties/type")       |
| [column](#column)   | `array`  | Required | cannot be null | [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-visualization-list-visualization-dict-properties-column.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/graphics/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/visualization_options/items/properties/column")   |
| [options](#options) | `object` | Optional | cannot be null | [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-visualization-list-visualization-dict-properties-options.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/graphics/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/visualization_options/items/properties/options") |

## type

hover_data changes what data is shown when scrolling over data. examples of the other two: groupby: <https://plotly.com/javascript/group-by/> aggregate: <https://plotly.com/javascript/aggregations/>


`type`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-visualization-list-visualization-dict-properties-type.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/graphics/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/visualization_options/items/properties/type")

### type Type

`string`

### type Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value          | Explanation |
| :------------- | ----------- |
| `"hover_data"` |             |
| `"groupby"`    |             |
| `"aggregate"`  |             |

## column




`column`

-   is required
-   Type: `string[]`
-   cannot be null
-   defined in: [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-visualization-list-visualization-dict-properties-column.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/graphics/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/visualization_options/items/properties/column")

### column Type

`string[]`

## options




`options`

-   is optional
-   Type: `object` ([Details](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-visualization-list-visualization-dict-properties-options.md))
-   cannot be null
-   defined in: [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-visualization-list-visualization-dict-properties-options.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/graphics/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/visualization_options/items/properties/options")

### options Type

`object` ([Details](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-visualization-list-visualization-dict-properties-options.md))
