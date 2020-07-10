## ^\[a-zA-Z0-9\_]\*$ Type

`object` ([Dashboard Page](escos-properties-dashboard-dictionary-patternproperties-dashboard-page.md))

# Dashboard Page Properties

| Property                      | Type     | Required | Nullable       | Defined by                                                                                                                                                                                                                     |
| :---------------------------- | -------- | -------- | -------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [button_label](#button_label) | `string` | Required | cannot be null | [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-button_label.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/button_label")    |
| [graphics](#graphics)         | `object` | Optional | cannot be null | [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/graphics") |

## button_label

label of the page that will show up on the website


`button_label`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-button_label.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/button_label")

### button_label Type

`string`

## graphics

a dictionary containing the graphics on the page


`graphics`

-   is optional
-   Type: `object` ([Graphics Dictionary](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary.md))
-   cannot be null
-   defined in: [escalation_config](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary.md "undefined#/properties/available_pages/patternProperties/^\[a-zA-Z0-9\_]\*$/properties/graphics")

### graphics Type

`object` ([Graphics Dictionary](escos-properties-dashboard-dictionary-patternproperties-dashboard-page-properties-graphics-dictionary.md))
