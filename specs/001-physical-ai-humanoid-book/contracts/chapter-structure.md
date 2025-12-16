# Contract: Chapter Structure

**Feature**: `001-physical-ai-humanoid-book`
**Date**: 2025-12-16
**Type**: Content Format Contract

## Purpose

Defines the standard structure for all chapters/sections in the Physical AI & Humanoid Robotics book to ensure consistency across modules.

## Chapter Template

```markdown
---
sidebar_position: [N]
title: [Chapter Title]
description: [One-line description for SEO]
---

# [Chapter Title]

[Opening paragraph: 2-3 sentences introducing the topic and its relevance to Physical AI]

## Learning Objectives

By the end of this chapter, you will be able to:

- [Objective 1: Action verb + specific outcome]
- [Objective 2: Action verb + specific outcome]
- [Objective 3: Action verb + specific outcome]

## Prerequisites

- [Prerequisite 1: What reader should know/have]
- [Prerequisite 2: What reader should know/have]

---

## [Section 1 Title]

[Section content: explanatory prose, concepts, theory]

### [Subsection if needed]

[More detailed content]

> **Key Concept**: [Important concept highlighted in blockquote]

---

## [Section 2 Title]

[Section content]

### Code Example: [Example Name]

[Brief explanation of what the code does]

```python
# filename: example_name.py
# Description: [what this code demonstrates]

[code content]
```

**Expected Output:**
```
[expected terminal output]
```

**Troubleshooting:**
- If you see [error], try [solution]

---

## [Section N Title]

[Continue pattern...]

---

## Hands-On Exercise

### Exercise [N]: [Exercise Title]

**Objective**: [What reader will accomplish]

**Steps**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Validation**: [How reader knows they succeeded]

---

## Summary

- [Key point 1]
- [Key point 2]
- [Key point 3]

## What's Next

In the next chapter, we will [preview of next topic].

---

## References

[Citations in APA 7 format, linked to bibliography]

- [Author, Year](#ref-id) - [Brief description of relevance]
```

## Required Elements

| Element | Required | Notes |
|---------|----------|-------|
| Frontmatter | Yes | Docusaurus metadata |
| Learning Objectives | Yes | 2-4 objectives per chapter |
| Prerequisites | Yes | Link to prior chapters |
| Key Concepts | Yes | Highlighted in blockquotes |
| Code Examples | Yes (if technical) | With filename, description, output |
| Hands-On Exercise | Yes | At least 1 per chapter |
| Summary | Yes | 3-5 bullet points |
| What's Next | Yes | Narrative connection |
| References | Yes | APA 7 format |

## Formatting Rules

### Headers

- H1 (`#`): Chapter title only (once per page)
- H2 (`##`): Major sections
- H3 (`###`): Subsections, code examples
- H4+ (`####`): Avoid, restructure instead

### Code Blocks

- Always specify language: ` ```python `
- Include filename comment at top
- Show expected output separately
- Provide troubleshooting tips

### Admonitions (Docusaurus)

```markdown
:::tip Tip Title
Helpful tip content
:::

:::warning Warning Title
Important warning content
:::

:::info Note
Additional information
:::

:::danger Danger
Critical warning content
:::
```

### Images/Diagrams

```markdown
![Alt text describing the diagram](./assets/diagrams/diagram-name.svg)

*Figure N: Caption describing the diagram*
```

### Citations

Inline: `(Author, Year)` or `Author (Year)`
Reference list: Full APA 7 entry

## Word Count Guidelines

| Chapter Type | Target Words | Sections |
|--------------|--------------|----------|
| Introduction | 500-800 | 3-4 |
| Standard Chapter | 400-600 | 4-6 |
| Deep Dive | 600-800 | 5-7 |
| Capstone | 500-700 | 4-6 |

## Validation Checklist

Before submitting a chapter:

- [ ] Frontmatter complete with correct sidebar_position
- [ ] Learning objectives are measurable (action verbs)
- [ ] All code examples tested on Ubuntu 22.04 + ROS 2 Humble
- [ ] All images have alt text
- [ ] Citations in APA 7 format
- [ ] Word count within target range
- [ ] Flesch-Kincaid grade 10-12
- [ ] No broken links
- [ ] Hands-on exercise included
- [ ] Summary captures key points
