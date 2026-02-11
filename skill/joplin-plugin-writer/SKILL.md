---
name: joplin-plugin-writer
description: Write, refactor, and debug Joplin plugins for desktop/mobile using the official Joplin plugin architecture, API, and manifest rules. Use when a user asks to create a new Joplin plugin, add features to an existing plugin, build CodeMirror/editor extensions, fix plugin loading/runtime errors, prepare manifest/package output, or align implementation with official docs from laurent22/joplin and joplin/plugins.
---

# Joplin Plugin Writer

## Overview

Implement Joplin plugins with a reliable flow from idea to runnable build.
Use official docs first, then produce code, manifest updates, and validation steps.

## Workflow

1. Clarify plugin type and target.
Gather target platform (`desktop` or `desktop+mobile`), core user action, UI surface (command, panel, toolbar, editor content script), and expected trigger.

2. Bootstrap or inspect the project.
For a new plugin, scaffold with:

```bash
npm install -g yo generator-joplin
yo joplin
```

For an existing plugin, inspect `src/index.ts`, `src/manifest.json`, `plugin.config.json`, and `webpack.config.js`.

3. Implement with the official plugin lifecycle.
Always register through `joplin.plugins.register({ onStart: async () => {} })`.
Place command/view/content-script wiring in `onStart`.
Treat handlers and API calls as async.

4. Choose the integration pattern.
If the feature targets note/workspace behavior, use `joplin.workspace`, `joplin.commands`, `joplin.views`.
If the feature targets editor behavior, use content scripts and choose CodeMirror strategy:
- Prefer CodeMirror 6 plugin flow for modern Joplin.
- Add dual CM5+CM6 scripts only when explicit backward compatibility is required.
- Keep CM packages externalized to avoid duplicate-instance runtime issues.

5. Keep manifest and packaging correct.
Update `src/manifest.json` with accurate `app_min_version`, `platforms`, metadata, and assets.
Build with `npm run dist` so runtime artifacts are available under `dist/` and publish output under `publish/`.

6. Run and verify in Development Mode.
Launch Joplin in Development Mode, point "Development plugins" to plugin root, restart fully, and validate:
- Plugin loads without errors
- Core command/view behavior works
- Console/log output is clean

7. Debug with directed checks.
For loading failures, check compiled entry and load paths (`dist/index.js` and plugin directory selection).
For editor issues, verify CM6/CM5 compatibility branch and content script registration IDs.
For mobile/web behavior, follow mobile debugging flow and ensure `platforms` contains `mobile` when needed.

## Implementation Rules

- Read `references/official-docs-index.md` first and load only the minimum relevant section.
- Keep generated code TypeScript-first unless the repository is clearly JavaScript-only.
- Modify existing plugin structure instead of rewriting whole files when possible.
- Preserve user/plugin IDs and public command names unless migration is explicitly requested.
- Explain manifest-impacting changes (ID/version/platforms/min-version) before finalizing.
- Prefer incremental commits: scaffold, core feature, polish/fix, docs update.

## Task Playbooks

### New Plugin From Requirement

1. Convert requirement into one primary user interaction.
2. Scaffold with `yo joplin`.
3. Implement minimum viable command/panel/content script.
4. Update manifest metadata.
5. Build and run in Development Mode.
6. Return install/run steps and known limitations.

### Feature Upgrade In Existing Plugin

1. Identify extension points in existing `onStart` registration.
2. Add feature with minimal API surface change.
3. Keep compatibility with existing settings and data where possible.
4. Validate build and runtime regressions.

### Debugging and Fixes

1. Reproduce in Development Mode.
2. Triage by category: load-time, API/runtime, editor-content-script, packaging.
3. Apply smallest fix with clear reason.
4. Rebuild and re-test.

## References

Use `references/official-docs-index.md` for direct links and focused loading guidance.
