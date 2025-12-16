# Contract: Citation Format (APA 7th Edition)

**Feature**: `001-physical-ai-humanoid-book`
**Date**: 2025-12-16
**Type**: Citation Format Contract

## Purpose

Defines the APA 7th edition citation format for all references in the Physical AI & Humanoid Robotics book.

## In-Text Citations

### Single Author

```
(Spong, 2020)
Spong (2020) demonstrated that...
```

### Two Authors

```
(Thrun & Burgard, 2005)
Thrun and Burgard (2005) proposed...
```

### Three or More Authors

```
(Siciliano et al., 2010)
Siciliano et al. (2010) explained...
```

### Organization as Author

```
(Open Robotics, 2023)
NVIDIA (2023) released...
```

### Direct Quote

```
"Direct quote here" (Author, Year, p. X).
```

### Multiple Sources

```
(Author1, Year; Author2, Year)
```

## Reference List Formats

### Book

```
Author, A. A. (Year). Title of work: Capital letter also for subtitle. Publisher.

Example:
Spong, M. W., Hutchinson, S., & Vidyasagar, M. (2020). Robot modeling and control (2nd ed.). Wiley.
```

### Edited Book Chapter

```
Author, A. A. (Year). Title of chapter. In E. E. Editor (Ed.), Title of book (pp. xx-xx). Publisher.

Example:
Pratt, J. (2006). Virtual model control. In K. Kaneko (Ed.), Humanoid robots: Modeling and control (pp. 42-67). Springer.
```

### Journal Article

```
Author, A. A., & Author, B. B. (Year). Title of article. Title of Periodical, volume(issue), page–page. https://doi.org/xxxxx

Example:
Mur-Artal, R., & Tardós, J. D. (2017). ORB-SLAM2: An open-source SLAM system for monocular, stereo, and RGB-D cameras. IEEE Transactions on Robotics, 33(5), 1255-1262. https://doi.org/10.1109/TRO.2017.2705103
```

### Conference Paper

```
Author, A. A., & Author, B. B. (Year). Title of paper. In Proceedings of the Conference Name (pp. xx-xx). Publisher. https://doi.org/xxxxx

Example:
Koenig, N., & Howard, A. (2004). Design and use paradigms for Gazebo, an open-source multi-robot simulator. In Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems (pp. 2149-2154). IEEE. https://doi.org/10.1109/IROS.2004.1389727
```

### Technical Report

```
Author, A. A. (Year). Title of report (Report No. xxx). Organization.

Example:
Radford, A., Kim, J. W., Xu, T., Brockman, G., McLeavey, C., & Sutskever, I. (2022). Robust speech recognition via large-scale weak supervision (Technical Report). OpenAI.
```

### Website/Documentation

```
Author/Organization. (Year, Month Day). Title of page. Site Name. URL

Example:
Open Robotics. (2023). ROS 2 Humble documentation. ROS 2 Documentation. https://docs.ros.org/en/humble/
```

### Software/GitHub Repository

```
Author, A. A. (Year). Title of software (Version X.X) [Computer software]. Publisher/Repository. URL

Example:
Open Robotics. (2023). Gazebo Sim (Version 8.0) [Computer software]. GitHub. https://github.com/gazebosim/gz-sim
```

### arXiv Preprint

```
Author, A. A. (Year). Title of article. arXiv. https://arxiv.org/abs/XXXX.XXXXX

Example:
Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., ... & Zitkovich, B. (2022). RT-1: Robotics transformer for real-world control at scale. arXiv. https://arxiv.org/abs/2212.06817
```

## Reference List Organization

References must be:
1. Alphabetized by first author's surname
2. Hanging indent (first line flush left, subsequent indented)
3. Double-spaced (in final document)
4. Include DOI when available (as hyperlink)

## Required Citation Categories

| Category | Minimum | Peer-Reviewed |
|----------|---------|---------------|
| Peer-reviewed journals | 8 | Yes |
| Conference proceedings | 5 | Yes |
| Textbooks | 4 | N/A |
| Technical reports | 3 | Varies |
| Official documentation | 5 | No |
| **Total** | **25+** | **≥50%** |

## Citation Validation Rules

1. **DOI Required**: Include DOI for all journal/conference papers when available
2. **Access Date**: Include for web content that may change
3. **Version**: Include version numbers for software citations
4. **No Wikipedia**: Do not cite Wikipedia; find primary sources
5. **Recency**: Prefer sources from last 10 years unless foundational
6. **Authority**: Prioritize peer-reviewed venues (IEEE, ACM, Springer)

## Bibliography File Format

Store in `docs/appendices/references.md`:

```markdown
---
sidebar_position: 99
title: References
---

# References

## A

Brohan, A., Brown, N., Carbajal, J., ... (2022). RT-1: Robotics transformer...

## C

Craig, J. J. (2005). Introduction to robotics: Mechanics and control...

[Continue alphabetically]
```

## Linking Citations

In chapter content, link to bibliography:

```markdown
ROS 2 uses a publish-subscribe pattern (Quigley et al., 2009)[^quigley2009].

[^quigley2009]: See [References](/appendices/references#quigley2009)
```

## Example Bibliography Entry Set

```markdown
Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., ... & Zitkovich, B. (2022). RT-1: Robotics transformer for real-world control at scale. *arXiv*. https://arxiv.org/abs/2212.06817

Craig, J. J. (2005). *Introduction to robotics: Mechanics and control* (3rd ed.). Pearson.

Koenig, N., & Howard, A. (2004). Design and use paradigms for Gazebo, an open-source multi-robot simulator. In *Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems* (pp. 2149-2154). IEEE. https://doi.org/10.1109/IROS.2004.1389727

Macenski, S., Foote, T., Gerkey, B., Lalancette, C., & Woodall, W. (2022). Robot Operating System 2: Design, architecture, and uses in the wild. *Science Robotics*, 7(66), eabm6074. https://doi.org/10.1126/scirobotics.abm6074

Mur-Artal, R., & Tardós, J. D. (2017). ORB-SLAM2: An open-source SLAM system for monocular, stereo, and RGB-D cameras. *IEEE Transactions on Robotics*, 33(5), 1255-1262. https://doi.org/10.1109/TRO.2017.2705103

NVIDIA. (2023). *Isaac Sim documentation*. NVIDIA Developer. https://developer.nvidia.com/isaac-sim

Open Robotics. (2023). *ROS 2 Humble documentation*. https://docs.ros.org/en/humble/

Quigley, M., Conley, K., Gerkey, B., Faust, J., Foote, T., Leibs, J., ... & Ng, A. Y. (2009). ROS: An open-source robot operating system. In *ICRA Workshop on Open Source Software* (Vol. 3, No. 3.2, p. 5).

Radford, A., Kim, J. W., Xu, T., Brockman, G., McLeavey, C., & Sutskever, I. (2022). *Robust speech recognition via large-scale weak supervision* (Technical Report). OpenAI.

Siciliano, B., Sciavicco, L., Villani, L., & Oriolo, G. (2010). *Robotics: Modelling, planning and control*. Springer.

Spong, M. W., Hutchinson, S., & Vidyasagar, M. (2020). *Robot modeling and control* (2nd ed.). Wiley.

Thrun, S., Burgard, W., & Fox, D. (2005). *Probabilistic robotics*. MIT Press.
```
