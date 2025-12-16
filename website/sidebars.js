// @ts-check

/**
 * Physical AI and Humanoid Robotics Book - Sidebar Configuration
 * @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  mySidebar: [
    "intro",
    {
      type: "category",
      label: "Module 1: ROS2",
      items: ["module-1-ros2/index", "module-1-ros2/python-urdf"],
    },
    {
      type: "category",
      label: "Module 2: Digital Twin",
      items: ["module-2-digital-twin/index", "module-2-digital-twin/unity-visualization"],
    },
    {
      type: "category",
      label: "Module 3: Isaac Sim",
      items: ["module-3-isaac/index"],
    },
    {
      type: "category",
      label: "Module 4: VLA",
      items: ["module-4-vla/index"],
    },
    {
      type: "category",
      label: "Capstone",
      items: ["capstone/index"],
    },
    {
      type: "category",
      label: "Appendices",
      items: ["appendices/hardware-lab-infrastructure", "appendices/weekly-learning-path"],
    },
    "conclusion",
  ],
};

export default sidebars;
