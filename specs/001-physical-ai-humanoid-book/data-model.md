# Data Model: Physical AI & Humanoid Robotics Book

**Feature**: `001-physical-ai-humanoid-book`
**Date**: 2025-12-16
**Phase**: 1 (Design)

## Overview

This document defines the content entities, their attributes, relationships, and validation rules for the Physical AI & Humanoid Robotics technical book.

## Core Entities

### 1. Book

The top-level container for all content.

| Attribute | Type | Validation | Description |
|-----------|------|------------|-------------|
| title | string | Required, max 100 chars | Book title |
| tagline | string | Required, max 200 chars | Short description |
| version | semver | Required, format X.Y.Z | Book version |
| wordCount | integer | 10,000-15,000 | Total word count |
| citationCount | integer | ≥ 25 | Total citations |
| peerReviewedRatio | float | ≥ 0.50 | % peer-reviewed citations |
| fleschKincaid | float | 10.0-12.0 | Readability score |
| modules | Module[] | 5 required | Child modules |
| appendices | Appendix[] | ≥ 1 | Reference materials |

**Relationships**:
- Book → has many → Modules
- Book → has many → Appendices
- Book → has one → Bibliography

---

### 2. Module

A major section of the book covering a coherent topic area.

| Attribute | Type | Validation | Description |
|-----------|------|------------|-------------|
| id | string | Required, unique | Module identifier (e.g., "module-1-ros2") |
| title | string | Required, max 80 chars | Module title |
| priority | integer | 1-5, unique | Implementation priority |
| wordTarget | range | 2000-3500 | Target word count |
| sections | Section[] | ≥ 3 | Child sections |
| diagrams | Diagram[] | ≥ 2 | Required diagrams |
| codeExamples | CodeExample[] | ≥ 2 | Required code examples |
| prerequisites | Module[] | Optional | Dependent modules |

**Relationships**:
- Module → belongs to → Book
- Module → has many → Sections
- Module → has many → Diagrams
- Module → has many → CodeExamples
- Module → may depend on → other Modules

**Defined Modules**:

| ID | Title | Priority | Prerequisites |
|----|-------|----------|---------------|
| module-1-ros2 | ROS 2: The Robotic Nervous System | P1 | None |
| module-2-digital-twin | Digital Twin: Gazebo + Unity | P2 | module-1-ros2 |
| module-3-isaac | NVIDIA Isaac: The AI-Robot Brain | P3 | module-1-ros2, module-2-digital-twin |
| module-4-vla | Vision-Language-Action | P4 | module-1-ros2, module-3-isaac |
| capstone | The Autonomous Humanoid | P5 | All previous |

---

### 3. Section

A chapter or subsection within a module.

| Attribute | Type | Validation | Description |
|-----------|------|------------|-------------|
| id | string | Required, unique within module | Section identifier |
| title | string | Required, max 60 chars | Section title |
| wordTarget | integer | 100-600 | Target word count |
| content | markdown | Required | Section content |
| learningObjectives | string[] | ≥ 1 | What reader will learn |
| keyTerms | Term[] | Optional | Terms defined in section |

**Relationships**:
- Section → belongs to → Module
- Section → may contain → Terms
- Section → may contain → CodeExamples (inline)

---

### 4. CodeExample

A runnable code snippet with documentation.

| Attribute | Type | Validation | Description |
|-----------|------|------------|-------------|
| id | string | Required, unique | Example identifier |
| filename | string | Required, valid filename | File name with extension |
| language | enum | python/xml/yaml/sdf/bash | Programming language |
| code | string | Required, valid syntax | The code content |
| description | string | Required | What the code does |
| expectedOutput | string | Optional | Expected result when run |
| dependencies | string[] | Required | Required packages/setup |
| platform | enum | ubuntu-22.04 | Target platform |
| ros2Version | enum | humble/iron | ROS 2 version |

**Relationships**:
- CodeExample → belongs to → Module or Section
- CodeExample → may reference → other CodeExamples

**Validation Rules**:
- Python code must be PEP 8 compliant
- URDF/SDF must pass schema validation
- All dependencies must be documented

---

### 5. Diagram

A visual representation of concepts or architecture.

| Attribute | Type | Validation | Description |
|-----------|------|------------|-------------|
| id | string | Required, unique | Diagram identifier |
| title | string | Required, max 60 chars | Diagram title |
| type | enum | system/dataflow/state/tree | Diagram type |
| format | enum | svg/png/mermaid | File format |
| altText | string | Required | Accessibility description |
| source | string | Optional | Source file (if editable) |

**Relationships**:
- Diagram → belongs to → Module
- Diagram → may illustrate → Sections

**Required Diagrams by Module**:

| Module | Diagram | Type |
|--------|---------|------|
| 1 | ROS 2 Architecture | system |
| 1 | Humanoid Node Graph | dataflow |
| 1 | URDF Link Hierarchy | tree |
| 2 | Gazebo Architecture | system |
| 2 | Sensor Data Pipeline | dataflow |
| 2 | Digital Twin Architecture | system |
| 3 | Isaac Ecosystem | system |
| 3 | Perception Pipeline | dataflow |
| 3 | Nav2 Integration | system |
| 4 | VLA Architecture | system |
| 4 | Speech-to-Action Pipeline | dataflow |
| Capstone | Complete System Architecture | system |
| Capstone | Task Execution State Machine | state |

---

### 6. Citation

An academic reference in APA 7 format.

| Attribute | Type | Validation | Description |
|-----------|------|------------|-------------|
| id | string | Required, unique | Citation key (e.g., "spong2020") |
| type | enum | book/article/conference/web/report | Source type |
| authors | Author[] | Required for most types | Author list |
| year | integer | Required, 1900-2025 | Publication year |
| title | string | Required | Work title |
| source | string | Required | Journal/Publisher/URL |
| doi | string | Optional | Digital Object Identifier |
| url | string | Optional | Access URL |
| isPeerReviewed | boolean | Required | Is source peer-reviewed? |

**Relationships**:
- Citation → referenced by → Sections
- Citation → belongs to → Bibliography

**Validation Rules**:
- APA 7 format must be followed
- DOI preferred when available
- URL required for web sources
- At least 50% must have isPeerReviewed = true

---

### 7. Term

A technical term with definition.

| Attribute | Type | Validation | Description |
|-----------|------|------------|-------------|
| term | string | Required, unique | The term |
| definition | string | Required, 20-200 chars | Clear definition |
| firstUsedIn | Section | Required | Where term first appears |
| relatedTerms | Term[] | Optional | Related concepts |

**Relationships**:
- Term → defined in → Section
- Term → may relate to → other Terms

---

### 8. Appendix

Supplementary reference material.

| Attribute | Type | Validation | Description |
|-----------|------|------------|-------------|
| id | string | Required, unique | Appendix identifier |
| title | string | Required | Appendix title |
| type | enum | installation/hardware/bibliography | Content type |
| content | markdown | Required | Appendix content |

**Relationships**:
- Appendix → belongs to → Book

**Required Appendices**:
- installation: Software setup guide
- hardware-requirements: System requirements
- references: Bibliography (APA 7)

---

## State Transitions

### Module Lifecycle

```
DRAFT → IN_REVIEW → APPROVED → PUBLISHED
  ↑         │           │
  └─────────┴───────────┘ (revision required)
```

| State | Description | Exit Criteria |
|-------|-------------|---------------|
| DRAFT | Initial content creation | Word count met, all code tested |
| IN_REVIEW | Quality validation | Constitution check passed |
| APPROVED | Ready for publication | Expert review completed |
| PUBLISHED | Live on GitHub Pages | Build successful |

### Content Validation Pipeline

```
Content Created
      ↓
Word Count Check → FAIL → Revise
      ↓ PASS
Citation Check → FAIL → Add Sources
      ↓ PASS
Code Execution Test → FAIL → Fix Code
      ↓ PASS
Readability Check → FAIL → Simplify
      ↓ PASS
Plagiarism Check → FAIL → Rewrite
      ↓ PASS
Expert Review → FAIL → Address Feedback
      ↓ PASS
Ready for Publication
```

---

## Entity Relationship Diagram (Textual)

```
Book (1) ─────────────── has many ──────────────→ (N) Module
  │                                                    │
  │                                                    │
  └── has many → Appendix                              ├── has many → Section
                                                       │       │
                                                       │       └── contains → Term
                                                       │
                                                       ├── has many → Diagram
                                                       │
                                                       ├── has many → CodeExample
                                                       │
                                                       └── depends on → Module (optional)

Book (1) ─────────────── has one ───────────────→ (1) Bibliography
                                                       │
                                                       └── contains → Citation (N)
```

---

## Constraints Summary

| Constraint | Value | Enforced By |
|------------|-------|-------------|
| Total word count | 10,000-15,000 | Build validation |
| Total citations | ≥ 25 | Bibliography check |
| Peer-reviewed ratio | ≥ 50% | Citation validation |
| Module count | 5 | Spec requirement |
| Code examples per module | ≥ 2 | Module spec |
| Diagrams per module | ≥ 2 | Module spec |
| Flesch-Kincaid grade | 10-12 | Readability tool |
| Plagiarism | 0% | Plagiarism checker |
