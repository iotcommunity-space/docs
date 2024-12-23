# IoT Community Documentation Repository

This repository houses the comprehensive documentation for the IoT Community platform, accessible at [iotCommunity.space/docs](https://iotCommunity.space/docs). It implements a three-column documentation system covering various IoT topics including Architecture, API, Networking, Security, Data, and Deployment.

## Repository Structure

The documentation system is built using a three-column architecture:

```
Example Structure -> iotCommunity.space/docs/
│       └── docs/
│           ├── Architecture/
│           │   ├── authentication.md
│           │   ├── device-management.md
│           │   └── network-topologies.md
│           ├── Api/
│           └── Networking/
├── structure.json
└── *-tree.yml
```

### Column Organization

1. **Left Column (Navigation)**
   - Rendered through YAML configuration files
   - Defines the hierarchical structure of documentation
   - Example structure:
   ```yaml
   sections:
     - title: Network
       subsections:
         - local: network-topologies
           title: Network Topologies
         - local: device-management
           title: Device Management Models
   ```

2. **Center Column (Content)**
   - Displays the main documentation content
   - Content is pulled from Markdown files
   - Rendering is controlled by `structure.json`

3. **Right Column (Section Navigation)**
   - Automatically generated from headings in Markdown files
   - Provides quick navigation within the current document

## Configuration Files

### structure.json
Controls which Markdown files are rendered and their organization:
```json
{
  "Architecture": [
    "authentication.md",
    "device-management.md",
    "network-topologies.md"
  ],
  "API": [
    "authentication.md",
    "endpoints.md"
  ]
}
```

### Navigation YML Files
Define the left sidebar structure and document hierarchy:
- `api-tree.yml`: API documentation structure
- `architecture-tree.yml`: Architecture documentation structure

## Content Organization

### Documentation Categories
- Architecture
- API
- Networking
- Security
- Data
- Deployment

### Markdown Files
- Each documentation page is written in Markdown
- Files should include proper headings for right-column navigation
- Example structure:
```markdown
# Main Topic
## Subtopic 1
### Detailed Point
## Subtopic 2
```

## Contributing

### Adding New Documentation
1. Create the Markdown file in the appropriate directory
2. Update `structure.json` to include the new file
3. Add the navigation entry in the corresponding tree YML file
4. Ensure proper heading structure for right-column navigation

### Style Guidelines
- Use consistent heading levels
- Include introduction paragraphs
- Add code examples where appropriate
- Use proper Markdown formatting

## Local Development

1. Clone the repository
2. Install dependencies
3. Run the documentation server locally
4. Preview changes in the three-column layout

## Links

- Live Documentation: [iotCommunity.space/docs](https://iotCommunity.space/docs)
- About Page: [Project Information](https://iotCommunity.space/about)

## Support

For questions or issues:
- Open an issue in the repository
- Contact the documentation team
- Visit the community forums
