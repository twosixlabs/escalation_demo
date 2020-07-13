## items Type

`object` ([Selector Dict](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-selector-list-selector-dict.md))

all of

-   [Untitled undefined type in escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-selector-list-selector-dict-allof-0.md "check type definition")
-   [Untitled undefined type in escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-selector-list-selector-dict-allof-1.md "check type definition")

# Selector Dict Properties

| Property              | Type     | Required | Nullable       | Defined by                                                                                                                                                                                                                                                                                                                                                                                                          |
| :-------------------- | -------- | -------- | -------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [type](#type)         | `string` | Required | cannot be null | [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-selector-list-selector-dict-properties-type.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/graphics/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/selectable_data_list/items/properties/type") |
| Additional Properties | Any      | Optional | can be null    |                                                                                                                                                                                                                                                                                                                                                                                                                     |

## type

select is a filter operation based on label,numerical_filter is a filter operation on numerical data,axis you can use to change what column data is shown on a axis


`type`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary-patternproperties-a-single-graphic-properties-selector-list-selector-dict-properties-type.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/graphics/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/selectable_data_list/items/properties/type")

### type Type

`string`

### type Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value                | Explanation |
| :------------------- | ----------- |
| `"select"`           |             |
| `"numerical_filter"` |             |
| `"axis"`             |             |

## Additional Properties

Additional properties are allowed and do not have to follow a specific schema
