"""Builds report.html from the project sources, logs and screenshots,
then prints it to AMAD_Report03_Vardal_Deniz.pdf with headless Edge."""
import html
import subprocess
import tempfile
from pathlib import Path

DOCS = Path(__file__).resolve().parent
PROJECT = DOCS.parent
SRC = PROJECT / "app/src/main/java/com/example/amadlab"
LOGS = DOCS / "logs"
OUT_HTML = DOCS / "report.html"
OUT_PDF = DOCS / "AMAD_Report03_Vardal_Deniz.pdf"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def rel(path: Path) -> str:
    return str(path.relative_to(PROJECT)).replace("\\", "/")


def code(path: Path, title: str | None = None) -> str:
    text = path.read_text(encoding="utf-8").rstrip()
    return f'<div class="file">{html.escape(title or rel(path))}</div><pre>{html.escape(text)}</pre>'


def excerpt(path: Path, start: str, end: str, note: str = "", exact: bool = True) -> str:
    """Lines from the first line containing `start` to the next line equal to `end`
    (or containing it when exact=False), inclusive."""
    lines = path.read_text(encoding="utf-8").splitlines()
    i = next(n for n, l in enumerate(lines) if start in l)
    j = next(n for n in range(i, len(lines)) if (lines[n] == end if exact else end in lines[n]))
    body = "\n".join(lines[i:j + 1])
    title = f"{rel(path)} – lines {i + 1}–{j + 1}" + (f" ({note})" if note else "")
    return f'<div class="file">{html.escape(title)}</div><pre>{html.escape(body)}</pre>'


def snippet(text: str, title: str) -> str:
    return f'<div class="file">{html.escape(title)}</div><pre>{html.escape(text.strip())}</pre>'


def log(name: str, caption: str) -> str:
    text = (LOGS / f"{name}.txt").read_text(encoding="utf-8").rstrip()
    return f'<div class="file">{html.escape(caption)}</div><pre class="log">{html.escape(text)}</pre>'


def figs(*items, landscape=False, wide=False) -> str:
    cls = "fig wide" if wide else ("fig land" if landscape else "fig")
    cells = "".join(
        f'<figure class="{cls}"><img src="img/{f}.png"><figcaption>{c}</figcaption></figure>'
        for f, c in items
    )
    return f'<div class="figs">{cells}</div>'


def comment(text: str) -> str:
    return f'<div class="comment"><b>Comment.</b> {text}</div>'


CSS = """
@page { size: A4; margin: 16mm 15mm 16mm 15mm; }
body { font-family: 'Segoe UI', Calibri, Arial, sans-serif; font-size: 10.5pt; line-height: 1.42; color: #111; }
h1 { font-size: 20pt; margin: 0 0 4px 0; color: #0b4f6c; }
h2 { font-size: 15pt; color: #0b4f6c; border-bottom: 2px solid #0b4f6c; padding-bottom: 3px; margin-top: 26px; break-after: avoid; }
h3 { font-size: 12.5pt; margin: 22px 0 6px 0; color: #00696b; break-after: avoid; }
h4 { font-size: 10.5pt; margin: 12px 0 4px 0; break-after: avoid; }
p { margin: 5px 0; text-align: justify; }
code { font-family: Consolas, 'Cascadia Mono', 'Courier New', monospace; font-size: 9.2pt; background: #f1f3f4; padding: 0 2px; border-radius: 2px; }
pre { font-family: Consolas, 'Cascadia Mono', 'Courier New', monospace; font-size: 8.1pt; line-height: 1.32;
      background: #f7f8fa; border: 1px solid #d5d9de; border-left: 3px solid #00696b; padding: 6px 8px; margin: 0 0 10px 0;
      white-space: pre-wrap; word-break: break-word; }
pre.log { background: #1e1e1e; color: #e6e6e6; border-left-color: #f0a030; }
.file { font-family: Consolas, monospace; font-size: 8.4pt; font-weight: bold; color: #444; margin-top: 8px; padding: 2px 8px;
        background: #e3e7eb; border: 1px solid #d5d9de; border-bottom: none; display: inline-block; }
.figs { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin: 8px 0 10px 0; break-inside: avoid; }
figure { margin: 0; text-align: center; break-inside: avoid; }
figure.fig img { width: 52mm; border: 1px solid #bbb; }
figure.land img { width: 118mm; border: 1px solid #bbb; }
figure.wide img { width: 178mm; border: 1px solid #bbb; }
figcaption { font-size: 8.6pt; color: #444; max-width: 56mm; margin: 3px auto 0 auto; }
figure.land figcaption, figure.wide figcaption { max-width: 170mm; }
.comment { background: #fff8e6; border-left: 3px solid #f0a030; padding: 6px 9px; margin: 8px 0; break-inside: avoid; }
.meta td { padding: 1px 12px 1px 0; vertical-align: top; }
table.t { border-collapse: collapse; margin: 6px 0; font-size: 9.6pt; }
table.t td, table.t th { border: 1px solid #c8ccd0; padding: 3px 7px; text-align: left; vertical-align: top; }
table.t th { background: #e9f4f4; }
.q { font-weight: 600; margin-top: 10px; break-after: avoid; }
.pb { break-before: page; }
"""

parts: list[str] = []
add = parts.append

# ---------------------------------------------------------------- title page
add("""
<h1>Lab Report 03</h1>
<div style="font-size:12pt;color:#333;margin-bottom:10px">Advanced Mobile Application Development &middot; 2026/2027</div>
<table class="meta">
<tr><td><b>Student</b></td><td>Deniz Vardal</td></tr>
<tr><td><b>Instruction</b></td><td>03 &ndash; Architecture: MVVM, ViewModel and navigation</td></tr>
<tr><td><b>Tasks</b></td><td>3.1&ndash;3.5 and the control questions</td></tr>
<tr><td><b>Date</b></td><td>14.11.2026</td></tr>
</table>

<h2>Environment and project structure</h2>
<table class="t">
<tr><th>Item</th><th>Value</th></tr>
<tr><td>Project</td><td>new project <code>AmadLab</code> (Empty Activity structure), package <code>com.example.amadlab</code></td></tr>
<tr><td>Build</td><td>Gradle 8.7, Android Gradle Plugin 8.5.2, Kotlin 2.0.21 (Compose and serialization plugins), Compose BOM 2024.09.03, JDK 17</td></tr>
<tr><td>Architecture libraries</td><td>navigation-compose 2.8.3, lifecycle 2.8.6 (viewmodel-compose, runtime-compose), kotlinx-serialization-json 1.7.3</td></tr>
<tr><td>SDK / device</td><td><code>compileSdk = targetSdk = 34</code>, <code>minSdk = 24</code>; Android Emulator, Android 14 (API 34), 1080&times;2400 px</td></tr>
</table>
<table class="t">
<tr><th>File</th><th>Layer / role</th></tr>
<tr><td><code>Task.kt</code>, <code>TaskRepository.kt</code></td><td>model; the repository is the single source of truth</td></tr>
<tr><td><code>TasksViewModel.kt</code>, <code>TaskDetailViewModel.kt</code>, <code>StatisticsViewModel.kt</code></td><td>state holders: UI state + events</td></tr>
<tr><td><code>TaskListScreen.kt</code>, <code>TaskDetailScreen.kt</code>, <code>StatisticsScreen.kt</code></td><td>view: a stateful route + a stateless screen for every destination</td></tr>
<tr><td><code>Navigation.kt</code>, <code>MainActivity.kt</code></td><td>type-safe routes, <code>NavHost</code>, entry point</td></tr>
</table>
""")
add(comment("Listing 6 uses navigation 2.10.2, lifecycle 2.11.0 and serialization 1.9.0. These versions need a newer "
            "<code>compileSdk</code>, Android Gradle Plugin and Kotlin than the ones installed on my machine (API 34, "
            "Kotlin 2.0.21), so I used navigation 2.8.3, lifecycle 2.8.6 and serialization 1.7.3. The API from the "
            "instruction is the same: type-safe routes, <code>composable&lt;T&gt;</code> and "
            "<code>SavedStateHandle.toRoute&lt;T&gt;()</code> exist since navigation 2.8.0. All files below are shown in "
            "their final version; the parts added in tasks 3.2&ndash;3.4 are marked with comments <code>// Task 3.x</code>."))

# ---------------------------------------------------------------- 3.1
add('<h2 class="pb">Task 3.1 &ndash; MVVM, ViewModel and navigation</h2>')
add("<h4>Gradle files (listings 6 and 7)</h4>")
add(code(PROJECT / "gradle/libs.versions.toml"))
add(code(PROJECT / "build.gradle.kts"))
add(code(PROJECT / "app/build.gradle.kts"))
add("<h4>Model and repository (listing 1)</h4>")
add(code(SRC / "Task.kt"))
add(code(SRC / "TaskRepository.kt"))
add("<h4>View model of the list (listing 2, with the filter from task 3.2)</h4>")
add(code(SRC / "TasksViewModel.kt"))
add("<h4>Route and stateless screen of the list (listing 3)</h4>")
add(code(SRC / "TaskListScreen.kt"))
add("<h4>View model and screen of the details (listing 5 and the description below it)</h4>")
add(code(SRC / "TaskDetailViewModel.kt"))
add(code(SRC / "TaskDetailScreen.kt"))
add("<h4>Routes and navigation graph (listing 4), MainActivity, theme</h4>")
add(code(SRC / "Navigation.kt"))
add(code(SRC / "MainActivity.kt"))
add(code(SRC / "ui/theme/Theme.kt"))

add("<h4>Result: rotation on both screens</h4>")
add("<p>I added two tasks (&ldquo;Write lab report 03&rdquo;, &ldquo;Prepare presentation&rdquo;), typed &ldquo;Buy milk&rdquo; "
    "into the field without adding it, and rotated the emulator; then I opened the details of task 4 and rotated again.</p>")
add(figs(("3_1_list_portrait", "List before rotation: 5 tasks, half-typed &ldquo;Buy milk&rdquo;"),
         ("3_1_detail_portrait", "Details of task 4 before rotation")))
add(figs(("3_1_list_landscape", "List after rotation: still Done 1 / 5 and the text &ldquo;Buy milk&rdquo;"), landscape=True))
add(figs(("3_1_detail_landscape", "Details after rotation: the same task 4"), landscape=True))
add(log("3_1_rotation", "Logcat (tags ViewModel, BackStack): start, rotation of the list, opening task 4, rotation of the details"))
add("""
<p><b>Why the tasks survive the rotation now.</b> In instruction 02.2 the list was kept with <code>remember</code> inside the
composable. Rotation destroys the Activity (task 2.1.1), the whole composition is thrown away, and the new composition started
again from the two initial tasks &ndash; everything added was lost. Now the data is not stored in the UI at all:</p>
<ul>
<li>the tasks live in <code>TaskRepository</code>, a Kotlin <code>object</code>. It belongs to the application process, not to
the Activity, and the process is not killed by a rotation (same PID 15376 in the whole log);</li>
<li>the state of the screen (the typed text, the filter) lives in <code>TasksViewModel</code>. The view model is stored in the
<code>ViewModelStore</code> of the navigation back stack entry, which is kept across configuration changes. The new Activity
gets the <b>same</b> object: the log shows &ldquo;TasksViewModel created&rdquo; only once, and the back stack entries
(<code>b31a71ef</code>, <code>62194dbf</code>) have the same ids before and after each rotation. The new composition only
collects the current <code>uiState</code> again;</li>
<li>the detail screen keeps its argument <code>taskId</code> in the back stack (thanks to <code>@Serializable</code>), so after the
rotation it still shows task 4.</li>
</ul>
""")
add(comment("After rotating the list with the text field focused, the keyboard opened again and covered the list in "
            "landscape, so I hid it before taking the screenshot. In landscape the detail screen is cut off at the bottom "
            "(the buttons do not fit) because its <code>Column</code> is not scrollable &ndash; "
            "<code>Modifier.verticalScroll(rememberScrollState())</code> would fix it. One change to listing 1: in "
            "<code>add()</code> the id is taken <i>before</i> <code>update { }</code>, because <code>update</code> may run its "
            "lambda again if two changes happen at the same time, and <code>nextId++</code> inside it would then skip ids. "
            "The data still exists only in memory: if the system kills the process in the background, the added tasks are "
            "lost (a database will solve this later)."))

# ---------------------------------------------------------------- 3.2
add('<h2 class="pb">Task 3.2 &ndash; Filter in the view model</h2>')
add("<p><code>TasksUiState</code> got the property <code>filter</code> and the view model the event <code>onFilterChange</code>. "
    "The filter is a third <code>MutableStateFlow</code> joined in <code>combine</code>; the screen receives an already filtered "
    "list and only draws three buttons. The counts are computed from the whole list, so they do not change with the filter.</p>")
add(excerpt(SRC / "TasksViewModel.kt", "enum class TaskFilter", "}", "UI state"))
add(excerpt(SRC / "TasksViewModel.kt", "// Task 3.2: combine takes three flows", "        )", "the part with combine"))
add(excerpt(SRC / "TasksViewModel.kt", "fun onFilterChange", "    }", "the event"))
add(excerpt(SRC / "TaskListScreen.kt", "// Task 3.2: the buttons only report", "            }", "the screen only reports the event"))
add(figs(("3_2_filter_all", "All: 6 tasks shown, Done 2 / 6"),
         ("3_2_filter_active", "Active: 4 shown, still Done 2 / 6"),
         ("3_2_filter_done", "Done: 2 shown, still Done 2 / 6")))
add("<p><b>Proof that the view model filters.</b> The screen has no filtering code &ndash; it shows <code>state.tasks</code> as it "
    "comes. The line &ldquo;Done: 2 / 6 (shown: n)&rdquo; uses <code>doneCount</code> and <code>totalCount</code>, which the view "
    "model counts on the full list from the repository, while <code>shown</code> is the size of the filtered list. The total stays "
    "6 for every filter, so the repository is not changed &ndash; only the UI state is.</p>")
add(comment("A name clash: the lambda parameter of <code>combine</code> could not be called <code>filter</code>, because it "
            "would hide the property and make <code>tasks.filter { }</code> confusing; I called it <code>selected</code>. "
            "The chosen filter now also survives rotation and returning from the details, because it is kept in the view model."))

# ---------------------------------------------------------------- 3.3
add("<h2>Task 3.3 &ndash; Editing the title</h2>")
add("<p>The repository got <code>rename(id, title)</code>. The detail view model keeps the text of the field "
    "(<code>editedTitle</code>) and exposes it in <code>TaskDetailUiState</code>; <code>canSave</code> is derived from it. "
    "The route connects the button: first the event <code>save()</code> goes to the view model, then <code>onBack()</code> "
    "calls <code>popBackStack()</code> in the navigation graph.</p>")
add(excerpt(SRC / "TaskRepository.kt", "// Task 3.3", "    }", "repository"))
add(excerpt(SRC / "TaskDetailViewModel.kt", "data class TaskDetailUiState", "}", "UI state"))
add(excerpt(SRC / "TaskDetailViewModel.kt", "// Task 3.3: the view model asks", "    }", "event"))
add(excerpt(SRC / "TaskDetailScreen.kt", "onSave = {", "        },", "route"))
add(figs(("3_3_detail_editing", "Editing: title changed to &ldquo;Read about MVVM and UDF&rdquo;, Save enabled"),
         ("3_3_list_after_save", "After Save and popBackStack(): the list shows the new title")))
add(log("3_3_save", "Logcat: the detail view model is created when the screen opens and cleared after popBackStack()"))
add(comment("Save is enabled only when the text is not blank and differs from the current title, so an unchanged title "
            "is not saved. The list shows the new title without any extra code: both screens collect the same "
            "<code>TaskRepository.tasks</code>, so <code>rename()</code> produces a new list and the list screen recomposes "
            "when it becomes visible again. The log confirms that the detail view model is destroyed "
            "(<code>onCleared</code>) as soon as its destination leaves the back stack."))

# ---------------------------------------------------------------- 3.4
add('<h2 class="pb">Task 3.4 &ndash; Statistics and launchSingleTop</h2>')
add(code(SRC / "StatisticsViewModel.kt"))
add(code(SRC / "StatisticsScreen.kt"))
add(excerpt(SRC / "Navigation.kt", "// Task 3.4: third destination", "const val STATISTICS_SINGLE_TOP", "route", exact=False))
add(excerpt(SRC / "Navigation.kt", "onStatisticsClick = {", "                }", "navigation with launchSingleTop"))
add(excerpt(SRC / "TaskListScreen.kt", "// Task 3.4: opens the Statistics", "actions =", "TextButton in the top bar", exact=False))
add(figs(("3_4_statistics", "Statistics: 6 tasks, 2 done, 4 remaining, 33 %")))

add("<h4>Clicking the button twice</h4>")
add("<p>To reproduce two clicks that are handled before the screen changes, I temporarily replaced the click handler with "
    "the code below, ran it once with <code>STATISTICS_SINGLE_TOP = false</code> and once with <code>true</code>, and "
    "pressed Back after each run. The log line shows which entry lies directly under the top of the back stack.</p>")
add(snippet("""
onStatisticsClick = {
    repeat(2) { // EXPERIMENT: two clicks handled before the screen changes
        navController.navigate(Statistics) {
            launchSingleTop = STATISTICS_SINGLE_TOP
        }
    }
    val below = navController.previousBackStackEntry?.destination?.route
    Log.d("BackStack", "singleTop=$STATISTICS_SINGLE_TOP, entry below the top = ${below?.substringAfterLast('.')}")
}
""", "Navigation.kt – temporary experiment (removed from the final code)"))
add(log("3_4_singletop_false", "Without launchSingleTop: two clicks, Back, Back"))
add(log("3_4_singletop_true", "With launchSingleTop = true: two clicks, Back"))
add(figs(("3_4_exp_false_after_click", "Without: after two clicks"),
         ("3_4_exp_false_after_one_back", "Without: after one Back &ndash; Statistics again"),
         ("3_4_exp_true_after_one_back", "With: after one Back &ndash; the list")))
add("""
<table class="t">
<tr><th></th><th>Back stack after two clicks</th><th>Back</th></tr>
<tr><td><b>without</b> <code>launchSingleTop</code></td><td><code>[TaskList, Statistics, Statistics]</code> &ndash; the entry under
the top is Statistics; two different entries <code>99cfadee</code> and <code>57879ff7</code>, each with its own view model</td>
<td>the first Back shows the same Statistics screen again (the user thinks Back did not work); only the second Back returns to the list</td></tr>
<tr><td><b>with</b> <code>launchSingleTop = true</code></td><td><code>[TaskList, Statistics]</code> &ndash; the second
<code>navigate</code> sees that Statistics is already on top and does not add a copy; the entry under the top is TaskList</td>
<td>one Back returns to the list; the next Back leaves the application</td></tr>
</table>
""")
add(comment("First I tried a real double tap on the emulator: with <code>adb shell input tap</code> twice and then with raw "
            "touch events sent about 10&nbsp;ms apart (<code>sendevent</code>). In both cases the second tap never reached the "
            "button &ndash; most likely because right after <code>navigate()</code> the Statistics screen is placed over the "
            "list and its <code>Scaffold</code> receives the next touches. That is why I simulated the second click in code. "
            "On a real phone the duplicate can still happen with a very fast double tap or a slow device, and for buttons that "
            "stay visible after navigating (e.g. a bottom bar), so <code>launchSingleTop = true</code> is the safe choice for "
            "this kind of button. The final code calls <code>navigate</code> once with <code>launchSingleTop = true</code>."))

# ---------------------------------------------------------------- 3.5
add('<h2 class="pb">Task 3.5 &ndash; Architecture diagram</h2>')
add("<p>The diagram shows the application from task 3.4. The data layer is at the top and the user interface at the bottom, "
    "so the green state arrows point <b>down</b> (repository &rarr; <code>StateFlow</code> &rarr; view model &rarr; "
    "<code>uiState</code> &rarr; composables) and the orange event arrows point <b>up</b> (lambdas of the screens &rarr; "
    "functions of the view models &rarr; functions of the repository). Navigation events (dashed) go from the screens to the "
    "<code>NavHost</code>. <code>TaskRepository</code> is marked as the <b>single source of truth</b>: it is the only class "
    "that changes the list of tasks. I drew it in SVG (file <code>docs/diagram/architecture.html</code>).</p>")
add(figs(("3_5_architecture", "Architecture of the AmadLab application (MVVM + UDF + Navigation Compose)"), wide=True))

# ---------------------------------------------------------------- questions
add('<h2 class="pb">Control questions</h2>')
QA = [
    ("1. What problems of the task list from instruction 02.2 does the MVVM architecture solve?",
     "<b>Lost state</b> &ndash; the list was in <code>remember</code> and disappeared after rotation; now the data is in the "
     "repository and the screen state in a view model that survives configuration changes (task 3.1). <b>Sharing</b> &ndash; "
     "a second screen could not see the list; now the list, the details and the statistics read the same "
     "<code>TaskRepository.tasks</code>. <b>Testing</b> &ndash; the logic (adding, filtering, renaming, statistics) is in plain "
     "Kotlin classes that can be tested without a user interface. <b>Mixed responsibilities</b> &ndash; one composable decided "
     "about the look, the clicks and the data; now the screen only draws the UI state and reports events."),
    ("2. Why does a view model survive the rotation of the screen? When is it destroyed?",
     "The view model is not kept in the Activity object but in a <code>ViewModelStore</code> (of the Activity or, with "
     "Navigation Compose, of the back stack entry). On a configuration change the system keeps this store and gives it to the "
     "new Activity, so <code>viewModel()</code> returns the existing object instead of creating a new one (one &ldquo;created&rdquo; "
     "line in the log of task 3.1). It is destroyed and <code>onCleared()</code> is called when its owner is finished for good: the "
     "destination is removed from the back stack (e.g. <code>popBackStack()</code> in task 3.3) or the Activity is finished "
     "(Back from the start screen), and also when the process is killed."),
    ("3. Why must a view model not keep a reference to an Activity or a composable?",
     "Because they live shorter than the view model: after a rotation the old Activity (and its composition and views) is "
     "destroyed, but the view model stays. A reference would keep the dead Activity with all its views and resources in memory "
     "&ndash; a memory leak &ndash; and code using it would work on a screen that is no longer displayed. The view model should "
     "only expose state; the UI observes it. If a context is really needed, the <code>Application</code> context can be used "
     "(<code>AndroidViewModel</code>)."),
    ("4. What is unidirectional data flow? Describe one cycle of it on the example of ticking a task.",
     "State flows in one direction &ndash; down, from its owner to the UI &ndash; and events flow in the other direction &ndash; "
     "up, from the UI to the owner. The UI never changes the data itself. Ticking a task: (1) <code>Checkbox</code> in "
     "<code>TaskRow</code> calls <code>onToggle(task.id)</code>, the event goes up through <code>TaskListScreen</code> to the route "
     "and to <code>viewModel.toggle(id)</code>; (2) the view model calls <code>repository.toggle(id)</code>; (3) the repository "
     "creates a new list with <code>copy(done = !done)</code> and puts it into <code>_tasks</code>; (4) <code>combine</code> in the "
     "view model emits a new <code>TasksUiState</code>; (5) <code>collectAsStateWithLifecycle</code> receives it, the state goes "
     "down and Compose recomposes the row with the ticked box and the new counter."),
    ("5. Why is the MutableStateFlow in the repository private and only a StateFlow public?",
     "This is the backing property pattern. Outside code gets a read-only <code>StateFlow</code>, so it can observe the tasks "
     "but cannot assign <code>value</code>; every change must go through the functions of the repository (<code>add</code>, "
     "<code>toggle</code>, <code>rename</code>, &hellip;). That makes the repository the real single source of truth: there is "
     "one place where the list changes, the rules (e.g. trimming titles, new ids) cannot be bypassed, and changes are easy to "
     "find, log and test."),
    ("6. What are the advantages of type-safe routes over routes written as text? How does the detail screen receive the identifier of the task?",
     "A route is a Kotlin type (<code>object TaskList</code>, <code>data class TaskDetail(val taskId: Long)</code>), so the "
     "compiler checks the destination name and the names and types of the arguments; a typo or a wrong type is a compile error "
     "instead of a crash at runtime, the IDE can find usages and rename them, and there is no manual building and parsing of "
     "strings like <code>\"detail/{id}\"</code>. The detail screen gets the id like this: the list calls "
     "<code>navController.navigate(TaskDetail(id))</code>; the library serializes the object into the back stack entry "
     "(<code>@Serializable</code>); the view model of the destination receives a <code>SavedStateHandle</code> with the "
     "arguments and converts it back with <code>savedStateHandle.toRoute&lt;TaskDetail&gt;().taskId</code>."),
]
for q, a in QA:
    add(f'<p class="q">{q}</p><p>{a}</p>')

page = (f"<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'><title>AMAD Report 03 - Deniz Vardal</title>"
        f"<style>{CSS}</style></head><body>{''.join(parts)}</body></html>")
OUT_HTML.write_text(page, encoding="utf-8")
print("HTML written:", OUT_HTML)

subprocess.run([
    EDGE, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--no-first-run",
    "--user-data-dir=" + str(Path(tempfile.gettempdir()) / "edge-report-profile"),
    f"--print-to-pdf={OUT_PDF}", OUT_HTML.as_uri(),
], check=True, timeout=180)
print("PDF written:", OUT_PDF, OUT_PDF.stat().st_size, "bytes")
