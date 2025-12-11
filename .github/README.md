# GitHub Configuration for Judo Framework

This directory contains GitHub-specific configuration files for the Judo Framework repository.

---

## 📁 Directory Structure

```
.github/
├── workflows/
│   └── close-prs.yml          # Auto-closes Pull Requests
├── ISSUE_TEMPLATE/
│   ├── bug_report.md          # Bug report template
│   ├── feature_request.md     # Feature request template
│   └── config.yml             # Issue template configuration
├── CODEOWNERS                 # Code ownership rules
├── PULL_REQUEST_TEMPLATE.md   # PR template (explains policy)
├── REPOSITORY_SETUP.md        # Setup instructions
└── README.md                  # This file
```

---

## 🔧 What Each File Does

### `workflows/close-prs.yml`
Automatically closes any Pull Request that is opened with a message explaining that:
- Judo Framework doesn't accept PRs
- How to contribute through Issues instead
- Links to CONTRIBUTING.md

### `CODEOWNERS`
Defines that @FelipeFariasAlfaro is the sole code owner for all files in the repository.

### `PULL_REQUEST_TEMPLATE.md`
Template that appears when someone tries to create a PR, explaining:
- Why PRs are not accepted
- How to contribute properly
- Links to resources

### `ISSUE_TEMPLATE/bug_report.md`
Structured template for bug reports with sections for:
- Bug description
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Code samples

### `ISSUE_TEMPLATE/feature_request.md`
Structured template for feature requests with sections for:
- Feature description
- Problem/use case
- Proposed solution
- Example usage
- Priority/impact

### `ISSUE_TEMPLATE/config.yml`
Configuration for issue templates, including:
- Links to Discussions
- Links to Documentation
- Links to CENTYC website

---

## 🎯 Contribution Policy

**Judo Framework only accepts contributions through GitHub Issues.**

### ✅ What We Accept:
- 🐛 Bug reports
- 💡 Feature suggestions
- 📝 Documentation feedback
- ❓ Questions (in Discussions)

### ❌ What We Don't Accept:
- Pull Requests (auto-closed)
- Code contributions
- Modified forks

### Why?
Judo Framework is professionally maintained by CENTYC to ensure:
- Consistent code quality
- Reliable releases
- Professional support
- Clear roadmap

---

## 📚 More Information

- **Contributing Guide:** [CONTRIBUTING.md](../CONTRIBUTING.md)
- **Setup Instructions:** [REPOSITORY_SETUP.md](REPOSITORY_SETUP.md)
- **Main README:** [README.md](../README.md)

---

## 🔗 Links

- **Repository:** https://github.com/FelipeFariasAlfaro/Judo-Framework
- **Issues:** https://github.com/FelipeFariasAlfaro/Judo-Framework/issues
- **Discussions:** https://github.com/FelipeFariasAlfaro/Judo-Framework/discussions
- **PyPI:** https://pypi.org/project/judo-framework/
- **CENTYC:** https://www.centyc.cl

---

**Made with ❤️ at CENTYC for API testing excellence** 🥋
