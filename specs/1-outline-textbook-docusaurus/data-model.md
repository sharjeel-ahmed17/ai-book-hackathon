# Data Model: Physical AI Humanoid Robotics Textbook

## Entities

### TextbookSection
- **name**: String (required) - The name of the section (e.g., "Foundations of Physical AI")
- **description**: String (required) - Brief description of the section content
- **weeks**: Range (required) - The weeks covered by this section (e.g., 1-2 for Foundations)
- **learningObjectives**: Array<String> (required) - List of learning objectives for this section
- **prerequisites**: Array<String> (optional) - Prerequisites needed before this section
- **contentFiles**: Array<String> (required) - List of content files in this section
- **exercises**: Array<Exercise> (optional) - Exercises associated with this section

### Exercise
- **title**: String (required) - Title of the exercise
- **description**: String (required) - Detailed description of the exercise
- **difficulty**: Enum (required) - Difficulty level (beginner, intermediate, advanced)
- **estimatedTime**: Number (required) - Estimated time to complete in minutes
- **requirements**: Array<String> (required) - Technical requirements for the exercise
- **solution**: String (optional) - Solution or guidance for the exercise

### PlatformSetupGuide
- **name**: String (required) - Name of the platform (Digital Twin workstation, Physical AI Edge Kit, cloud-native)
- **description**: String (required) - Brief description of the platform
- **prerequisites**: Array<String> (required) - Prerequisites for setting up this platform
- **steps**: Array<String> (required) - Step-by-step setup instructions
- **troubleshooting**: Array<String> (optional) - Common issues and solutions
- **validationSteps**: Array<String> (required) - Steps to verify successful setup

### LearningModule
- **title**: String (required) - Title of the learning module
- **section**: TextbookSection (required) - Reference to the parent section
- **content**: String (required) - Main content of the module
- **examples**: Array<String> (optional) - Code examples or practical examples
- **resources**: Array<String> (optional) - Additional resources for the module
- **duration**: Number (required) - Estimated duration in minutes

### CapstoneProject
- **title**: String (required) - Title of the capstone project
- **description**: String (required) - Detailed description of the project
- **requirements**: Array<String> (required) - Technical and knowledge requirements
- **components**: Array<String> (required) - Components of the project (speech → planning → navigation → perception → manipulation)
- **evaluationCriteria**: Array<String> (required) - Criteria for evaluating the project
- **resources**: Array<String> (optional) - Additional resources for the project

## Relationships

- TextbookSection contains multiple LearningModule
- TextbookSection may contain multiple Exercise
- LearningModule may reference multiple PlatformSetupGuide (for platform-specific examples)
- CapstoneProject may span multiple TextbookSection (integrating concepts from different sections)
- PlatformSetupGuide may be referenced by multiple LearningModule

## Validation Rules

- TextbookSection.name must be unique within the textbook
- TextbookSection.weeks must not overlap with other sections
- Exercise.difficulty must be one of: beginner, intermediate, advanced
- LearningModule.duration must be positive
- PlatformSetupGuide.name must be one of: "Digital Twin workstation", "Physical AI Edge Kit", "cloud-native"