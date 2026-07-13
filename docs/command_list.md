# Command List

Here is a list of the commands available in the editor console.

> Please keep in mind that this feature is experimental and still in its early stages. The commands currently available are primarily intended for demonstration and testing purposes.

### Legend
- Not done: `[]`
- In Progress `[.]`
- Done: `[x]`

### Planned Commands
| Done | Command | Arguments | Description |
|----|---------|-----------|-------------|
| `[]` | `link.help` | None | Displays the link for the command documentation
| `[x]` | `link.discord` | None | Displays the link to the OpenGS Discord server |
| `[x]` | `link.github` | None | Displays the link to the editor's GitHub repository |
||||
| `[x]` | `console.commands.list` | None | Display a simplified list of commands |
| `[x]` | `console.history.clear` | None | Clears the console message history |
| `[x]` | `console.history.list` | None | Displays the history of console commands entered by the user or GUI |
||||
| `[]` | `project.new` | `[<path>]` | Creates a new project (optionally at a target path) |
| `[]` | `project.open` | `<path>` | Opens an existing project file |
| `[]` | `project.save` | `[<path>]` | Saves the current project (or saves to a target path) |
| `[]` | `project.details` | `[...]` | **With subcommands** to read or edit author, description, etc. |
||||
| `[x]` | `land.image.import` | `<path>` | Imports the land image from a file |
| `[x]` | `boundary.image.import` | `<path>` | Imports the boundary image from a file |
| `[x]` | `density.image.import` | `<path>` | Imports the density image from a file |
| `[x]` | `terrain.image.import` | `<path>` | Imports the terrain image from a file |
||||
| `[]` | `density.image.remove` | None | Removes the current density image |
| `[]` | `density.map.normalize` | None | Normalizes density values |
| `[]` | `density.map.equator_distribute` | None | Generates equator-based density distribution |
||||
| `[]` | `territory.map.generate` | None | Generates the territory map |
| `[]` | `territory.image.export` | `<path>` | Exports the territory image |
| `[]` | `territory.definitions.export` | `<path> <format>` | Exports territory definitions |
| `[]` | `territory.history.export` | `<path> <format>` | Exports territory history |
| `[]` | `territory.exclude_ocean` | `<true\|false>` | Sets whether territory generation excludes ocean |
| `[]` | `territory.land_density` | `<value>` | Sets land territory density |
| `[]` | `territory.ocean_density` | `<value>` | Sets ocean territory density |
| `[]` | `territory.density_strength` | `<value>` | Sets territory density strength |
| `[]` | `territory.jagged_land` | `<true\|false>` | Sets jagged land border behavior for territories |
| `[]` | `territory.jagged_ocean` | `<true\|false>` | Sets jagged ocean border behavior for territories |
||||
| `[]` | `province.map.generate` | None | Generates the province map |
| `[]` | `province.image.export` | `<path>` | Exports the province image |
| `[]` | `province.definitions.export` | `<path> <format>` | Exports province definitions |
| `[]` | `province.exclude_ocean` | `<true\|false>` | Sets whether province generation excludes ocean |
| `[]` | `province.land_density` | `<value>` | Sets land province density |
| `[]` | `province.ocean_density` | `<value>` | Sets ocean province density |
| `[]` | `province.density_strength` | `<value>` | Sets province density strength |
| `[]` | `province.jagged_land` | `<true\|false>` | Sets jagged land border behavior for provinces |
| `[]` | `province.jagged_ocean` | `<true\|false>` | Sets jagged ocean border behavior for provinces |

## Aliases
| Done | Alias Name | Real Command |
|----|---------|-----------|
| `[]` | `?` | `link.help` |
| `[]` | `h` | `link.help` |
| `[]` | `help` | `link.help` |

# More optional future commands
- Commands to export input images (purpose: e.g. pull land image from maptool save file)
- Commands to export json file of project information
