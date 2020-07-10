## escalation_config Type

`object` ([escalation_config](escos.md))

# escalation_config Properties

| Property                                    | Type     | Required | Nullable       | Defined by                                                                                               |
| :------------------------------------------ | -------- | -------- | -------------- | :------------------------------------------------------------------------------------------------------- |
| [title](#title)                             | `string` | Required | cannot be null | [escalation_config](escos-properties-title.md "undefined#/properties/title")                             |
| [brief_desc](#brief_desc)                   | `string` | Required | cannot be null | [escalation_config](escos-properties-brief_desc.md "undefined#/properties/brief_desc")                   |
| [data_backend](#data_backend)               | `string` | Required | cannot be null | [escalation_config](escos-properties-data_backend.md "undefined#/properties/data_backend")               |
| [data_file_directory](#data_file_directory) | `string` | Required | cannot be null | [escalation_config](escos-properties-data_file_directory.md "undefined#/properties/data_file_directory") |
| [data_sources](#data_sources)               | `array`  | Required | cannot be null | [escalation_config](escos-properties-data_sources.md "undefined#/properties/data_sources")               |
| [available_pages](#available_pages)         | `object` | Required | cannot be null | [escalation_config](escos-properties-dashboard-dictionary.md "undefined#/properties/available_pages")    |

## title

title shown at the top of the website


`title`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [escalation_config](escos-properties-title.md "undefined#/properties/title")

### title Type

`string`

## brief_desc

description shown at the top of the website


`brief_desc`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [escalation_config](escos-properties-brief_desc.md "undefined#/properties/brief_desc")

### brief_desc Type

`string`

## data_backend

How the data is being managed on the server


`data_backend`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [escalation_config](escos-properties-data_backend.md "undefined#/properties/data_backend")

### data_backend Type

`string`

### data_backend Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value         | Explanation |
| :------------ | ----------- |
| `"psql"`      |             |
| `"mysql"`     |             |
| `"local_csv"` |             |

## data_file_directory

Where the data is on the server


`data_file_directory`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [escalation_config](escos-properties-data_file_directory.md "undefined#/properties/data_file_directory")

### data_file_directory Type

`string`

## data_sources

list of tables or folders that server will use for the plots


`data_sources`

-   is required
-   Type: `string[]`
-   cannot be null
-   defined in: [escalation_config](escos-properties-data_sources.md "undefined#/properties/data_sources")

### data_sources Type

`string[]`

## available_pages

a dictionary containing the dashboard pages of the site


`available_pages`

-   is required
-   Type: `object` ([Dashboard Dictionary](escos-properties-dashboard-dictionary.md))
-   cannot be null
-   defined in: [escalation_config](escos-properties-dashboard-dictionary.md "undefined#/properties/available_pages")

### available_pages Type

`object` ([Dashboard Dictionary](escos-properties-dashboard-dictionary.md))
