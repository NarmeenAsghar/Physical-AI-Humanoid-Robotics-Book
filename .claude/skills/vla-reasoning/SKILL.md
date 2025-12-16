# Skill: vla-reasoning

## Purpose

Teach Vision-Language-Action (VLA) model concepts for humanoid robotics, emphasizing multimodal reasoning and perception-to-action pipelines. This skill focuses on conceptual understanding of how robots interpret visual scenes, process natural language instructions, and generate appropriate physical actions. The approach prioritizes intuition and architectural understanding over implementation details.

## Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `concept` | string | Yes | VLA concept to explain (e.g., "multimodal fusion", "action tokenization", "grounding") |
| `focus` | string | No | Emphasis area: `perception`, `language`, `action`, `integration`. Default: `integration` |
| `depth` | string | No | Conceptual depth: `overview`, `detailed`, `comparative`. Default: `detailed` |
| `output_format` | string | No | Format: `explanation`, `diagram`, `analogy`, `case_study`. Default: `explanation` |
| `prior_knowledge` | string | No | Assumed background: `ml_basics`, `robotics_basics`, `both`, `minimal`. Default: `robotics_basics` |

## Outputs

| Output | Description |
|--------|-------------|
| Conceptual explanations | Clear descriptions of VLA components and their interactions |
| Architecture diagrams | Text-based representations of model structure and data flow |
| Analogies | Intuitive comparisons to familiar systems for complex concepts |
| Case studies | Concrete scenarios showing VLA reasoning in humanoid contexts |
| Reasoning traces | Step-by-step breakdowns of how VLA models process inputs to outputs |
| Comparison tables | Side-by-side analysis of approaches, architectures, or design choices |

## Boundaries

### In Scope

- VLA model architecture concepts (encoders, fusion mechanisms, decoders)
- Vision processing: object detection, scene understanding, spatial reasoning
- Language understanding: instruction parsing, intent extraction, grounding
- Action representation: discrete tokens, continuous trajectories, primitives
- Multimodal fusion strategies: early, late, cross-attention
- Perception-action loops and feedback mechanisms
- Embodiment and its role in grounded reasoning
- Sim-to-real considerations for learned policies
- Emergent capabilities in large multimodal models
- Safety and alignment in embodied AI systems

### Out of Scope

- Model training procedures and hyperparameter tuning
- Specific framework implementations (PyTorch, JAX details)
- Dataset curation and annotation pipelines
- GPU cluster setup and distributed training
- Model compression and deployment optimization
- Specific proprietary model architectures (internal details of RT-2, PaLM-E)
- Mathematical derivations of attention mechanisms
- Benchmark reproduction and evaluation scripts

## Linked Documentation Paths

Content aligns with the following structure:

```
docs/module-4-vla/
├── index.md                           # Module overview and learning objectives
├── 01-introduction-to-vla.md          # What are VLA models, why they matter
├── 02-vision-foundations.md           # Visual encoders and representations
├── 03-language-foundations.md         # Language models in robotics context
├── 04-action-representations.md       # How robots encode actions
├── 05-multimodal-fusion.md            # Combining vision and language
├── 06-grounding.md                    # Connecting words to world state
├── 07-perception-action-loop.md       # Closed-loop reasoning and control
├── 08-spatial-reasoning.md            # Understanding 3D space from 2D inputs
├── 09-temporal-reasoning.md           # Sequences, planning, and prediction
├── 10-instruction-following.md        # From commands to behaviors
├── 11-emergent-capabilities.md        # What large scale enables
├── 12-embodiment-matters.md           # Why physical form shapes reasoning
├── 13-sim-to-real-transfer.md         # Bridging simulated and real perception
├── 14-safety-alignment.md             # Ensuring safe embodied behavior
├── 15-humanoid-applications.md        # VLA for bipedal robots specifically
└── case-studies/
    ├── case-study-01-pick-place.md    # Object manipulation reasoning
    ├── case-study-02-navigation.md    # Spatial instruction following
    ├── case-study-03-tool-use.md      # Inferring affordances
    └── case-study-04-social.md        # Human-robot interaction
```

## Core Concepts Reference

### The VLA Triad

```
┌─────────────────────────────────────────────────────────────┐
│                     VLA Model Architecture                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────┐    ┌──────────┐    ┌─────────┐              │
│   │ VISION  │    │ LANGUAGE │    │ ACTION  │              │
│   │         │    │          │    │         │              │
│   │ Camera  │    │ "Pick up │    │ Joint   │              │
│   │ frames  │───▶│ the red  │───▶│ targets │              │
│   │ → scene │    │ cup"     │    │ or      │              │
│   │ features│    │ → intent │    │ motion  │              │
│   └─────────┘    └──────────┘    └─────────┘              │
│        │              │              ▲                      │
│        └──────────────┴──────────────┘                      │
│                Multimodal Fusion                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Perception-Action Loop

```
Environment ──────┐
      ▲           │
      │           ▼
   Action    ┌─────────┐
   Execute   │ Observe │ (Vision)
      ▲      └────┬────┘
      │           │
      │           ▼
┌─────┴────┐ ┌─────────┐
│ Actuate  │ │ Fuse    │ (Vision + Language)
└─────┬────┘ └────┬────┘
      ▲           │
      │           ▼
      │      ┌─────────┐
      └──────│ Reason  │ (Select Action)
             └─────────┘
```

## Instructional Guidelines

1. **Intuition before formalism**: Use analogies and diagrams before technical definitions.
2. **Grounded examples**: Every concept illustrated with humanoid robot scenarios.
3. **Minimal code**: Prefer pseudocode or natural language algorithms over implementation.
4. **Highlight tradeoffs**: Present design choices with their consequences.
5. **Connect to embodiment**: Emphasize what makes VLA different from disembodied AI.
6. **Progressive complexity**: Build from single-modality to full multimodal integration.

## Example Usage

### Example 1: Explain multimodal fusion

**Input:**
```
concept: "multimodal fusion"
focus: "integration"
depth: "detailed"
output_format: "explanation"
```

**Output:**
```markdown
## Multimodal Fusion in VLA Models

### The Central Challenge

A humanoid robot receives a camera image showing a cluttered table and hears "Hand me the tool I need to fix this." The robot must:
1. Parse what "this" refers to (a loose screw visible in the image)
2. Infer which tool is appropriate (a screwdriver)
3. Locate that tool in the visual scene
4. Generate actions to grasp and hand it over

No single modality contains enough information. Fusion is how the model combines them.

### Fusion Strategies

#### Early Fusion
Combine raw inputs before any processing.

```
Image pixels + Text tokens → Shared Encoder → Unified Representation
```

**Analogy**: Like mixing ingredients before cooking. Everything becomes one blend.

**Tradeoff**:
- Enables deep interaction between modalities
- Requires aligned training data
- Loses modality-specific structure

#### Late Fusion
Process each modality independently, combine at decision time.

```
Image → Vision Encoder → Visual Features ──┐
                                           ├→ Combine → Decision
Text → Language Encoder → Text Features ───┘
```

**Analogy**: Like consulting two experts separately, then synthesizing their opinions.

**Tradeoff**:
- Preserves modality-specific representations
- Simpler to train incrementally
- May miss cross-modal patterns

#### Cross-Attention Fusion
Allow each modality to query the other during processing.

```
Visual tokens ←──────────────────────→ Language tokens
              cross-attend each layer
```

**Analogy**: Like two translators working together, constantly checking each other's interpretation.

**Tradeoff**:
- Rich bidirectional interaction
- Computationally expensive
- Current state-of-the-art for VLA

### Fusion in Action: "Get the red cup"

| Stage | Vision Processing | Language Processing | Fusion Event |
|-------|-------------------|---------------------|--------------|
| 1 | Detect objects: cup, mug, bottle | Parse: action=get, target=cup, color=red | — |
| 2 | Extract colors: red cup, blue mug | Ground "cup" to object class | Vision provides candidates |
| 3 | Locate red cup at (x, y, z) | Confirm "red" attribute match | Language filters vision |
| 4 | Estimate grasp pose | — | Vision informs action |

### Why Fusion Matters for Humanoids

Humanoids face complex, unstructured environments. Unlike industrial arms with fixed tasks:
- Objects are unnamed and must be inferred from context
- Instructions use pronouns, deixis, and implicit references
- Actions must adapt to spatial relationships described verbally

Effective fusion enables:
- **Disambiguation**: "The one on the left" requires vision to resolve
- **Inference**: "Something to write with" requires reasoning over affordances
- **Verification**: Checking that the grasped object matches the request

### Reference Documentation
- Detailed fusion architectures: docs/module-4-vla/05-multimodal-fusion.md
- Grounding mechanisms: docs/module-4-vla/06-grounding.md
```

### Example 2: Perception-action loop

**Input:**
```
concept: "perception-action loop"
focus: "integration"
depth: "detailed"
output_format: "diagram"
```

**Output:**
```markdown
## The Perception-Action Loop in VLA Systems

### Overview

The perception-action loop is the fundamental cycle through which a VLA-powered humanoid interacts with its environment. Unlike open-loop execution, VLA models continuously observe, reason, and adjust.

### Loop Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PERCEPTION-ACTION LOOP                           │
│                                                                     │
│    ┌─────────────────────────────────────────────────────────┐     │
│    │                    ENVIRONMENT                          │     │
│    │  • Physical world state                                 │     │
│    │  • Objects, surfaces, humans                            │     │
│    │  • Dynamic changes                                      │     │
│    └──────────────────────┬──────────────────────────────────┘     │
│                           │                                         │
│                           │ sensory input                           │
│                           ▼                                         │
│    ┌─────────────────────────────────────────────────────────┐     │
│    │                    PERCEPTION                           │     │
│    │                                                         │     │
│    │  ┌───────────┐  ┌───────────┐  ┌───────────┐          │     │
│    │  │  Vision   │  │Propriocep-│  │  Other    │          │     │
│    │  │  Encoder  │  │   tion    │  │ Sensors   │          │     │
│    │  │           │  │           │  │           │          │     │
│    │  │ RGB/Depth │  │Joint state│  │Force, IMU │          │     │
│    │  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘          │     │
│    │        └──────────────┼──────────────┘                 │     │
│    │                       ▼                                 │     │
│    │              Observation Vector                         │     │
│    └──────────────────────┬──────────────────────────────────┘     │
│                           │                                         │
│                           ▼                                         │
│    ┌─────────────────────────────────────────────────────────┐     │
│    │                    REASONING                            │     │
│    │                                                         │     │
│    │  ┌─────────────────────────────────────────────────┐   │     │
│    │  │            VLA Model Core                        │   │     │
│    │  │                                                  │   │     │
│    │  │  Observation ──┐                                 │   │     │
│    │  │                ├──▶ Multimodal ──▶ Action        │   │     │
│    │  │  Instruction ──┘    Reasoning      Selection     │   │     │
│    │  │                                                  │   │     │
│    │  │  "Place the cup on the marked spot"              │   │     │
│    │  │           +                                      │   │     │
│    │  │  [Scene with cup, table, marker]                 │   │     │
│    │  │           =                                      │   │     │
│    │  │  Action: move_to(marker_pos), release()          │   │     │
│    │  └─────────────────────────────────────────────────┘   │     │
│    └──────────────────────┬──────────────────────────────────┘     │
│                           │                                         │
│                           │ action command                          │
│                           ▼                                         │
│    ┌─────────────────────────────────────────────────────────┐     │
│    │                    ACTION                               │     │
│    │                                                         │     │
│    │  Action Representation    Motor Execution               │     │
│    │  ┌───────────────┐       ┌───────────────┐             │     │
│    │  │ • Discrete    │       │ • Joint       │             │     │
│    │  │   tokens      │──────▶│   controllers │             │     │
│    │  │ • Continuous  │       │ • Trajectory  │             │     │
│    │  │   waypoints   │       │   tracking    │             │     │
│    │  └───────────────┘       └───────┬───────┘             │     │
│    └──────────────────────────────────┼──────────────────────┘     │
│                                       │                             │
│                                       │ physical effect             │
│                                       ▼                             │
│    ┌─────────────────────────────────────────────────────────┐     │
│    │                    ENVIRONMENT                          │     │
│    │                    (state changed)                      │     │
│    └─────────────────────────────────────────────────────────┘     │
│                                                                     │
│    Loop frequency: 10-50 Hz for reactive control                    │
│                    1-5 Hz for high-level reasoning                  │
└─────────────────────────────────────────────────────────────────────┘
```

### Loop Characteristics

| Property | Open-Loop | Closed-Loop (VLA) |
|----------|-----------|-------------------|
| Feedback | None | Continuous |
| Error correction | Impossible | Automatic |
| Adaptability | None | High |
| Failure recovery | Fails silently | Can retry/adjust |
| Computational cost | Low | Higher |

### Timing Considerations

```
High-Level Loop (VLA Reasoning)
├── Frequency: 1-5 Hz
├── Latency tolerance: 200-1000 ms
└── Purpose: Decide WHAT to do

Low-Level Loop (Motor Control)
├── Frequency: 100-1000 Hz
├── Latency tolerance: 1-10 ms
└── Purpose: Execute HOW to do it

┌─────────────────────────────────────────────────────┐
│ Time ─────────────────────────────────────────────▶ │
│                                                     │
│ VLA:    [reason]........[reason]........[reason]   │
│              │              │              │        │
│              ▼              ▼              ▼        │
│ Motor: ─────────────────────────────────────────── │
│         ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲   │
│         (high-frequency control updates)            │
└─────────────────────────────────────────────────────┘
```

### Reference Documentation
- Loop implementation: docs/module-4-vla/07-perception-action-loop.md
- Action representations: docs/module-4-vla/04-action-representations.md
```

### Example 3: Grounding concepts

**Input:**
```
concept: "grounding"
focus: "language"
depth: "detailed"
output_format: "analogy"
```

**Output:**
```markdown
## Grounding: Connecting Words to the World

### The Grounding Problem

When you say "the cup" to a robot, you mean a specific physical object. When the robot's language model processes "the cup," it starts as abstract symbols. Grounding is the process of connecting those symbols to entities in the robot's perceived world.

### Analogy: The Tourist and the Local

Imagine a tourist in a foreign city with a phrase book.

**Without Grounding (Phrase Book Only)**
- Tourist can say "Where is the museum?"
- Knows the words are grammatically correct
- Has no idea what a museum looks like
- Cannot recognize one when standing in front of it

**With Grounding (Local Guide)**
- Guide points: "That building with columns is the museum"
- Tourist now connects the word to a visual pattern
- Can find similar buildings independently
- Understands "museum" in context of this city

The VLA model is the tourist. Grounding is the local guide.

### Grounding in VLA: A Concrete Example

**Instruction**: "Put the leftmost apple in the bowl"

**What Needs Grounding**:

| Word/Phrase | Grounding Required | Resolution |
|-------------|-------------------|------------|
| "apple" | Object class → visual detection | Find objects matching 'apple' appearance |
| "leftmost" | Spatial relation → coordinate comparison | Among apples, find minimum X coordinate |
| "bowl" | Object class → visual detection | Find container matching 'bowl' appearance |
| "in" | Spatial relation → target pose | Calculate position inside bowl bounds |
| "put" | Action verb → motor primitive | Map to place() action with parameters |

**Grounding Flow**:

```
"Put the leftmost apple in the bowl"
         │
         ▼
┌─────────────────────────────────────┐
│ Language Parser                      │
│ action: PUT                          │
│ object: APPLE                        │
│ modifier: LEFTMOST                   │
│ destination: BOWL                    │
│ relation: IN                         │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│ Visual Scene                         │
│                                      │
│   🍎 (x=0.2)  🍎 (x=0.5)  🍎 (x=0.7) │
│                                      │
│              🥣 (x=0.4)              │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│ Grounded Resolution                  │
│                                      │
│ object: Apple at (0.2, y, z)         │
│ destination: Bowl at (0.4, y, z)     │
│ action: PLACE(apple_0, bowl_0)       │
└─────────────────────────────────────┘
```

### Types of Grounding

#### Referential Grounding
Connecting noun phrases to objects.
- "The red cup" → specific object instance
- "A screwdriver" → any matching object

#### Spatial Grounding
Connecting spatial language to coordinates.
- "On top of" → relative position offset
- "Between the boxes" → computed midpoint

#### Temporal Grounding
Connecting time references to action sequences.
- "After you pick it up" → action ordering constraint
- "While walking" → concurrent action requirement

#### Action Grounding
Connecting verbs to motor behaviors.
- "Push" → apply_force(direction, magnitude)
- "Hand over" → extend_arm() + release_when_contact()

### Why Grounding is Hard for Humanoids

| Challenge | Example | Difficulty |
|-----------|---------|------------|
| Ambiguity | "That thing" could be anything | Requires context |
| Implicit references | "The other one" assumes shared attention | Requires history |
| Partial observability | Object behind another | Requires exploration |
| Dynamic scenes | Object moved since instruction | Requires re-grounding |
| Novel descriptions | "The thingy with buttons" | Requires inference |

### Grounding Failure Modes

```
Instruction: "Hand me my glasses"

Failure Mode 1: Wrong Object Class
├── Robot picks up drinking glasses
└── Needed: eyeglasses

Failure Mode 2: Wrong Instance
├── Robot picks up someone else's eyeglasses
└── Needed: ownership inference from context

Failure Mode 3: Stale Grounding
├── Robot reaches for where glasses were
└── Needed: re-localize moved object

Failure Mode 4: Missing Object
├── Glasses not in view
└── Needed: search behavior, ask for help
```

### Reference Documentation
- Grounding mechanisms: docs/module-4-vla/06-grounding.md
- Spatial reasoning: docs/module-4-vla/08-spatial-reasoning.md
- Instruction following: docs/module-4-vla/10-instruction-following.md
```

### Example 4: Action representations

**Input:**
```
concept: "action representation"
focus: "action"
depth: "comparative"
output_format: "case_study"
```

**Output:**
```markdown
## Case Study: Action Representations for Humanoid Cup Handover

### Scenario

A humanoid robot must take a cup from a table and hand it to a human. We examine how different action representations encode this task.

### The Task Decomposed

```
Subtasks:
1. Approach table
2. Position hand above cup
3. Grasp cup
4. Lift cup
5. Turn toward human
6. Extend arm to human
7. Wait for human to take cup
8. Release grasp
9. Retract arm
```

### Representation 1: Discrete Action Tokens

**Approach**: Actions as vocabulary items, similar to language tokens.

```
Token sequence: [APPROACH_TABLE] [REACH_OBJECT_cup] [GRASP]
                [LIFT] [TURN_TO_human] [EXTEND_ARM]
                [WAIT_CONTACT] [RELEASE] [RETRACT]
```

**Characteristics**:

| Aspect | Analysis |
|--------|----------|
| Abstraction level | High (semantic actions) |
| Output space | Small (hundreds of tokens) |
| Generalization | Good across similar tasks |
| Precision | Limited (no continuous control) |
| Training data | Easier to label |

**Humanoid suitability**: Good for high-level task planning. Must combine with lower-level controller for execution.

### Representation 2: Continuous Waypoints

**Approach**: Actions as 6-DOF end-effector poses (x, y, z, roll, pitch, yaw).

```
Waypoint sequence:
  W1: (0.5, 0.0, 0.8, 0, 0, 0)      # Above table
  W2: (0.5, 0.2, 0.7, 0, π/4, 0)    # Above cup, tilted
  W3: (0.5, 0.2, 0.65, 0, π/4, 0)   # At cup
  W4: (0.5, 0.2, 0.85, 0, π/4, 0)   # Cup lifted
  W5: (0.3, -0.4, 1.0, 0, 0, π/2)   # Toward human
  W6: (0.3, -0.6, 1.0, 0, 0, π/2)   # Extended to human
```

**Characteristics**:

| Aspect | Analysis |
|--------|----------|
| Abstraction level | Medium (Cartesian space) |
| Output space | Continuous (6D per waypoint) |
| Generalization | Moderate (position-specific) |
| Precision | High for positioning |
| Training data | Requires pose annotation |

**Humanoid suitability**: Good for manipulation. Requires inverse kinematics for joint commands.

### Representation 3: Joint Position Targets

**Approach**: Actions as target angles for each joint.

```
For a 7-DOF arm, each action is a 7-dimensional vector:
  A1: [0.1, -0.3, 0.0, -1.2, 0.0, 0.8, 0.0]   # Reach config
  A2: [0.2, -0.5, 0.1, -1.5, 0.0, 1.0, 0.0]   # Grasp config
  ...
```

**Characteristics**:

| Aspect | Analysis |
|--------|----------|
| Abstraction level | Low (joint space) |
| Output space | High-dimensional (N joints × timesteps) |
| Generalization | Poor (robot-specific) |
| Precision | Highest (direct motor control) |
| Training data | Requires joint trajectories |

**Humanoid suitability**: Direct but complex. 30+ dimensions for full-body humanoid.

### Representation 4: Action Primitives with Parameters

**Approach**: Parameterized skill library.

```
Primitive calls:
  navigate(target=table_position)
  reach(target=cup_position, approach=top)
  grasp(object=cup, force=gentle)
  lift(height=0.2)
  turn(target=human_position)
  handover(recipient=human, wait=True)
```

**Characteristics**:

| Aspect | Analysis |
|--------|----------|
| Abstraction level | High (skills with parameters) |
| Output space | Discrete skills + continuous params |
| Generalization | Excellent (skills transfer) |
| Precision | Depends on skill implementation |
| Training data | Requires skill segmentation |

**Humanoid suitability**: Excellent. Matches how complex behaviors compose.

### Comparison Matrix

| Criterion | Tokens | Waypoints | Joint Pos | Primitives |
|-----------|--------|-----------|-----------|------------|
| Learning difficulty | Easy | Medium | Hard | Medium |
| Execution precision | Low | High | Highest | Medium |
| Transfer to new robot | Good | Medium | Poor | Good |
| Handles dynamics | No | Partial | Yes | Partial |
| Interpretable | Yes | Partial | No | Yes |
| Reactive adjustment | Hard | Medium | Easy | Medium |

### Humanoid-Specific Considerations

```
Challenge: Whole-body coordination during handover

Token approach:
└── Cannot specify balance maintenance

Waypoint approach:
└── Hand pose only; legs/torso implicit

Joint approach:
└── Must specify all 30+ joints; hard to learn

Primitive approach:
└── handover() skill encapsulates balance
    └── Best fit for humanoid complexity
```

### Emerging Hybrid Approaches

Modern VLA models increasingly use:
1. **Hierarchical**: High-level tokens select primitives, low-level outputs parameters
2. **Diffusion**: Generate continuous trajectories conditioned on language
3. **Token-continuous**: Discretize continuous space into large token vocabulary

### Reference Documentation
- Action spaces: docs/module-4-vla/04-action-representations.md
- Instruction following: docs/module-4-vla/10-instruction-following.md
- Humanoid applications: docs/module-4-vla/15-humanoid-applications.md
```

## Integration Notes

This skill coordinates with:
- `ros2-teaching`: Action commands ultimately become ROS2 messages to robot hardware
- `digital-twin-visualization`: VLA model inputs visualized in simulation
- `isaac-sim-guidance`: Training environments and synthetic perception data for VLA models
- `capstone-mentor`: VLA understanding enables advanced capstone projects with learned behaviors

## Version

- Skill version: 1.0.0
- Conceptual framework: Architecture-agnostic, applicable to RT-2, PaLM-E, and similar models
- Last updated: 2025-01-15
