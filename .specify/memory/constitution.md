<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.1.0
- Modified principles: All principles updated for RAG Chatbot project
- Added sections: RAG-specific principles and content standards
- Removed sections: Physical AI Humanoid Robotics specific content
- Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ✅ reviewed
- Follow-up TODOs: None
-->

# Integrated RAG Chatbot for a Published Book Constitution

## Core Principles

### I. Content Grounding (NON-NEGOTIABLE)
All responses must be strictly grounded in the published book's content with zero hallucination tolerance. Responses generated only from retrieved text with source references included in every answer. Accuracy and source attribution are prioritized over response fluency.

### II. Retrieval-First Architecture
The system must prioritize retrieval from the book's content before generating any response. All responses follow retrieval → validation → generation flow. The RAG pipeline ensures every answer can be traced back to specific source passages.

### III. Transparency and Traceability
All responses must be transparent about their source origins and provide clear traceability to the book content. Every answer includes source references and context snippets. Users must be able to verify and locate the information in the original book.

### IV. AI-Assisted Development
Leverage Claude Code and Spec-Kit Plus for all development tasks to ensure consistency and quality. All AI-generated content must be validated by human reviewers for technical accuracy. Maintain transparency about AI tool usage in development process.

### V. Full-Book and Selective Q&A Support
The system must support both full-book Q&A and user-selected-text Q&A modes. Users can query the entire book or specific sections/chapters. The system maintains flexibility to work with different scopes of book content.

### VI. Stack-Driven Implementation
Implementation must leverage the specified technology stack: OpenAI Agents/ChatKit, FastAPI, Qdrant, Neon Postgres. All components must integrate seamlessly within this stack for optimal performance and cost efficiency.

## Content Standards
<!-- RAG system content requirements -->

All content must include relevant source references and context snippets in every response. Content follows accessibility standards to ensure usability for readers with diverse needs. All external dependencies and libraries must be clearly documented with version requirements. The system must maintain strict content boundaries, never incorporating external knowledge beyond the specified book content.

## Development Workflow
<!-- Process and quality requirements -->

All changes must pass content accuracy review by domain experts before merging. Code examples must be tested with the specified book content to verify proper RAG functionality. All content changes require specification updates and must reference the Integrated RAG Chatbot for a Published Book project goals. Each implementation must validate retrieval relevance and maintain zero-hallucination behavior.

## Governance

This constitution governs all development and content creation for the Integrated RAG Chatbot for a Published Book project. All pull requests and reviews must verify compliance with these principles. Any conflicts between this constitution and other practices are resolved in favor of these principles. All team members must acknowledge and adhere to these principles during project participation. The system must maintain free-tier friendly infrastructure while ensuring low-latency, in-book interaction.

**Version**: 1.1.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-07