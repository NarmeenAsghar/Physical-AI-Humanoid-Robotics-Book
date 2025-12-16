<!--
SYNC IMPACT REPORT
==================
Version change: 0.0.0 → 1.0.0
Bump rationale: MAJOR - Initial constitution creation with full principle set

Modified principles: N/A (initial creation)

Added sections:
- Core Principles (5 principles: Accuracy, Clarity, Reproducibility, Rigor, Spec-First Workflow)
- Key Standards (citation, source composition, code, diagrams, plagiarism, style)
- Constraints (word count, sources, structure, formats)
- Success Criteria (validation, plagiarism, review, build, deployment, traceability)
- Tools & Workflow (Spec-Kit Plus, Claude Code, Qwen, Docusaurus)
- Governance (amendment procedure, versioning, compliance)

Removed sections: N/A (initial creation)

Templates requiring updates:
- .specify/templates/plan-template.md: ✅ Compatible (Constitution Check section exists)
- .specify/templates/spec-template.md: ✅ Compatible (requirements structure aligns)
- .specify/templates/tasks-template.md: ✅ Compatible (phase structure supports book chapters)

Follow-up TODOs: None
==================
-->

# Physical AI & Humanoid Robotics Book Constitution

## Core Principles

### I. Accuracy

All technical content MUST be grounded in primary sources from robotics, artificial intelligence, biomechanics, and control theory disciplines.

**Requirements**:
- Every factual claim MUST reference a traceable scientific or engineering source
- Equations, algorithms, and system architectures MUST match established conventions in the field
- No speculative or unverified technical claims permitted
- Cross-reference multiple authoritative sources when possible

**Rationale**: A technical book serves as a reference; inaccurate information propagates errors through student work and industry applications.

### II. Clarity

Content MUST be accessible to engineering, computer science, and robotics students at intermediate-to-advanced levels.

**Requirements**:
- Target Flesch-Kincaid grade level: 10–12 (technical but readable)
- Complex concepts MUST include explanatory context before formal definitions
- Notation and terminology MUST remain consistent throughout the manuscript
- Jargon MUST be defined on first use

**Rationale**: The book bridges academic rigor and practical understanding; clarity ensures knowledge transfer without sacrificing precision.

### III. Reproducibility

All technical claims, equations, algorithms, and system architectures MUST be reproducible by readers.

**Requirements**:
- Code examples MUST be verifiable and runnable (Python, ROS2, Unity, or simulation environment)
- Mathematical derivations MUST show intermediate steps sufficient for verification
- System diagrams MUST include enough detail for independent implementation
- External dependencies MUST be explicitly documented with versions

**Rationale**: Reproducibility is the foundation of scientific communication; readers must be able to verify and build upon presented work.

### IV. Rigor

Content MUST be cross-verified with peer-reviewed research, IEEE/ACM papers, and authoritative robotics textbooks.

**Requirements**:
- Source composition: minimum 50% peer-reviewed publications (IEEE, ACM, Springer, Nature, Science Robotics)
- Citation format: APA 7th edition
- Minimum 25 academically verified sources across the manuscript
- Claims conflicting with established literature MUST acknowledge and justify the divergence

**Rationale**: Academic rigor ensures the book can be used as a reliable reference in educational and professional contexts.

### V. Spec-First Workflow

All content generation MUST follow the Spec-Driven Development workflow using Spec-Kit Plus, Claude Code, and supporting tools.

**Requirements**:
- Every chapter MUST have a corresponding specification in `specs/<chapter>/spec.md`
- Changes MUST flow through the `/sp.*` command workflow
- All outputs MUST be traceable to specification files
- PHRs (Prompt History Records) MUST document significant generation sessions

**Rationale**: Spec-first workflow ensures consistency, traceability, and quality control across distributed content generation.

## Key Standards

### Citation & Source Standards

| Standard | Requirement |
|----------|-------------|
| Citation format | APA 7th edition |
| Peer-reviewed minimum | 50% of all sources |
| Total verified sources | ≥ 25 across manuscript |
| Acceptable peer-reviewed venues | IEEE, ACM, Springer, Nature, Science Robotics |

### Code & Technical Standards

| Standard | Requirement |
|----------|-------------|
| Code verifiability | All examples MUST be runnable |
| Supported environments | Python, ROS2, Unity, simulation environments |
| Diagrams & formulas | MUST match standard robotics conventions |
| Kinematic notation | Follow Denavit-Hartenberg or equivalent established convention |

### Quality Standards

| Standard | Requirement |
|----------|-------------|
| Plagiarism tolerance | 0% prior to merge |
| Readability | Flesch-Kincaid grade 10–12 |
| Notation consistency | Single convention per concept type |

## Constraints

### Scope Constraints

| Constraint | Value |
|------------|-------|
| Target word count | 10,000–15,000 words (full book) |
| Minimum verified sources | 25 |

### Technical Constraints

| Constraint | Requirement |
|------------|-------------|
| Primary format | Docusaurus (Markdown → sidebar → build → GitHub Pages) |
| Output formats | Docusaurus website (live), PDF with embedded references, optional EPUB |
| Structure | All chapters via Spec-Kit Plus specifications |

## Success Criteria

### Content Validation

- [ ] Every claim and equation validated against authoritative robotics sources
- [ ] Zero plagiarism detected across entire manuscript
- [ ] Passes expert review in AI, control systems, and humanoid robotics

### Technical Validation

- [ ] Book builds successfully in Docusaurus with clean sidebar structure
- [ ] GitHub Pages deployment functional with versioned documentation
- [ ] All `/sp.*` specification files followed and traceable

### Workflow Validation

- [ ] All chapters have corresponding `specs/<chapter>/spec.md` files
- [ ] PHRs document generation sessions
- [ ] ADRs capture significant architectural decisions

## Tools & Workflow

### Primary Tools

| Tool | Purpose |
|------|---------|
| **Spec-Kit Plus** | Create and maintain specifications for each chapter |
| **Claude Code** | Generate, refine, and test technical content |
| **Qwen/Other LLMs** | Assist with computational, simulation, and control examples |
| **Docusaurus** | Host and publish the book as a static site |

### Workflow Sequence

1. **Specify** (`/sp.specify`): Create chapter specification
2. **Plan** (`/sp.plan`): Design chapter architecture and content outline
3. **Tasks** (`/sp.tasks`): Break down into implementable content tasks
4. **Implement** (`/sp.implement`): Generate and refine content
5. **Review**: Validate against constitution principles
6. **Build**: Docusaurus build and deployment

## Governance

### Amendment Procedure

1. Proposed amendments MUST be documented with rationale
2. Amendments affecting core principles require explicit approval
3. All amendments MUST update the version number per semantic versioning
4. Sync Impact Report MUST be generated for each amendment

### Versioning Policy

- **MAJOR**: Backward-incompatible principle changes or removals
- **MINOR**: New principles, sections, or materially expanded guidance
- **PATCH**: Clarifications, wording improvements, typo fixes

### Compliance Review

- All PRs MUST verify compliance with constitution principles
- Content merges require plagiarism check (0% tolerance)
- Source verification required before technical content merge
- Build validation required before deployment

**Version**: 1.0.0 | **Ratified**: 2025-12-16 | **Last Amended**: 2025-12-16
