# MVVM Task Manager

AMAD Lab 03 – MVVM, ViewModel and navigation. Android app for Lab Report 03 of Advanced Mobile Application Development (2026/2027). The task list from lab 02 rebuilt in the MVVM architecture: a repository as the single source of truth, a view model with one UI state per screen, unidirectional data flow and Navigation Compose with type-safe routes.

| Task | What it adds |
|---|---|
| 3.1 | `TaskRepository`, `TasksViewModel`, route + stateless screen, detail screen, `NavHost` with `TaskList` and `TaskDetail(taskId)` |
| 3.2 | All / Active / Done filter moved into the view model (`combine` of three flows) |
| 3.3 | Editing the title on the detail screen, `rename()` in the repository, back with `popBackStack()` |
| 3.4 | `Statistics` destination with its own view model, opened with `launchSingleTop = true` |
| 3.5 | Architecture diagram: composables, view models, repository, state down, events up |

## How it works

1. **Single source of truth.** `TaskRepository` (a Kotlin `object`) keeps the tasks in a private `MutableStateFlow` and exposes a read-only `StateFlow`. Only its functions change the list.
2. **View models.** Each screen has a view model that turns the repository flow into one immutable UI state (`StateFlow<…UiState>`) and offers functions for the events. The view models survive rotation.
3. **Routes and screens.** A thin route gets the view model and collects the state with `collectAsStateWithLifecycle()`; the stateless screen only draws the state and calls lambdas.
4. **Navigation.** `@Serializable` routes; the detail view model reads its argument with `savedStateHandle.toRoute<TaskDetail>()`.

## Getting started

Requires JDK 17 and the Android SDK (API 34). Open the folder in Android Studio, or build from the command line:

```bash
./gradlew assembleDebug
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

Logcat tags `ViewModel` and `BackStack` show when view models are created and cleared and which destination is on top of the back stack.

Rebuild the report after changing the code or the screenshots:

```bash
python docs/build_report.py
```

## Project structure

```
├── app/src/main/java/com/example/amadlab/
│   ├── Task.kt, TaskRepository.kt          model, single source of truth
│   ├── TasksViewModel.kt                   list UI state, filter, events
│   ├── TaskListScreen.kt                   list route + stateless screen
│   ├── TaskDetailViewModel.kt              reads taskId from SavedStateHandle, editing
│   ├── TaskDetailScreen.kt                 detail route + stateless screen
│   ├── StatisticsViewModel.kt              all / done / remaining / percent
│   ├── StatisticsScreen.kt                 statistics route + stateless screen
│   ├── Navigation.kt                       type-safe routes and NavHost
│   └── MainActivity.kt, ui/theme/
└── docs/
    ├── AMAD_Report03_Vardal_Deniz.pdf      the submitted report
    ├── img/                                emulator screenshots and the diagram
    ├── logs/                               Logcat output used in the report
    ├── diagram/architecture.html           source of the architecture diagram
    └── build_report.py                     report generator
```

Built with Kotlin, Jetpack Compose, Material 3, Navigation Compose, Lifecycle ViewModel and kotlinx.serialization.
