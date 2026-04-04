# Multi-Environment Container Configuration

## Overview

This directory contains configuration templates for deploying the DIBBS application across multiple cloud environments (AWS, Azure, GCP) with different database backends (PostgreSQL, SQL Server).

## Directory Structure

```
configs/
├── base/                       # Common services - single source of truth
│   ├── compose.yaml           # All 6 core services + docs (optional)
│   ├── env/
│   │   ├── dibbs-ecr-viewer.env
│   │   └── dibbs-orchestration.env
│   └── CLAUDE.md              # See directory structure
├── overlays/                   # Environment-specific configurations
│   ├── AWS_INTEGRATED/        # See CLAUDE.md for structure
│   ├── AZURE_PG_DUAL/         # See CLAUDE.md for structure
│   ├── GCP_PG_DUAL/           # See CLAUDE.md for structure
│   ├── AWS_PG_NON_INTEGRATED/ # See CLAUDE.md for structure
│   ├── AZURE_PG_NON_INTEGRATED/ # See CLAUDE.md for structure
│   ├── GCP_PG_NON_INTEGRATED/ # See CLAUDE.md for structure
│   ├── AWS_SQLSERVER_DUAL/    # See CLAUDE.md for structure
│   ├── AZURE_SQLSERVER_DUAL/  # See CLAUDE.md for structure
│   ├── GCP_SQLSERVER_DUAL/    # See CLAUDE.md for structure
│   ├── AWS_SQLSERVER_NON_INTEGRATED/ # See CLAUDE.md for structure
│   ├── AZURE_SQLSERVER_NON_INTEGRATED/ # See CLAUDE.md for structure
│   └── GCP_SQLSERVER_NON_INTEGRATED/ # See CLAUDE.md for structure
├── templates/                  # Template files for new environments
│   ├── ecr-viewer-template.env
│   └── CLAUDE.md
└── scripts/
    ├── generate-env.py        # Generate environment configs
    ├── generate-overlays.py   # Generate overlay compose.yaml files
    └── CLAUDE.md              # See script documentation
```

## Understanding the Pattern

### Base Configuration (`configs/base/`)
Contains all services with **version variables** and **placeholders**:
- All 6 core services defined: ecr-viewer, ingestion, fhir-converter, message-parser, trigger-code-reference, orchestration
- Docker image versions controlled via `${VARIABLE:-default}` syntax
- Docs service included with `integrated` profile (disabled by default)

### Overlay Configuration (`configs/overlays/<ENV>/`)
Contains environment-specific overrides:
- `compose.yaml`: Empty overlay (all services in base)
- `env/dibbs-ecr-viewer.env`: Cloud-specific credentials and settings

## Usage

### Running with Base + Overlay

```bash
# Using docker-compose directly (from project root)
docker-compose \
  -f configs/base/compose.yaml \
  -f configs/overlays/AZURE_PG_DUAL/compose.yaml \
  --env-file configs/overlays/AZURE_PG_DUAL/env/dibbs-ecr-viewer.env \
  up

# Or using the compose file in a specific overlay
cd configs/overlays/AZURE_PG_DUAL
docker-compose --env-file env/dibbs-ecr-viewer.env up
```

### With docs service enabled (integrated environments)

```bash
# Use profiles to enable optional services
docker-compose -p integrated \
  -f configs/base/compose.yaml \
  --profile integrated \
  up
```

### Adding New Environments

Run the generator script from the `configs/scripts` directory:

```bash
cd configs/scripts

# For a new Azure PostgreSQL dual environment
python generate-env.py AZURE_PG_DUAL

# For AWS SQL Server non-integrated
python generate-env.py AWS_SQLSERVER_NON_INTEGRATED
```

Or from project root:

```bash
python configs/scripts/generate-env.py <CONFIG_NAME>
```

This creates `configs/overlays/<ENV>/` with:
- An empty compose.yaml (inherits from base)
- An ecr-viewer.env template with cloud-specific placeholders

Update the placeholder values in `configs/overlays/<ENV>/env/dibbs-ecr-viewer.env`.

## Configuration Types

The CONFIG_NAME environment variable determines which cloud provider and database configuration is used:

| Environment Pattern | Description |
|---------------------|-------------|
| `*_INTEGRATED`      | Full stack with docs enabled (use `--profile integrated`) |
| `*_DUAL`            | Dual database setup (no additional services) |
| `*_NON_INTEGRATED`  | Minimal setup (no additional services) |

### Cloud-Specific Settings

#### AWS
```env
AWS_REGION=us-east-1
ECR_BUCKET_NAME=my-bucket
```

#### Azure
```env
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;...
AZURE_CONTAINER_NAME=dibbs-storage
```

#### GCP
```env
GCP_PROJECT_ID=my-project
GCP_SERVICE_ACCOUNT_KEY_PATH=/path/to/key.json
```

## Benefits

1. **Single Source of Truth**: Base compose.yaml defines all services once
2. **Easy Updates**: Change image version in one place, all environments inherit
3. **Clear Differences**: Environment-specific values are obvious in ecr-viewer.env
4. **Template Generation**: New environments created with one command
5. **Minimal Overlays**: No service duplication - differences are configuration-only

## Migration from Old Structure

The old structure (`AWS_INTEGRATED/`, `AZURE_PG_DUAL/`, etc.) has:
- Full compose.yaml in each directory (duplicated)
- Portainer included in all environments

The new structure:
- Base config with version variables
- Empty overlays - services defined once in base
- No portainer - removed from all configurations

To migrate, keep old directories but use `configs/` going forward.

