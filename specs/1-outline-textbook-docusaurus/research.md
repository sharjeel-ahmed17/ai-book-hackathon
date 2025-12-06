# Research: Physical AI Humanoid Robotics Textbook and Docusaurus Setup

## Decision: Docusaurus Version and Configuration
**Rationale**: Using Docusaurus 3.x with modern plugin architecture to support educational content requirements, including code examples, diagrams, and responsive design for learning.

## Decision: Textbook Structure Organization
**Rationale**: Organizing content by the 13-week curriculum structure with clear sections for each topic area. Each week's content will include theoretical concepts, practical examples, and exercises.

## Decision: Platform Setup Documentation Approach
**Rationale**: Creating separate setup guides for each platform option (Digital Twin workstation, Physical AI Edge Kit, cloud-native) with step-by-step instructions and troubleshooting sections.

## Alternatives Considered:

### For Documentation Platform:
- GitBook: Less customizable than Docusaurus
- Hugo: More complex setup for educational content
- MkDocs: Good but Docusaurus has better support for technical documentation with code examples

### For Textbook Structure:
- Topic-based organization: Could work but the 13-week curriculum structure is already well-defined
- Skill progression approach: Would require restructuring the existing curriculum

### For Platform Documentation:
- Single unified guide: Would be too complex with conditional steps
- Separate repositories: Would fragment the learning experience

## Technical Research Findings:

### Docusaurus Features for Educational Content:
- Code blocks with syntax highlighting for Python, ROS 2, and Isaac Sim examples
- Math support for technical concepts
- Diagram integration for architecture and workflows
- Search functionality for easy navigation
- Mobile-responsive design for flexible learning

### GitHub Pages Deployment:
- Static site generation with fast loading
- Version control integration
- Custom domain support
- Automatic deployment from main branch

### Curriculum Integration:
- Navigation structure following the 13-week progression
- Cross-references between related topics
- Exercise and capstone project integration
- Platform-specific examples where relevant