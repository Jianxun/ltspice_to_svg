# Publishing to PyPI

This repository uses **PyPI Trusted Publishing** for secure, automated publishing to PyPI using GitHub Actions.

## Setup Requirements

### 1. PyPI Trusted Publishing Setup
1. Go to [PyPI](https://pypi.org) and create an account if you don't have one
2. Go to your PyPI account settings → Publishing
3. Add a new trusted publisher:
   - **PyPI project name**: `ltspice-to-svg` (or your actual PyPI project name)
   - **Owner**: `Jianxun` (your GitHub username)
   - **Repository name**: `ltspice_to_svg`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `publish`

### 2. GitHub Environment Setup
1. Go to your GitHub repository → Settings → Environments
2. Create a new environment named `publish`
3. (Optional) Add protection rules like requiring reviews for deployments

**Note**: No API tokens needed! Trusted publishing uses OpenID Connect (OIDC) for secure authentication.

## Release Process

The automated publishing workflow triggers on:

1. **GitHub Releases**: When you create a new release on GitHub
2. **Git Tags**: When you push a tag starting with `v` (e.g., `v1.0.0`)

### Creating a Release

#### Method 1: GitHub UI
1. Go to your repository → Releases
2. Click "Create a new release"
3. Choose or create a tag (e.g., `v0.2.1`)
4. Fill in release title and description
5. Click "Publish release"

#### Method 2: Command Line
```bash
# Tag the release
git tag v0.2.1
git push origin v0.2.1

# Or create and push in one step
git tag v0.2.1 && git push origin v0.2.1
```

## Workflow Details

The build and publish pipeline:

1. **Build & Publish**: Only runs on releases
   - Builds source distribution and wheel
   - Validates the package with `twine check`
   - Publishes to PyPI automatically

**Note**: CI testing is not included as this package requires LTspice libraries and Windows-specific functionality that are not available on Linux CI runners.

## Version Management

- Update version in `setup.py` before creating a release
- Use semantic versioning (e.g., `0.2.1`, `1.0.0`)
- Tag format: `v{major}.{minor}.{patch}`

## Troubleshooting

- **Build fails**: Check Python version compatibility and dependencies
- **Upload fails**: Verify PyPI token is correct and has sufficient permissions
- **Version conflict**: Ensure version number hasn't been used before on PyPI