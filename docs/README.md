# Documentation

This folder is the reader's entry to the safety-assurance record that the Asimov v1 fork carries beside the robot's
mechanical, electrical and simulation sources. The upstream documentation stays where upstream keeps it
([docs.asimovrobot.com](https://docs.asimovrobot.com)); the record never restates it.

| If you want to | Read |
|---|---|
| Understand the safety architecture argument | [Architecture](architecture.md) |
| Browse every work product, with its gate and status | [Assurance record](../assurance/README.md) |
| See what the inherited robot lacks, finding by finding | [Gap assessment](../assurance/00-assessment/gap-assessment.md) |
| See the concept-phase package the record was seeded from | [Concept package](../assurance/00-assessment/concept-package/README.md) |
| Get oriented: processes, process maps, standards, glossary | [Wiki](https://github.com/jherrodthomas/asimov-v1/wiki), kept in [`wiki/`](../wiki/README.md) and mirrored on merge |
| Contribute | [Contributing](../CONTRIBUTING.md) |
| Report a vulnerability | [Security policy](../SECURITY.md) |

Every figure is generated and checked by CI; nothing in them is drawn by hand:

| Figures | Generator |
|---|---|
| README and wiki figures under [`assets/asimov/`](assets/asimov/): hero, standards, architecture, roadmap, lifecycle, status card, standards map, repository map | [`make_assets.py`](assets/asimov/make_assets.py) |
| Process swimlanes, lifecycle grid and interface figure under [`assets/asimov/process/`](assets/asimov/process/) | [`process_figures.py`](../assurance/process/tools/process_figures.py), from the process model |
| Living Safety Case dashboard and lifecycle areas under [`assets/assurance/`](assets/assurance/) | [`generate_dashboard.py`](../assurance/case/tools/generate_dashboard.py), from the case records |
