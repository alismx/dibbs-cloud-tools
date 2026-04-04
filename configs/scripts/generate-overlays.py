#!/usr/bin/env python3
"""
Generate overlay compose.yaml files for each environment.

All environments use the same base services. The differences between
environments are handled via environment variables in ecr-viewer.env.
"""

from pathlib import Path


def generate_overlay(config_name: str) -> str:
    """Generate overlay compose.yaml content based on config name."""

    lines = [
        f"# Overlay for {config_name}",
        "",
        "# This overlay is intentionally empty.",
        "# All services are defined in configs/base/compose.yaml",
        "# Environment-specific configuration is handled via env/dibbs-ecr-viewer.env",
        ""
    ]

    return "\n".join(lines)


def main():
    base_dir = Path(__file__).parent.parent
    overlays_dir = base_dir / "overlays"

    # Get all overlay directories
    overlay_names = sorted([d.name for d in overlays_dir.iterdir() if d.is_dir()])

    for config_name in overlay_names:
        overlay_file = overlays_dir / config_name / "compose.yaml"
        content = generate_overlay(config_name)

        with open(overlay_file, 'w') as f:
            f.write(content)

        print(f"Updated: {overlay_file}")


if __name__ == "__main__":
    main()
