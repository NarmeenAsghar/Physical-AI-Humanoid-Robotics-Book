#!/usr/bin/env python3
"""
Populate Qdrant Script - Local Embedded Mode
=============================================
This script populates the local Qdrant database with book content.

Usage:
    python populate_qdrant.py                    # Populate with dummy data
    python populate_qdrant.py --test            # Run quick test with 3 samples
    python populate_qdrant.py --file book.txt   # Populate from file
    python populate_qdrant.py --clear           # Clear and repopulate

Features:
- Creates 'book_chunks' collection if it doesn't exist
- Inserts dummy/sample data for testing
- Can process actual book markdown files
- No external server required (uses local embedded Qdrant)

@author AI Backend Developer
@version 1.0.0
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import (
    get_qdrant_client,
    init_qdrant_collection,
    embed_text,
    upsert_chunks,
    retrieve_from_qdrant,
    get_collection_info,
    chunk_text,
    EMBEDDING_DIMENSION,
    DEFAULT_COLLECTION,
)


# =============================================================================
# SAMPLE DATA
# =============================================================================

# Dummy data for testing the RAG system
SAMPLE_CHUNKS = [
    {
        "id": 1,
        "content": "ROS2 (Robot Operating System 2) is a flexible framework for writing robot software. "
                   "It provides tools, libraries, and conventions that simplify the task of creating "
                   "complex robot behavior across a wide variety of robotic platforms.",
        "metadata": {
            "chapter": "Introduction to ROS2",
            "section": "What is ROS2?",
            "page": 1,
        }
    },
    {
        "id": 2,
        "content": "A digital twin is a virtual representation of a physical object, process, or system. "
                   "In robotics, digital twins allow engineers to simulate robot behavior, test control "
                   "algorithms, and predict maintenance needs without risking the physical hardware.",
        "metadata": {
            "chapter": "Digital Twins",
            "section": "Introduction to Digital Twins",
            "page": 15,
        }
    },
    {
        "id": 3,
        "content": "Forward kinematics calculates the position and orientation of the end-effector "
                   "given the joint angles. This is the fundamental problem in robotics: given joint "
                   "parameters, determine where the robot's tool or hand is located in 3D space.",
        "metadata": {
            "chapter": "Robot Kinematics",
            "section": "Forward Kinematics",
            "page": 45,
        }
    },
    {
        "id": 4,
        "content": "Inverse kinematics (IK) solves the opposite problem: given a desired end-effector "
                   "position and orientation, calculate the joint angles required to achieve it. "
                   "IK is more complex and may have multiple solutions or no solution at all.",
        "metadata": {
            "chapter": "Robot Kinematics",
            "section": "Inverse Kinematics",
            "page": 52,
        }
    },
    {
        "id": 5,
        "content": "URDF (Unified Robot Description Format) is an XML format used in ROS to describe "
                   "robots. It specifies the robot's links (rigid bodies), joints (connections between "
                   "links), visual appearance, and collision geometry.",
        "metadata": {
            "chapter": "Robot Modeling",
            "section": "URDF Basics",
            "page": 30,
        }
    },
    {
        "id": 6,
        "content": "Gazebo is a powerful physics simulator for robotics. It integrates with ROS2 and "
                   "allows testing robot algorithms in a realistic environment with accurate physics, "
                   "sensor simulation, and 3D visualization before deploying on real hardware.",
        "metadata": {
            "chapter": "Simulation",
            "section": "Gazebo Simulator",
            "page": 78,
        }
    },
    {
        "id": 7,
        "content": "The MoveIt framework provides motion planning capabilities for robotic arms. "
                   "It computes collision-free paths from the current pose to a goal pose, considering "
                   "obstacles in the environment and robot joint limits.",
        "metadata": {
            "chapter": "Motion Planning",
            "section": "MoveIt Framework",
            "page": 95,
        }
    },
    {
        "id": 8,
        "content": "Humanoid robots are designed to resemble the human body. They typically have "
                   "a torso, head, two arms, and two legs. Key challenges include balance, bipedal "
                   "walking, and natural human-robot interaction.",
        "metadata": {
            "chapter": "Humanoid Robotics",
            "section": "Introduction",
            "page": 120,
        }
    },
    {
        "id": 9,
        "content": "Physical AI refers to artificial intelligence systems that interact with the "
                   "physical world through sensors and actuators. Unlike purely software AI, physical "
                   "AI must handle real-world uncertainties, noise, and safety constraints.",
        "metadata": {
            "chapter": "Physical AI",
            "section": "What is Physical AI?",
            "page": 5,
        }
    },
    {
        "id": 10,
        "content": "Reinforcement learning allows robots to learn optimal behaviors through trial "
                   "and error. The robot receives rewards for desired actions and penalties for "
                   "undesired ones, gradually learning a policy that maximizes cumulative reward.",
        "metadata": {
            "chapter": "Machine Learning for Robotics",
            "section": "Reinforcement Learning",
            "page": 150,
        }
    },
]


# =============================================================================
# POPULATION FUNCTIONS
# =============================================================================

def populate_with_samples(clear_first: bool = False) -> int:
    """
    Populate the collection with sample book content.

    Args:
        clear_first: If True, recreate the collection before populating

    Returns:
        int: Number of chunks inserted
    """
    print("\n" + "=" * 60)
    print("Populating Qdrant with Sample Book Content")
    print("=" * 60)

    # Initialize collection (optionally recreate)
    init_qdrant_collection(DEFAULT_COLLECTION, recreate=clear_first)

    # Insert sample chunks
    count = upsert_chunks(SAMPLE_CHUNKS, DEFAULT_COLLECTION)

    print(f"\n[OK] Inserted {count} sample chunks into '{DEFAULT_COLLECTION}'")

    # Show collection info
    info = get_collection_info(DEFAULT_COLLECTION)
    if info:
        print(f"\nCollection Info:")
        print(f"  - Points: {info['points_count']}")
        print(f"  - Vector Size: {info['vector_size']}")
        print(f"  - Status: {info['status']}")

    return count


def populate_from_file(filepath: str, chapter: str = "Unknown") -> int:
    """
    Populate collection from a text/markdown file.

    Args:
        filepath: Path to the file to process
        chapter: Chapter name to use in metadata

    Returns:
        int: Number of chunks inserted
    """
    print(f"\n[FILE] Processing file: {filepath}")

    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        return 0

    # Read file content
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract filename as section name
    section = os.path.basename(filepath).replace(".md", "").replace(".txt", "")

    # Chunk the content
    chunks = chunk_text(
        content,
        chunk_size=500,
        overlap=50,
        metadata={"chapter": chapter, "section": section, "source_file": filepath}
    )

    print(f"  Created {len(chunks)} chunks")

    # Insert chunks
    count = upsert_chunks(chunks, DEFAULT_COLLECTION)
    print(f"  [OK] Inserted {count} chunks")

    return count


def test_retrieval():
    """
    Test the retrieval functionality with sample queries.
    """
    print("\n" + "=" * 60)
    print("Testing Retrieval")
    print("=" * 60)

    test_queries = [
        "What is ROS2?",
        "How does inverse kinematics work?",
        "Tell me about digital twins",
        "What is physical AI?",
    ]

    for query in test_queries:
        print(f"\n[SEARCH] Query: '{query}'")
        results = retrieve_from_qdrant(query, top_k=2, score_threshold=0.3)

        if not results:
            print("   No results found (score below threshold)")
        else:
            for i, r in enumerate(results, 1):
                print(f"\n   Result {i} (score: {r['score']:.3f}):")
                print(f"   Chapter: {r['chapter']} > {r['section']}")
                # Truncate content for display
                content = r['content'][:150] + "..." if len(r['content']) > 150 else r['content']
                print(f"   Content: {content}")


def quick_test():
    """
    Run a quick test with 3 samples.
    """
    print("\n" + "=" * 60)
    print("Quick Test Mode")
    print("=" * 60)

    # Use just 3 samples
    test_chunks = SAMPLE_CHUNKS[:3]

    # Clear and create fresh collection
    init_qdrant_collection("test_chunks", recreate=True)

    # Insert test chunks
    count = upsert_chunks(test_chunks, "test_chunks")
    print(f"[OK] Inserted {count} test chunks")

    # Test retrieval
    print("\n[SEARCH] Testing search for 'ROS2'...")
    results = retrieve_from_qdrant("ROS2", top_k=1, score_threshold=0.3, collection_name="test_chunks")

    if results:
        print(f"[OK] Found result with score: {results[0]['score']:.3f}")
        print(f"  Content preview: {results[0]['content'][:100]}...")
    else:
        print("[WARN] No results found")

    print("\n[OK] Quick test completed!")


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """
    Main entry point for the populate script.
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Populate Qdrant with book content for RAG chatbot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python populate_qdrant.py              # Populate with sample data
  python populate_qdrant.py --test       # Quick test with 3 samples
  python populate_qdrant.py --clear      # Clear and repopulate
  python populate_qdrant.py --query "What is ROS2?"  # Test a query
        """
    )

    parser.add_argument(
        "--test",
        action="store_true",
        help="Run quick test with 3 samples"
    )

    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear collection before populating"
    )

    parser.add_argument(
        "--file",
        type=str,
        help="Path to a text/markdown file to process"
    )

    parser.add_argument(
        "--chapter",
        type=str,
        default="Unknown",
        help="Chapter name for file import (default: Unknown)"
    )

    parser.add_argument(
        "--query",
        type=str,
        help="Test a retrieval query"
    )

    parser.add_argument(
        "--info",
        action="store_true",
        help="Show collection info only"
    )

    args = parser.parse_args()

    # Show info only
    if args.info:
        info = get_collection_info(DEFAULT_COLLECTION)
        if info:
            print("\nCollection Info:")
            for k, v in info.items():
                print(f"  {k}: {v}")
        else:
            print("Collection not found. Run populate first.")
        return

    # Quick test mode
    if args.test:
        quick_test()
        return

    # Test a query
    if args.query:
        print(f"\n[SEARCH] Searching for: '{args.query}'")
        results = retrieve_from_qdrant(args.query, top_k=3, score_threshold=0.3)
        if not results:
            print("No results found")
        else:
            for i, r in enumerate(results, 1):
                print(f"\n[{i}] Score: {r['score']:.3f}")
                print(f"    {r['chapter']} > {r['section']}")
                print(f"    {r['content'][:200]}...")
        return

    # Populate from file
    if args.file:
        init_qdrant_collection(DEFAULT_COLLECTION)
        populate_from_file(args.file, chapter=args.chapter)
        test_retrieval()
        return

    # Default: populate with samples
    populate_with_samples(clear_first=args.clear)
    test_retrieval()

    print("\n" + "=" * 60)
    print("Population Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Start the backend: python main.py")
    print("  2. Test the chatbot: curl -X POST https://narmeenasghar-rag-chatbot.hf.space/chat \\")
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"query": "What is ROS2?"}\'')


if __name__ == "__main__":
    main()
