# Publishing to PyPI

This repository is configured for automated publishing to PyPI using GitHub Actions.

## Setup Requirements

### 1. PyPI API Token
1. Go to [PyPI](https://pypi.org) and create an account if you don't have one
2. Generate an API token:
   - Go to Account Settings → API tokens
   - Create a new token with "Entire account" scope
   - Copy the token (starts with `pypi-`)

### 2. GitHub Secrets
Add the following secrets to your GitHub repository:
- Go to Settings → Secrets and variables → Actions
- Add repository secret:
  - Name: `PYPI_API_TOKEN`
  - Value: Your PyPI API token

### 3. Test PyPI (Optional)
For testing releases, you can also set up Test PyPI:
1. Create account at [Test PyPI](https://test.pypi.org)
2. Generate API token
3. Add `TEST_PYPI_API_TOKEN` secret to GitHub

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

The CI/CD pipeline:

1. **Tests**: Runs on Python 3.8-3.12 for all pushes and PRs
2. **Build & Publish**: Only runs on releases
   - Builds source distribution and wheel
   - Validates the package with `twine check`
   - Publishes to PyPI automatically

## Version Management

- Update version in `setup.py` before creating a release
- Use semantic versioning (e.g., `0.2.1`, `1.0.0`)
- Tag format: `v{major}.{minor}.{patch}`

## Troubleshooting

- **Build fails**: Check Python version compatibility and dependencies
- **Upload fails**: Verify PyPI token is correct and has sufficient permissions
- **Version conflict**: Ensure version number hasn't been used before on PyPI