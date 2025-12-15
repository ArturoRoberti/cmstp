Look for TODOs in code. Otherwise, look at:

# !!! Major !!!
- Update the README with proper documentation
- Update and document pytests, and use them in CI (e.g. make sure there is no `✖ Failure` in output)

# Minor
## CI
- (If possible) Only run CI on new or edited tasks
## Core
- Define and document behaviour of using none, one of, or both `--config-file` and `--config-directory`
    - How can a config file in a config dir repo be specified?
        - (Maybe) If it's an absolute path, look there. If it is relative, look locally and then in the repo
- Test cyclic `supercedes` fields
- Update logging to file (i.e. `CMSTP START ...`) to only have a single CMSTP section, and fill stuff in there
- Remove uninstallations from "enable_all" etc. Or better, have a "counterpart" field or similar and if both install/uninstall are enabled, disable uninstall (say this in debug, not info/warning message)
- It seems that something may suspend all tasks running (if many are running)
    - Maybe this is caused by one task failing?
    - Can be restarted sing `fg %<id>` (bash; manually) (see id from output: `[<id>]+ Stopped`), but ofc that should not be necessary in the long term
- Maybe add a `requires-restart` flag or so to each task and make final message depend on that
- If verbose is set, save the modified scripts in log dir
- Make dev instructions (e.g. to add a task, edit <...>; to add a field to tasks, edit <...>; to add a test, edit <...>; etc.)
- Remove `sudo: mon_handle_sigchld: waitpid: No child processes` outputs (how to reproduce?)
- Restructure `default.yaml` 'file' field, to specify one for each OS type (ubuntu, macos, windows)
    - If null, then skip with warning via scheduler
    - Shell scripts will be OS-specific. Question is, should python scripts be so too or rather made cross-platform?
- Make uninstallation scripts (current and future) such that if e.g. files are removed, than even if one fails (e.g. "cannot remove file: No such file or directory"), the rest is still run
## Features
- Add mujoco stuff (mujoco, dmcontrol, sim applications)
- Add file with list of debian file links (then get and dpkg (or step apt?) them)
    - How to specify pkg? Via url, gitref, local path, package path, ...?
- Allow user creation (incl. permission)
    - Read out and automatically add to all groups (except sudo) and if `--sudo` flag is given, also add to sudo group
